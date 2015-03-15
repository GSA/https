---
layout: page
title: Server Name Indication
permalink: /sni/
---

**[Server Name Indication](https://en.wikipedia.org/wiki/Server_Name_Indication)**, often abbreviated **SNI**, is an extension to TLS that allows multiple hostnames to be served over HTTPS from the same IP address. SNI accomplishes this by providing a mechanism for the client to tell the server which hostname it is trying to connect to.

Without SNI, a given IP address is only capable of reliably hosting a single hostname over `https://`.

For many web hosts and content delivery networks, requiring that clients support SNI allows secure websites to be more efficiently hosted and can greatly reduce costs.

However, some [legacy clients](#client-support) do not support SNI -- notably, IE on Windows XP -- and so many major services still do not require SNI support.

## Background

If the [server handles traffic for multiple hostnames](https://en.wikipedia.org/wiki/Virtual_hosting#Name-based), then without the client's explicit indication of which hostname it is attempting to connect to, the server may have difficulty determining the appropriate server certificate to present to the client in the TLS handshake.

If a server only ever handles traffic for a single hostname, there's no need for SNI. Similarly, a server may have multiple IP address, each of which is used only for a single hostname/certificate pair. Additionally, a single certificate may be able to cover all the possible hostnames for a given server IP address using [wildcards](https://en.wikipedia.org/wiki/Wildcard_certificate) or [Subject Alternative Names](https://en.wikipedia.org/wiki/SubjectAltName).

However, in many cases, such as [content distribution networks (CDNs)](https://en.wikipedia.org/wiki/Content_delivery_network), the server services far too many unrelated hostnames to reasonably share a single server certificate. Due to the scarcity of IPv4 addresses, it is also long-term untenable to simply acquire a new IPv4 address for each hostname. Therefore, client SNI support is extremely useful.

Thus, it can be highly desirable for servers to depend on client SNI support. All modern browsers support SNI, but some older browsers on older OSes (notably IE6 and Android versions before Honeycomb). Depending on what clients are necessary to support, servers may or may not be able to depend on client SNI support.

## Client support

The most commonly used clients without support for SNI are:

* Internet Explorer on Windows XP
* Some versions of Python 2 (fixed in 2.7.9)
* The default browser in Android 2.3 and earlier

Additionally, some enterprise networks may not yet be configured for SNI support.

Note that Internet Explorer on Windows XP has already been rendered nearly unusable by the [POODLE vulnerability](https://en.wikipedia.org/wiki/POODLE). This vulnerability caused many major websites to disable support for SSLv3, which IE6 requires.

For specific detail on client support for SNI, refer to [Wikipedia](https://en.wikipedia.org/wiki/Server_Name_Indication#Client_side).
