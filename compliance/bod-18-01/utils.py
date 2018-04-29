import csv
import io
import os
import errno
import urllib
import urllib.request
import logging
import requests
import base64
import re
import json

# == compliance

# Given a dict of pshtt results for a hostname, what are the
# Uses, Enforces, and HSTS conclusions?
#
# borrows the pulse.cio.gov code for calculating conclusions:
# https://github.com/18F/pulse/blob/0528773b1d39a664ff8f62d655b8bb7c8979874c/data/processing.py#L408-L509
def compliance_for(pshtt, sslyze, parent_preloaded=False):
  report = {}
  # assumes that HTTPS would be technically present, with or without issues
  if (pshtt["Downgrades HTTPS"] == "True"):
    https = 0 # No
  else:
    if (pshtt["Valid HTTPS"] == "True"):
      https = 2 # Yes
    elif (
      (pshtt["HTTPS Bad Chain"] == "True") and
      (pshtt["HTTPS Bad Hostname"] == "False")
    ):
      https = 1 # Yes
    else:
      https = -1 # No


  ###
  # Is HTTPS enforced?

  if (https <= 0):
    behavior = 0 # N/A

  else:

    # "Yes (Strict)" means HTTP immediately redirects to HTTPS,
    # *and* that HTTP eventually redirects to HTTPS.
    #
    # Since a pure redirector domain can't "default" to HTTPS
    # for itself, we'll say it "Enforces HTTPS" if it immediately
    # redirects to an HTTPS URL.
    if (
      (pshtt["Strictly Forces HTTPS"] == "True") and
      (
        (pshtt["Defaults to HTTPS"] == "True") or
        (pshtt["Redirect"] == "True")
      )
    ):
      behavior = 3 # Yes (Strict)

    # "Yes" means HTTP eventually redirects to HTTPS.
    elif (
      (pshtt["Strictly Forces HTTPS"] == "False") and
      (pshtt["Defaults to HTTPS"] == "True")
    ):
      behavior = 2 # Yes

    # Either both are False, or just 'Strict Force' is True,
    # which doesn't matter on its own.
    # A "present" is better than a downgrade.
    else:
      behavior = 1 # Present (considered 'No')

  report['enforces'] = behavior


  ###
  # Characterize the presence and completeness of HSTS.

  if pshtt["HSTS Max Age"]:
    hsts_age = int(pshtt["HSTS Max Age"])
  else:
    hsts_age = None

  # If this is a subdomain, it can be considered as having HSTS, via
  # the preloading of its parent.
  if parent_preloaded:
    hsts = 3 # Yes, via preloading

  # Otherwise, without HTTPS there can be no HSTS for the domain directly.
  elif (https <= 0):
    hsts = -1  # N/A (considered 'No')

  else:

    # HSTS is present for the canonical endpoint.
    if (pshtt["HSTS"] == "True") and hsts_age:

      # Say No for too-short max-age's, and note in the extended details.
      if hsts_age >= 31536000:
        hsts = 2  # Yes, directly
      else:
        hsts = 1  # No

    else:
      hsts = 0  # No

  # Separate preload status from HSTS status:
  #
  # * Domains can be preloaded through manual overrides.
  # * Confusing to mix an endpoint-level decision with a domain-level decision.
  if pshtt["HSTS Preloaded"] == "True":
    preloaded = 2  # Yes
  elif (pshtt["HSTS Preload Ready"] == "True"):
    preloaded = 1  # Ready for submission
  else:
    preloaded = 0  # No

  report['hsts'] = hsts
  report['hsts_age'] = hsts_age
  report['preloaded'] = preloaded

  ###
  # Get cipher/protocol data via sslyze for a host.

  sslv2 = None
  sslv3 = None
  any_rc4 = None
  any_3des = None

  # values: unknown or N/A (-1), No (0), Yes (1)
  bod_crypto = None

  # N/A if no HTTPS
  if (https <= 0):
    bod_crypto = -1 # N/A

  elif sslyze is None:
    # LOGGER.info("[https][%s] No sslyze scan data found." % name)
    bod_crypto = -1 # Unknown

  else:
    ###
    # BOD 18-01 (cyber.dhs.gov) cares about SSLv2, SSLv3, RC4, and 3DES.
    any_rc4 = boolean_for(sslyze["Any RC4"])
    # TODO: kill conditional once everything is synced
    if sslyze.get("Any 3DES"):
      any_3des = boolean_for(sslyze["Any 3DES"])
    sslv2 = boolean_for(sslyze["SSLv2"])
    sslv3 = boolean_for(sslyze["SSLv3"])

    if any_rc4 or any_3des or sslv2 or sslv3:
      bod_crypto = 0
    else:
      bod_crypto = 1

  report['bod_crypto'] = bod_crypto
  report['rc4'] = any_rc4
  report['3des'] = any_3des
  report['sslv2'] = sslv2
  report['sslv3'] = sslv3

  # Final calculation: is the service compliant with all of M-15-13
  # (HTTPS+HSTS) and BOD 18-01 (that + RC4/3DES/SSLv2/SSLv3)?

  # For M-15-13 compliance, the service has to enforce HTTPS,
  # and has to have strong HSTS in place (can be via preloading).
  m1513 = (behavior >= 2) and (hsts >= 2)

  # For BOD compliance, only ding if we have scan data:
  # * If our scanner dropped, give benefit of the doubt.
  # * If they have no HTTPS, this will fix itself once HTTPS comes on.
  bod1801 = m1513 and (bod_crypto != 0)

  # Phew!
  report['m1513'] = m1513
  report['compliant'] = bod1801 # equivalent, since BOD is a superset

  return report


