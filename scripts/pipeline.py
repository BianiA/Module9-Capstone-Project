"""Reproducible customer purchase analytics pipeline. Run from any directory."""
from pathlib import Path
import pandas as pd
import sqlite3, logging, time, json
ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/'data/raw/dataset.csv'; CLEAN=ROOT/'data/cleaned'; LOGS=ROOT/'logs'; DASH=ROOT/'dashboards'
for folder in (CLEAN,LOGS,DASH):folder.mkdir(parents=True,exist_ok=True)
logging.basicConfig(filename=LOGS/'pipeline.log',level=logging.INFO,format='%(asctime)s %(levelname)s %(message)s',force=True)
def run():
 start=time.perf_counter();logging.info('START pipeline')
 try:
  df=pd.read_csv(RAW);assert len(df)>0,'Empty source';logging.info('Ingested %d rows',len(df))
  df.to_csv(CLEAN/'dataset_storage.csv',index=False)
  df.columns=df.columns.str.strip().str.lower().str.replace(' ','_',regex=False)
  df=df.drop_duplicates(subset=['customerid']).dropna(subset=['customerid','name','age','purchaseamount','country','date']).copy()
  df['date']=pd.to_datetime(df['date'],errors='coerce');df['age']=pd.to_numeric(df['age'],errors='coerce');df['purchaseamount']=pd.to_numeric(df['purchaseamount'],errors='coerce')
  df=df.dropna().query('age >= 18 and age <= 100 and purchaseamount > 0 and purchaseamount <= 5000').copy()
  df['age']=df['age'].astype(int);df['customerid']=df['customerid'].astype(int);df['date']=df['date'].dt.strftime('%Y-%m-%d')
  df.to_csv(CLEAN/'dataset_cleaned.csv',index=False)
  df['age_group']=pd.cut(df.age,bins=[0,18,35,50,100],labels=['Teen','Young Adult','Adult','Senior'],include_lowest=True).astype(str)
  df['purchase_category']=pd.cut(df.purchaseamount,bins=[0,100,500,1000,5000],labels=['Low','Medium','High','VIP'],include_lowest=True).astype(str)
  df['purchase_year']=pd.to_datetime(df.date).dt.year
  df.to_csv(CLEAN/'dataset_enriched.csv',index=False)
  checks={'no_nulls':bool(df.notna().all().all()),'unique_customer_ids':bool(df.customerid.is_unique),'age_range':bool(df.age.between(18,100).all()),'purchase_range':bool(df.purchaseamount.between(0.01,5000).all()),'valid_categories':bool((df.purchase_category!='nan').all()),'row_count':int(len(df))}
  (LOGS/'validation.json').write_text(json.dumps(checks,indent=2));logging.info('Validation: %s',checks)
  assert all(v for k,v in checks.items() if k!='row_count'),'Quality checks failed'
  df.to_csv(CLEAN/'dataset_final.csv',index=False)
  with sqlite3.connect(ROOT/'capstone.db') as con:
   df.to_sql('customer_purchases',con,if_exists='replace',index=False)
   assert con.execute('SELECT COUNT(*) FROM customer_purchases').fetchone()[0]==len(df)
  import matplotlib
  matplotlib.use('Agg')
  import matplotlib.pyplot as plt
  by_country=df.groupby('country').purchaseamount.sum().sort_values(ascending=False)
  fig,ax=plt.subplots(figsize=(9,5));by_country.plot.bar(ax=ax);ax.set(title='Total purchase amount by country',xlabel='Country',ylabel='Purchase amount (synthetic units)');fig.tight_layout();fig.savefig(DASH/'revenue_by_country.png',dpi=150);plt.close(fig)
  fig,ax=plt.subplots(figsize=(8,5));df.purchaseamount.hist(bins=30,ax=ax);ax.set(title='Purchase amount distribution',xlabel='Purchase amount',ylabel='Number of purchases');fig.tight_layout();fig.savefig(DASH/'purchase_distribution.png',dpi=150);plt.close(fig)
  summary=df.groupby('age_group',observed=True).agg(purchases=('customerid','count'),total_purchase_amount=('purchaseamount','sum'),average_purchase_amount=('purchaseamount','mean')).reset_index();summary.to_csv(DASH/'age_group_summary.csv',index=False)
  logging.info('SUCCESS rows=%d duration_seconds=%.2f',len(df),time.perf_counter()-start)
  print('SUCCESS:',len(df),'rows; outputs in data/cleaned, dashboards, logs and capstone.db')
 except Exception:
  logging.exception('FAILED pipeline');raise
if __name__=='__main__':run()
