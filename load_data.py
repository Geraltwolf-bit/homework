import os
from dotenv import load_dotenv
import json
from datetime import datetime
import requests

load_dotenv()

def download_data():
    url = os.getenv('url')
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        os.makedirs('data', exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d')
        filename = f"data/allWorks_{timestamp}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(response.json(), f, indent=2, ensure_ascii=False)
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error downloading data: {e}")
        return None
            
if __name__=='__main__':
    download_data()