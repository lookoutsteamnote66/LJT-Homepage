# LJT-Homepage

Junteng Liu's single-page academic homepage, forked from [Academic Pages](https://github.com/academicpages/academicpages.github.io).

## Content and scope

- `_pages/about.md` is the only published HTML page. It contains the biography, academic background, research experience, all six publications with authors and venues, research areas and interests, scholarship, and contact information from the supplied memory.
- `_data/navigation.yml` links only to sections of that About page.
- `_config.yml` excludes all template demo pages, posts, publication detail pages, teaching, talks, portfolio, sample downloads, and talk maps from the build. No other personal pages have been added.
- The remembered first-year status and date ranges are preserved rather than updated or inferred. No specific programming-language or tooling skills, portrait, paper URLs, or code-repository URLs were supplied, so none are invented. Known code-repository names remain plain text.
- `Vicent0205` remains the personal GitHub contact from memory. `lookoutsteamnote66/LJT-Homepage` is the hosting repository.

## Build and verify

```sh
bundle install
bundle exec jekyll build
python3 scripts/verify_homepage.py
```

The verification checks that the output contains only `index.html`, that all six publications appear in the About section, that remembered details and contact links are present, that template placeholders are absent, and that local links and assets use the project-site path.

## GitHub Pages

The configured project URL is `https://lookoutsteamnote66.github.io/LJT-Homepage/`.

The workflow in `.github/workflows/jekyll.yml` builds and verifies the site, then attempts GitHub Pages configuration and deployment. GitHub may require the repository owner to enable Actions for a new fork and select **Settings → Pages → Source → GitHub Actions** before deployment can succeed. A configured URL alone does not mean the site is live.

The original template's MIT license is retained in `LICENSE`.
