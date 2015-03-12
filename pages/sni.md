---
layout: page
title: Server Name Indication
permalink: /sni/
---

**Server Name Indication**, often abbreviated SNI, is a TLS extension with which the client can indicate to the server to which hostname it is attempting to connect. If the server handles traffic for multiple hostnames, then without the client's explicit indication of which hostname it is attempting to connect to, the server may have difficulty determining the appropriate server certificate to present to the client in the TLS handshake.
