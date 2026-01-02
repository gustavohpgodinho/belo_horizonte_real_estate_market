from curl_cffi import requests as cureq
import pandas as pd
import io

def list_files(dataset_id):
    url = f"https://ckan.pbh.gov.br/api/3/action/package_show?id={dataset_id}"
    # scraper = cloudscraper.create_scraper()  # burlar o Cloudflare
    # response = scraper.get(url)
    response = cureq.get(url, impersonate = "chrome", timeout = 300)

    if response.status_code == 200:
        data = response.json()
        resources = data['result']['resources']

        obj_files = []
        for resource in resources:
            df_file = pd.DataFrame(
                data = {"name": resource["name"], "url": resource["url"], "id": resource["id"], "format": resource["format"]},
                index = [0])
            obj_files.append(df_file)

        df_files = pd.concat(objs = obj_files, ignore_index = True).reset_index(drop = True)
        return df_files
    else:
        raise Exception(f"API ERROR: {response.status_code} - {response.text}")

def get_csv_file(url, dataset = None, separate = ";", verbose = 1):
    if url == "":
        return None

    # headers = {
    #     "User-Agent": "Mozilla/5.0",
    #     "Referer": "https://ckan.pbh.gov.br"
    # }

    # scraper = cloudscraper.create_scraper()
    # response = scraper.get(url, headers = headers)
    response = cureq.get(url, impersonate = "chrome", timeout = 300)

    if response.status_code == 200:
        # Get the binary content
        csv_data = io.BytesIO(response.content)
        
        # read the csv file using pandas
        df = pd.DataFrame()
        try:
            df = pd.read_csv(csv_data, sep = separate, encoding = 'utf-8')
            if verbose: print(f"{url}: successful downloaded data!")
        except Exception as e:
            # Try another encoding if the first fail
            csv_data.seek(0)
            df = pd.read_csv(csv_data, sep = separate, encoding = 'latin-1')
            if verbose: print(f"{url}: successful downloaded data (latin-1)!")
    else:
        print(f"ERROR TO DOWNLOAD {url}: {response.status_code}")
    df.columns = [item.replace("çã", "ca").replace("ï»¿", "").replace("(", "").replace(")", "") for item in df.columns]
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.lower()
    df.columns = [item.replace(" ", "_") for item in df.columns]
    df.columns = [item.replace("_de_", "_") for item in df.columns]
    df.columns = [item.replace('"', "") for item in df.columns]

    if dataset == "itbi":
        df = df.rename(columns = {"zona_uso": "zona_uso_itbi", "data_quitacao": "data_quitacao_transacao"})
    
    df = df.assign(urlfile = url)

    return df

