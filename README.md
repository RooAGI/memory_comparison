# Memory Systems Comparison

A source-led static site for project-owned system reviews, article provenance, and benchmark records. Review criteria live in [REVIEW.md](REVIEW.md); metric formulas live in [METRICS.md](METRICS.md). Source inspection and measured workload outcomes are separate evidence types. The site does not calculate a composite score or rank systems.

The project assessment roster is stored in [data/project-assessments.json](data/project-assessments.json). Detailed source articles are stored in [data/system-articles.json](data/system-articles.json) and companion article JSON files in `data/`. Atlas information, where retained, is attributed only as discovery metadata and is not used as a project assessment.

## Requirements

- Node.js 22 LTS (Node 20.19+ or 22.12+ is also supported by Vite 7)
- npm 10 or newer
- Git for cloning and pushing the repository

The built site is static HTML, CSS, JavaScript, and JSON. Visitors need no Python runtime, application server, or server-side process.

## Develop locally

From the repository root:

```sh
npm install
npm run dev
```

Open the local URL printed by Vite (usually [http://localhost:5173](http://localhost:5173)).

## Build and preview production output

```sh
npm run build
npm run preview
```

The production site is written to `dist/`. The build bundles the React UI and copies article evidence records and project reference documents needed by source links. Vite preview prints a local URL, usually [http://localhost:4173](http://localhost:4173).

## GitHub Pages setup and deployment

The repository includes [the Pages Actions workflow](.github/workflows/deploy-pages.yml). It builds and deploys on pushes to `main` and can also be started manually.

1. Push the repository to GitHub.
2. Open **Settings → Pages** for the repository.
3. Under **Build and deployment → Source**, select **GitHub Actions** and save.
4. Push to `main`, or open **Actions → Deploy static site to GitHub Pages → Run workflow**.
5. Check the workflow run and the URL shown under **Settings → Pages**.

Vite uses relative asset URLs so the app works at a repository path such as `https://<owner>.github.io/memory_comparison/`. Local build commands do not publish or deploy the site.

## Review content

The system review list searches names, repositories, and source labels. Each article retains its reviewed revision, source links, evidence by metric domain, and benchmark status. The project roster and benchmark records are available under **Project assessment**.

The site loads records listed in [results/index.json](results/index.json). Execution-status records describe planned or blocked work and are not measured outcomes. A record with `data_kind: measured_benchmark_result` represents a versioned workload run. Null values mean unavailable or not observed; planned fixture counts are not measured denominators. The result display retains units, sample counts or denominators, unknown and unsupported states, and raw record links.

Update [data/project-assessments.json](data/project-assessments.json) only from the chosen roster and direct review of each upstream repository. Record the analyzed commit, review date, inspected evidence, and unknown scope. To add a benchmark record, put its versioned JSON in `results/` and add its relative path and label to `results/index.json`.

Python is optional for maintenance tools, not site hosting: Python 3.10+ is used by the optional catalog refresh and benchmark fixture checker. The fixture and metric definitions are in [fixtures/memory-benchmark-v1.json](fixtures/memory-benchmark-v1.json) and [METRICS.md](METRICS.md).
