"""
Run a complete ingestion pipeline for government health datasets.
"""

from pathlib import Path
import pandas as pd
import schedule
import time

from ingest_nhm_csv import ingest_nhm_csv
from ingest_idsp_json import ingest_idsp_json
from fetch_government_datasets import fetch_datasets


def merge_and_export(nhm_file, idsp_file, output_file):
    nhm_df = ingest_nhm_csv(nhm_file, 'data/processed/nhm_cleaned_cases.csv')
    idsp_df = ingest_idsp_json(idsp_file, 'data/processed/idsp_cleaned_cases.csv')

    merged = pd.concat([nhm_df, idsp_df], ignore_index=True)
    merged['district'] = merged['district'].astype(str).str.strip()
    merged['disease'] = merged['disease'].astype(str).str.strip()
    merged = merged.sort_values(by=['date', 'district', 'disease'])

    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(output_file, index=False)
    return merged


def pipeline():
    print("Running ingestion pipeline")

    fetch_datasets()

    output = 'data/processed/government_disease_cases.csv'
    combined = merge_and_export(
        'data/raw/nhm_weekly_cases.csv',
        'data/raw/idsp_alerts.json',
        output,
    )

    print(f'Ingestion pipeline complete. Output: {output}. Rows: {len(combined)}')
    print("Pipeline completed")


if __name__ == '__main__':
    # Run once immediately
    pipeline()

    # Schedule to run every 6 hours
    schedule.every(6).hours.do(pipeline)

    while True:
        schedule.run_pending()
        time.sleep(1)
