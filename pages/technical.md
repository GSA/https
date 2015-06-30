---
layout: page
title: Technical Concepts
permalink: /technical-concepts/
description: "More relevant technical concepts relating to HTTPS."
---

This page covers some relevant technical concepts relevant to the **strength and quality** of a server's HTTPS configuration.

* [SSL and TLS](#ssl-and-tls)
* [Forward secrecy](#forward-secrecy)
* [Signature algorithms](#signature-algorithms), such as SHA-1 and SHA-2
* [RC4](#rc4), a common but insecure cipher

### SSL and TLS

HTTPS today uses **Transport Layer Security (TLS)**. TLS is a network protocol that establishes an encrypted connection to an authenticated peer over an untrusted network.

Earlier, less secure versions of this protocol went by the name **Secure Sockets Layer (SSL)**.

SSL and TLS do the same thing, and because of its early ubiquity, "SSL" is frequently used today to generically refer to TLS/HTTPS. However, all versions of SSL as a protocol are now considered insecure for modern use.

The major versions of SSL/TLS in use today are:

* **SSLv3:** [Released in 1996.](https://tools.ietf.org/html/rfc6101) **Considered to be insecure** after the [POODLE](https://www.openssl.org/~bodo/ssl-poodle.pdf) attack was published in 2014. Turning off SSLv3 effectively removes support for Internet Explorer 6.
* **TLSv1.0:** - [Released in 1999.](https://tools.ietf.org/html/rfc2246). Used widely today to support [some older clients](https://www.ssllabs.com/ssltest/clients.html), like IE8 and Android 4.3 and below. [NIST Special Publication 800-52](http://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-52r1.pdf) disallows TLSv1.0 for government-facing systems.
* **TLSv1.1:** - [Released in 2006.](https://tools.ietf.org/html/rfc4346) An improvement over TLSv1.0, but was quickly superseded by TLSv1.2.
* **TLSv1.2:** - [Released in 2008.](https://tools.ietf.org/html/rfc5246) This is the strongest form of TLS today, and is widely supported by modern browsers.

Typically, browsers and servers support multiple versions, and will attempt to negotiate the strongest mutually supported version.

It is possible for an attacker to interfere with the negotiation process and attempt to "downgrade" connections to the oldest mutually supported version.

A downgrade attack can be prevented by using **[TLS Fallback SCSV](https://tools.ietf.org/html/rfc7507)**, a TLS extension proposed in 2014 and which is enabled by default in newer versions of OpenSSL.

For more details of NIST recommendations, read [NIST Special Publication 800-52](http://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-52r1.pdf).

* **[The Pulse HTTPS dashboard for .gov domains](https://pulse.cio.gov/https/domains/)** will note when a domain still offers insecure SSLv3, or when a domain does not yet offer TLSv1.2.
**[https.cio.gov is configured](https://www.ssllabs.com/ssltest/analyze.html?d=https.cio.gov)** to support TLSv1.0, TLSv1.1, and TLSv1.2, and has TLS Fallback SCSV enabled.

### Forward secrecy

**Forward secrecy** protects information sent over an encrypted HTTPS connection _now_ from being decrypted _later_, even if the server's private key is later compromised.

In non-forward-secret HTTPS connections, if an attacker records encrypted traffic between a website and its visitors, and later obtains the website's private key, that key can be used to decrypt all past recorded traffic.

In forward secret connections, the server and client create a temporary key for every new session that gets effectively "thrown away" after the session is complete. This means that even if the server's base private key is compromised, an attacker can't retroactively decrypt information.

In TLS, forward secrecy is provided by choosing ciphersuites that include the [Ephemeral Diffie-Hellman (DHE)](https://en.wikipedia.org/wiki/Diffie–Hellman_key_exchange) and [Ephemeral Elliptic Curve Diffie–Hellman (ECDHE)](https://en.wikipedia.org/wiki/Elliptic_curve_Diffie%E2%80%93Hellman) key exchanges.

* **[The Pulse HTTPS dashboard for .gov domains](https://pulse.cio.gov/https/domains/)** will note when a domain offers little or no forward secrecy.
**[https.cio.gov is configured](https://www.ssllabs.com/ssltest/analyze.html?d=https.cio.gov)** to offer robust forward secrecy.

### Signature algorithms

The HTTPS/TLS security model uses "certificates" to guarantee authenticity. These certificates are cryptographically "signed" by a trusted certificate authority.

The certificate authority's trusted root certificate (which is included with your OS or browser) is used to sign an intermediary certificate, which is used to sign your website's certificate. There may be more than one intermediary certificate in the chain.

A part of the signature process is computing a "hash" of the data included in the certificate. This can be done using a standard hashing algorithm, such as [SHA-1](https://en.wikipedia.org/wiki/SHA-1) or [SHA-2](https://en.wikipedia.org/wiki/SHA-2).

SHA-1 has been shown to have serious weaknesses, and so browser and OS providers like [Google](http://googleonlinesecurity.blogspot.com/2014/09/gradually-sunsetting-sha-1.html), [Microsoft](http://blogs.technet.com/b/pki/archive/2013/11/12/sha1-deprecation-policy.aspx), and [Mozilla](https://blog.mozilla.org/security/2014/09/23/phasing-out-certificates-with-sha-1-based-signature-algorithms/) have announced timelines to deprecate SHA-1 in favor of the SHA-2 family of algorithms.

While details on browser and OS policies vary, site owners should generally consider SHA-1 to be unsupported by January 2017.

* **[The Pulse HTTPS dashboard for .gov domains](https://pulse.cio.gov/https/domains/)** will note when a domain is still using a certificate signed with SHA-1.
* **[https.cio.gov is configured](https://www.ssllabs.com/ssltest/analyze.html?d=https.cio.gov)** to use a certificate chain signed with SHA-2.

### RC4

There are a number of ciphers available to a TLS connection, and one of those is the [RC4](https://en.wikipedia.org/wiki/RC4) (Also known as ARC4 or ARCFOUR). RC4 was a popular cipher due to being a fast cipher which was not vulnerable to the [BEAST](https://community.qualys.com/blogs/securitylabs/2011/10/17/mitigating-the-beast-attack-on-tls) attack. However, in 2013 it was announced that [RC4 had a serious flaw](http://www.isg.rhul.ac.uk/tls/) that would make it possible for a determined attacker to decrypt data encrypted with RC4 in TLS.

Due to the serious flaw in RC4, and the fact that the BEAST attack has been mitigated by all modern browsers, all HTTPS sites should be configured to use ciphers other than RC4.

* **[The Pulse HTTPS dashboard for .gov domains](https://pulse.cio.gov/https/domains/)** will note when a domain employs the RC4 cipher.
**[https.cio.gov is configured](https://www.ssllabs.com/ssltest/analyze.html?d=https.cio.gov)** to avoid using the RC4 cipher.
