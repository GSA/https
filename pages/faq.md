---
layout: page
title: Introduction to HTTPS
permalink: /faq/
description: "An introduction to HTTPS, and frequently asked questions."
---

Below are some frequently asked questions and answers about HTTPS.

For an in-depth introduction (no technical background required), check out the DigitalGov University presentation, **["An Introduction to HTTPS"](https://www.youtube.com/watch?v=d2GmcPYWm5k)**, to learn what HTTPS is and how it protects web services and users.

* [What does HTTPS do?](#what-does-https-do%3f)
* [What information does HTTPS protect?](#what-information-does-https-protect%3f)
* [What information does HTTPS _not_ protect?](#what-information-does-https-not-protect%3f)
* [How does HTTPS relate to HTTP/2?](#how-does-https-relate-to-http/2%3f)
* [How does migrating to HTTPS affect search engine optimization (SEO)?](#how-does-migrating-to-https-affect-search-engine-optimization-(seo)%3f)
* [How can an HTTPS site keep sending referrer information to linked HTTP sites?](#how-can-an-https-site-keep-sending-referrer-information-to-linked-http-sites%3f)
* [How difficult is it to attack an HTTPS connection?](#how-difficult-is-it-to-attack-an-https-connection%3f)
* [Why are domain names unencrypted over HTTPS today?](#why-are-domain-names-unencrypted-over-https-today%3f)
* [Why isn't DNSSEC good enough?](#why-isn't-dnssec-good-enough%3f)
* [How does HTTPS protect against DNS spoofing?](#how-does-https-protect-against-dns-spoofing%3f)

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

### How does HTTPS relate to HTTP/2?

HTTP/2 (finalized in [2015](https://tools.ietf.org/html/rfc7540)) is a backwards-compatible update to HTTP/1.1 (finalized in [1999](https://tools.ietf.org/html/rfc2616)) that is optimized for the modern web.

HTTP/2 includes many features that can drastically speed up website performance, and emerged from the advancements Google demonstrated with [SPDY](https://blog.chromium.org/2009/11/2x-faster-web.html) in 2009.

While HTTP/2 does not require the use of encryption in its formal spec, every major browser that has implemented HTTP/2 has only implemented support for encrypted connections, and no major browser is working on support for HTTP/2 over unencrypted connections.

This means that in practice, **the major performance benefits of HTTP/2 first require the use of HTTPS.**

For more information:

* [HTTP/2 Working Group FAQ](https://http2.github.io/faq/)
* [RFC 7540](https://tools.ietf.org/html/rfc7540), the final spec
* [HTTP/2 Implementation Status](https://www.mnot.net/blog/2015/06/15/http2_implementation_status), by Mark Nottingham (working group chair)

### How does migrating to HTTPS affect search engine optimization (SEO)?

In general, migrating to HTTPS improves a website's own SEO and analytics.

* As of August 2014, Google [uses HTTPS as a ranking signal](https://security.googleblog.com/2014/08/https-as-ranking-signal_6.html), which can improve search rankings.
* Migrating to HTTPS will improve analytics about web traffic referred from HTTPS websites, as referrer information [is not passed from HTTPS websites to HTTP websites](https://stackoverflow.com/questions/1361705/is-http-header-referer-sent-when-going-to-a-http-page-from-a-https-page/1361720#1361720).

To make the migration as smooth as possible, and avoid taking a SEO hit:

* Use a **proper 301 redirect** to redirect users from `http://` to `https://`. **Do not use a 302 redirect**, as this may negatively impact search rankings.
* Use the [canonical link element](https://en.wikipedia.org/wiki/Canonical_link_element) (`<link rel="canonical">`) to inform search engines that the "canonical" URL for a website uses `https://`.

### How can an HTTPS site keep sending referrer information to linked HTTP sites?

By default, when a user is on an HTTPS website and clicks a link to an HTTP website, browsers will not send a `Referer` header to the HTTP website. This is [defined in the HTTP 1.1 specification](https://tools.ietf.org/html/rfc2616#section-15.1.3), and is designed to avoid exposing HTTPS URLs that would otherwise have remained protected by the guarantees of HTTPS.

However, this means that if a website migrates to HTTPS, any HTTP sites it links to will stop seeing referrer data from the HTTPS website. This can be a disincentive to migrate to HTTPS, as it deprives linked HTTP sites of analytics data, and means the HTTPS website won't get "credit" for referring traffic to linked websites.

Website owners who wish to continue sending outbound referrer information to linked HTTP sites can use **[Referrer Policy](https://www.w3.org/TR/referrer-policy/)** to override browser default behavior, while retaining the privacy of HTTPS URLs.

To do this, websites **should use** the [`origin-when-cross-origin`](https://www.w3.org/TR/referrer-policy/#referrer-policy-origin-when-cross-origin) policy. This will allow supporting browsers to send **only the origin** as the `Referer` header when going from an HTTPS site to an HTTP site. 

For example, if a user is on `https://agency.gov/help/aids.html` and clicks a link to `http://moreinformation.com`, then if `origin-when-cross-origin` is set, the browser will make an HTTP request to `http://moreinformation.com` with a `Referer` header of `https://agency.gov`.

The simplest way to set this policy is by including a `<meta>` tag in the body of the HTTPS website:

```html
<meta name="referrer" value="origin-when-cross-origin" />
```

Websites **should not use** the `unsafe-url` policy, as this will cause HTTPS URLs to be exposed on the wire over an HTTP connection, which defeats one of the important privacy and security guarantees of HTTPS.

### How difficult is it to attack an HTTPS connection?

Attacks on HTTPS connections generally fall into 3 categories:

* Compromising the quality of the HTTPS connection, through cryptanalysis or other protocol weaknesses.
* Compromising the client computer, such as by installing a malicious root certificate into the system or browser trust store.
* Obtaining a "rogue" certificate trusted by major browsers, generally by manipulating or compromising a certificate authority.

These are all possible, but for most attackers they are very difficult and require significant expense. Importantly, they are all _targeted_ attacks, and are not feasible to execute against any user connecting to any website.

By contrast, plain HTTP connections can be easily intercepted and modified by anyone involved in the network connection, and so attacks can be carried out at large scale and at low cost.

## Why are domain names unencrypted over HTTPS today?

This is primarily to support **[Server Name Indication](/sni/)** (SNI), a TLS extension that allows multiple hostnames to be served over HTTPS from one IP address.

The SNI extension was introduced in 2003 to allow HTTPS deployment to scale more easily and cheaply, but it does mean that the hostname is sent by browsers to servers "in the clear" so that the receiving IP address knows which certificate to present to the client.

When a domain or a subdomain itself reveals sensitive information (e.g. 'contraception.foo.gov' or 'suicide-help.foo.gov'), this can reveal that information to passive eavesdroppers.

From a network privacy perspective, DNS also "leaks" hostnames in the clear across the network today (even when DNSSEC is used). There are ongoing efforts in the network standards community to encrypt both the SNI hostname and DNS lookups, but as of late 2015, nothing has been deployed to support these goals.

Most clients support SNI today, and site owners are encouraged to [evaluate the feasibility of requiring SNI support](/sni/), to save money and resources. However, whether SNI support is required to access a specific website or not, a website's owner should consider their hostnames to be unencrypted over HTTPS, and account for this when provisioning domains and subdomains.

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
