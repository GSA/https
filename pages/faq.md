---
layout: page
title: HTTPS FAQ
permalink: /faq/
description: "Frequently asked questions about HTTPS: what it does, and what it doesn't do."
---

### What does HTTPS do?

When properly configured, an HTTPS connection guarantees three things:

* **Confidentiality.** The visitor's connection is encrypted, obscuring URLs, cookies, and other sensitive metadata.
* **Authenticity.** The visitor is talking to the "real" website, and not to an impersonator or through a "man-in-the-middle".
* **Integrity.** The data sent between the visitor and the website has not been tampered with or modified.

A plain HTTP connection can be easily monitored, modified, and impersonated.

### What information does HTTPS protect?

HTTPS encrypts nearly all information sent between a client and a web service.

For example, an **unencrypted HTTP** request reveals not just the body of the request, but the full URL, query string, and various HTTP headers about the client and request:

<img src="/assets/images/with-http-headers.png" title="What you see with HTTP" style="border: 1px solid black" />

An **encrypted HTTPS** request protects most things:

<img src="/assets/images/with-https-headers.png" title="What you see with HTTPS" style="border: 1px solid black" />

This is the same for all HTTP methods (GET, POST, PUT, etc.). The URL path and query string parameters are encrypted, as are POST bodies.

### What information does HTTPS _not_ protect?

While HTTPS encrypts the entire HTTP request and response, the DNS resolution and connection setup can reveal other information, such as the full domain or subdomain and the originating IP address, as shown above.

Additionally, attackers can still analyze encrypted HTTPS traffic for "side channel" information. This can include the time spent on site, or the relative size of user input.

### How does migrating to HTTPS affect search engine optimization (SEO)?

In general, migrating to HTTPS improves website SEO and intelligence.

* As of August 2014, Google [uses HTTPS as a ranking signal](http://googlewebmastercentral.blogspot.com/2014/08/https-as-ranking-signal.html), which can improve search rankings.
* Migrating to HTTPS will improve analytics about web traffic referred from HTTPS websites, as referrer information [is not passed from HTTPS websites to HTTP websites](https://stackoverflow.com/a/1361720/16075).

To make the migration as smooth as possible, and avoid taking a SEO hit:

* Use a **proper 301 redirect** to redirect users from `http://` to `https://`. **Do not use a 302 redirect**, as this may negatively impact search rankings.
* Use the [canonical link element](https://en.wikipedia.org/wiki/Canonical_link_element) (`<link rel="canonical">`) to inform search engines that the "canonical" URL for a website uses `https://`.

### How difficult is it to attack an HTTPS connection?

Attacks on HTTPS connections generally fall into 3 categories:

* Compromising the quality of the HTTPS connection, through cryptanalysis or other protocol weaknesses.
* Compromising the client computer, such as by installing a malicious root certificate into the system or browser trust store.
* Obtaining a "rogue" certificate trusted by major browsers, generally by manipulating or compromising a certificate authority.

These are all possible, but for most attackers they are very difficult and require significant expense. Importantly, they are all _targeted_ attacks, and are not feasible to execute against any user connecting to any website.

By contrast, plain HTTP connections can be easily intercepted and modified by anyone involved in the network connection, and so attacks can be carried out at large scale and at low cost.

### Why isn't DNSSEC good enough?

[DNSSEC](https://en.wikipedia.org/wiki/Domain_Name_System_Security_Extensions) attempts to guarantee that domain names are resolved to correct IP addresses.

However, DNS resolution is just one aspect of securely communicating on the internet. DNSSEC does not fully secure a domain:

* Once DNS resolution is complete, DNSSEC does not ensure the confidentiality or integrity of communication between a client and the destination IP.

* No major web browsers inform the user when DNSSEC validation fails, limiting its strength and enforceability.

HTTPS guarantees the confidentiality and integrity of communication between client and server, and web browsers have rigorous and evolving HTTPS enforcement policies.

### How does HTTPS protect against DNS spoofing?

In practice, HTTPS can protect communication with a domain even in the absence of DNSSEC support.

A valid HTTPS certificate shows that the server has demonstrated ownership over the domain to a trusted certificate authority at the time of certificate issuance.

To ensure that an attacker cannot use DNS spoofing to direct the user to a plain `http://` connection where traffic can be intercepted, websites can use [HTTP Strict Transport Security](/hsts/) (HSTS) to instruct browsers to require an HTTPS connection for their domain at all times.

This means that an attacker that successfully spoofs DNS resolution must also create a valid HTTPS connection. This makes DNS spoofing as challenging and expensive as [attacking HTTPS generally](#how-difficult-is-it-to-attack-an-https-connection?).

If the attacker spoofs DNS but doesn't compromise HTTPS, users will receive a notable warning message from their browser that will prevent them from visiting the possibly malicious site. If the site uses HSTS, there will be no option for the visitor to disregard and click through the warning.

HTTPS and HSTS work together to protect a domain against DNS spoofing.
