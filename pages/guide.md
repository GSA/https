---
layout: page
title: Compliance Guide
permalink: /guide/
description: "Guide for agencies on implementing the HTTPS transition."
---

[M-15-13](https://www.whitehouse.gov/sites/default/files/omb/memoranda/2015/m-15-13.pdf) calls for "all publicly accessible Federal websites and web services" to only provide service through a secure connection (HTTPS), and to use [HTTP Strict Transport Security](/hsts/) (HSTS) to ensure this.

This applies to all public domains and subdomains operated by the federal government, regardless of the domain suffix, as long as they are reachable over HTTP/HTTPS on the public internet.

This page provides implementation guidance for agencies by the White House Office of Management and Budget, as agencies manage the transition to HTTPS by December 31, 2016.


## Compliance and best practice checklist

Each public website or web service an agency operates **must**:

* Provide service over HTTPS.
* Automatically redirect HTTP requests to HTTPS, or disable HTTP entirely.
* Have an HSTS policy in place, through either of the [two approaches described below](#options-for-hsts-compliance).

Each public website or web service an agency operates **should**:

* Follow [technical best practices](/technical-guidelines/) around TLS quality, as [demonstrated by https.cio.gov](https://www.ssllabs.com/ssltest/analyze.html?d=https.cio.gov) and measured by [pulse.cio.gov](https://pulse.cio.gov/).
* Address any [mixed content issues](/mixed-content/) that arise from the migration process.
* Evaluate the viability of dropping support for legacy clients and using modern standards like [Server Name Indication](/sni/).

## Options for HSTS compliance

There are a great number of federal websites and web services. To simplify the process of transitioning the federal government to HTTPS, agencies are encouraged to take advantage of **[HSTS preloading](/hsts/#hsts-preloading)**.

Preloading marks entire domains as HTTPS-only, and allows browsers to enforce this rigorously and automatically for every subdomain. Many `.gov` domains [have already implemented HSTS preloading](https://18f.gsa.gov/2015/02/09/the-first-gov-domains-hardcoded-into-your-browser-as-all-https/), as have a large number of private sector web services.

Agencies should generally take one of two approaches, on a per-domain basis, to ensure that an HSTS policy is set for all public websites.

Under either approach, web services used by non-browser clients (e.g. APIs) must still individually enforce HTTPS, as HSTS is not supported by non-browser clients.

**1. Full HSTS preloading of the parent domain (preferred)**

* The parent domain (e.g. `https://agency.gov`) has an HSTS policy that includes subdomains and has a max-age of at least 1 year, like this one:

```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

* The domain has been successfully submitted and added to the HSTS preload list.
* Individual website subdomains are still encouraged to set their own HSTS policies.

HSTS preloading a parent domain allows agencies to avoid inventorying and configuring an HSTS policy for every individual subdomain. However, this approach also automatically includes **all** subdomains present on this domain -- including intranet subdomains. All subdomains will need to support HTTPS in order to remain reachable for use in major browsers.

**2. Compliance for each individual subdomain**

* The parent domain and each of its publicly reachable subdomains must set an HSTS policy with a max-age of at least 1 year, like this one:

```
Strict-Transport-Security: max-age=31536000
```

This approach allows agencies the flexibility to focus only on publicly accessible subdomains, but could entail significantly more work to add an HSTS policy header to each individual website.

## Compliance FAQ

**What about domains that are only used to redirect visitors to other websites?**

These domains must follow all the same requirements and guidelines as domains used to host websites and APIs, including HSTS and preloading.

**What about domains that are technically public, but in practice are only used internally?**

M-15-13 includes all domains and subdomains that are publicly reachable over HTTP/HTTPS, regardless of agency operational practices.

**This site redirects users to HTTPS, but Pulse is saying it doesn't enforce HTTPS.**

Pulse looks for server-side redirects, using an appropriate HTTP response code. Sites that use client-side redirects -- such as a <meta refresh> tag or JavaScript -- will not be seen as redirects. To meet the M-15-13 requirement of enforcing HTTPS, agencies should employ server-side redirects (or alternatively, disable HTTP access altogether).

Sites that are reachable on both a root domain (`http://agency.gov`) and their www subdomain (`http://www.agency.gov`) should perform a redirect to HTTPS in both cases. Redirecting one but not the other could also cause Pulse to indicate that a domain does not enforce HTTPS.
