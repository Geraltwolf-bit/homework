import json
import pandas as pd 

def extract_data(filename: str = 'file_name'):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    results = []
    
    for group in data.get('groups', []):
        for work in group.get('works', []):
            result = {
                'year': None,
                'title': None,
                'doi': None,
                'eid': None
            }
            
            #get year
            pub_date = work.get('publicationDate', {})
            if isinstance(pub_date, dict):
                result['year'] = pub_date.get('year')
                
            #get title
            title = work.get('title', {})
            if isinstance(title, dict):
                result['title'] = title.get('value')
                
            #get doi and eid
            for ext_id in work.get('workExternalIdentifiers', []):
                ext_type = ext_id.get('externalIdentifierType', {})
                ext_value = ext_id.get('externalIdentifierId', {})
                
                if isinstance(ext_value, dict):
                    value = ext_value.get('value')
                    if ext_type['value'] == 'doi' and value:
                        result['doi'] = value
                    elif ext_type['value'] == 'eid' and value:
                        result['eid'] = value
                        
            if any(result.values()):
                results.append(result)
                
    df = pd.DataFrame(results)
    
    df.to_csv('result.csv', index = False)
    
    return df

df = extract_data('data/allWorks_20260210.json')
print(df.head())