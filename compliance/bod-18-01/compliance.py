#!/usr/bin/env python

import utils

## Todo for DHS:
# * combine parents + subdomains data
# * factor in preloading of parents into HSTS
# * load in sslyze data too
# * download all data from S3

## Todo for me:
# * pre-bod path and post-bod path
# * parents-only data going back to 2015?
# * cross-reference with DAP?

# get mapping of domains to agency
base_domains = utils.domains_to_agencies()

# get current and pending preloaded domains
# Downloads live from remote sources. (clear cache/ to re-download)
preloaded = set(utils.fetch_preloaded()) & set(base_domains)
preload_pending = set(utils.fetch_preload_pending()) & set(base_domains)

# pre-BOD measurements (no 3DES checking, old dir structure)
pre_bod = []

# post-BOD measurements (bod_crypto measured, new dir structure)
post_bod = ["2018-04-28"]


# post-bod paths
def pshtts_and_sslyzes_for(date):
  pshtts = []
  pshtts.append("data/pulse/post-bod/%s/parents/results/pshtt.csv" % date)
  pshtts.append("data/pulse/post-bod/%s/subdomains/scan/results/pshtt.csv" % date)

  sslyzes = []
  sslyzes.append("data/pulse/post-bod/%s/parents/results/sslyze.csv" % date)
  sslyzes.append("data/pulse/post-bod/%s/subdomains/scan/results/sslyze.csv" % date)

  return pshtts, sslyzes

def pct(num, denom):
  return round((num / denom) * 100)

def compliance_stats(name, date, filter):
  pshtts, sslyzes = pshtts_and_sslyzes_for(date)
  data = utils.load_pshtt_sslyze(pshtts, sslyzes, base_domains, filter=filter)
  totals = utils.compliance_totals(data, preload_pending, preloaded)

  count = len(data.keys())

  if count == 0:
    print("No rows returned, no data to display.")
    return

  print()
  print("=====================================================")
  print("  %s" % name)
  print("=====================================================")
  print()
  print("Total domains: %i" % count)
  print()
  print("== Direct enforcement ==")
  print("Enforces HTTPS: %i (%i%%)" % (totals['enforces'], pct(totals['enforces'], count)))
  print("Strong HSTS: %i (%i%%)" % (totals['hsts'], pct(totals['hsts'], count)))
  print("RC4 support: %i (%i%%)" % (totals['rc4'], pct(totals['rc4'], count)))
  print("3DES support: %i (%i%%)" % (totals['3des'], pct(totals['3des'], count)))
  print("Free of Known-weak Crypto: %i (%i%%)" % (totals['bod_crypto'], pct(totals['bod_crypto'], count)))
  print("Compliant with BOD 18-01: %i (%i%%)" % (totals['compliant'], pct(totals['compliant'], count)))
  print()

def compliance_csv(reports, path):
  header = ["Type", "Name", "Total Domains", "Enforces HTTPS", "HSTS", "Free of SSLv2/SSLv3/RC4/3DES", "Enforces HTTPS (%)", "HSTS (%)"]
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
    totals['enforces'],
    totals['hsts'],
    totals['bod_crypto'],
    pct(totals['enforces'], count),
    pct(totals['hsts'], count),
    pct(totals['bod_crypto'], count),
  ]


# This should reproduce Pulse top-line stats for a given date.
most_recent = "2018-04-28"
compliance_stats("Most recent Pulse numbers", most_recent, utils.executive_only)
