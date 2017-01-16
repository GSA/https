---
layout: page
title: Compliance Guide
permalink: /guide/
description: "Guide for agencies on implementing the HTTPS transition."
---

[M-15-13](https://www.whitehouse.gov/sites/default/files/omb/memoranda/2015/m-15-13.pdf) calls for "all publicly accessible Federal websites and web services" to only provide service through a secure connection (HTTPS), and to use [HTTP Strict Transport Security](/hsts/) (HSTS) to ensure this.

This applies to all public domains and subdomains operated by the federal government, regardless of the domain suffix, as long as they are reachable over HTTP/HTTPS on the public internet.

This page provides implementation guidance for agencies by the White House Office of Management and Budget, as agencies manage the transition to HTTPS by December 31, 2016.

* [Compliance and best practice checklist](#compliance-and-best-practice-checklist)
* [Options for HSTS compliance](#options-for-hsts-compliance)
* [Compliance FAQ](#compliance-faq)
  * [What protocols are covered by M-15-13?](#what-protocols-are-covered-by-m-15-13%3f)
  * [Do I need to shut off port 80?](#do-i-need-to-shut-off-port-80%3f)
  * [What does "all Federal agency domains or subdomains" include?](#what-does-"all-federal-agency-domains-or-subdomains"-include%3f)
  * [What about domains that are only used to redirect visitors to other websites?](#what-about-domains-that-are-only-used-to-redirect-visitors-to-other-websites%3f)
  * [What about domains that are technically public, but in practice are only used internally?](#what-about-domains-that-are-technically-public,-but-in-practice-are-only-used-internally%3f)
  * [What happens to visitors using browsers that don&rsquo;t support HSTS, like older versions of Internet Explorer?](#what-happens-to-visitors-using-browsers-that-don't-support-hsts,-like-older-versions-of-internet-explorer%3f)
  * [This site redirects users to HTTPS -- why is Pulse saying it doesn't enforce HTTPS?](#this-site-redirects-users-to-https----why-is-pulse-saying-it-doesn't-enforce-https%3f)
  * [Are federally operated certificate revocation services (CRL, OCSP) also required to move to HTTPS?](#are-federally-operated-certificate-revocation-services-(crl,-ocsp)-also-required-to-move-to-https%3f)
  * [What if I'm using a federally issued certificate -- such as from the Federal PKI or Department of Defense -- for my web service?](#what-if-i'm-using-a-federally-issued-certificate----such-as-from-the-federal-pki-or-department-of-defense----for-my-web-service%3f)


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

* The domain has been successfully [submitted and added to the HSTS preload list](https://hstspreload.appspot.com).
* Individual website subdomains are still encouraged to set their own HSTS policies.

HSTS preloading a parent domain allows agencies to avoid inventorying and configuring an HSTS policy for every individual subdomain. However, this approach also automatically includes **all** subdomains present on this domain -- including intranet subdomains. All subdomains will need to support HTTPS in order to remain reachable for use in major browsers.

**2. Compliance for each individual subdomain**

* The parent domain and each of its publicly reachable subdomains must set an HSTS policy with a max-age of at least 1 year, like this one:

```
Strict-Transport-Security: max-age=31536000
```

This approach allows agencies the flexibility to focus only on publicly accessible subdomains, but could entail significantly more work to add an HSTS policy header to each individual website.

## Compliance FAQ

Answers to other common compliance questions appear below.

### What protocols are covered by M-15-13?

M-15-13 requires secure connections for **websites and web services**, which means **only HTTP-based protocols**. This includes all federal websites, as well as federally operated HTTP-based APIs.

M-15-13 does not address the use of DNS or DNSSEC, FTP or SFTP, or any other non-HTTP network protocol.

### Do I need to shut off port 80?

**No.** [M-15-13 states](https://https.cio.gov/#footnote-3):

> Allowing HTTP connections for the sole purpose of redirecting clients to HTTPS connections is acceptable and encouraged.

Agencies may employ port 80 for the sole purpose of redirecting clients to a secure connection.

Note that while connections to port 80 are insecure, even for redirects, the use of [HSTS](/hsts/]) will instruct supporting HTTP clients to automatically redirect themselves from port 80 to port 443, without attempting to connect to port 80 over the network.

HSTS mitigates the security impact of connections over port 80, while allowing agencies the flexibility to continue redirecting legacy clients or clients which have not yet received an HSTS policy for the target domain.

### What does "all Federal agency domains or subdomains" include?

Domains and subdomains, in the context of M-15-13, refer to hostnames that are publicly accessible via HTTP or HTTPS.

**Domain** refers to hostnames that are directly registerable. Some examples include `gsa.gov`, `whitehouse.gov`, `dodig.mil`, or `fs.fed.us`.

**Subdomain** refers to any hostname that is a child of a registerable domain, and may be of any length. Some examples include `www.gsa.gov`, `planthardiness.ars.usda.gov`, `www.fia.fs.fed.us`, or `www.usar.army.mil`.

Federally operated domains do not all end in `.gov`, `.mil`, or `.fed.us`. Some may end in `.com`, `.org`, `.us`, or other suffixes. Any federally operated domain is covered by M-15-13.

### What about domains that are only used to redirect visitors to other websites?

These domains must enable port 443, use and enforce HTTPS, and follow all the same requirements and guidelines as domains used to host websites and APIs, including HSTS and preloading.

### Do domains that redirect to an external domain first need to redirect internally to the secure form of itself?

It is not required, for example, to redirect from `http://example.gov:80` to `https://example.gov:443` before redirecting to `https://another-example.gov:443`. However, doing so enables the connecting client to see and cache the HSTS header on `example.gov`, which may not otherwise be seen. 

Redirecting internally is a [prerequisite to preloading a domain](https://hstspreload.org/#submission-requirements). As only second-level domains can be preloaded, this practice is recommended for second-level domains.

### What about domains that are technically public, but in practice are only used internally?

M-15-13 includes all domains and subdomains that are publicly reachable over HTTP/HTTPS, regardless of agency operational practices.

### What happens to visitors using browsers that don't support HSTS, like older versions of Internet Explorer?

Browsers that don't support HSTS are simply unaffected by HSTS, so there is no harm in enabling it.

### This site redirects users to HTTPS -- why is Pulse saying it doesn't enforce HTTPS?

[Pulse](https://pulse.cio.gov) looks for server-side redirects, using an appropriate HTTP response code. Sites that use client-side redirects -- such as a &lt;meta refresh&gt; tag or JavaScript -- will not be seen as redirects. To meet the M-15-13 requirement of enforcing HTTPS, agencies should employ server-side redirects (or alternatively, disable HTTP access altogether).

Sites that are reachable on both a root domain (`http://agency.gov`) and their www subdomain (`http://www.agency.gov`) should perform a redirect to HTTPS in both cases. Redirecting one but not the other could also cause Pulse to indicate that a domain does not enforce HTTPS.

### Are federally operated certificate revocation services (CRL, OCSP) also required to move to HTTPS?

No. This very narrow class of services, that provide CRL and OCSP information for the purposes of verifying the revocation status of certificates used to make other HTTPS connections, should abide by best practices in the field and their respective specifications.

For CRL, [RFC 5280](https://tools.ietf.org/html/rfc5280) says:

```
CAs SHOULD NOT include URIs that specify https, ldaps, or similar schemes in extensions.  CAs that include an https URI in one of these extensions MUST ensure that the server's certificate can be validated without using the information that is pointed to by the URI.  Relying parties that choose to validate the server's certificate when obtaining information pointed to by an https URI in the cRLDistributionPoints, authorityInfoAccess, or subjectInfoAccess extensions MUST be prepared for the possibility that this will result in unbounded recursion.
```

For OCSP, [RFC 6960](https://tools.ietf.org/html/rfc6960) says:

```
Where privacy is a requirement, OCSP transactions exchanged using HTTP MAY be protected using either Transport Layer Security/Secure Socket Layer (TLS/SSL) or some other lower-layer protocol.
```

Agencies are encouraged to operate OCSP and CRL services via hostnames specifically reserved for those services, so that other related information and functionality can be served securely and privately.


### What if I'm using a federally issued certificate -- such as from the Federal PKI or Department of Defense -- for my web service?

There are [no restrictions on acceptable certificate authorities](/certificates/#are-there-federal-restrictions-on-acceptable-certificate-authorities-to-use%3f) agencies might use to meet the requirements of M-15-13.

However, M-15-13 requires agencies to do more than just redirect HTTP traffic to HTTPS. It also requires agencies to enable **[HTTP Strict Transport Security](/hsts/)** (HSTS), as [described above](#options-for-hsts-compliance). HSTS ensures that HTTPS is always used, and protects users from several common vulnerabilities.

One important effect of HSTS is that it **disables the ability for users to click through certificate warnings** in supporting browsers. This means that **agencies cannot instruct users to click through certificate warnings** to use their web service while also complying with M-15-13.

This is also consistent with security best practices, as instructing users to click through certificate warnings defeats the point of HTTPS, and will subject users to potential network attacks.

In practice, to deploy HSTS while using federally issued certificates, an agency will likely need to separate its web services by hostname, based on their expected audience:

* Federally issued certificates may be practical for web services whose users can be consistently expected to trust the issuing federal certificate authority (CA). Users whose devices do not trust the issuing CA will experience a connection failure and be unable to use the web service.
* Federally issued certificates will not be practical for web services whose users may not always be expected to trust the issuing federal certificate authority. These web services will likely require the use of a certificate from a publicly trusted (commercial) CA.

Whatever strategy an agency employs to manage the use of federally issued certificates, it should allow the practical deployment of [HSTS](/hsts/) across all of its publicly accessible websites and web services.
