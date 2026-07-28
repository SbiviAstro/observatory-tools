# Deploying

    site/
      public/     <- publish this directory, and only this one
      build/      <- tooling and internal documents; never published

Point Cloudflare Pages (or Netlify) at `public/` as the output directory. Both
read `_headers` from the root of whatever they publish, which is why it lives
inside `public/` rather than beside this file.

## Before every publish

    cd build
    python3 build-csp-headers.py

The Content-Security-Policy names the SHA-256 of each page's inline script, so
the browser will run a block only if its hash matches. That also means **a hash
is only valid for the exact bytes it was taken from**: change one character of
any page and that page stops running until the header is regenerated. The script
rewrites `public/_headers` from the current files and refuses to write a partial
result.

If a page ever renders blank with "Refused to execute inline script" in the
console, a stale hash is the first thing to check.

## Why the split

`build-csp-headers.py` was previously being served alongside the site. It is a
build tool: publishing it exposed internals for no benefit. Keeping tooling in a
sibling directory means the deploy target can never pick it up by accident.

## Why the pages stayed flat

Every page kept its existing URL. Grouping them into `docs/` and `legal/` would
read a little tidier but would break every existing link and bookmark for a
sixteen-page site, which is a poor trade. Only the downloadable files moved, into
`assets/`, and those were referenced from four places.

## What is in assets/

| file | linked from |
|---|---|
| `overview.pdf` | overview.html |
| `sample-horizon.hrz` | horizon-guide.html, both calculators |
| `logo.svg` | nothing — kept as the brand original; the nav logo is inline SVG |
