# Critical Review of AI-Generated Starter Code

Task 2 asks whether coding assistants can provide useful starter code for descriptive statistics in Pure Python, Pandas, and Polars. My conclusion is **yes, but only as scaffolding**.

AI-generated templates are usually strong at the obvious API calls: `csv.DictReader`, `DataFrame.describe()`, `value_counts()`, Pandas `groupby()`, and Polars `group_by()`. They can also quickly create command-line argument handling and reusable functions.

The weaknesses appear at the boundaries of the data. A generic AI answer may:

- trust automatic type inference without checking mixed values;
- use population standard deviation in one script and sample standard deviation in another;
- treat `$1,200`, percentages, or parenthesized negatives inconsistently;
- assume nested/list-like strings are ordinary categories;
- silently drop null grouping keys;
- compare outputs that were produced under different preprocessing rules.

For this repository, the important improvement over a generic starter template was to define common preprocessing assumptions first and then implement those assumptions separately in all three approaches. That makes the comparison about the tools rather than about accidental differences in cleaning.

The broader lesson is that AI can save time on syntax, but the analyst still has to define what counts as missing, numeric, comparable, and meaningful.
