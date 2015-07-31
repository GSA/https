Links used in **[Implementing HTTPS](https://www.digitalgov.gov/event/implementing-https/)**, by Gray Brooks and Eric Mill of GSA.

See the [recorded presentation on YouTube](https://www.youtube.com/watch?v=rnM2qAfEG-M) (1 hour, 40 minutes).

#### Introduction

* [https.cio.gov FAQ on HTTPS](https://https.cio.gov/faq/)
* [Mozilla blog post on deprecating non-secure HTTP](https://blog.mozilla.org/security/2015/04/30/deprecating-non-secure-http/)
* [OMB Memorandum M-15-13](https://www.whitehouse.gov/sites/default/files/omb/memoranda/2015/m-15-13.pdf)

#### How HTTPS Works

* [Simple explanation for elliptic curve cryptography](https://bithin.wordpress.com/2012/02/22/simple-explanation-for-elliptic-curve-cryptography-ecc/)
* [Prime factorization](http://modular.math.washington.edu/edu/2007/spring/ent/ent-html/node7.html)
* [SSL Labs analysis of https.cio.gov](https://www.ssllabs.com/ssltest/analyze.html?d=https.cio.gov)
* [nginx configuration for https.cio.gov](https://github.com/GSA/https/blob/master/deploy/site.conf)
* [general nginx HTTPS configuration template](https://github.com/fisma-ready/nginx/blob/master/ssl/ssl.rules)
* [Apache configuration for courtlistener.com](https://github.com/freelawproject/courtlistener/blob/master/apache/courtlistener.com.conf)
* [Mozilla CA certificate policy](https://www.mozilla.org/en-US/about/governance/policies/security-group/certs/policy/)
* [Domain name system overview](http://www.itgeared.com/articles/1354-domain-name-system-dns-tutorial-overview/)

#### Migrating to HTTPS

* [https.cio.gov page on mixed content](https://https.cio.gov/mixed-content/)
* [W3C upgrade-insecure-requests spec](https://w3c.github.io/webappsec/specs/upgrade/)

#### HTTP Strict Transport Security

* [https.cio.gov page on HSTS](https://https.cio.gov/hsts/)
* [18F blog: The first .gov domains hardcoded into your browser as all-HTTPS](https://18f.gsa.gov/2015/02/09/the-first-gov-domains-hardcoded-into-your-browser-as-all-https/)
* [@HttpSecHeaders tweet about HSTS preloading](https://twitter.com/HttpSecHeaders/status/618546051641909248)
* [Chrome HSTS/HPKP preload list](https://chromium.googlesource.com/chromium/src/+/master/net/http/transport_security_state_static.json)

#### Technical Guidelines

* [https.cio.gov page on technical guidelines](https://https.cio.gov/technical-guidelines/)
* [Google security blog post on SHA-1 deprecation](http://googleonlinesecurity.blogspot.com/2014/09/gradually-sunsetting-sha-1.html)
* [Pulse page on HTTPS for .gov domains](https://pulse.cio.gov/https/domains/)
* [https.cio.gov page on Server Name Indication](https://https.cio.gov/sni/)
* [Introduction to OCSP](http://www.x500standard.com/index.php?n=X509W.OCSP)

#### The Future

* [TLS 1.3](https://tlswg.github.io/tls13-spec/)
* [Google blog post on QUIC](http://blog.chromium.org/2015/04/a-quic-update-on-googles-experimental.html)
* [HTTP/2 spec on TLS requirements](http://http2.github.io/http2-spec/#TLSUsage)
* [Digital Analytics Program dashboard](https://analytics.usa.gov)
* [Certificate transparency readings for *.whitehouse.gov](https://crt.sh/?q=%25whitehouse.gov)
* [Certificate Transparency homepage](http://www.certificate-transparency.org/)
* [Mozilla blog post on distrusting CNNIC](https://blog.mozilla.org/security/2015/04/02/distrusting-new-cnnic-certificates/)
* [RFC 7469, HTTP Public Key Pinning](http://tools.ietf.org/html/rfc7469)
* [HTTP Public Key Pinning, Explained](https://timtaubert.de/blog/2014/10/http-public-key-pinning-explained/)
* [CA/Browser Forum Baseline Requiremets](https://cabforum.org/baseline-requirements-documents/)
* [House Energy and Commerce Committee letter to browsers regarding government CAs](https://energycommerce.house.gov/letter/letters-browsers-regarding-government-certificate-authorities)
* [Mozilla's response to the House letter](https://blog.mozilla.org/netpolicy/files/2015/06/Mozilla-Response-to-Congressional-letter-on-CAs-signed.pdf)
* [Let's Encrypt, an upcoming free non-profit certificate authority](https://letsencrypt.org/)
