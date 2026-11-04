# Task 02 — Descriptive Statistics with Pure Python, Pandas, and Polars

## Project description

This repository implements **Research Task 2 / Milestone A**. It extends Task 1 by adding **Polars** as a third analytical approach and by introducing **grouped analysis** at two levels:

- `page_id`
- `page_id, ad_id`

The same Facebook political-advertising CSV was analyzed independently with Pure Python, Pandas, and Polars. The three implementations use aligned missing-value and numeric-cleaning rules so that their results can be compared directly.

## Dataset

The assignment specifies the **2024 Facebook Political Ads** CSV supplied through the program's Google Drive. The Task 2 dataset is different from the Task 1 file.

The dataset is intentionally **not included in this GitHub repository**. Download it from the program's Google Drive source and place it locally at:

```text
data/facebook_political_ads.csv
```

The completed local analysis contained:

- **246,745 rows**
- **41 columns**
- **4,475 unique `page_id` values**
- **246,745 unique `ad_id` values**

## Repository contents

- `pure_python_stats.py` — standard-library-only descriptive and grouped analysis.
- `pandas_stats.py` — equivalent analysis using Pandas.
- `polars_stats.py` — equivalent analysis using Polars.
- `verify_results.py` — checks agreement among the three dataset-level summaries.
- `FINDINGS.md` — narrative interpretation of the actual Task 2 results.
- `REFLECTION.md` — comparison of Pure Python, Pandas, and Polars.
- `AI_CODE_REVIEW.md` — reflection on critically evaluating AI-generated starter code.
- `requirements.txt` — dependencies for Pandas and Polars.
- `SUBMISSION_CHECKLIST.md` — final submission checklist.

## Setup

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

Create the local data folder if needed:

```bash
mkdir -p data outputs
```

Place the instructor-provided CSV at:

```text
data/facebook_political_ads.csv
```

## Run all three analyses

```bash
python3 pure_python_stats.py data/facebook_political_ads.csv --output-dir outputs
python3 pandas_stats.py data/facebook_political_ads.csv --output-dir outputs
python3 polars_stats.py data/facebook_political_ads.csv --output-dir outputs
python3 verify_results.py outputs
```

The completed local run returned:

```text
PASS: core dataset-level statistics agree across Pure Python, Pandas, and Polars.
```

## Main output files

The scripts create machine-readable outputs such as:

```text
outputs/pure_python_dataset_summary.json
outputs/pandas_dataset_summary.json
outputs/polars_dataset_summary.json
outputs/*_page_id_counts.csv
outputs/*_page_id_ad_id_counts.csv
```

The dataset itself should not be committed to GitHub.

## Data-cleaning decisions

To make the implementations comparable:

1. Blank values and common null tokens (`NA`, `N/A`, `null`, `none`, `nan`, `missing`, `-`) are treated as missing.
2. Numeric candidates are cleaned consistently before analysis.
3. A column is treated as numeric only when the same parsing rule is satisfied across approaches.
4. Complex dictionary/list-like values remain categorical strings unless a separate transformation is explicitly justified.

This is important because several fields contain serialized structures rather than simple scalar values.

## Key findings

### Concentration by page

The largest `page_id` group contained **55,503 records**, representing approximately **22.5%** of the full dataset. The next-largest groups contained **23,988**, **14,822**, **10,461**, and **9,851** records.

This shows that advertising records are not evenly distributed across pages.

### `page_id/ad_id` uniqueness

The grouped analysis produced **246,745 unique `page_id/ad_id` pairs**, and every pair had row count 1. Therefore, there were **zero duplicated page/ad pairs**.

### Spend and impressions

The data are strongly right-skewed:

- estimated spend: mean **1,061.29**, median **49**
- estimated impressions: mean **45,601.53**, median **3,499**
- estimated audience size: mean **556,462.86**, median **300,000**

The difference between means and medians shows why a single average can be misleading in this dataset.

### Platforms

The most common publisher combination was **Facebook + Instagram**, with **214,434 records (86.9%)**. Facebook-only records accounted for about 9.4%, and Instagram-only records for about 3.4%.

### Timing

The most frequent ad-creation date was **October 27, 2024**, with **8,619 records**. Several other top dates also fell in late October.

### Byline and candidate references

`HARRIS FOR PRESIDENT` was the most frequent byline with **49,788 records**, followed by `HARRIS VICTORY FUND` with **32,612**.

The `illuminating_mentions` field most commonly contained no named mention. Among explicitly named values, `Donald Trump` appeared most frequently, followed by `Kamala Harris`, `President Trump`, and `Joe Biden`. Because naming variants exist, they should be normalized before combining counts.

See `FINDINGS.md` for the full narrative.

## Comparison of the three approaches

See `REFLECTION.md` for the detailed discussion.

In summary:

- **Pure Python** exposes every parsing and grouping decision and is valuable for understanding the mechanics.
- **Pandas** is the most convenient for familiar exploratory analysis and concise grouping.
- **Polars** offers a strict, expression-oriented workflow that is attractive for scalable processing.

The final verification confirmed that all three implementations agreed on the core dataset-level statistics when the same preprocessing rules were applied.

## AI-assisted code review

`AI_CODE_REVIEW.md` discusses how AI-generated starter code can accelerate development but must still be checked for type handling, null semantics, standard-deviation conventions, nested fields, and grouped-analysis correctness.

## Reproducibility

A peer can clone the repository, install the dependencies, download the Task 2 CSV separately, place it at `data/facebook_political_ads.csv`, and run the four commands above to reproduce the analysis.
