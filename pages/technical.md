---
layout: page
title: Technical Guidelines
permalink: /technical-guidelines/
description: "Technical guidelines relating to HTTPS strength and quality."
---

This page covers some relevant technical concepts relevant to the **strength and quality** of a server's HTTPS configuration.

* [SSL and TLS](#ssl-and-tls)
* [Forward secrecy](#forward-secrecy)
* [Signature algorithms](#signature-algorithms), such as SHA-1 and SHA-2
* [RC4](#rc4), a common but insecure cipher
* [A complete certificate chain](#a-complete-certificate-chain)

### SSL and TLS

HTTPS today uses **Transport Layer Security**, or **TLS**. TLS is a network protocol that establishes an encrypted connection to an authenticated peer over an untrusted network.

Earlier, less secure versions of this protocol were called **Secure Sockets Layer**, or **SSL)**.

SSL and TLS perform the same function, and TLS is a direct successor and replacement for SSL. Because of its early ubiquity, "SSL" is frequently used today to generically refer to TLS/HTTPS. However, all versions of SSL as a protocol are now considered insecure for modern use.

The major versions of SSL/TLS in use today are:

* **SSLv3:** [Released in 1996.](https://tools.ietf.org/html/rfc6101) **Considered to be insecure** after the [POODLE](https://www.openssl.org/~bodo/ssl-poodle.pdf) attack was published in 2014. Turning off SSLv3 effectively removes support for Internet Explorer 6.
* **TLSv1.0:** - [Released in 1999.](https://tools.ietf.org/html/rfc2246) Used widely today to support [some older clients](https://www.ssllabs.com/ssltest/clients.html), like IE8 and Android 4.3 and below. [NIST Special Publication 800-52](http://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-52r1.pdf) disallows TLSv1.0 for government-facing systems.
* **TLSv1.1:** - [Released in 2006.](https://tools.ietf.org/html/rfc4346) An improvement over TLSv1.0, but was quickly superseded by TLSv1.2.
* **TLSv1.2:** - [Released in 2008.](https://tools.ietf.org/html/rfc5246) This is the strongest form of TLS today, and is widely supported by modern browsers.

Typically, browsers and servers support multiple versions, and will attempt to negotiate the strongest mutually supported version.

It is possible for an attacker to interfere with the negotiation process and attempt to "downgrade" connections to the oldest mutually supported version.

A downgrade attack can be prevented by using **[TLS Fallback SCSV](https://tools.ietf.org/html/rfc7507)**, a TLS extension proposed in 2014 and which is enabled by default in newer versions of OpenSSL.

For more details of NIST recommendations, read [NIST Special Publication 800-52](http://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-52r1.pdf).

* **[The Pulse HTTPS dashboard for .gov domains](https://pulse.cio.gov/https/domains/)** will note when a domain still offers insecure SSLv3, or when a domain does not yet offer TLSv1.2.
* **[https.cio.gov is configured](https://www.ssllabs.com/ssltest/analyze.html?d=https.cio.gov)** to support TLSv1.0, TLSv1.1, and TLSv1.2, and has TLS Fallback SCSV enabled.

### Forward secrecy

**Forward secrecy** protects information sent over an encrypted HTTPS connection _now_ from being decrypted _later_, even if the server's private key is later compromised.

In non-forward-secret HTTPS connections, if an attacker records encrypted traffic between a website and its visitors, and later obtains the website's private key, that key can be used to decrypt all past recorded traffic.

In forward secret connections, the server and client create a temporary key for every new session that gets effectively "thrown away" after the session is complete. This means that even if the server's base private key is compromised, an attacker can't retroactively decrypt information.

In TLS, forward secrecy is provided by choosing ciphersuites that include the [DHE](https://en.wikipedia.org/wiki/Diffie–Hellman_key_exchange) and [ECDHE](https://en.wikipedia.org/wiki/Elliptic_curve_Diffie%E2%80%93Hellman) key exchanges.

**Note:** Current drafts of TLS 1.3, the next version of TLS, require new connections to use employ forward secrecy by [removing support for static RSA and DH key exchange](https://tools.ietf.org/html/draft-ietf-tls-tls13-02#section-1.2).

* **[The Pulse HTTPS dashboard for .gov domains](https://pulse.cio.gov/https/domains/)** will note when a domain offers little or no forward secrecy.
* **[https.cio.gov is configured](https://www.ssllabs.com/ssltest/analyze.html?d=https.cio.gov)** to offer robust forward secrecy.

### Signature algorithms

The HTTPS/TLS security model uses "certificates" to guarantee authenticity. These certificates are cryptographically "signed" by a trusted certificate authority.

The certificate authority's trusted root certificate (which is included with your OS or browser) is used to sign an intermediary certificate, which is used to sign your website's certificate. There may be more than one intermediary certificate in the chain. A part of the signature process is computing a "hash" of the data included in the certificate. This can be done using a standard hashing algorithm, such as [SHA-1](https://en.wikipedia.org/wiki/SHA-1) or [SHA-2](https://en.wikipedia.org/wiki/SHA-2).

SHA-1 has been shown to have serious weaknesses, and so browser and OS providers like [Google](https://security.googleblog.com/2014/09/gradually-sunsetting-sha-1.html), [Microsoft](http://social.technet.microsoft.com/wiki/contents/articles/32288.windows-enforcement-of-authenticode-code-signing-and-timestamping.aspx), and [Mozilla](https://blog.mozilla.org/security/2014/09/23/phasing-out-certificates-with-sha-1-based-signature-algorithms/) have announced timelines to deprecate SHA-1 in favor of the SHA-2 family of algorithms.

[NIST has disallowed SHA-1](http://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-52r1.pdf) for digital signature generation after 2013.

As of January 2016, commercial CAs are forbidden by most root programs from issuing a SHA-1 certificate. As such, obtaining a publicly trusted SHA-1 certificate is no longer feasible. In addition, site owners with an existing SHA-1 certificate should be aware that many browsers and OSes will be disabling SHA-1 support in early 2017.

### RC4

There are a number of ciphers available to a TLS connection, and one of those is [RC4](https://en.wikipedia.org/wiki/RC4) (also known as ARC4 or ARCFOUR). RC4 was a popular cipher due to being a fast cipher which was not vulnerable to the [BEAST](https://blog.qualys.com/ssllabs/2011/10/17/mitigating-the-beast-attack-on-tls) attack. However, in 2013 it was announced that [RC4 had a serious flaw](http://www.isg.rhul.ac.uk/tls/) that would make it possible for a determined attacker to decrypt data encrypted with RC4 in TLS.

Due to the serious flaw in RC4, and the fact that the BEAST attack has been mitigated by all modern browsers, modern browsers no longer support RC4-based ciphersuites. Therefore all HTTPS sites need to be configured to use ciphers other than RC4.

* **[The Pulse HTTPS dashboard for .gov domains](https://pulse.cio.gov/https/domains/)** will note when a domain employs the RC4 cipher.
* **[https.cio.gov is configured](https://www.ssllabs.com/ssltest/analyze.html?d=https.cio.gov)** to avoid using the RC4 cipher.

### A complete certificate chain

In addition to the certificate itself, you should provide a "chain" of intermediate certificates that give the connecting browser or client enough information to connect the certificate to a trusted root certificate.

Failing to provide intermediates could prevent various browsers and clients from successfully connecting to your service, especially mobile browsers and non-browser clients (such as cURL, and tools based on libcurl).

Some browsers will cache intermediates from a previous connection or attempt to automatically download missing intermediates that are presented in a certificate's [Authority Information Access](https://tools.ietf.org/html/rfc5280#section-4.2.2.1) extension, and so it can be easy to miss this problem during initial configuration. Though most browsers have an option to inspect the certificates on a site, they vary in whether they show the exact certificates the server presented or a chain as reconstructed through the fetching of an intermediate listed in the AIA extension. 

In general:

* You **do not** need to serve the trusted root that the certificate chains to. The client will compare the chain to a local root store, so serving the root will only waste bytes and slow the connection.
* You **do** need to serve any intermediate certificates that connect your web server certificate to the trusted root. Doing so removes the potential for problems caused by the variation in how clients facilitate trust verification.

Web servers vary in how they are configured to serve intermediates, but it should generally be straightforward.

* **[What's My Chain Cert?](https://whatsmychaincert.com/)** can help determine if any intermediate certificates are not being served.
