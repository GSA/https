##
# Download data from the Pulse S3 bucket to measure scans over time.
# Must be run from a machine where "aws s3 cp" has credentials for the bucket.

import os
import subprocess

AWS_REGION = "us-gov-west-1"
BUCKET_NAME = "cg-4adefb86-dadb-4ecf-be3e-f1c7b4f6d084"
DATA_DIR = "data/pulse"

# Before BOD 18-01 was issued and before Pulse data was restructured
pre_bod = ["2017-02-10", "2017-02-12", "2017-02-15", "2017-02-17", "2017-02-20", "2017-02-22", "2017-02-24", "2017-02-27", "2017-03-01", "2017-03-03", "2017-03-06", "2017-03-08", "2017-03-10", "2017-03-13", "2017-03-15", "2017-03-17", "2017-03-20", "2017-03-22", "2017-03-24", "2017-03-27", "2017-03-30", "2017-03-31", "2017-04-04", "2017-04-06", "2017-04-08", "2017-04-11", "2017-04-13", "2017-04-20", "2017-04-22", "2017-04-25", "2017-04-27", "2017-04-29", "2017-05-02", "2017-05-04", "2017-05-06", "2017-05-09", "2017-05-11", "2017-05-13", "2017-05-16", "2017-05-18", "2017-05-20", "2017-05-23", "2017-05-25", "2017-05-27", "2017-05-30", "2017-06-01", "2017-06-03", "2017-06-05", "2017-07-02", "2017-07-03", "2017-07-05", "2017-07-07", "2017-07-10", "2017-07-12", "2017-07-14", "2017-07-17", "2017-07-19", "2017-07-21", "2017-07-25", "2017-07-26", "2017-07-28", "2017-07-31", "2017-08-02", "2017-08-07", "2017-08-09", "2017-08-11", "2017-08-14", "2017-08-16", "2017-08-18", "2017-08-21", "2017-08-23", "2017-08-25", "2017-09-28"]

# After BOD 18-01 was issued and after Pulse data was restructured
# Exceptions:
#  2018-01-02: no subdomains/scan/results
post_bod = ["2017-11-20", "2017-11-25", "2017-12-11", "2017-12-13", "2017-12-15", "2017-12-16", "2017-12-17", "2017-12-18", "2017-12-19", "2017-12-20", "2017-12-21", "2017-12-22", "2017-12-23", "2017-12-24", "2017-12-25", "2017-12-26", "2017-12-27", "2017-12-28", "2017-12-29", "2017-12-30", "2017-12-31", "2018-01-01", "2018-01-03", "2018-01-04", "2018-01-05", "2018-01-06", "2018-01-07", "2018-01-08", "2018-01-09", "2018-01-10", "2018-01-11", "2018-01-12", "2018-01-13", "2018-01-14", "2018-01-15", "2018-01-16", "2018-01-17", "2018-01-18", "2018-01-19", "2018-01-20", "2018-01-21", "2018-01-22", "2018-01-23", "2018-01-24", "2018-01-25", "2018-01-26", "2018-01-27", "2018-01-28", "2018-01-29", "2018-01-30", "2018-01-31", "2018-02-01", "2018-02-02", "2018-02-03", "2018-02-04", "2018-02-05", "2018-02-06", "2018-02-07", "2018-02-08", "2018-02-09", "2018-02-10", "2018-02-11", "2018-02-12", "2018-02-13", "2018-02-14", "2018-02-15", "2018-02-16", "2018-02-17", "2018-02-18", "2018-02-19", "2018-02-20", "2018-02-21", "2018-02-22", "2018-02-23", "2018-02-24", "2018-02-25", "2018-02-26", "2018-02-27", "2018-02-28", "2018-03-01", "2018-03-02", "2018-03-03", "2018-03-04", "2018-03-05", "2018-03-06", "2018-03-07", "2018-03-08", "2018-03-09", "2018-03-10", "2018-03-11", "2018-03-15", "2018-03-16", "2018-03-17", "2018-03-18", "2018-03-19", "2018-03-20", "2018-03-21", "2018-03-23", "2018-03-24", "2018-03-25", "2018-03-26", "2018-03-27", "2018-03-28", "2018-03-29", "2018-03-30", "2018-03-31", "2018-04-01", "2018-04-02", "2018-04-03", "2018-04-09", "2018-04-10", "2018-04-11", "2018-04-12", "2018-04-13", "2018-04-14", "2018-04-15", "2018-04-16", "2018-04-25", "2018-04-26", "2018-04-27", "2018-04-28"]

def shell_out(command, env=None):
    response = subprocess.check_output(command, shell=False, env=env)
    output = str(response, encoding='UTF-8')
    return output

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST:
            pass
        else:
            raise


# when = "pre" or "post"
def download_date(date, when="post"):

  def download(date, file):
    url = "s3://%s/archive/%s/%s" % (BUCKET_NAME, date, file)

    # local destinations are relative to data/
    path = os.path.join(DATA_DIR, "%s-bod" % when, date, file)

    shell_out(["aws", "s3", "cp", url, path])

  try:
    # Newer streamlined directory structure
    if when == "post":
      download(date, "parents/results/pshtt.csv")
      download(date, "parents/results/sslyze.csv")
      download(date, "parents/results/meta.json")
      download(date, "subdomains/scan/results/pshtt.csv")
      download(date, "subdomains/scan/results/sslyze.csv")
      download(date, "subdomains/scan/results/meta.json")

    # Older, more laborious directory structure
    elif when == "pre":
      download(date, "scan/pshtt.csv")
      download(date, "scan/sslyze.csv")
      download(date, "scan/meta.json")
      download(date, "subdomains/scan/url/results/pshtt.csv")
      download(date, "subdomains/scan/url/results/sslyze.csv")
      download(date, "subdomains/scan/url/results/meta.json")
      download(date, "subdomains/scan/censys/results/pshtt.csv")
      download(date, "subdomains/scan/censys/results/sslyze.csv")
      download(date, "subdomains/scan/censys/results/meta.json")
  except subprocess.CalledProcessError:
    print("[%s] MISSING SOMETHING" % date)


# for date in post_bod:
#   download_date(date, "post")

# for date in pre_bod:
#   download_date(date, "pre")
