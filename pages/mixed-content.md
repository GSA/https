---
layout: page
title: Mixed Content
permalink: /mixed-content/
---

### What is mixed content?

When you view a page in your browser, it is almost never just a single request. Almost every web page contains resources, such as Javascript, CSS, and images, which cause additional requests. Sometimes these requests are to the same servers as the rest of the site, other times they are external resources (such as Google Analytics snippets of JavaScript).

When the main page is loaded over `HTTPS` and these sub-resources are loaded over `HTTP` this is called **mixed content**.

Mixed content comes in two varieties:

**Active** mixed content includes resources that can greatly change the behavior of a website, such as JavaScript, CSS, fonts, and iframes. Browsers block active content, which often results in affected pages being completely unstyled or broken.

**Passive** mixed content includes resources whose impact on the page's overall behavior is more minimal, such as images, audio, and video. Browsers will load passive mixed content, but will typically change the HTTPS indicator. For example, in Chrome this means that the "green lock" icon becomes a gray lock with a yellow triangle over it.

### Why is mixed content a problem?

Mixed content is a problem because, were browsers to allow it, an attacker would be able to conduct a MITM attack against it the same way they could the main page. Even where browsers do allow it, as with images, attackers can manipulate what the page looks like, and so the yellow-lock icon is intended to communicate that security has been weakened and user confidence should be reduced.

When a website is `HTTP`-only, loading other `HTTP` sub-resources does not generate any sort of warning, and so websites operating over `HTTP` often accumulate many of these sub-resources.

When an `HTTP` website tries to migrate to `HTTPS`, these can often become a source of difficulty.

### Strategies for dealing with mixed content

The easiest approaches are to use relative URLS (e.g. `<img src="/media/my-picture.png" />`) or protocol-relative URLs (e.g. `<img src="//other-website.com/their-picture.png" />`). These will work with both `HTTP` and `HTTPS` websites. `https://` can also be safely used from both `HTTP` and `HTTPS` pages (however these are often more difficult for local development).

In order to locate mixed content, the easiest way to start is to load your website in a browser over `https://` and see if it looks ok. Both Chrome and Firefox will log any mixed content to the console. This gives a quick way to get a sense of how large the problem is.

Another approach is to grep your codebase for any explicit `http://` URLs, since these will always cause a problem.

### Tools

* [`mixed-content-scan`](https://github.com/bramus/mixed-content-scan) can crawl a website to see if it contains any references to insecure resources. It can work on either `HTTP` or `HTTPS` websites.
