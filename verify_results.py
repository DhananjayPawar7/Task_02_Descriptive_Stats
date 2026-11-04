"""Compare core dataset-level JSON summaries produced by the three Task 02 scripts."""
import argparse, json, math
from pathlib import Path

def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def close(a,b,tol=1e-8):
    if a is None or b is None:return a is b
    if isinstance(a,(int,float)) and isinstance(b,(int,float)):return math.isclose(a,b,rel_tol=tol,abs_tol=tol)
    return a==b

def compare(a,b,label):
    errs=[]
    for k in ["row_count","column_count"]:
        if a[k]!=b[k]:errs.append(f"{label}: {k} differs: {a[k]} vs {b[k]}")
    if set(a["columns"])!=set(b["columns"]):errs.append(f"{label}: column names differ"); return errs
    for c in a["columns"]:
        x,y=a["columns"][c],b["columns"][c]
        for k in set(x)&set(y):
            if k=="top5":continue
            if not close(x[k],y[k]):errs.append(f"{label}: {c}.{k}: {x[k]} vs {y[k]}")
    return errs

def main():
    ap=argparse.ArgumentParser();ap.add_argument("output_dir",type=Path,nargs="?",default=Path("outputs"));args=ap.parse_args()
    p=load(args.output_dir/"pure_python_dataset_summary.json"); d=load(args.output_dir/"pandas_dataset_summary.json"); l=load(args.output_dir/"polars_dataset_summary.json")
    errs=compare(p,d,"pure vs pandas")+compare(p,l,"pure vs polars")
    if errs:
        print("FAIL"); print("\n".join(errs[:100])); raise SystemExit(1)
    print("PASS: core dataset-level statistics agree across Pure Python, Pandas, and Polars.")
if __name__=="__main__":main()
