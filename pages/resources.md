---
layout: base

title: Resources
permalink: /resources/
description: "Articles, news, and tools about HTTPS."
---

### Ask Others In Government

The HTTPS-Help listserv is a support forum for anyone with a `.gov` or `.mil` email address.  Any questions, ideas, or general discussion about HTTPS is welcome.  Join by sending a message to [`listserv@listserv.gsa.gov`](mailto:listserv@listserv.gsa.gov) with **no subject** and a body of "subscribe https-help".

### Learning

The DigitalGov University has several presentations on HTTPS from the General Services Administration:

* **[An Introduction to HTTPS for Beginners](https://www.youtube.com/watch?v=d2GmcPYWm5k)** (June 2015), by Eric Mill and Gray Brooks. This introduction runs a little over an hour, and covers how HTTP and the web work, what HTTPS does to help, and [why we should use it for everything](/everything/).

* **[Implementing HTTPS](https://www.youtube.com/watch?v=rnM2qAfEG-M)** (July 2015), by Eric Mill and Gray Brooks. A more detailed explanation of how HTTPS works, how to migrate a website to HTTPS, the [technical concepts](/technical-guidelines/) you should be aware of when implementing HTTPS, and new and upcoming advances in HTTPS.

* **[Migrating to HTTPS](https://www.youtube.com/watch?v=X5H8JRULDOo)** (July 2016), by Eric Mill and Timothy Badaczewski. This presentation covers common issues common to federal HTTPS migrations, including: [HTTP Strict Transport Security](/hsts/) (HSTS), [getting certificates](/certificates/), [mixed content](/mixed-content/), and [search engine optimization](/faq/#how-does-migrating-to-https-affect-search-engine-optimization-seo) (SEO).

### Tools

* [`crt.sh`](https://crt.sh) - An [open source](https://github.com/crtsh) public viewer for [Certificate Transparency](/certificates/#certificate-transparency) logs. For example, you can view [all publicly logged whitehouse.gov certificates](https://crt.sh/?q=whitehouse.gov).
* [`certspotter`](https://github.com/SSLMate/certspotter) - An open source tool for monitoring issuance of certificates that appear in [Certificate Transparency](/certificates/#certificate-transparency) logs.
* [`certlint`](https://github.com/awslabs/certlint) - An open source tool that reviews x.509 certificates for compliance with CA/Browser Forum requirements and various RFCs.
* [`ssllabs-scan`](https://github.com/ssllabs/ssllabs-scan) - Command line tool for the API for [SSL Labs](https://www.ssllabs.com/ssltest/), a universally referenced HTTPS evaluation and grading tool for public-facing websites.
* [`site-inspector`](https://github.com/benbalter/site-inspector) - Scan a domain for various web/HTTP-related properties, including HTTPS support.
* [`mixed-content-scan`](https://github.com/bramus/mixed-content-scan) - Command line tool for walking over a website and scanning for the use of insecure resources.

### HTTPS in .gov

* DigitalGov: [Secure Central Hosting for the Digital Analytics Program](https://www.digitalgov.gov/2015/08/14/secure-central-hosting-for-the-digital-analytics-program/)
* FTC: [FTC.gov is now HTTPS by default](https://www.ftc.gov/news-events/blogs/techftc/2015/03/ftcgov-now-https-default)
* Privacy and Civil Liberties Oversight Board: [PCLOB.gov is now HTTPS by default](https://www.pclob.gov/newsroom/20150318.html)
* CIA: [Statement on CIA Website Enhancement](https://www.cia.gov/news-information/press-releases-statements/press-release-archive-2006/statement-on-cia-website-enhancement.html) from 2006
* 18F: [Why we use HTTPS for every .gov we make](https://18f.gsa.gov/2014/11/13/why-we-use-https-in-every-gov-website-we-make/)
* 18F: [The first .gov domains hardcoded into your browser as all-HTTPS](https://18f.gsa.gov/2015/02/09/the-first-gov-domains-hardcoded-into-your-browser-as-all-https/)
