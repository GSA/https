---
layout: page
title: Mixed Content
permalink: /mixed-content/
description: "Strategies for dealing with mixed content when upgrading a website from HTTP to HTTPS."
---

When an HTTPS website references insecure (HTTP) resources, this is called **[mixed content](http://www.w3.org/TR/mixed-content/)**.

Browsers prevent an HTTPS website from loading most insecure resources, like fonts, scripts, etc. Migrating an existing website from HTTP to HTTPS means identifying and fixing or replacing mixed content.

[Mixed content](http://www.w3.org/TR/mixed-content/) comes in two varieties:

**Active** mixed content includes resources that can greatly change the behavior of a website, such as JavaScript, CSS, fonts, and iframes. Browsers refuse to load active mixed content, which often results in affected pages being completely unstyled or broken. Browsers treat these very aggressively because of the consequences if they were compromised. For example, a single compromised Javascript file compromises the entire website, regardless of how other resources are loaded.

**Passive** mixed content includes resources whose impact on the page's overall behavior is more minimal, such as images, audio, and video. Browsers will load passive mixed content, but will typically change the HTTPS indicator.

In Chrome, a website indicator for passive mixed content looks like this:

![fedramp in chrome](/assets/images/mixed-content.png)

## Migration strategy

Every website's mixed content situation will be different, but the general approach is:

* Enable `https://` for your website, but don't force a redirect. Continue to present the `http://` version as the canonical URL to search engines.
* Identify the most obvious and widespread pieces of mixed content by loading your website in a browser over `https://` and observing breakages. Chrome and Firefox will log any mixed content warnings to the console, which should point out necessary site-wide changes. Use these to [secure your resource links](#linking-to-resources-securely).
* After fixing them, tackle the long tail by [scanning your code](#scanning-your-code) and [crawling your website](#crawling-your-website).
* Finally, force the redirect to HTTPS, and tell search engines that your new URL starts with `https://`.

Note: the below instructions use tools **optimized for an OS X or Linux environment**. Documentation for Windows-based tools would be a welcome contribution to this guide.

## Linking to resources securely

Most commonly used third party services, such as Google Analytics or AddThis, **will automatically adapt** when migrating to HTTPS.

Other services may require manual updates, but have an `https://` version ready:

```html
<link href="https://fonts.googleapis.com/css?family=Open+Sans" rel="stylesheet" type="text/css">
```

Generally speaking, for content on your own domain, stick to site-relative URLs wherever possible:

```html
<img src="/media/my-picture.png" />
```

When migrating a site with a lot of user- or staff-submitted content (e.g. a blog), you may find media hotlinked from a third-party domain which doesn't support HTTPS.

This is a great opportunity to improve your website's privacy and lessen your dependency on third parties, by copying those media files to your own server instead and hosting them yourself.

## Scanning your code

After identifying and fixing the obvious issues, you can scan your website's files for leads. On a Mac or Linux-based system, `grep` is very handy:

Images and scripts:

    grep -r "src=\"http:" *

Stylesheets and fonts:

    grep -r "href=\"http:" * | grep "<link"

CSS imports and references:

    grep -r "url(\"http:"

Finding links in JavaScript is more challenging, but you can look for all `http:` references and try to exclude hyperlinks in HTML or Markdown:

    grep -r "http:" | grep -v "href=\"http:"
    grep -r "http:" | grep -v "](http:"


## Crawling your website

[`mixed-content-scan`](https://github.com/bramus/mixed-content-scan) is a very handy command line tool that can crawl an `http://` or `https://` website to see if it contains any references to insecure resources. This is especially helpful if your content is primarily managed in a CMS.

`mixed-content-scan` requires PHP, then [installing Composer](https://getcomposer.org/doc/00-intro.md). [Install with Composer](https://github.com/bramus/mixed-content-scan#installation), then use it with your domain:

```bash
mixed-content-scan https://https.cio.gov
```

You should see something like this:

```
[2015-03-15 16:56:48] MCS.NOTICE: Scanning https://https.cio.gov/ [] []
[2015-03-15 16:56:49] MCS.INFO: 00000 - https://https.cio.gov/ [] []
[2015-03-15 16:56:49] MCS.INFO: 00001 - https://https.cio.gov/faq/ [] []
[2015-03-15 16:56:49] MCS.INFO: 00002 - https://https.cio.gov/hsts/ [] []
[2015-03-15 16:56:49] MCS.INFO: 00003 - https://https.cio.gov/resources/ [] []
[2015-03-15 16:56:49] MCS.NOTICE: Scanned 4 pages for Mixed Content [] []
```

Any discovered mixed content will be listed as a `WARNING`. You can also get the results as newline-separated JSON objects:

```bash
mixed-content-scan https://https.cio.gov --format=json
```

## Why do browsers block mixed content?

If mixed content were not blocked, an attacker could control the main website by conducting a MITM attack against any of its active resources.

Even with passive content like images, attackers can manipulate what the page looks like, and so the yellow-lock icon is intended to communicate that security has been weakened and user confidence should be reduced. In addition, an attacker will be able to read any cookies for that domain which do have the `Secure` flag, and set cookies.

When a website is accessible over `http://`, loading other insecure resources does not generate any sort of warning, and so websites operating over plain HTTP often accumulate many of these sub-resources.
