---
layout: page
title: Certificates
permalink: /certificates/
description: "Guidance around certificates for use in HTTPS."
---

This page covers certificates, certificate authorities, and related frequently asked questions.

* [Introduction](#introduction)
* [Getting a certificate](#getting-a-certificate)
* [Trusting certificate authorities](#signature-algorithms)
* [Certificate FAQ](#certificate-faq)

## Introduction

Websites use **certificates** to create an HTTPS connection. When signed by a trusted **certificate authority** (CA), certificates give confidence to browsers that they are visiting the "real" website.

Technically, a certificate is a file that contains:

* The domain(s) it is authorized to represent.
* A numeric "public key" that mathematically corresponds to a "private key" held by the website owner.
* A cryptographic signature by a certificate authority (CA) that vouches for the relationship between the private key and the authorized domain(s).
* Other technical information, such when the certificate expires, and how extensively the domain was validated.
* Optionally, information about a person or organization that owns the domain(s).

Web browsers are generally set to trust a pre-selected list of certificate authorities (CAs), and the browser can verify that any signature it sees comes from a CA in that list. The list of trusted CAs is set either by the underlying operating system or by the browser itself.

When a website presents a certificate to a browser during an HTTPS connection, the browser uses the information and signature in the certificate to confirm that a CA it trusts has decided to trust the website the browser is connecting to.

## Getting a certificate



## Certificate authorities




## Certificate FAQ

