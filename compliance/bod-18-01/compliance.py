#!/usr/bin/env python

import utils
import glob

## Todo for DHS:
# * compare data across all dates

## Todo for me:
# * pre-bod path and post-bod path
# * parents-only data going back to 2015?
# * cross-reference with DAP?

# get mapping of domains to agency
base_domains = utils.domains_to_agencies()

# get current and pending preloaded domains
# Downloads live from remote sources. (clear cache/ to re-download)
preloaded = set(utils.fetch_preloaded()) & set(base_domains)

# See download.py for which dates are downloaded for each phase.

# pre-BOD measurements (no 3DES checking, old dir structure)
pre_bod = [x.split("/")[-1] for x in glob.glob("data/pulse/pre-bod/*")]
pre_bod.sort()

# post-BOD measurements (bod_crypto measured, new dir structure)
post_bod = [x.split("/")[-1] for x in glob.glob("data/pulse/post-bod/*")]
post_bod.sort()


# post-bod paths
def pshtts_and_sslyzes_for(date):
  pshtts = []
  sslyzes = []

  if date in post_bod:
    pshtts.append("data/pulse/post-bod/%s/parents/results/pshtt.csv" % date)
    pshtts.append("data/pulse/post-bod/%s/subdomains/scan/results/pshtt.csv" % date)
    sslyzes.append("data/pulse/post-bod/%s/parents/results/sslyze.csv" % date)
    sslyzes.append("data/pulse/post-bod/%s/subdomains/scan/results/sslyze.csv" % date)
  elif date in pre_bod:
    pshtts.append("data/pulse/pre-bod/%s/scan/pshtt.csv" % date)
    pshtts.append("data/pulse/pre-bod/%s/subdomains/scan/censys/results/pshtt.csv" % date)
    pshtts.append("data/pulse/pre-bod/%s/subdomains/scan/url/results/pshtt.csv" % date)
    sslyzes.append("data/pulse/pre-bod/%s/scan/sslyze.csv" % date)
    sslyzes.append("data/pulse/pre-bod/%s/subdomains/scan/censys/results/sslyze.csv" % date)
    sslyzes.append("data/pulse/pre-bod/%s/subdomains/scan/url/results/sslyze.csv" % date)

  return pshtts, sslyzes

def pct(num, denom):
  return round((num / denom) * 100)

def compliance_stats(name, date, filter):
  pshtts, sslyzes = pshtts_and_sslyzes_for(date)
  data = utils.load_pshtt_sslyze(pshtts, sslyzes, base_domains, preloaded, filter=filter)
  totals = utils.compliance_totals(data)

  count = len(data.keys())

  if count == 0:
    print("No rows returned, no data to display.")
    return

  print()
  print("=====================================================")
  print(" [%s] %s" % (date, name))
  print("=====================================================")
  print()
  print("Total domains: %i" % count)
  print()
  print("== Direct enforcement ==")
  print("Enforces HTTPS: %i (%i%%)" % (totals['enforces'], pct(totals['enforces'], count)))
  print("Strong HSTS: %i (%i%%)" % (totals['hsts'], pct(totals['hsts'], count)))

  if date in post_bod:
    print("RC4 support: %i (%i%%)" % (totals['rc4'], pct(totals['rc4'], count)))
    print("3DES support: %i (%i%%)" % (totals['3des'], pct(totals['3des'], count)))
    print("Free of Known-weak Crypto: %i (%i%%)" % (totals['bod_crypto'], pct(totals['bod_crypto'], count)))
    print("Compliant with BOD 18-01: %i (%i%%)" % (totals['compliant'], pct(totals['compliant'], count)))
  elif date in pre_bod:
    print("Compliant with M-15-13: %i (%i%%)" % (totals['m1513'], pct(totals['m1513'], count)))

  print()

def compliance_csv(dates, when, filter, path):
  if when == "pre":
    header = [
      "Date", "Total Hostnames",
      "Enforces HTTPS", "HSTS",
      "Compliant with M-15-13",
      "Enforces HTTPS (%)", "HSTS (%)",
      "Compliant with M-15-13 (%)",
    ]
  elif when == "post":
    header = [
      "Date", "Total Hostnames",
      "Enforces HTTPS", "HSTS",
      "RC4", "3DES", "Free of SSLv2/SSLv3/RC4/3DES",
      "Compliant with BOD 18-01",
      "Enforces HTTPS (%)", "HSTS (%)",
      "RC4 (%)", "3DES (%)", "Free of SSLv2/SSLv3/RC4/3DES (%)",
      "Compliant with BOD 18-01 (%)",
    ]

  rows = []
  for date in dates:
    rows.append(compliance_csv_row(date, filter))

  utils.save_csv(header, rows, path)

def compliance_csv_row(date, filter):
  pshtts, sslyzes = pshtts_and_sslyzes_for(date)
  data = utils.load_pshtt_sslyze(pshtts, sslyzes, base_domains, preloaded, filter=filter)
  totals = utils.compliance_totals(data)

  count = len(data.keys())

  if date in pre_bod:
    return [
      date,
      count,
      totals['enforces'],
      totals['hsts'],
      totals['m1513'],
      pct(totals['enforces'], count),
      pct(totals['hsts'], count),
      pct(totals['m1513'], count)
    ]
  elif date in post_bod:
    return [
      date,
      count,
      totals['enforces'],
      totals['hsts'],
      totals['rc4'],
      totals['3des'],
      totals['bod_crypto'],
      totals['compliant'],
      pct(totals['enforces'], count),
      pct(totals['hsts'], count),
      pct(totals['rc4'], count),
      pct(totals['3des'], count),
      pct(totals['bod_crypto'], count),
      pct(totals['compliant'], count)
    ]



name = "Most recent (all executive)"
compliance_stats(name, post_bod[-1], utils.executive_only)

# This should reproduce Pulse top-line stats for a given date.
compliance_csv([post_bod[-1]], "post", utils.executive_only, "cache/most-recent-post-bod.csv")
