"""Task 02 - equivalent descriptive statistics and grouped analysis using Pandas."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
import pandas as pd

MISSING = {"", "na", "n/a", "null", "none", "nan", "missing", "-"}

def clean_text_series(s: pd.Series) -> pd.Series:
    x = s.astype("string").str.strip()
    return x.mask(x.str.lower().isin(MISSING))

def numeric_series(s: pd.Series) -> pd.Series:
    x = clean_text_series(s).str.replace(",", "", regex=False).str.replace("$", "", regex=False).str.replace("%", "", regex=False)
    x = x.str.replace(r"^\((.*)\)$", r"-\1", regex=True)
    return pd.to_numeric(x, errors="coerce")

def infer_numeric(s: pd.Series, threshold=0.90) -> bool:
    x = clean_text_series(s).dropna()
    if x.empty: return False
    return numeric_series(x).notna().mean() >= threshold

def summarize_column(s: pd.Series) -> dict:
    x = clean_text_series(s)
    non = x.dropna()
    out = {"count": int(non.size), "missing": int(x.isna().sum())}
    if infer_numeric(s):
        n = numeric_series(s).dropna()
        out.update({"type":"numeric","numeric_count":int(n.size),"mean":float(n.mean()) if len(n) else None,
                    "min":float(n.min()) if len(n) else None,"max":float(n.max()) if len(n) else None,
                    "std":float(n.std(ddof=1)) if len(n)>1 else (0.0 if len(n)==1 else None),
                    "median":float(n.median()) if len(n) else None})
    else:
        vc = non.value_counts(dropna=True)
        out.update({"type":"categorical","unique":int(non.nunique(dropna=True)),
                    "mode":str(vc.index[0]) if len(vc) else None,"mode_frequency":int(vc.iloc[0]) if len(vc) else 0,
                    "top5":[[str(k),int(v)] for k,v in vc.head(5).items()]})
    return out

def summarize_df(df: pd.DataFrame) -> dict:
    return {"row_count":int(len(df)),"column_count":int(len(df.columns)),"columns":{c:summarize_column(df[c]) for c in df.columns}}

def main():
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument("data_path",type=Path); ap.add_argument("--output-dir",type=Path,default=Path("outputs")); args=ap.parse_args()
    args.output_dir.mkdir(parents=True,exist_ok=True)
    df=pd.read_csv(args.data_path,dtype=str,keep_default_na=False,encoding="utf-8-sig")
    print("Shape:",df.shape); print("\nDtypes:\n",df.dtypes); print("\nDataFrame.info():"); df.info()
    print("\nPandas describe(include='all'):\n",df.describe(include="all").transpose())
    missing=pd.DataFrame({"missing_count":[int(clean_text_series(df[c]).isna().sum()) for c in df.columns] },index=df.columns)
    missing["missing_pct"]=(missing["missing_count"]/len(df)*100 if len(df) else 0)
    print("\nMissing values:\n",missing)
    for c in df.columns:
        if not infer_numeric(df[c]):
            _=clean_text_series(df[c]).value_counts(dropna=True)
            _=clean_text_series(df[c]).nunique(dropna=True)
    summary=summarize_df(df)
    (args.output_dir/"pandas_dataset_summary.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding="utf-8")
    if "page_id" in df.columns:
        g=df.groupby("page_id",dropna=False).size().sort_values(ascending=False)
        g.rename("row_count").to_csv(args.output_dir/"pandas_page_id_counts.csv")
        print("\nTop page_id groups:\n",g.head(20))
    if {"page_id","ad_id"}.issubset(df.columns):
        pairs=df.groupby(["page_id","ad_id"],dropna=False).size().sort_values(ascending=False)
        pairs.rename("row_count").to_csv(args.output_dir/"pandas_page_id_ad_id_counts.csv")
        print(f"\npage_id/ad_id pairs: {len(pairs):,}; duplicated pairs: {(pairs>1).sum():,}")
    print(f"\nOutputs written to {args.output_dir}")
if __name__=="__main__": main()
