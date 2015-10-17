---
layout: page
title: Server Name Indication
permalink: /sni/
description: "An overview of Server Name Indication (SNI), a TLS extension to allow multiple secure hostnames to be served from a single IP address."
---

**[Server Name Indication](https://en.wikipedia.org/wiki/Server_Name_Indication)**, often abbreviated **SNI**, is an [extension to TLS](https://tools.ietf.org/html/rfc6066#page-6) that allows multiple hostnames to be served over HTTPS from the same IP address.

A website owner can **require SNI support**, either by allowing their host to do this for them, or by directly consolidating multiple hostnames onto a smaller number of IP addresses. Requiring SNI has the potential to [save significant money](#making-https-cheaper) and resources.

However, a few [legacy clients](#client-support) (notably, Internet Explorer on Windows XP) do not support SNI, and will be cut off if SNI is required.

Website owners are encouraged to **evaluate whether requiring SNI is feasible**:

* For websites accessed primarily by browsers, look at usage by **Internet Explorer 8 and Android 2.3** (and below). If these usage numbers are low, requiring SNI is likely feasible.

* For web services accessed by non-browser clients (e.g. APIs), look at usage by Python 2.7.8 and Java 1.6 (and below), and [any other relevant clients](https://en.wikipedia.org/wiki/Server_Name_Indication#Client_side). APIs with heterogeneous clients may wish to do more sophisticated client detection, or staged rollouts.

See [`analytics.usa.gov`](https://analytics.usa.gov) for an example of a .gov website which requires support for SNI.

## Making HTTPS cheaper

Without SNI, a given IP address is only capable of reliably hosting a single hostname over `https://`. Since [IPv4 addresses are running out](https://en.wikipedia.org/wiki/IPv4_address_exhaustion), IP addresses are expensive to reserve for single domains.

For many web hosts and content delivery networks, requiring that clients support SNI allows secure websites to be more efficiently hosted and can greatly reduce costs.

## Client support

The most commonly used clients without support for SNI are:

* Internet Explorer 8 (and below) on Windows XP
* Some versions of Python 2 (fixed in 2.7.9)
* The default browser in Android 2.3 and earlier

Additionally, some enterprise networks may not yet be configured for SNI support.

For specific detail on client support for SNI, refer to [Wikipedia](https://en.wikipedia.org/wiki/Server_Name_Indication#Client_side).

## Privacy considerations

SNI is sent by browsers to servers "in the clear" -- it is not part of the encrypted TLS handshake. When a domain or a subdomain itself reveal sensitive information (e.g. 'contraception.foo.gov' or 'suicide-help.foo.gov'), this can reveal that information to passive eavesdroppers. 

Whether SNI is enabled for their websites or not, website managers should consider all domains and subdomains as unencrypted over HTTPS, and account for this when provisioning domains and subdomains.

## Resources

* See ["If you can read this, you're SNIing"](https://www.mnot.net/blog/2014/05/09/if_you_can_read_this_youre_sniing) for an example of a site that will hard-fail when accessed by a client that does not support SNI.
* [Wikipedia page for SNI](https://en.wikipedia.org/wiki/Server_Name_Indication)
