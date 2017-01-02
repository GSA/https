name = "All executive parent domains"
compliance_stats(name, parents_only, utils.executive_only)

name ="All executive CFO Act parent domains"
compliance_stats(name, parents_only, utils.cfo_act_only)

name ="All executive CFO Act (minus DoD) parent domains"
compliance_stats(name, parents_only, utils.cfo_act_only_sans_dod)

name ="All executive non-CFO-Act parent domains"
compliance_stats(name, parents_only, utils.executive_non_cfo_act)


name = "All subdomains"
compliance_stats(name, subdomains, utils.live_only)

name = "All executive subdomains"
compliance_stats(name, subdomains, utils.executive_only)

name ="All executive CFO Act subdomains"
compliance_stats(name, subdomains, utils.cfo_act_only)

name ="All executive CFO Act (minus DoD) subdomains"
compliance_stats(name, subdomains, utils.cfo_act_only_sans_dod)

name ="All executive non-CFO-Act subdomains"
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

