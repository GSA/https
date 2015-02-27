---
layout: page
title: FAQ
permalink: /faq/
---


### What information does HTTPS protect?

HTTPS encrypts nearly all information sent between a client and a web service.

For example, an **unencrypted HTTP** request reveals not just the body of the request, but the full URL, query string, and various HTTP headers about the client and request:

<img src="/assets/images/with-http-headers.png" title="What you see with HTTP" style="border: 1px solid black" />

An **encrypted HTTPS** request protects most things:

<img src="/assets/images/with-https-headers.png" title="What you see with HTTPS" style="border: 1px solid black" />

This is the same for all HTTP methods (GET, POST, PUT, etc.). The URL path and query string parameters are encrypted, as are POST bodies.

### What information does HTTPS _not_ protect?

As shown above, the full domain or subdomain and the originating IP address remain unencrypted.

Additionally, attackers can still analyze encrypted HTTPS traffic for "side channel" information. This can include the time spent on site, or the relative size of user input.

### How difficult is it to attack an HTTPS connection?

Attacks on HTTPS connections generally fall into 3 categories:

* Compromising the quality of the HTTPS connection, through cryptanalysis or other protocol weaknesses.
* Compromising the client computer, such as by installing a malicious root certificate into the system or browser trust store.
* Obtaining a "rogue" certificate trusted by major browsers, generally by manipulating or compromising a certificate authority.

These are all possible, but for most attackers they are very difficult and require significant expense. Importantly, they are all _targeted_ attacks, and are not feasible to execute against any user connecting to any website.

By contrast, plain HTTP connections can be easily intercepted and modified by anyone involved in the network connection, and so attacks can be carried out at large scale and at low cost.

### Why isn't DNSSEC good enough?

[DNSSEC](https://en.wikipedia.org/wiki/Domain_Name_System_Security_Extensions) is designed to guarantee the authenticity of resolving domain names. DNSSEC doesn't encrypt anything, and so DNSSEC alone provides no privacy. HTTPS provides a private, encrypted connection.

As importantly, **no web browsers support DNSSEC today**. No web browsers inform users that DNSSEC validation has failed, which means that DNSSEC does not secure browsing activity in practice today. This situation may change, but it will take years, as there is no visible momentum in the web browser community to address this.

By contrast, HTTPS is universally implemented and enforced in browsers, and in recent years has seen serious investment by the web and security community.

### How does HTTPS protect against DNS spoofing?

In practice, HTTPS can protect a domain even in the absence of DNSSEC support.

A valid HTTPS certificate guarantees that the server has demonstrated ownership over the domain to a trusted certificate authority.

To ensure that an attacker cannot use DNS spoofing to direct the user to a plain `http://` connection, websites can use [HTTP Strict Transport Security](/hsts/) (HSTS) to instruct browsers to require an HTTPS connection for their domain at all times.

This means that an attacker that successfully spoofs a DNS resolution must also create a valid HTTPS connection. This makes DNS spoofing as challenging as [attacking HTTPS](#).

HTTPS and HSTS work together to protect a domain against DNS spoofing.