# Given a compliance report (e.g. uses=1, enforces=2, hsts=2)
# return a dict with them turned into labels
def compliance_labels(report):
    return {
        'enforces': (report['enforces'] >= 2),
        'hsts': (report['hsts'] >= 2),
        'bod_crypto': (report['bod_crypto'] == 1),
        'compliant': (report['compliant']),
        'rc4': report['rc4'],
        '3des': report['3des']
    }

def boolean_for(string):
  if string == "False":
    return False
  elif string == "True":
    return True
  else:
    return None

# Given a set of domains, calculate the compliance totals
# that meet BOD 18-01 requirements.
# Adapted from a snapshot of Pulse code:
# https://github.com/18F/pulse/blob/0528773b1d39a664ff8f62d655b8bb7c8979874c/data/processing.py#L511-L539

def compliance_totals(data, preload_pending, preloaded):
    total_report = {
        'enforces': 0,
        'hsts': 0,
        'bod_crypto': 0,
        'compliant': 0,
        'rc4': 0,
        '3des': 0
    }

    for domain in data.keys():
        # calculated in compliance_for() method using pshtt data
        report = data[domain]['compliance']

        # Needs to be Default or Strict to be 'Yes'
        if report['enforces'] >= 2:
            total_report['enforces'] += 1

        # Needs to be present with >= 1 year max-age for canonical endpoint
        if report['hsts'] >= 2:
            total_report['hsts'] += 1

        if report['bod_crypto'] == 1:
            total_report['bod_crypto'] += 1

        if report['compliant']:
            total_report['compliant'] += 1

        if report['rc4']:
            total_report['rc4'] += 1

        if report['3des']:
            total_report['3des'] += 1

    return total_report

# == filters ==

def live_only(pshtt, agency, branch):
    return pshtt["Live"] == "True"

# return a dynamic filter function for a given agency
def for_agencies(filter_agencies):
    # render case-insensitive
    filtered = [agency.lower() for agency in filter_agencies]

    def the_filter(pshtt, agency, branch):
        live = live_only(pshtt, agency, branch)
        return live and (agency.lower() in filtered)

    return the_filter

# a specific list of executive branch domains
# used to filter on DAP-tracked domains
def specific_executive(list_of_domains):

    def the_filter(pshtt, agency, branch):
        executive = executive_only(pshtt, agency, branch)
        return executive and (pshtt['Domain'] in list_of_domains)

    return the_filter

def executive_only(pshtt, agency, branch):
    live = live_only(pshtt, agency, branch)
    return live and (branch == "executive")

def non_executive(pshtt, agency, branch):
    live = live_only(pshtt, agency, branch)
    return live and (branch != "executive")

def legislative_only(pshtt, agency, branch):
    live = live_only(pshtt, agency, branch)
    return live and (branch == "legislative")

def judicial_only(pshtt, agency, branch):
    live = live_only(pshtt, agency, branch)
    return live and (branch == "judicial")

def cfo_act_only(pshtt, agency, branch):
    live = live_only(pshtt, agency, branch)
    return live and cfo_act(agency)

def executive_non_cfo_act(pshtt, agency, branch):
    executive = executive_only(pshtt, agency, branch)
    return executive and (not cfo_act(agency))

def cfo_act_only_sans_dod(pshtt, agency, branch):
    live = live_only(pshtt, agency, branch)
    return live and cfo_act_sans_dod(agency)

