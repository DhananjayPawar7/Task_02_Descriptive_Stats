# Findings

## Dataset profile

The completed Task 2 run analyzed **246,745 Facebook political-ad records across 41 columns**. The dataset contained **4,475 unique `page_id` values** and **246,745 unique `ad_id` values**, meaning every ad identifier was unique in the file.

The grouped analysis showed that activity was highly concentrated. The largest `page_id` contributed **55,503 records (22.5%)**, followed by page groups with **23,988 (9.7%)**, **14,822 (6.0%)**, **10,461 (4.2%)**, and **9,851 (4.0%)** records. This concentration would be difficult to see from whole-dataset descriptive statistics alone.

Grouping by the combination of `page_id` and `ad_id` produced **246,745 pairs, all with row count 1**. There were therefore **zero duplicated page/ad pairs**. In this dataset, the pair-level grouping functions primarily as a useful uniqueness and data-quality check rather than as a way to identify repeated ad records.

## Spending, impressions, and audience size

The numeric summaries reveal strongly skewed distributions.

- **Estimated spend** had a mean of about **1,061.29** but a median of only **49**, with values ranging from **49** to **474,999**.
- **Estimated impressions** had a mean of about **45,601.53** but a median of **3,499**, with a maximum of **1,000,000**.
- **Estimated audience size** had a mean of about **556,462.86** and a median of **300,000**, ranging from **0** to **1,000,001**.

The large gaps between the means and medians for spend and impressions indicate that a relatively small number of high-value records pull the averages upward. For this reason, medians are especially important when describing a typical ad record.

## Timing and advertiser patterns

The most common ad-creation date was **October 27, 2024**, with **8,619 records**. Other highly represented dates included October 28, October 26, October 23, and October 25. The concentration in late October is consistent with intensified advertising activity near the end of the election cycle, although this descriptive analysis does not attempt to establish causality.

The `bylines` field had **1,009 missing values** and **3,786 unique non-missing values**. The most frequent bylines were:

1. **HARRIS FOR PRESIDENT** — 49,788 records
2. **HARRIS VICTORY FUND** — 32,612 records
3. **BIDEN VICTORY FUND** — 15,539 records
4. **DONALD J. TRUMP FOR PRESIDENT 2024, INC.** — 15,112 records
5. **Trump National Committee JFC** — 7,279 records

These counts show that a relatively small number of campaign organizations account for a substantial share of records while the dataset still contains thousands of distinct bylines.

## Platform distribution

The dominant publisher-platform combination was **Facebook + Instagram**, appearing in **214,434 records (86.9%)**. Facebook-only records accounted for **23,259 (9.4%)**, while Instagram-only records accounted for **8,395 (3.4%)**. Other combinations involving Audience Network or Messenger were comparatively rare.

This indicates that most ads in the dataset were distributed across both of Meta's major social platforms rather than being restricted to only one.

## Candidate mentions

The `illuminating_mentions` field contained **278 unique values**. The most common value was an empty list, appearing in **73,205 records (29.7%)**. Among explicitly named candidates or figures, the most common values were:

- `['Donald Trump']` — 53,182 records
- `['Kamala Harris']` — 31,019 records
- `['President Trump']` — 14,580 records
- `['Joe Biden']` — 14,059 records

Because some references to the same person appear under different labels, these values should not automatically be added together without first normalizing the naming conventions.

## Message and topic indicators

Several binary indicator fields also reveal the composition of the advertising messages. Their means can be interpreted as approximate proportions of records flagged for each category:

- Call-to-action message: **57.3%**
- Advocacy message: **54.9%**
- Issue message: **38.2%**
- Attack message: **27.2%**
- Fundraising call-to-action subtype: **22.8%**
- Incivility indicator: **18.8%**
- Voting call-to-action subtype: **14.4%**
- Economy topic: **12.2%**
- Health topic: **10.9%**
- Women's issues topic: **8.1%**
- Scam indicator: **7.2%**
- Election-integrity/truth indicator: **5.0%**

These categories are not necessarily mutually exclusive, so the percentages should be interpreted independently rather than as parts of a single distribution.

## Data-quality observations

Most columns used in this analysis were complete. The clearest missing-value issue was `bylines`, which was missing in **1,009 records**. Several fields such as `delivery_by_region`, `demographic_distribution`, `publisher_platforms`, and `illuminating_mentions` contain serialized dictionary/list-like values. They are therefore treated as categorical strings in the general descriptive-statistics scripts rather than incorrectly forcing them into scalar numeric columns.

The `currency` column was overwhelmingly USD: **246,599 of 246,745 records (99.94%)**. A small number of records used other currencies such as INR, GBP, EUR, and PKR. This is a useful reminder that even a U.S.-election-focused dataset can contain exceptional values that should not be silently assumed away.

## Main analytical takeaway

The major lesson from Task 2 is that **grouped analysis reveals structure that whole-dataset summaries hide**. The overall dataset is large, but records are unevenly distributed among pages and campaign organizations. At the same time, the `page_id/ad_id` grouping confirms that each ad record is unique at that level.

The three implementations—Pure Python, Pandas, and Polars—produced matching core dataset-level statistics when the same cleaning rules were applied. This confirms that the analytical results are driven by the data and preprocessing decisions rather than by the choice of library.
