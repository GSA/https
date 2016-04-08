---
layout: page
title: Certificates
permalink: /certificates/
description: "FAQ on certificates and certificate authorities for agencies migrating to HTTPS."
---

Frequently asked questions and answers about HTTPS certificates and certificate authorities.

* [What are certificates and certificate authorities?](#what-are-certificates-and-certificate-authorities?)
* [What kind of certificate should I get for my domain?](#what-kind-of-certificate-should-i-get-for-my-domain?)
* [What rules and oversight are certificate authorities subject to?](#what-rules-and-oversight-are-certificate-authorities-subject-to?)
* [Does the US government operate a publicly trusted certificate authority?](#does-the-us-government-operate-a-publicly-trusted-certificate-authority?)
* [Are there federal restrictions on acceptable certificate authorities to use?](#are-there-federal-restrictions-on-acceptable-certificate-authorities-to-use?)
* [Then how can I limit which CAs can issue certificates for a domain?](#then-how-can-i-limit-which-cas-can-issue-certificates-for-a-domain?)

  * [Certificate Transparency](#certificate-transparency)
  * [HTTP Public Key Pinning](#http-public-key-pinning)

## What are certificates and certificate authorities?

Websites use **certificates** to create an HTTPS connection. When signed by a trusted **certificate authority** (CA), certificates give confidence to browsers that they are visiting the "real" website.

Technically, a certificate is a file that contains:

* The domain(s) it is authorized to represent.
* A numeric "public key" that mathematically corresponds to a "private key" held by the website owner.
* A cryptographic signature by a certificate authority (CA) that vouches for the relationship between the keypair and the authorized domain(s).
* Other technical information, such as when the certificate expires, what algorithm the CA used to sign it, and how extensively the domain was validated.
* Optionally, information about a person or organization that owns the domain(s).

Web browsers are generally set to trust a pre-selected list of certificate authorities (CAs), and the browser can verify that any signature it sees comes from a CA in that list. The list of trusted CAs is set either by the underlying operating system or by the browser itself.

When a website presents a certificate to a browser during an HTTPS connection, the browser uses the information and signature in the certificate to confirm that a CA it trusts has decided to trust the information in the certificate.

## What kind of certificate should I get for my domain?

There are many kinds of certificates in use in the federal government today, and the right one may depend on a system's technical architecture or an agency's business policies.

In general:

* "Domain Validation" (DV) certificates are usually less expensive and more amenable to automation than "Extended Validation" (EV) certificates. EV certificates generally result in the domain owner's name appearing in the browser URL bar visitors see. **Ordinary DV certificates are completely acceptable for government use.**

* Certificates can be valid for anywhere from years to days. In general, **shorter-lived certificates offer a better security posture**, since the impact of key compromise is less severe. Automating the issuance and renewal of certificates is an overall best practice, and can make the adoption of shorter-lived certificates more practical.

* Agencies [should not use certificates signed with SHA-1](/technical-guidelines/#signature-algorithms), and commercial CAs are forbidden from issuing them entirely as of January 1, 2016. **Any existing certificates signed with SHA-1 should be replaced immediately**, as browsers are quickly moving to remove support for the SHA-1 algorithm.

As a general matter, certificates from any commercial CA will meet the few [NIST technical requirements](http://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-52r1.pdf) that relate to certificates.

## What rules and oversight are certificate authorities subject to?

Since 2012, all major browsers and certificate authorities participate in the **[CA/Browser Forum](https://cabforum.org)**. Though self-regulated, the CA/Browser Forum is effectively the governing body for publicly trusted certificate authorities.

The CA/B Forum produces the **[Baseline Requirements](https://cabforum.org/baseline-requirements-documents/)** (BRs), a set of technical and procedural policies that all CAs must adhere to. These policies are determined through a [formal voting process](https://cabforum.org/ballots/) of browsers and CAs. The BRs are enforced through a combination of technical measures, standard third-party audits, and the overall community's attention to publicly visible certificates.

The Baseline Requirements only constrain CAs -- they do not constrain browser behavior. Since browser vendors ultimately decide which certificates their browser will trust, they are the enforcers and adjudicators of BR violations. If a CA is found to be in violation of the Baseline Requirements, a browser may penalize or inhibit that CA's ability to issue certificates that that browser will trust, up to and including expulsion from that browser's trust store.

#### CA / Browser Resources

* The current [Baseline Requirements](https://cabforum.org/baseline-requirements-documents/)
* [CA/B Forum voting record](https://cabforum.org/ballots/)
* [Mozilla revoking an ANSSI intermediate](https://blog.mozilla.org/security/2013/12/09/revoking-trust-in-one-anssi-certificate/) after ANSSI was found to have violated the Baseline Requirements by inappropriately issuing an intermediate certificate for use in network monitoring.
* [Google requiring Symantec to employ Certificate Transparency](https://googleonlinesecurity.blogspot.com/2015/10/sustaining-digital-certificate-security.html) after Symantec was found to have violated the Baseline Requirements by misissuing certificates.

## Does the US government operate a publicly trusted certificate authority?

Yes, but it is not trusted by all public browsers.

The [Federal PKI](https://www.idmanagement.gov/IDM/s/article_content_old?tag=a0Gt0000000SfwP) root is trusted by Microsoft and Apple browsers and operating systems, but is not contained in the [Mozilla Trusted Root Program](https://www.mozilla.org/en-US/about/governance/policies/security-group/certs/policy/). The Mozilla Trusted Root Program is used by Firefox, as well as a wide variety of devices and operating systems. This means that the Federal PKI is able to issue certificates for use in TLS/HTTPS that are trusted by some browsers and operating systems, but may give a different user experience based on the browser that is used.

The Federal PKI has an [open application](https://bugzilla.mozilla.org/show_bug.cgi?id=478418) to the Mozilla Trusted Root Program. However, even if the Federal PKI's application is accepted, it may take a significant amount of time for the Federal PKI's root certificate to actually be shipped onto devices and propagate widely around the world.

The Federal PKI has [cross-certified other agencies and commercial CAs](https://www.idmanagement.gov/IDM/s/article_content_old?tag=a0Gt0000000SfwR), which means their certificates will be trusted by clients that trust the Federal PKI and some of these roots are _publicly trusted_. It is dependent on the Federal PKI Partner CA if it maintains a separation between their publicly trusted certificates and their Federal PKI cross-certified certificates. A list of availabe [Federal PKI Partners](https://www.idmanagement.gov/IDM/s/article_content_old?tag=a0Gt0000000XRrC) is available on IDManagement.gov with contact information if an agency has a requirement to use Federal PKI certificates.

There is a viable way to obtain an individual certificate for use in TLS/HTTPS that is issued or trusted by the Federal PKI and also trusted by the general public, but it may impact the user experience based on the browser or operating system.

## Are there federal restrictions on acceptable certificate authorities to use?

There are no government-wide rules limiting what CAs federal domains can use.

It is important to understand that, while there may be technical or business reasons for an agency to limit which CAs it uses, **there is no security benefit** to limiting CAs through internal policies alone. Browsers will trust certificates acquired from any publicly trusted CA, and so limiting CA usage internally will not limit the CAs from which an attacker may obtain a forged certificate.

As an analogy: consider a New York company which insists its employees only show New York photo IDs when gaining access to the secure facilities of other US companies or governments. This company's policy alone will not stop someone with a Pennsylvania ID from gaining access while pretending to work for this New York company. For this to be effective, every secure facility in the country must also know to insist on New York IDs for this company, and must enforce this rule.

In practice, federal agencies use a wide variety of publicly trusted commercial CAs and privately trusted enterprise CAs to secure their web services.

## Then how can I limit which CAs can issue certificates for a domain?

There is no simple and 100% effective way to force all browsers to only trust certificates for your domain that have been issued from a certain CA. In general, the strength of HTTPS on today's internet depends on the overall standards, competence, and accountability of the entire CA system.

However, domain owners have some options to reduce the risk or impact of misissued or fraudulent certificates:

### Certificate Transparency

**[Certificate Transparency](https://en.wikipedia.org/wiki/Certificate_Transparency)** (CT) allows domain owners to **detect missuance of certificates after the fact**.

CT allows CAs to publish some or all of the publicly trusted certificates that they issue to one or more public logs. Multiple organizations run CT logs, and it is possible to automatically monitor the logs for any certificates that are issued for any domains of interest.

Comodo has released an [open source](https://github.com/crtsh) Certificate Transparency log viewer that they operate at [crt.sh](https://crt.sh). For example, it is possible to see [all recent certificates for whitehouse.gov](https://crt.sh/?q=whitehouse.gov), and [details of specific certificates](https://crt.sh/?id=7976268).

The strength of Certificate Transparency increases as more CAs publish more certificates to public CT logs. Certificate Transparency is not currently a requirement for CAs -- however, as the use of CT increases, so does the viability of requiring CT for publicly issued certificates.

#### Certificate Transparency Resources

* [Google CT FAQ](https://www.certificate-transparency.org/faq)
* [RFC 6962](https://tools.ietf.org/html/rfc6962), the experimental standard for CT
* [Wikipedia entry](https://en.wikipedia.org/wiki/Certificate_Transparency) for CT

### HTTP Public Key Pinning

**[HTTP Public Key Pinning](https://en.wikipedia.org/wiki/HTTP_Public_Key_Pinning)** (HPKP) allows domain owners to **tell browsers which certain keys, certs or CAs are trusted for their domain**.

Domain owners can use HPKP in one of two ways:

* The `Public-Key-Pins` header contains a list of SHA-256 hashes of public key information corresponding to client, intermediate, or root certificates. [Supporting browsers](http://caniuse.com/#search=hpkp) **will hard-fail** on certificates whose validated chain does not contain at least one of the listed keys. The domain owner can list a URI that browsers can POST to with error information when a hard-fail occurs.

* The `Public-Key-Pins-Report-Only` HTTP header contains the same information, but **will not fail or show users an error** if a pinning violation is detected. Browsers will report detected violations to a given URI.

Using `Public-Key-Pins` is **powerful but potentially dangerous**, as mistakes can lead to a site being rendered entirely inaccessible for weeks or months.

Using `Public-Key-Pins-Report-Only` is very safe, and can provide useful information to detect potential certificate misissuance or attacks on users.

Like [HSTS](/hsts/), HPKP only takes effect once the browser has visited the site once and received the HPKP header over a secure connection. HPKP preloading is possible, but as of 2016 this requires special manual coordination with browsers to do.

**Note:** As currently implemented in [Chrome](https://www.chromium.org/Home/chromium-security/security-faq#TOC-How-does-key-pinning-interact-with-local-proxies-and-filters-) and [Firefox](https://wiki.mozilla.org/SecurityEngineering/Public_Key_Pinning#How_to_use_pinning), pinning rules can be overridden by locally installed root certificates. This allows device owners -- and attackers who are able to install a local root -- to intercept or modify traffic even when a web service uses HPKP.

#### HPKP Resources

* [Guide to rolling out HPKP reporting](https://developers.google.com/web/updates/2015/09/HPKP-reporting-with-chrome-46?hl=en) by the Chrome team
* [RFC 7469](https://tools.ietf.org/html/rfc7469), the official standard
* [Discussion on GitHub](https://github.com/SSLMate/sslmate/issues/10) about HPKP strategy
* [Wikipedia entry](https://en.wikipedia.org/wiki/HTTP_Public_Key_Pinning) for HPKP
* [Browser support](http://caniuse.com/#search=hpkp) for HPKP
* [Mozilla documentation](https://developer.mozilla.org/en-US/docs/Web/Security/Public_Key_Pinning) for HPKP
