"""
Fetch government health datasets from configured URLs.
"""

from pathlib import Path
import requests


DATA_SOURCES = {
    'nhm_weekly_cases.csv': 'https://example.gov.in/health/nhm_weekly_cases.csv',
    'idsp_alerts.json': 'https://example.gov.in/health/idsp_alerts.json',
}


def fetch_file(url, destination):
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    Path(destination).parent.mkdir(parents=True, exist_ok=True)
    with open(destination, 'wb') as file:
        file.write(response.content)


def fetch_all(data_sources=None, output_dir='data/raw'):
    sources = data_sources or DATA_SOURCES
    downloaded = []

    for filename, url in sources.items():
        output_path = Path(output_dir) / filename
        fetch_file(url, output_path)
        downloaded.append(str(output_path))

    return downloaded


if __name__ == '__main__':
    files = fetch_all()
    print('Downloaded files:')
    for item in files:
        print('-', item)
