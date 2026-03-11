"""
Ingest Integrated Disease Surveillance Programme style JSON records.
"""

from pathlib import Path
import json
import pandas as pd


def ingest_idsp_json(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as file:
        payload = json.load(file)

    records = payload if isinstance(payload, list) else payload.get('records', [])
    df = pd.DataFrame(records)

    column_map = {
        'district_name': 'district',
        'disease_name': 'disease',
        'reported_cases': 'cases',
        'report_date': 'date',
    }

    for source_col, target_col in column_map.items():
        if source_col in df.columns:
            df[target_col] = df[source_col]

    required = ['district', 'disease', 'cases', 'date']
    for required_col in required:
        if required_col not in df.columns:
            raise ValueError(f'Missing required field in JSON feed: {required_col}')

    cleaned = df[required].copy()
    cleaned['cases'] = pd.to_numeric(cleaned['cases'], errors='coerce').fillna(0).astype(int)
    cleaned['date'] = pd.to_datetime(cleaned['date'], errors='coerce').dt.date
    cleaned = cleaned.dropna(subset=['date'])

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(output_path, index=False)
    return cleaned


if __name__ == '__main__':
    input_file = Path('data/raw/idsp_alerts.json')
    output_file = Path('data/processed/idsp_cleaned_cases.csv')
    data = ingest_idsp_json(input_file, output_file)
    print(f'IDSP ingestion complete. Rows: {len(data)}')
