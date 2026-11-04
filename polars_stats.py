"""Task 02 - equivalent descriptive statistics and grouped analysis using Polars."""
from __future__ import annotations
import argparse, json, math, re
from collections import Counter
from pathlib import Path
from statistics import median
import polars as pl

MISSING={"","na","n/a","null","none","nan","missing","-"}

def is_missing(v): return v is None or str(v).strip().lower() in MISSING

def clean_number(v):
    if is_missing(v): return None
    s=str(v).strip().replace(",","").replace("$","").replace("%","")
    s=re.sub(r"^\((.*)\)$",r"-\1",s)
    try:return float(s)
    except ValueError:return None

def sample_std(vals):
    if len(vals)<=1:return 0.0 if vals else None
    m=sum(vals)/len(vals); return math.sqrt(sum((x-m)**2 for x in vals)/(len(vals)-1))

def summarize_values(values):
    non=[str(v).strip() for v in values if not is_missing(v)]
    parsed=[clean_number(v) for v in non]
    numeric=bool(non) and sum(v is not None for v in parsed)/len(non)>=0.90
    out={"count":len(non),"missing":len(values)-len(non)}
    if numeric:
        nums=[v for v in parsed if v is not None]
        out.update({"type":"numeric","numeric_count":len(nums),"mean":sum(nums)/len(nums) if nums else None,
                    "min":min(nums) if nums else None,"max":max(nums) if nums else None,
                    "std":sample_std(nums),"median":median(nums) if nums else None})
    else:
        c=Counter(non); mode,freq=c.most_common(1)[0] if c else (None,0)
        out.update({"type":"categorical","unique":len(c),"mode":mode,"mode_frequency":freq,"top5":c.most_common(5)})
    return out

def main():
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument("data_path",type=Path); ap.add_argument("--output-dir",type=Path,default=Path("outputs")); args=ap.parse_args()
    args.output_dir.mkdir(parents=True,exist_ok=True)
    # infer_schema_length=0 keeps CSV values as strings so preprocessing matches the other scripts.
    df=pl.read_csv(args.data_path,infer_schema_length=0,encoding="utf8-lossy",null_values=list(MISSING),ignore_errors=True)
    print("Shape:",df.shape); print("Schema:",df.schema); print("\nPolars describe():\n",df.describe())
    summary={"row_count":df.height,"column_count":df.width,"columns":{}}
    for c in df.columns:
        vals=df.get_column(c).to_list(); summary["columns"][c]=summarize_values(vals)
        if summary["columns"][c]["type"]=="categorical":
            _=df.get_column(c).value_counts(); _=df.get_column(c).n_unique()
    (args.output_dir/"polars_dataset_summary.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding="utf-8")
    if "page_id" in df.columns:
        g=df.group_by("page_id").len().sort("len",descending=True)
        g.write_csv(args.output_dir/"polars_page_id_counts.csv"); print("\nTop page_id groups:\n",g.head(20))
    if {"page_id","ad_id"}.issubset(set(df.columns)):
        pairs=df.group_by(["page_id","ad_id"]).len().sort("len",descending=True)
        pairs.write_csv(args.output_dir/"polars_page_id_ad_id_counts.csv")
        dup=pairs.filter(pl.col("len")>1).height
        print(f"\npage_id/ad_id pairs: {pairs.height:,}; duplicated pairs: {dup:,}")
    print(f"\nOutputs written to {args.output_dir}")
if __name__=="__main__": main()