# Return base domain for a subdomain.
# Simplified to not use PSL for the federal use case, while handling .fed.us.
def base_domain_for(subdomain):
    if subdomain.endswith(".fed.us"):
        return str.join(".", subdomain.split(".")[-3:])
    else: # .gov
        return str.join(".", subdomain.split(".")[-2:])

# save an array of domain names to a CSV at a given path
def save_domains(domains, path):
    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)
    header = ["Domain", "Base Domain"]
    writer.writerow(header)
    for domain in domains:
        writer.writerow([domain, base_domain_for(domain)])
    write(output.getvalue(), path)

def save_csv(header, rows, path):
    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)
    writer.writerow(header)
    for row in rows:
        writer.writerow(row)
    write(output.getvalue(), path)


# Load the first column of a CSV into memory as an array of strings.
def load_domains(domain_csv, whole_rows=False):
    domains = []
    with open(domain_csv, newline='') as csvfile:
        for row in csv.reader(csvfile):
            if (not row[0]) or (row[0].lower() == "domain") or (row[0].lower() == "domain name"):
                continue

            row[0] = row[0].lower()

            if whole_rows:
                domains.append(row)
            else:
                domains.append(row[0])
    return domains

# Return true if it's a CFO Act agency
def cfo_act(agency):
    return agency in [
        "U.S. Department of Agriculture",
        "Department of Commerce",
        "Department of Defense",
        "Department of Education",
        "Department of Energy",
        "Department of Health and Human Services",
        "Department of Homeland Security",
        "Department of Housing and Urban Development",
        "Department of the Interior",
        "Department of Justice",
        "Terrorist Screening Center", # (DOJ/FBI) as seen in .gov data
        "Department of Labor",
        "Department of State",
        "Department of State, Office of Inspector General", # seen in .gov data
        "Department of Transportation",
        "Department of the Treasury",
        "Department of Veterans Affairs",
        "Environmental Protection Agency",
        "National Aeronautics and Space Administration",
        "U.S. Agency for International Development",
        "General Services Administration",
        "National Science Foundation",
        "Nuclear Regulatory Commission",
        "Office of Personnel Management",
        "Small Business Administration",
        "Social Security Administration"
    ]

# Return true if it's a CFO act agency and not DoD
def cfo_act_sans_dod(agency):
    return cfo_act(agency) and (agency != "Department of Defense")

# Taken from a snapshot of Pulse's branch detection code:
# https://github.com/18F/pulse/blob/c5b15bc1d2c9e4ff3b20e352e0a0b4f3d131d70f/data/processing.py#L1165-L1174
def branch_for(domain_type):
  if (not domain_type.startswith("Federal Agency - ")):
    return None

  branch = domain_type.replace("Federal Agency - ", "")
  branch = branch.lower().strip()

  return branch


# Download official GSA .gov dataset and create a dict of domains to agencies/branches.
def domains_to_agencies():
    official_csv = "cache/federal-domains.csv"
    if not os.path.exists(official_csv):
        print("Downloading federal domains...")

        # Snapshot as of 2018-04-27
        url = "https://github.com/GSA/data/raw/4513ad8ce1548fdb34509e7361d806a5a1e4288b/dotgov-domains/current-federal.csv"
        official_csv = download(url, "cache/federal-domains.csv")

    official_data = load_domains(official_csv, whole_rows=True)

    # header row for latest .gov data
    headers = [
        "Domain Name", "Domain Type",
        "Agency", "Organization", "City", "State"
    ]

    domain_map = {}
    for row in official_data:
        # Turn row headers into a dict.
        dict_row = {}
        for i, cell in enumerate(row):
            dict_row[headers[i]] = cell

        domain = dict_row["Domain Name"].lower()
        agency = dict_row["Agency"].strip()
        domain_type = dict_row["Domain Type"]
        branch = branch_for(domain_type)

        domain_map[domain] = {
            "agency": agency,
            "branch": branch
        }

    return domain_map

# Not great at error handling.
def download(url, destination):
    filename, headers = urllib.request.urlretrieve(url, destination)
    return filename

