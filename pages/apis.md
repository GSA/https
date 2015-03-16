---
layout: page
title: Migrating APIs to HTTPS
permalink: /apis/
---

All APIs should use and require HTTPS to [help guarantee](/faq/) **confidentiality**, **authenticity**, and **integrity**.

HTTPS provides a stronger guarantee that a client is communicating with the real API and receiving back authentic contents. It also enhances privacy for applications and users using the API. For APIs that support cross-origin request sharing (CORS) or JSONP requests, it also ensures the requests are not blocked as [mixed content](/mixed-content/).

All new APIs should use and require HTTPS. Rather than issue a redirect when visited over HTTP (redirects within APIs are problematic, as outlined below), the API should likely return an error message (such as the HTTP status code 403 Forbidden).

To migrate an existing API that runs over plain HTTP, start by adding HTTPS support.

## Add HTTPS Support

Once you've acquired and installed a certificate, you should test the API over HTTPS and make any needed adjustments.

Enable [HTTP Strict Transport Security](/hsts/) if possible, but do **not** redirect API traffic from HTTP to HTTPS.

You can safely enable HSTS and submit the domain to the HSTS browser preload list. HSTS was primarily [designed](http://tools.ietf.org/html/rfc6797#section-2.1) for web sites and is only supported in web browsers, not clients that would be used for integrating with APIs. As the API will continue to serve content over both HTTP and HTTPS, clients making HTTP requests to the API will continue to work.

## Update Your Documentation

Update your documentation to refer only to the HTTPS endpoint. Be sure to update all code examples, client libraries, sample applications, and your own applications (if you are an integrator of your own API). Update any pages, lists, or indexes that reference your API, such as `/data` or [data.gov](http://www.data.gov) (via `data.json`).

Mark HTTP as deprecated in your documentation and strongly recommend migrating to the HTTPS endpoint. Publish a dedicated information and resources page to which you can link.

## Measure HTTPS Usage

API analytics are key for measuring performance, seeing how others are using your API, and tracking usage over time.

You should track usage of the API over HTTP versus HTTPS. If you have a way of identifying individual integrators, such as via an API key, application secret, or other submitted value, you can monitor their usage of HTTP versus HTTPS.

## Announce HTTP Deprecation

Announce that you have deprecated the HTTP endpoint of your API. Post this to your developer hub, blog, and/or mailing list. Optionally, include a deadline.

If you have a method of contacting specific API integrators, such as an email address when they signed up for an API key, contact them. You may also have a list of known API-driven projects.

Search the internet, and GitHub in particular, for references to the domain name or URL of your API, and your API's documentation. Open issues on GitHub repositories about moving to the HTTPS endpoint, or even file a pull request making the change yourself.

## Disable the HTTP Endpoint

This entire process could take anywhere from two weeks to six months or longer. You will want to weigh how widely used your API is, how critical it is, and how quickly integrators of your API make adjustments. Questions to ask at this stage:

* Does my API work over HTTPS?
* Am I recommending HTTPS for my API?
* Am I collecting useful information from API clients?

First, perform a "blackout test" by turning off the HTTP endpoint for a set time period, usually somewhere between a few hours and a few days. Monitor your analytics and see what complaints this sends your way.

Refer complainants to your dedicated page in your documentation and encourage them to migrate as soon as possible. It usually takes just a few lines of code or configuration for an API integrator to switch to the HTTPS endpoint of an API, so do not be discouraged by the feedback from eventually disabling the HTTP endpoint.

Announce any blackout tests ahead of time. Optional: Pick a deadline for when you will turn off the HTTP API and include this in your announcement.

If you had no complaints, try a longer blackout, such as as a few days to a week. (This is especially helpful if you have no analytics and are relying on complaints as a metric.)

You can conduct multiple blackouts if your analytics show they make a good improvement the number of integrators using HTTPS over HTTP, but be mindful of diminishing returns.

Announce a deadline for when you will turn off the HTTP API if you have not yet done so.

On the deadline, disable the HTTP endpoint. Make an announcement, referring your previous efforts to ensure a smooth transition and to your documentation, which includes a page on the migration.

## Technical Considerations

When turning off an HTTP endpoint, return an error in the same consumable manner with which your API would typically respond. Issue a clear error message, include a hyperlink if possible, and use an appropriate HTTP status code such as 403 Forbidden.

**Do not redirect HTTP to HTTPS.** Redirects may break API clients as, unlike browsers, they may not be configured to follow redirects. Even if they followed the redirect, many API clients will change a POST request into a GET request, breaking RESTful APIs.

RFC2616 [documented this improper behavior](http://tools.ietf.org/html/rfc2616#section-10.3.2). [RFC7231](https://tools.ietf.org/html/rfc7231#section-6.4.7) (HTTP/1.1) introduced a new HTTP status code 307 as a temporary redirect that does not allow changing the request method, and [https://tools.ietf.org/html/rfc7238](RFC7238) proposes 308 as a permanent redirect. While most web browsers support 307, and some support 308, these may not be supported by API clients and should not be relied on for migrating an API.

This is meant to apply to APIs that are RESTful or equivalent. If your API is actually a public dataset that is downloaded usually through a web browser, a redirect would likely be appropriate. (Note that HSTS could also handle this redirect for you.)

**Redirecting CORS Requests:** Your API may support cross-origin resource sharing (CORS) through the use of `Access-Control-Allow-Origin` headers. While we recommend returning an error once an HTTP version of an API is shut down, you can optionally choose to redirect CORS requests, which is widely supported in web browsers. These web browsers will obey HSTS and the HSTS preload list, thus your choices are 1) break non-HTTPS CORS requests or 2) specially handle and redirect CORS requests.

 * First determine how widespread CORS requests are, what browsers make them, and ideally, what the referring URLs are (for ease of contacting the integrator).
 * Redirect to the HTTPS version of the API endpoint when the `Origin` HTTP header is present to signify a CORS request. **Note:** CORS headers must be included in the redirect response, as well as the response to which the request is redirected.
 * CORS GET requests will not follow a redirect in Android before version 4.4, all versions of iOS, and all versions of Safari. This also applies to an HSTS "internal" redirect. If mobile browsers are not a major user, then forcing a redirect should go pretty smoothly.

**Redirecting JSONP Requests:** Your API may support JSONP requests. Web browsers will follow redirects for JSONP requests, since these are simply `<script>` elements. Enabling HSTS and submitting the domain to the HSTS preload list would be enough for browsers that support the preload list. If you wish to handle all JSONP requests:

* First determine how widespread JSONP requests are, what browsers make them, and ideally, what the referring URLs are (for ease of contacting the integrator).
* Redirect to the HTTPS version of the API endpoint when the JSONP callback parameter for your API is present (usually `?jsonp=` or `?callback=`).
* Consider whether to support JSONP going forward, as it is [not secure or performant](https://gist.github.com/tmcw/6244497).
