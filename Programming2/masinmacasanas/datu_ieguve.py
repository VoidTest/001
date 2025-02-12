import requests
import os
import re
import csv
import time
from bs4 import BeautifulSoup as bs

# For the price prediction (machine learning) part:
import pandas as pd
from sklearn.linear_model import LinearRegression

# Base URL and file directories
URL = "https://www.ss.lv/lv/transport/cars/today-5/sell/"
DATI = "masinmacisanas/dati/"
LAPAS = "masinmacisanas/lapas/"

# Ensure directories exist
os.makedirs(DATI, exist_ok=True)
os.makedirs(LAPAS, exist_ok=True)

def saglaba_lapu(url, nosaukums):
    try:
        iegutais = requests.get(url)
        print(f"Fetching {url}: {iegutais.status_code}")
        if iegutais.status_code == 200:
            with open(nosaukums, "w", encoding="utf-8") as f:
                f.write(iegutais.text)
    except Exception as e:
        print(f"Error saving page {url}: {e}")
    return

def saglaba_visas_lapas(skaits):
    """Fetch and save multiple pages."""
    for i in range(1, skaits + 1):
        lapas_nosaukums = f"{LAPAS}lapa{i}.html"
        saglaba_lapu(f"{URL}page{i}.html", lapas_nosaukums)
        time.sleep(0.5)
    return

def dabut_info(lapa):
    dati = []
    try:
        with open(lapa, "r", encoding="utf-8") as f:
            html = f.read()
        zupa = bs(html, "html.parser")
        galvenais = zupa.find(id="page_main")
        tabulas = galvenais.find_all('table')
        rindas = tabulas[2].find_all('tr')
        for rinda in rindas[1:]:
            lauki = rinda.find_all('td')
            if len(lauki) < 8:
                print(f"Skipping unusual row in {lapa}")
                continue
            
            # Model text: contains brand and model details.
            modelis_text = lauki[2].text.strip()
            marka = modelis_text.split()[0] if modelis_text else ""
            
            # Year (gads): extract a 4-digit number.
            gads_text = lauki[3].text.strip()
            gads_match = re.search(r'\d{4}', gads_text)
            gads = int(gads_match.group()) if gads_match else None
            
            # Engine information (motors): extract displacement and determine engine type.
            motors_text = lauki[4].text.strip().lower()
            tilpums_match = re.search(r'(\d+(?:[.,]\d+)?)', motors_text)
            tilpums = float(tilpums_match.group().replace(',', '.')) if tilpums_match else None
            if "benz" in motors_text:
                dzineja_tips = "benzīns"
            elif "dīzel" in motors_text:
                dzineja_tips = "dīzelis"
            elif "elektro" in motors_text:
                dzineja_tips = "elektro"
            elif "hibr" in motors_text:
                dzineja_tips = "hibrīds"
            else:
                dzineja_tips = "nav zināms"
            
            # Mileage (nobraukums): extract digits, remove spaces.
            nobraukums_text = lauki[5].text.strip()
            nobraukums_match = re.search(r'([\d\s]+)', nobraukums_text)
            nobraukums = int(nobraukums_match.group(1).replace(" ", "")) if nobraukums_match else None
            
            # Price (cena): extract digits.
            cena_text = lauki[6].text.strip()
            cena_match = re.search(r'([\d\s]+)', cena_text)
            cena = int(cena_match.group(1).replace(" ", "")) if cena_match else None
            
            auto = {
                'marka': marka,
                'gads': gads,
                'tilpums': tilpums,
                'dzineja_tips': dzineja_tips,
                'nobraukums': nobraukums,
                'cena': cena,
                'sludinajuma_saite': f"https://www.ss.lv{lauki[1].find('a')['href']}" if lauki[1].find('a') else "",
                'bilde': lauki[1].find('img')['src'] if lauki[1].find('img') else "Nav bildes",
            }
            dati.append(auto)
    except Exception as e:
        print(f"Error parsing {lapa}: {e}")
    return dati

def dabut_info_daudz(skaits):
    visi_dati = []
    for i in range(1, skaits + 1):
        lapa = f"{LAPAS}lapa{i}.html"
        dati = dabut_info(lapa)
        visi_dati += dati
    return visi_dati

def saglaba_datus_separati(dati):
    data_by_engine = {}
    for auto in dati:
        etype = auto.get('dzineja_tips', 'nav_zinams')
        if etype not in data_by_engine:
            data_by_engine[etype] = []
        data_by_engine[etype].append(auto)
    
    for etype, autos in data_by_engine.items():
        # Normalize engine type string for filename (remove diacritics and spaces)
        etype_filename = etype.replace("ī", "i").replace(" ", "_")
        filename = os.path.join(DATI, f"sslv_{etype_filename}.csv")
        try:
            with open(filename, "w", encoding="utf-8", newline='') as f:
                fieldnames = ['marka', 'gads', 'tilpums', 'dzineja_tips', 'nobraukums', 'cena', 'sludinajuma_saite', 'bilde']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for auto in autos:
                    writer.writerow(auto)
            print(f"Data saved to {filename}")
        except Exception as e:
            print(f"Error saving data for engine type {etype}: {e}")

def predict_price(nobraukums, gads, tilpums, dzineja_tips=None):
    if dzineja_tips:
        etype_filename = dzineja_tips.lower().replace("ī", "i").replace(" ", "_")
        file_path = os.path.join(DATI, f"sslv_{etype_filename}.csv")
        if not os.path.exists(file_path):
            print(f"Data file for engine type '{dzineja_tips}' not found.")
            return None
        df = pd.read_csv(file_path)
    else:
        files = [f for f in os.listdir(DATI) if f.startswith("sslv_") and f.endswith(".csv")]
        if not files:
            print("No data files found in the DATI directory.")
            return None
        df_list = [pd.read_csv(os.path.join(DATI, file)) for file in files]
        df = pd.concat(df_list, ignore_index=True)
    
    # Ensure numeric conversion for features and target.
    for col in ["nobraukums", "gads", "tilpums", "cena"]:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df.dropna(subset=["nobraukums", "gads", "tilpums", "cena"], inplace=True)
    
    if df.empty:
        print("No valid data available for training.")
        return None
    
    X = df[["nobraukums", "gads", "tilpums"]]
    y = df["cena"]
    
    model = LinearRegression()
    model.fit(X, y)
    
    input_data = [[nobraukums, gads, tilpums]]
    predicted = model.predict(input_data)[0]
    print(f"Predicted price: {predicted:.2f}")
    return predicted

# Main execution
if __name__ == "__main__":
    lapu_skaits = 20  # Adjust the number of pages to scrape
    saglaba_visas_lapas(lapu_skaits)      # Fetch pages from ss.lv
    info = dabut_info_daudz(lapu_skaits)    # Extract data from saved pages
    saglaba_datus_separati(info)            # Save data to separate CSV files by engine type

    # Example usage of the price prediction function:
    # Predict the price for a car with 100000 km mileage, from year 2015,
    # engine displacement of 2.0 (liters) and engine type "benzīns".
    predict_price(nobraukums=100000, gads=2015, tilpums=2.0, dzineja_tips="benzīns")
