---
layout: page
title: HTTP Strict Transport Security
permalink: /hsts/
description: "An overview of HTTP Strict Transport Security (HSTS), a lightweight standard that prevents privacy leaks and downgrade attacks."
---

**[HTTP Strict Transport Security](https://developer.mozilla.org/en-US/docs/Web/Security/HTTP_strict_transport_security)** (HSTS) is a simple and [widely supported](http://caniuse.com/#search=hsts) standard to protect visitors by ensuring that their browsers _always_ connect to a website over HTTPS. HSTS exists to remove the need for the common, insecure practice of redirecting users from `http://` to `https://` URLs.

When a browser knows that a domain has enabled HSTS, it does two things:

* Always uses an `https://` connection, even when clicking on an `http://` link or after typing a domain into the location bar without specifying a protocol.
* Removes the ability for users to click through warnings about invalid certificates.

A domain instructs browsers that it has enabled HSTS by returning an HTTP header over an HTTPS connection.

In its simplest form, the policy tells a browser to enable HSTS for that exact domain or subdomain, and to remember it for a given number of seconds:

```
Strict-Transport-Security: max-age=31536000;
```

In its **strongest and recommended form**, the HSTS policy includes all subdomains, and indicates a willingness to be ["preloaded"](#hsts-preloading) into browsers:

```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

## Background

Strict Transport Security was [proposed in 2009](https://lists.w3.org/Archives/Public/www-archive/2009Sep/att-0051/draft-hodges-strict-transport-sec-05.plain.html), motivated by [Moxie Marlinspike's demonstration](http://www.thoughtcrime.org/software/sslstrip/) of how a hostile network could downgrade visitor connections and exploit insecure redirects. It was quickly adopted by several major web browsers, and [finalized as RFC 6797 in 2012](https://tools.ietf.org/html/rfc6797).

The basic problem that HSTS solves is that even after a website turns on HTTPS, visitors may still end up trying to connect over plain HTTP. For example:

* When a user types "dccode.gov" into the URL bar, browsers default to using `http://`.
* A user may click on an old link that mistakenly uses an `http://` URL.
* A user's network may be hostile and actively rewrite `https://` links to `http://`.

Websites that prefer HTTPS will generally still listen for connections over HTTP in order to redirect the user to the HTTPS URL. For example:

```
$ curl --head http://www.facebook.com

HTTP/1.1 301 Moved Permanently
Location: https://www.facebook.com/
```

**This redirect is insecure** and is an opportunity for an attacker to capture information about the visitor (such as cookies from a previous secure session), or to maliciously redirect the user to a phishing site.

This can be addressed by returning a `Strict-Transport-Security` header whenever the user connects securely. For example:

```
$ curl --head https://www.facebook.com

HTTP/1.1 200 OK
Strict-Transport-Security: max-age=15552000; preload
```

This enables HSTS for `www.facebook.com`. While HSTS is in effect, clicking any links to `http://www.facebook.com` will cause the browser to issue a request directly for `https://www.facebook.com`.

In the above example, the browser will remember the HSTS policy for 180 days. The policy is refreshed every time browser sees the header again, so if a user visits `https://www.facebook.com` at least once every 180 days, they'll be indefinitely protected by HSTS.

## HSTS Preloading

Since it's just an HTTP header, HSTS is very easy to add to a domain.

However, to enable HSTS for a domain via the HTTP header, the browser does have to see the header at least once. This means that users are not protected until their first successful secure connection to a given domain.

To solve the "first visit" problem, the Chrome security team created an "HSTS preload list": a [list of domains](https://chromium.googlesource.com/chromium/src/+/master/net/http/transport_security_state_static.json) baked into Chrome that get Strict Transport Security enabled automatically, even for the first visit. Firefox and Safari also now use HSTS preload lists that include Chrome's list, as will upcoming versions of Internet Explorer.

The Chrome security team allows any domain to [submit their domain to the list](https://hstspreload.appspot.com/), provided it meets the following requirements:

* HTTPS is enabled on the root domain (e.g. `https://donotcall.gov`), and **all subdomains** (e.g. `https://www.donotcall.gov`).
* The HSTS policy includes all subdomains, with a long `max-age`, and a `preload` flag to indicate that the domain owner consents to preloading.
* The website redirects from HTTP to HTTPS, at least on the root domain.

An example of a valid HSTS header for preloading:

```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

While you can't hardcode the entire internet into a big list, the HSTS preload list is a simple, effective mechanism for locking down HTTPS for the near future. As the [web transitions fully to HTTPS](https://w3ctag.github.io/web-https/) over the long-term, and browsers can start phasing out plain HTTP and defaulting to HTTPS, the HSTS preload list (and HSTS itself) may eventually become unnecessary.

## HSTS as a forcing function

Strict Transport Security provides meaningful security benefits to visitors, especially visitors on hostile networks.

However, it's also highly valuable as an organizational forcing function and compliance mechanism.

When a domain owner follows the recommendations in this article and sets an HSTS policy on its base domain with `includeSubDomains` and `preload`, the domain owner is saying _"Every part of our web infrastructure is HTTPS, and always will be."_ &mdash; and is giving browsers permission to vigorously enforce that from then onwards.

It's a clear and auditable commitment, and gives anyone overseeing an organization's transition to HTTPS a way of marking domains as "done".

Zooming out even further: it's technically possible to preload HSTS for an entire top-level domain (e.g. ".gov"). No top-level domain has yet done this &mdash; but as a comparatively small, centrally managed top-level domain, perhaps someday `.gov` can be the first.

## Resources

* [Browser support for HSTS](http://caniuse.com/#search=hsts)
* [HSTS web developer documentation](https://developer.mozilla.org/en-US/docs/Web/Security/HTTP_strict_transport_security) maintained by the Mozilla community
* Chrome's [HSTS preload list](https://chromium.googlesource.com/chromium/src/+/master/net/http/transport_security_state_static.json), and their [submission form](https://hstspreload.appspot.com/).
* ["Upgrading HTTPS in Mid-Air"](http://www.internetsociety.org/sites/default/files/01_4_0.pdf) - A paper analyzing the current detailed practice of HSTS and [HTTP Public Key Pinning](https://developer.mozilla.org/en-US/docs/Web/Security/Public_Key_Pinning), as of November 2014.
* ["The first .gov domains hardcoded into your browser as all-HTTPS"](https://18f.gsa.gov/2015/02/09/the-first-gov-domains-hardcoded-into-your-browser-as-all-https/), by 18F.
