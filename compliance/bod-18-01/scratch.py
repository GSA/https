
reports = []
reports.append({
  'type': 'Most subdomains on 12/31 (all branches)',
  'name': "2016-12-31",
  'files': post_bod,
  'filter': utils.executive_only
})
compliance_csv(reports, "cache/all-domains-executive-snapshot.csv")
