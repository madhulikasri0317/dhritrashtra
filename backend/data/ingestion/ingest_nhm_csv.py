"""
Ingest National Health Mission style CSV disease records.
"""

from pathlib import Path
import pandas as pd


REQUIRED_COLUMNS = {
    'district': 'district',
    'disease': 'disease',
    'cases': 'cases',
    'date': 'date',
}


def ingest_nhm_csv(input_path, output_path):
    df = pd.read_csv(input_path)

    for source_col, target_col in REQUIRED_COLUMNS.items():
        if source_col not in df.columns:
            raise ValueError(f'Missing required column: {source_col}')
        if source_col != target_col:
            df[target_col] = df[source_col]

    cleaned = df[list(REQUIRED_COLUMNS.values())].copy()
    cleaned['cases'] = pd.to_numeric(cleaned['cases'], errors='coerce').fillna(0).astype(int)
    cleaned['date'] = pd.to_datetime(cleaned['date'], errors='coerce').dt.date
    cleaned = cleaned.dropna(subset=['date'])

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(output_path, index=False)
    return cleaned


if __name__ == '__main__':
    input_file = Path('data/raw/nhm_weekly_cases.csv')
    output_file = Path('data/processed/nhm_cleaned_cases.csv')
    data = ingest_nhm_csv(input_file, output_file)
    print(f'NHM ingestion complete. Rows: {len(data)}')
