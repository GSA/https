#!/usr/bin/env python

import utils

# get mapping of domains to agency
base_domains = utils.domains_to_agencies()

# get current and pending preloaded domains
# Downloads live from remote sources. (clear cache/ to re-download)
preloaded = set(utils.fetch_preloaded()) & set(base_domains)
preload_pending = set(utils.fetch_preload_pending()) & set(base_domains)

# paths to scanned data
parents_path = "../hostnames/scanned/parents-2016-12.csv"
dap_path = "../hostnames/scanned/dap-2016-12.csv"
censys_path = "../hostnames/scanned/censys-2016-12.csv"
eot_2012_path = "../hostnames/scanned/eot-2012.csv"
eot_2016_path = "../hostnames/scanned/eot-2016.csv"

# past scans
def past(type, date):
  return ("../hostnames/scanned/past/%s-%s.csv" % (type, date))

def pct(num, denom):
  return round((num / denom) * 100)

def compliance_stats(name, scans, filter):
  data = utils.load_pshtt(scans, base_domains, filter=filter)
  totals = utils.compliance_totals(data, preload_pending, preloaded)

  count = len(data.keys())

  print()
  print("=====================================================")
  print("  %s" % name)
  print("=====================================================")
  print()
  print("Total domains: %i" % count)
  print()
  print("== Direct enforcement ==")
  print("Uses HTTPS: %i (%i%%)" % (totals['uses'], pct(totals['uses'], count)))
  print("Enforces HTTPS: %i (%i%%)" % (totals['enforces'], pct(totals['enforces'], count)))
  print("Strong HSTS: %i (%i%%)" % (totals['hsts'], pct(totals['hsts'], count)))
  # print("Strong HSTS (+ preloading): %i (%i%%)" % (totals['hsts_or_preloading'], pct(totals['hsts_or_preloading'], count)))
  # print()
  # print("== Coverage through preloading alone ==")
  # print("Preloaded: %i (%i%%)" % (totals['through_preloading'], pct(totals['through_preloading'], count)))
  # print("Preload pending: %i (%i%%)" % (totals['through_preloading_pending'], pct(totals['through_preloading_pending'], count)))

  print()

def compliance_csv(reports, path):
  header = ["Type", "Name", "Total Domains", "Uses HTTPS", "Enforces HTTPS", "HSTS", "Uses HTTPS (%)", "Enforces HTTPS (%)", "HSTS (%)"]
  rows = []
  for report in reports:
    rows.append(compliance_csv_row(report))

  utils.save_csv(header, rows, path)

def compliance_csv_row(report):
  data = utils.load_pshtt(report['files'], base_domains, filter=report['filter'])
  totals = utils.compliance_totals(data, preload_pending, preloaded)

  count = len(data.keys())

  return [
    report['type'],
    report['name'],
    count,
    totals['uses'],
    totals['enforces'],
    totals['hsts'],
    pct(totals['uses'], count),
    pct(totals['enforces'], count),
    pct(totals['hsts'], count),
  ]

# interesting swathes to check for compliance
parents_only = [parents_path]
all_domains = [parents_path, dap_path, censys_path, eot_2012_path, eot_2016_path]

# This should reproduce Pulse top-line stats: live second-level domains
# compliance_stats(parents_only, utils.live_only)

parent_pasts = ['2015-06-13',  '2015-06-19',  '2015-06-26',  '2015-07-03',  '2015-07-10',  '2015-07-17',  '2015-07-24',  '2015-07-31',  '2015-08-07',  '2015-08-14',  '2015-08-21',  '2015-08-28',  '2015-09-04',  '2015-09-11',  '2015-09-18',  '2015-09-25',  '2015-10-09',  '2015-10-16',  '2015-10-22',  '2015-10-30',  '2015-11-06',  '2015-11-13',  '2015-11-21',  '2015-11-28',  '2015-12-04',  '2015-12-10',  '2015-12-18',  '2015-12-26',  '2016-01-02',  '2016-01-08',  '2016-01-15',  '2016-01-23',  '2016-01-29',  '2016-02-04',  '2016-02-08',  '2016-02-17',  '2016-02-26',  '2016-03-03',  '2016-03-13',  '2016-03-18',  '2016-03-25',  '2016-04-01',  '2016-04-08',  '2016-04-15',  '2016-04-22',  '2016-04-29',  '2016-05-06',  '2016-05-13',  '2016-05-20',  '2016-05-27',  '2016-06-03',  '2016-07-05',  '2016-07-08',  '2016-07-15',  '2016-07-22',  '2016-07-29',  '2016-08-05',  '2016-08-12',  '2016-08-19',  '2016-08-26',  '2016-09-02',  '2016-09-09',  '2016-09-16',  '2016-09-23',  '2016-10-03',  '2016-10-07',  '2016-10-14',  '2016-10-21',  '2016-10-28',  '2016-11-04',  '2016-11-11',  '2016-11-18',  '2016-11-25',  '2016-12-02',  '2016-12-05',  '2016-12-08',  '2016-12-17',  '2016-12-21',  '2016-12-24',  '2016-12-26',  '2016-12-28',  '2016-12-31']
dap_pasts = ["2016-07-12", "2016-12-05", "2016-12-31"]
censys_pasts = ["2016-08-04", "2016-12-05", "2016-12-31"]

# approximation of all subdomains, given data known from 3 sources at 3 junctures
all_pasts = [

]


cfo_act_groups = [
    "Department of Agriculture",
    "Department of Commerce",
    "Department of Defense",
    "Department of Education",
    "Department of Energy",
    "Department of Health and Human Services",
    "Department of Homeland Security",
    "Department of Housing and Urban Development",
    "Department of the Interior",
    [
        "Department of Justice",
        "Terrorist Screening Center", # (DOJ/FBI) as seen in .gov data
    ],
    "Department of Labor",
    [
        "Department of State",
        "Department of State OIG", # seen in .gov data
    ],
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

reports = []
for group in cfo_act_groups:
  if isinstance(group, str):
    group = [group]

  reports.append({
    'type': 'agency parent domains',
    'name': str.join(", ", group),
    'files': parents_only,
    'filter': utils.for_agencies(group)
  })


compliance_csv(reports, "cache/agencies-parents-latest.csv")
