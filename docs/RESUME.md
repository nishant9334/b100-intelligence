# Resume, LinkedIn and interview kit

## Project line (resume header)
**B100 Intelligence — Fundamental-analysis dashboard & location API** | JavaScript, Chart.js, Python (pandas), GitHub Actions | [GitHub](https://github.com/nishant9334/b100-intelligence) · [Live demo](<pages-url>)

## Resume bullets (pick 3–4; every claim below is true of the code in this repo)
- Built an interactive web dashboard analysing 16 Nifty-style companies across 10 fiscal years (160 company-year records), covering profitability, growth, leverage, cash flow and dividends.
- Designed a 100-point composite financial-health score across six weighted dimensions, implemented in both JavaScript and Python (pandas) and cross-validated to within 0.01 points; covered by automated tests.
- Added a "health lab" that lets users re-weight the scoring model with sliders and investor-style presets and re-ranks all companies live, making model sensitivity visible.
- Implemented peer discovery with cosine similarity over z-scored financial ratios, and rule-based pros/cons that flag debt-free balance sheets, margin trends, weak cash conversion and low interest coverage.
- Built an in-browser mock of a B2B village-location REST API with API-key auth, plan-based state access control, standardised error responses, autocomplete and a map that highlights matches.
- Set up CI/CD with GitHub Actions to run tests and deploy the site to GitHub Pages on every push.

**Shorter, analyst-focused variant**
- Developed a company-health scoring model (6 dimensions, 100 points) and interactive dashboards on 10 years of financials; validated the model in Python and shipped it as a deployed web app.

## What NOT to claim (until it is true)
- Do not say it uses real Nifty 100 / census data: it is synthetic and labelled so.
- Do not claim Power BI, PostgreSQL, Django, Celery or real users/traffic until you build them.
- Do not quote performance, accuracy or revenue numbers that you have not measured.

## LinkedIn "Projects" description
Interactive dashboard that scores company financial health and benchmarks peers, paired with a demo location-API platform. Built with vanilla JS, Chart.js and Python; the scoring model is tested and cross-validated across two implementations. Uses synthetic data for demonstration. Code and live demo on GitHub.

## GitHub repo settings
- **Description:** Interactive fundamental-analysis dashboard (health scoring, peer similarity, risk map) and location-API demo. Synthetic data.
- **Topics:** `data-analytics` `dashboard` `chartjs` `financial-analysis` `pandas` `rest-api` `github-pages` `data-visualization`
- Pin the repo, add 3 screenshots to `docs/img/`, and set the Pages URL as the repo website.

## Interview prep
**Walk me through the health score.** Six dimensions summing to 100: profitability (percentile rank so it is relative to peers), growth, leverage, cash flow quality, dividends and trend. Each has an explicit rule, so the score is explainable rather than a black box.

**How do you know the model is correct?** I implemented it twice, in JavaScript and Python, and the outputs agree within rounding. Unit tests check bounds, band labels and edge cases such as debt-free and highly levered companies.

**What are its weaknesses?** Banks and NBFCs carry structurally high D/E, so a single leverage rule penalises them unfairly; sector-specific rules are the next step. The weights are judgement calls, which is why the health lab exposes them. Percentile ranking depends on the peer set.

**Why synthetic data?** The source database was not available, so I generated seeded, reproducible data with realistic ratios. The CSV schema is fixed, so real data drops in without code changes.

**What would you build next?** A PostgreSQL star schema with an ETL job, a real Django REST API with Swagger docs and rate limiting, scheduled re-scoring, and sector-specific scoring rules.

**How does peer similarity work?** Six ratios are standardised to z-scores and compared with cosine similarity, so peers are companies with similar financial shape, not just the same sector.