# Load one or more pshtt scan files, and turn them into a dict.
# If sending in multiple paths, send from oldest to newest, as
# later scan results for the same domain will overwrite older ones.
def load_pshtt_sslyze(pshtts, sslyzes, base_domains, preloaded, filter=None):
    data = {}

    for path in pshtts:
        headers = []
        with open(path, newline='') as csvfile:
            for row in csv.reader(csvfile):
                if (row[0].lower() == "domain"):
                    headers = row
                    continue

                domain = row[0].lower()
                base_domain = base_domain_for(domain)
                if not base_domains.get(base_domain):
                    print("[load_pshtt] Skipping %s, not a federal domain." % domain)
                    continue

                agency = base_domains[base_domain]["agency"]
                branch = base_domains[base_domain]["branch"]

                if agency == "Non-Federal Agency":
                    # print("[load_pshtt] Skipping %s, marked as non-federal." % domain)
                    continue

                pshtt = {}
                for i, cell in enumerate(row):
                    pshtt[headers[i]] = cell

                if filter and (not filter(pshtt, agency, branch)):
                    # print("[load_pshtt] Skipping %s, didn't pass filter." % domain)
                    continue

                # might overwrite a scan result from a previous
                # CSV file - that's fine, we'll just go with the
                # latest one, so inputs should use latest last.
                data[domain] = {
                    'pshtt': pshtt,
                    'base_domain': base_domain,
                    'agency': agency,
                    'branch': branch,
                    'cfo_act': cfo_act(agency)
                }

    for path in sslyzes:
        headers = []
        with open(path, newline='') as csvfile:
            for row in csv.reader(csvfile):
                if (row[0].lower() == "domain"):
                    headers = row
                    continue

                domain = row[0].lower()
                base_domain = base_domain_for(domain)
                if not data.get(domain):
                    # print("[load_sslyze] Skipping %s, filtered out." % domain)
                    continue

                sslyze = {}
                for i, cell in enumerate(row):
                    sslyze[headers[i]] = cell

                # if no scanned hostname value, then no scan was performed
                if sslyze["Scanned Hostname"] and sslyze["TLSv1.2"]:
                    data[domain]['sslyze'] = sslyze


    # Run each domain through compliance_for, with the pshtt, sslyze,
    # and whether its parent is known to be preloaded
    domains = list(data.keys())
    domains.sort()
    for domain in domains:
        # Debugging:
        # print(domain)

        base_domain = base_domain_for(domain)
        if domain == base_domain:
            parent_preloaded = False # Not relevant for base domains themselves.
        else:
            parent_preloaded = (base_domain in preloaded)

        data[domain]['compliance'] = compliance_for(data[domain]['pshtt'], data[domain].get('sslyze'), parent_preloaded)

    return data

def fetch_preloaded():
    preload_json = None

    preload_path = "cache/preload.json"

    if os.path.exists(preload_path):
        logging.debug("Using cached Chrome preload list.")
        preload_json = json.loads(open(preload_path).read())
    else:
        logging.debug("Fetching Chrome preload list from source...")

        # Downloads the chromium preloaded domain list and sets it to a global set
        file_url = 'https://chromium.googlesource.com/chromium/src/net/+/master/http/transport_security_state_static.json?format=TEXT'

        # TODO: proper try/except around this network request
        request = requests.get(file_url)
        raw = request.content

        # To avoid parsing the contents of the file out of the source tree viewer's
        # HTML, we download it as a raw file. googlesource.com Base64-encodes the
        # file to avoid potential content injection issues, so we need to decode it
        # before using it. https://code.google.com/p/gitiles/issues/detail?id=7
        raw = base64.b64decode(raw).decode('utf-8')

        # The .json file contains '//' comments, which are not actually valid JSON,
        # and confuse Python's JSON decoder. Begone, foul comments!
        raw = ''.join([re.sub(r'^\s*//.*$', '', line)
                       for line in raw.splitlines()])

        preload_json = json.loads(raw)

        logging.debug("Caching preload list at %s" % preload_path)
        write(json_for(preload_json), preload_path)

    # For our purposes, we only care about entries that includeSubDomains
    fully_preloaded = []
    for entry in preload_json['entries']:
        if entry.get('include_subdomains', False) is True:
            fully_preloaded.append(entry['name'])

    return fully_preloaded

def fetch_preload_pending():

    pending_path = "cache/preload-pending.json"
    if not os.path.exists(pending_path):
        logging.debug("Fetching Chrome pending preload list...")

        pending_url = "https://hstspreload.org/api/v2/pending"
        download(pending_url, pending_path)

    raw = open(pending_path).read()
    pending_json = json.loads(raw)

    # For our purposes, we only care about entries that include subdomains.
    pending = []
    for entry in pending_json:
        if entry.get('include_subdomains', False) is True:
            pending.append(entry['name'])

    return pending

def write(content, destination):
    mkdir_p(os.path.dirname(destination))

    f = open(destination, 'w', encoding='utf-8')
    f.write(content)
    f.close()

def json_for(object):
    return json.dumps(object, sort_keys=True,
                      indent=2, default=format_datetime)

def format_datetime(obj):
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, str):
        return obj
    else:
        return None

# mkdir -p in python, from:
# https://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST:
            pass
        else:
            raise
