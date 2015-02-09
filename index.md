---
layout: default
title: HTTPS in the government
permalink: /
---

HTTPS (`https://`) provides a secure, private connection across the public internet. Plain HTTP (`http://`) connections can be easily intercepted, manipulated, and impersonated.

In today's internet, and today's browsers, HTTPS is a helpful baseline for _all_ government websites, no matter how small or how static.

This website is a manual and support system for deploying HTTPS in the US federal government.

## Why HTTPS?

When properly configured, an HTTPS connection guarantees three things:

* **Privacy.** The visitor's connection is encrypted, obscuring URLs, cookies, and other sensitive metadata.
* **Authentication.** The visitor is talking to the "real" website, and not to an impersonator or through a "man-in-the-middle".
* **Integrity.** The data sent between the visitor and the website has not been tampered with or modified.

These properties have been considered an absolute requirement for highly sensitive services (e.g. password login forms, or bank accounts) for many years.

Over the last several years, it's become better understood that these properties should be the baseline for all web traffic.

* HTTPS today has seen [monumental speed improvements](https://istlsfastyet.com/), and [is not computationally expensive anymore](https://www.imperialviolet.org/2010/06/25/overclocking-ssl.html).
* Internet service providers [modify unencrypted websites in transit](http://arstechnica.com/tech-policy/2014/09/why-comcasts-javascript-ad-injections-threaten-security-net-neutrality/) and [add tracking headers](https://www.eff.org/deeplinks/2014/11/verizon-x-uidh) to their customers' unencrypted web activity.
* Newer versions of HTTP in modern browsers require encryption, and are [so blazing fast](https://www.httpvshttps.com/) that they may [reduce infrastructure costs](https://thethemefoundry.com/blog/why-we-dont-use-a-cdn-spdy-ssl/).

The GSA's [18F](https://18f.gsa.gov) team has written about [why they use HTTPS for every .gov they make](https://www.gov.uk/service-manual):

> The `.gov` in government websites carries a lot of weight. Citizens expect government websites to be secure, trustworthy, and reliable. Citizens expect anything they read on a `.gov` website to be official, and they expect any information they submit to that website — especially if they're submitting personal information — to be sent safely and only to the government.
>
> ...
>
> [Security, privacy, and speed are] useful for all of our applications, all of the time — not just when passwords or personal information are involved. By simply deploying HTTPS all of the time, we don't have to engineer a boundary around "sensitive" parts of the application, or judge where those lines should be drawn.

Many major organizations have reached the same conclusion:

* The UK government requires that [every government service use HTTPS](https://www.gov.uk/service-manual/domain-names/https.html).
* The internet's standards body (the IETF) and its parent organization (the Internet Society) have both stated that [encryption should be the norm on the internet](http://www.internetsociety.org/news/internet-society-commends-internet-architecture-board-recommendation-encryption-default).
* The technical architecture group at the W3C (the web's standards body) has declared that [the web should move to HTTPS](https://w3ctag.github.io/web-https/).
* Google [favors HTTPS websites in search rankings](http://googleonlinesecurity.blogspot.com/2014/08/https-as-ranking-signal_6.html), and the Chrome security team is working on [gradually marking plain HTTP as non-secure](https://www.chromium.org/Home/chromium-security/marking-http-as-non-secure).

Ultimately, the internet's goal is to establish encryption as the norm, and to phase out unencrypted connections entirely.

It's important to realize that investing in HTTPS makes it faster, cheaper, and easier for everyone. Many of the advancements of the last several years have come from major institutions and technology companies committing to migrate, improving the status quo, and contributing their improvements back to the public.

The more US government websites and services that join the transition to an encrypted internet, the smoother and faster it will be.
