---
layout: page
title: Resources
permalink: /resources/
---

### Articles

* 18F: [Why we use HTTPS for every .gov we make](https://18f.gsa.gov/2014/11/13/why-we-use-https-in-every-gov-website-we-make/)
* Ben Balter: [Why you should care about HTTPS, even if you have nothing to hide](http://ben.balter.com/2015/01/06/https-all-the-things/)
* Washington Post: [Federal sites leaked the locations of people seeking AIDS services for years](http://www.washingtonpost.com/blogs/the-switch/wp/2014/11/07/federal-sites-leaked-the-locations-of-people-seeking-aids-services-for-years/)
* Washington Post: [The federal government’s online privacy watchdog just made its Web site more secure](http://www.washingtonpost.com/blogs/the-switch/wp/2015/03/06/the-federal-governments-online-privacy-watchdog-just-made-its-web-site-more-secure/)
* Washington Post: [Your browser may soon force you to connect securely to some U.S. government Web sites](http://www.washingtonpost.com/blogs/the-switch/wp/2015/02/11/your-browser-may-soon-force-you-to-connect-securely-to-some-u-s-government-web-sites/)
* The Hill: [FTC enables default encryption](http://thehill.com/policy/technology/234873-ftc-enables-default-encryption)
* The Hill: [White House website goes secure](http://thehill.com/policy/technology/235323-white-house-website-goes-secure)
* 18F: [The first .gov domains hardcoded into your browser as all-HTTPS](https://18f.gsa.gov/2015/02/09/the-first-gov-domains-hardcoded-into-your-browser-as-all-https/)
* FTC: [Government agencies enable HTTP Strict Transport Security for public websites](http://www.ftc.gov/news-events/blogs/techftc/2015/02/government-agencies-enable-http-strict-transport-security-public)
* FTC: [FTC.gov is now HTTPS by default](https://www.ftc.gov/news-events/blogs/techftc/2015/03/ftcgov-now-https-default)
* Fast Company: [The Fight for HTTPS](http://www.fastcompany.com/3036430/the-fight-for-https)
* E Pluribus Unum: [White House moves WhiteHouse.gov to HTTPS by default, tying privacy to security](http://e-pluribusunum.com/2015/03/11/white-house-moves-whitehouse-gov-to-https-by-default-tying-privacy-to-security/)
* Motherboard: [Whitehouse.gov Is Now Secure By Default, Signaling a Trend in Government](http://motherboard.vice.com/read/whitehouse-site-is-now-secure-by-default-signaling-a-trend-in-government)
* NextGov: [WhiteHouse.gov Finally Gets Boosted Encryption](http://www.nextgov.com/cybersecurity/2015/03/white-house-dot-gov-website-use-https-encryption/107223/?oref=river)


### Internet standards movement

* The W3C's Technical Architecture Group has found that [the web should actively prefer secure connections](https://w3ctag.github.io/web-https/) and transition entirely to HTTPS.
* The IETF has said that [pervasive monitoring is an attack](https://datatracker.ietf.org/doc/rfc7258/), and the Internet Architecture Board (the IETF's parent organization) recommends that [new protocols use encryption by default](http://www.internetsociety.org/news/internet-society-commends-internet-architecture-board-recommendation-encryption-default).

### Industry movement

* Google [gives a search ranking boost](http://googlewebmastercentral.blogspot.com/2014/08/https-as-ranking-signal.html)  to HTTPS sites.
* Chrome plans to [mark HTTP as non-secure](https://www.chromium.org/Home/chromium-security/marking-http-as-non-secure).
* Chrome also plans to [restrict some features to HTTPS sites](https://groups.google.com/a/chromium.org/forum/#!topic/blink-dev/2LXKVWYkOus), including geolocation.
* Electronic Freedom Foundation's [HTTPS-Everywhere Project](https://www.eff.org/https-everywhere)

### Standards and tools

[SSL Labs](https://www.ssllabs.com/ssltest/) is a universally referenced HTTPS evaluation and grading tool.

18F has also written [`https-scan`](https://github.com/18F/https-scan), a command line tool which runs one or more domains through several separate small tools:

* [`ssllabs-scan`](https://github.com/ssllabs/ssllabs-scan) - Command line tool for the SSL Labs API. (See its [Terms of Use](https://github.com/ssllabs/ssllabs-scan/blob/master/ssllabs-api-docs.md#terms-and-conditions).)
* [`mixed-content-scan`](https://github.com/bramus/mixed-content-scan) - Command line tool for walking over a website and scanning for the use of insecure resources.
* [`site-inspector`](https://github.com/benbalter/site-inspector-ruby) - Scan a domain for various web/HTTP-related properties, including HTTPS support.
