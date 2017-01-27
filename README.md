## HTTPS Everywhere for the U.S. Government

The American people expect government websites to be secure and their interactions with those websites to be private.

This site contains a web-friendly version of the White House Office of Management and Budget memorandum [M-15-13](https://obamawhitehouse.archives.gov/sites/default/files/omb/memoranda/2015/m-15-13.pdf), **"A Policy to Require Secure Connections across Federal Websites and Web Services"**, and provides technical guidance and best practices to assist in its implementation.

**[Read the policy.](https://https.cio.gov)**

Please [open an issue](https://github.com/gsa/https/issues/new) to leave feedback or suggestions. Pull requests are welcome to pages _other_ than the homepage, which shows the final policy and is not subject to change through GitHub.

### Thank You For Your Feedback

This policy was open for public comment before its finalization. It received [numerous comments](https://github.com/GSA/https/issues?utf8=%E2%9C%93&q=label%3A%22Public+Comment%22+) whose thoughtfulness and feedback improved the **[final policy](https://obamawhitehouse.archives.gov/sites/default/files/omb/memoranda/2015/m-15-13.pdf)**.

You can see what changed between the proposal and the final policy in [pull request #108](https://github.com/GSA/https/pull/108).

The homepage of this site is the final policy. The other pages on [https.cio.gov](https://https.cio.gov) are open for contribution at any time, and are intended to be resources for agencies implementing the HTTPS policy.

### Developing on the site locally

This site uses [Jekyll](http://jekyllrb.com), [Sass](http://sass-lang.com), [Bourbon](http://bourbon.io), [Neat](http://neat.bourbon.io), and requires **Ruby 2.x**.

Install dependencies with Bundler:

```
bundle install
```

Start up a Sass watcher to keep assets auto-compiled:

```
make watch
```

And run the site with Jekyll:

```
bundle exec jekyll serve --watch
```

If all goes well, visit the site at `http://localhost:4000`.

### Public domain

This project is in the worldwide [public domain](LICENSE.md). As stated in [CONTRIBUTING](CONTRIBUTING.md):

> This project is in the public domain within the United States, and copyright and related rights in the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).
>
> All contributions to this project will be released under the CC0 dedication. By submitting a pull request, you are agreeing to comply with this waiver of copyright interest.
