---
layout: page
title: Server Name Indication
permalink: /sni/
---

**Server Name Indication**, often abbreviated SNI, is a TLS extension with which the client can indicate to the server to which hostname it is attempting to connect. If the [server handles traffic for multiple hostnames](http://en.wikipedia.org/wiki/Virtual_hosting#Name-based), then without the client's explicit indication of which hostname it is attempting to connect to, the server may have difficulty determining the appropriate server certificate to present to the client in the TLS handshake.

Some web servers may not require SNI in order to determine the correct certificate to serve. For example, the server may only ever handle traffic for a single hostname. Alternatively, the server may be able to determine the hostname the client wants to connect to if, for a given server IP address, there is only a single hostname that resolves to that address. Additionally, a single certificate may be able to cover all the possible hostnames for a given server IP address using [wildcards](http://en.wikipedia.org/wiki/Wildcard_certificate) or [Subject Alternative Names](http://en.wikipedia.org/wiki/SubjectAltName).

However, in many cases, such as [content distribution networks (CDNs)](http://en.wikipedia.org/wiki/Content_delivery_network), the server services far too many disparate hostnames to reasonably share a single server certificate. Due to the scarcity of IPv4 addresses, it is also long-term untenable to simply acquire a new IPv4 address for each hostname. In such situations, client SNI support is extremely useful.
