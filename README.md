# DH Conference Radar

A small Jekyll/GitHub Pages site for tracking major Digital Humanities conferences and the organizations behind them.

The site is deliberately data-first:

- `_data/conferences.yml` contains event facts and confidence/status fields.
- `_data/organizations.yml` contains association details.
- `_data/source_watch.yml` lists official pages to check every three months.
- `calendar/*.ics` contains one downloadable calendar file per confirmed dated conference.
- `scripts/generate_ics.py` regenerates the calendar downloads from `_data/conferences.yml`.
- `scripts/update_conferences.py` detects changed official source pages and writes a review report.

## Publish on GitHub Pages

Create a new repository from this folder:

```bash
git init
git add .
git commit -m "Initial DH conference radar site"
gh repo create dh-conference-radar --public --source=. --remote=origin --push
```

Then enable GitHub Pages with GitHub Actions as the source in the repository settings. The included `pages.yml` workflow builds and deploys the Jekyll site.

## Local development

```bash
bundle install
bundle exec jekyll serve
```

Open `http://127.0.0.1:4000`.

Use Ruby 3.2 or newer. The included `.ruby-version` and GitHub Actions workflow both target Ruby 3.2.

## Quarterly updates

The `Quarterly source check` workflow runs on the first day of every third month and can also be started manually. When a watched source page changes, it updates `_data/source_watch.yml`, writes a report under `reports/`, and opens a pull request for review.

This review step is intentional. DH organizations publish conference information in different formats, and reviewed updates reduce the risk of a brittle scraper silently changing dates incorrectly.

## Adding a conference

Add an entry to `_data/conferences.yml` with:

- `status: confirmed` when an official source gives dates and place.
- `status: watch` when the organization is important but the next event is not yet announced.
- `source` pointing to the specific official page where the claim can be checked.

Set `sort_date` to the start date for confirmed events or a far-future value such as `9999-01-01` for watchlist entries.

After adding or changing confirmed dates, regenerate downloadable calendar files:

```bash
python3 scripts/generate_ics.py
```
