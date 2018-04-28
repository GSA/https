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
def compliance_for(pshtt):
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

    report['uses'] = https


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

    # Without HTTPS there can be no HSTS.
    if (https <= 0):
      hsts = -1  # N/A (considered 'No')

    else:

      # HSTS is present for the canonical endpoint.
      if (pshtt["HSTS"] == "True"):

        # Say No for too-short max-age's, and note in the extended details.
        if hsts_age >= 31536000:
          hsts = 2  # Yes
        else:
          hsts = 1  # No

      else:
        hsts = 0  # No

    # Separate preload status from HSTS status:
    #
    # * Domains can be preloaded through manual overrides.
    # * Confusing to mix an endpoint-level decision with a domain-level decision.
    if pshtt.get("HSTS Preloaded") == "True":
      preloaded = 2  # Yes
    elif (pshtt["HSTS Preload Ready"] == "True"):
      preloaded = 1  # Ready for submission
    else:
      preloaded = 0  # No

    report['hsts'] = hsts
    report['preloaded'] = preloaded

    return report

# Given a compliance report (e.g. uses=1, enforces=2, hsts=2)
# return a dict with them turned into labels
def compliance_labels(report):
    return {
        'uses': (report['uses'] >= 1),
        'enforces': (report['enforces'] >= 2),
        'hsts': (report['hsts'] >= 2),
    }

# Given a set of domains, calculate the compliance totals
# that meet M-15-13 requirements.
# Adapted from a snapshot of Pulse code:
# https://github.com/18F/pulse/blob/0528773b1d39a664ff8f62d655b8bb7c8979874c/data/processing.py#L511-L539

def compliance_totals(data, preload_pending, preloaded):
    total_report = {
        'uses': 0,
        'enforces': 0,
        'hsts': 0,

        # includes auto-protected subdomains
        'through_preloading_pending': 0,
        'through_preloading': 0,
        'hsts_or_preloading': 0,
        'hsts_or_preloading_or_pending': 0,
    }

    for domain in data.keys():
        # calculated in compliance_for() method using pshtt dat
        report = data[domain]['compliance']

        # Needs to be enabled, it's allowed for the chain to have issues
        if report['uses'] >= 1:
            total_report['uses'] += 1

        # Needs to be Default or Strict to be 'Yes'
        if report['enforces'] >= 2:
            total_report['enforces'] += 1

        # Needs to be present with >= 1 year max-age for canonical endpoint
        if report['hsts'] >= 2:
            total_report['hsts'] += 1

        if data[domain]['base_domain'] in preload_pending:
            total_report['through_preloading_pending'] += 1

        if data[domain]['base_domain'] in preloaded:
            total_report['through_preloading'] += 1

        if (
            (report['hsts'] >= 2) or
            (data[domain]['base_domain'] in preloaded)
        ):
            total_report['hsts_or_preloading'] += 1

        if (
            (report['hsts'] >= 2) or
            (data[domain]['base_domain'] in preloaded) or
            (data[domain]['base_domain'] in preload_pending)
        ):
            total_report['hsts_or_preloading_or_pending'] += 1
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

# return base domain for a subdomain
def base_domain_for(subdomain):
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
            if (not row[0]) or (row[0].lower().startswith("domain")):
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
        "Department of Agriculture",
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
        "Department of State OIG", # seen in .gov data
        "Department of Transportation",
        "Department of the Treasury",
        "Department of Veterans Affairs",
        "Environmental Protection Agency",
        "National Aeronautics and Space Administration",
        "U.S. Agency for International Development", # as seen in .gov data
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
# https://github.com/18F/pulse/blob/0528773b1d39a664ff8f62d655b8bb7c8979874c/data/processing.py#L789-L813
def branch_for(agency):
  if agency in [
    "Library of Congress",
    "The Legislative Branch (Congress)",
    "Government Printing Office",
    "Government Publishing Office",
    "Congressional Office of Compliance",
    "Stennis Center for Public Service",
    "U.S. Capitol Police",
    "Architect of the Capitol"
  ]:
    return "legislative"

  if agency in [
    "The Judicial Branch (Courts)",
    "The Supreme Court",
    "U.S Courts"
  ]:
    return "judicial"

  # I think these:
  #     jusfc.gov, wmatc.gov, and heritageabroad.gov
  # are in the executive branch, in part because of
  # https://www.usa.gov/branches-of-government
  # but to stay consistent with Pulse, and because
  # it's neglible for parent domains (3) and subdomains (~10),
  # I'll continue ignoring them.
  if agency in ["Non-Federal Agency"]:
    return "non-federal"

  else:
    return "executive"

# Download official GSA .gov dataset and create a dict of domains to agencies.
def domains_to_agencies():
    official_csv = "cache/federal-domains.csv"
    if not os.path.exists(official_csv):
        print("Downloading federal domains...")
        url = "https://github.com/GSA/data/raw/1057ec36a1e97abeaea132d2d9e3e5a31eac5b51/dotgov-domains/current-federal.csv"
        official_csv = download(url, "cache/federal-domains.csv")

    official_data = load_domains(official_csv, whole_rows=True)

    domain_map = {}
    for row in official_data:
        domain = row[0].lower()
        agency = row[2]
        domain_map[domain] = agency

    return domain_map

# Not great at error handling.
def download(url, destination):
    filename, headers = urllib.request.urlretrieve(url, destination)
    return filename

# Load one or more pshtt scan files, and turn them into a dict.
# If sending in multiple paths, send from oldest to newest, as
# later scan results for the same domain will overwrite older ones.
def load_pshtt(paths, base_domains, filter=None):
    data = {}

    for path in paths:
        with open(path, newline='') as csvfile:
            for row in csv.reader(csvfile):
                if (row[0].lower() == "domain"):
                    headers = row
                    continue

                domain = row[0].lower()
                base_domain = base_domain_for(domain)
                if not base_domains.get(base_domain):
                    # print("[load_pshtt] Skipping %s, not a federal domain." % domain)
                    continue

                agency = base_domains[base_domain]
                branch = branch_for(agency)

                if branch == "non-federal":
                    # print("[load_pshtt] Skipping %s, a non-federal domain." % domain)
                    continue

                pshtt = {}
                for i, cell in enumerate(row):
                    pshtt[headers[i]] = cell

                # By default, only load in eligible (live) domains.
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
                    'cfo_act': cfo_act(agency),
                    'compliance': compliance_for(pshtt)
                }

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
