
#########################################################
#
# Just scratch space, this won't execute or import properly.
#
#########################################################

name = "All executive parent domains"
compliance_stats(name, parents_only, utils.executive_only)

name = "All executive CFO Act parent domains"
compliance_stats(name, parents_only, utils.cfo_act_only)

name = "All executive CFO Act (minus DoD) parent domains"
compliance_stats(name, parents_only, utils.cfo_act_only_sans_dod)

name = "All executive non-CFO-Act parent domains"
compliance_stats(name, parents_only, utils.executive_non_cfo_act)


name = "All subdomains"
compliance_stats(name, subdomains, utils.live_only)

name = "All executive subdomains"
compliance_stats(name, subdomains, utils.executive_only)

name = "All executive CFO Act subdomains"
compliance_stats(name, subdomains, utils.cfo_act_only)

name = "All executive CFO Act (minus DoD) subdomains"
compliance_stats(name, subdomains, utils.cfo_act_only_sans_dod)

name = "All executive non-CFO-Act subdomains"
compliance_stats(name, subdomains, utils.executive_non_cfo_act)

# agency = "General Services Administration"
# compliance_stats(agency, plus_dap_and_censys, utils.for_agency(agency))

for date in parents_pasts:
  name = "All parent domains (%s)" % date
  compliance_stats(name, [past("parents", date)], utils.live_only)

name = "All parent domains (2016-12-28)"
compliance_stats(name, parents_only, utils.live_only)


for date in dap_pasts:
  name = "All DAP subdomains (%s)" % date
  compliance_stats(name, [past("dap", date)], utils.live_only)

name = "All DAP subdomains (2016-12-28)"
compliance_stats(name, [dap_path], utils.live_only)


for date in censys_pasts:
  name = "All Censys subdomains (%s)" % date
  compliance_stats(name, [past("censys", date)], utils.live_only)

name = "All Censys subdomains (2016-12-28)"
compliance_stats(name, [censys_path], utils.live_only)




reports = []
for date in parent_pasts:
  reports.append({
    'type': 'parents',
    'name': date,
    'files': [past('parents', date)],
    'filter': utils.live_only
  })
compliance_csv(reports, "cache/parents-history.csv")


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




# approximation of all subdomains, given data known from 3 sources at 3 junctures
all_pasts = [
  ["data/parents-2016-07-15.csv", "data/dap-2016-07-12.csv", "data/censys-2016-08-04.csv"],
  ["data/parents-2016-12-05.csv", "data/dap-2016-12-05.csv", "data/censys-2016-12-05.csv"],
  ["data/parents-2016-12-31.csv", "data/dap-2016-12-31.csv", "data/censys-2016-12-31.csv"],
]

reports = []
reports.append({
  'type': 'all domains/subdomains',
  'name': "2016-08-01", # approximate
  'files': all_pasts[0],
  'filter': utils.live_only
})
reports.append({
  'type': 'all domains/subdomains',
  'name': "2016-12-05",
  'files': all_pasts[1],
  'filter': utils.live_only
})
reports.append({
  'type': 'all domains/subdomains',
  'name': "2016-12-31",
  'files': all_pasts[2],
  'filter': utils.live_only
})


compliance_csv(reports, "cache/all-domains-last-6-months.csv")




reports = []
for date in parent_pasts:
  reports.append({
    'type': 'parents',
    'name': date,
    'files': [past('parents', date)],
    'filter': utils.cfo_act_only
  })
compliance_csv(reports, "cache/cfo-act-parents-history.csv")




reports = []
reports.append({
  'type': 'Most subdomains on 12/31 (all branches)',
  'name': "2016-12-31",
  'files': all_domains,
  'filter': utils.cfo_act_only
})
compliance_csv(reports, "cache/cfo-act-all-domains-snapshot.csv")





reports = []
reports.append({
  'type': 'Most subdomains on 12/31 (all branches)',
  'name': "2016-12-31",
  'files': all_domains,
  'filter': utils.live_only
})
compliance_csv(reports, "cache/all-domains-snapshot.csv")




# Estimating traffic covered by HTTPS, now (for subdomains)
# and over time (for parent domains).
# Load in all DAP-tracked domains with > 1000 visits over the prior 30 days
analytics_rows = utils.load_domains("data/analytics-domains/all-domains-30-days-2017-01-01.csv", whole_rows=True)
analytics = {}
for row in analytics_rows:
  analytics[row[0].lower()] = int(row[1])

# load the exec branch domains to evaluate against, filter to those included
data = utils.load_pshtt(
  all_domains, base_domains,
  filter=utils.specific_executive(list(analytics.keys()))
)

# Now go through each one and write out a spreadsheet combining the
# results for each domain with their visits as recorded in DAP

tracked_domains = list(data.keys())
tracked_domains.sort()

headers = ["Domain", "Base Domain", "Visits", "Uses HTTPS", "Enforces HTTPS", "HSTS", "Downgrades HTTPS"]
rows = []
for domain in tracked_domains:
  labels = utils.compliance_labels(data[domain]['compliance'])

  rows.append([
    domain,
    data[domain]['base_domain'],
    analytics[domain],
    labels['uses'],
    labels['enforces'],
    labels['hsts'],
    data[domain]['pshtt']['Downgrades HTTPS']
  ])

utils.save_csv(headers, rows, "cache/https-by-dap-visits.csv")

