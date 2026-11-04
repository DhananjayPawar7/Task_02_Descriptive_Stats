# Reflection — Pure Python vs. Pandas vs. Polars

## Producing identical results

The most important validation step in this task was running the same dataset through all three implementations and then using `verify_results.py` to compare their core statistics. The final verification returned **PASS**, confirming that Pure Python, Pandas, and Polars agreed on the dataset-level results.

The main challenge was not the formulas themselves. It was making sure all three approaches treated missing values, mixed types, numeric strings, and complex text fields consistently. Harmonizing those decisions was necessary before the results could be compared fairly.

## Pure Python

Pure Python required the most explicit work. Loading the CSV, recognizing missing values, converting numeric strings, computing mean and standard deviation, finding medians and modes, and creating groups all had to be implemented directly.

This approach was the most useful for understanding what the higher-level libraries do internally. For example, grouping by `page_id` required manually organizing rows into keyed structures and then summarizing each group. That made the mechanics of `groupby` much clearer.

The tradeoff is verbosity and processing time. On a dataset with **246,745 rows and 41 columns**, the Pure Python implementation required noticeably more code and patience than the DataFrame approaches.

## Pandas

Pandas was the most familiar and convenient approach for exploratory work. `describe()`, `value_counts()`, `nunique()`, and `groupby()` made both dataset-level and grouped analysis concise.

It also made it easy to inspect the structure of the dataset. However, Pandas' convenience can hide assumptions. Fields such as `delivery_by_region` and `demographic_distribution` look like dictionaries stored inside CSV cells, while `publisher_platforms` and `illuminating_mentions` look like serialized lists. Pandas can load these without difficulty, but it cannot know what analytical transformation is appropriate unless the analyst explicitly decides how to parse them.

## Polars

Polars provided a similarly concise workflow while encouraging more explicit thinking about schemas and expressions. Once the syntax was understood, `group_by()` and expression-based aggregation were straightforward.

For repeated processing of larger datasets, Polars is attractive because its design focuses on efficient columnar execution and strict typing. The learning curve was slightly higher for me than Pandas because the syntax and expression model were less familiar, but the approach becomes logical once those differences are understood.

## What grouped analysis revealed

Grouping by `page_id` exposed strong concentration. The largest page group contained **55,503 records**, or about **22.5% of the entire dataset**. The next two groups contained 23,988 and 14,822 records. This pattern was not obvious from the dataset-level row count alone.

The `page_id, ad_id` grouped analysis produced a different insight: all **246,745 observed pairs had count 1**. Rather than revealing repeated clusters, this confirmed that `ad_id` behaves as a unique row-level identifier within the file.

This illustrates why the choice of grouping keys matters. One grouping reveals concentration; another verifies uniqueness.

## Data patterns that stood out

The large differences between means and medians for spend and impressions were particularly important. Estimated spend had a mean of about **1,061** but a median of only **49**, while estimated impressions had a mean of about **45,602** and a median of **3,499**. These gaps show why relying on a mean alone would give a misleading impression of a typical record.

The dataset also showed that most records were distributed across both Facebook and Instagram, and that late-October 2024 dates were especially common. These results demonstrate how descriptive statistics can move beyond code validation and reveal substantive patterns in a political-advertising dataset.

## Which tool would I recommend to a junior analyst?

I would recommend learning the concepts in Pure Python at least once, because it exposes how parsing, missing-value handling, grouping, and aggregation actually work. For day-to-day analysis, I would then recommend Pandas because it is widely used and easy to explore interactively. I would introduce Polars next, particularly for larger datasets or workflows where performance and stricter schema behavior matter.

## AI-generated starter code

AI coding tools are useful for scaffolding repetitive code, CLI parsing, and remembering library syntax. However, they should not be trusted without testing. A generated solution can easily use different standard-deviation conventions, rely on automatic type inference, or mishandle nested string values.

This task demonstrated why validation matters. Instead of accepting code because it ran, I compared the results from all three approaches. The final **PASS** from the verification script gave stronger evidence that the implementations were consistent.

## Overall conclusion

My view of the three approaches is now more nuanced. Pure Python is best for understanding the mechanics, Pandas is highly effective for fast exploratory analysis, and Polars provides an efficient and explicit alternative for modern data workflows.

More importantly, I learned that the library is not the main determinant of correctness. The most important decisions are how the data is cleaned, how missing values are defined, how complex fields are interpreted, and whether results are independently checked.
