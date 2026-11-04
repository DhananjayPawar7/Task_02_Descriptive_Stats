"""Task 02 - descriptive statistics and grouped analysis using only Python stdlib."""
from __future__ import annotations
import argparse, csv, json, math, re
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median

MISSING = {"", "na", "n/a", "null", "none", "nan", "missing", "-"}

def is_missing(v):
    return v is None or str(v).strip().lower() in MISSING

def clean_number(v):
    if is_missing(v): return None
    s = str(v).strip().replace(",", "").replace("$", "").replace("%", "")
    s = re.sub(r"^\((.*)\)$", r"-\1", s)
    try: return float(s)
    except ValueError: return None

def sample_std(values):
    if len(values) <= 1: return 0.0 if values else None
    m = sum(values)/len(values)
    return math.sqrt(sum((x-m)**2 for x in values)/(len(values)-1))

def load_csv(path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        return rows, list(reader.fieldnames or [])

def infer_numeric(values, threshold=0.90):
    nonmissing = [v for v in values if not is_missing(v)]
    if not nonmissing: return False
    parsed = [clean_number(v) for v in nonmissing]
    return sum(v is not None for v in parsed)/len(nonmissing) >= threshold

def summarize_column(values):
    nonmissing = [str(v).strip() for v in values if not is_missing(v)]
    out = {"count": len(nonmissing), "missing": len(values)-len(nonmissing)}
    if infer_numeric(values):
        nums = [clean_number(v) for v in nonmissing]
        nums = [v for v in nums if v is not None]
        out.update({
            "type": "numeric", "numeric_count": len(nums),
            "mean": sum(nums)/len(nums) if nums else None,
            "min": min(nums) if nums else None,
            "max": max(nums) if nums else None,
            "std": sample_std(nums),
            "median": median(nums) if nums else None,
        })
    else:
        counts = Counter(nonmissing)
        mode, freq = counts.most_common(1)[0] if counts else (None, 0)
        out.update({
            "type": "categorical", "unique": len(counts),
            "mode": mode, "mode_frequency": freq,
            "top5": counts.most_common(5),
        })
    return out

def summarize_dataset(rows, columns):
    result = {"row_count": len(rows), "column_count": len(columns), "columns": {}}
    for col in columns:
        result["columns"][col] = summarize_column([r.get(col, "") for r in rows])
    return result

def write_page_group_summary(rows, columns, out_path):
    if "page_id" not in columns: return None
    grouped = defaultdict(list)
    for row in rows: grouped[row.get("page_id", "")].append(row)
    with out_path.open("w", encoding="utf-8") as f:
        for key, group_rows in sorted(grouped.items(), key=lambda kv: len(kv[1]), reverse=True):
            record = {"page_id": key, "row_count": len(group_rows), "summary": summarize_dataset(group_rows, columns)}
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return sorted(((k, len(v)) for k,v in grouped.items()), key=lambda x:x[1], reverse=True)

def write_pair_counts(rows, columns, out_path):
    if not {"page_id","ad_id"}.issubset(columns): return None
    counts = Counter((r.get("page_id", ""), r.get("ad_id", "")) for r in rows)
    with out_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f); w.writerow(["page_id","ad_id","row_count"])
        for (p,a),n in counts.most_common(): w.writerow([p,a,n])
    return counts

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("data_path", type=Path)
    ap.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = ap.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    rows, columns = load_csv(args.data_path)
    summary = summarize_dataset(rows, columns)
    (args.output_dir/"pure_python_dataset_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    page_groups = write_page_group_summary(rows, columns, args.output_dir/"pure_python_page_id_groups.jsonl")
    pair_counts = write_pair_counts(rows, columns, args.output_dir/"pure_python_page_id_ad_id_counts.csv")
    print(f"Rows: {len(rows):,} | Columns: {len(columns):,}")
    if page_groups:
        print("\nTop page_id groups:")
        for key,n in page_groups[:20]: print(f"  {key}: {n:,}")
    if pair_counts is not None:
        duplicate_pairs = sum(1 for n in pair_counts.values() if n>1)
        print(f"\npage_id/ad_id pairs: {len(pair_counts):,}; duplicated pairs: {duplicate_pairs:,}")
    print(f"\nOutputs written to {args.output_dir}")
if __name__ == "__main__": main()
