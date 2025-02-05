import requests
import os
from bs4 import BeautifulSoup as bs
import csv
import time

# Base URL and file directories
URL = "https://www.ss.lv/lv/transport/cars/today-5/sell/"
DATI = "masinmacasanas/dati/"
LAPAS = "masinmacasanas/lapas/"

# Ensure directories exist
os.makedirs(DATI, exist_ok=True)
os.makedirs(LAPAS, exist_ok=True)

def saglaba_lapu(url, nosaukums):
    """Fetch and save a webpage to a file."""
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
    """Extract car information from a saved webpage."""
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
            auto = {
                'modelis': lauki[2].text.strip(),
                'gads': lauki[3].text.strip(),
                'motors': lauki[4].text.strip(),
                'nobraukums': lauki[5].text.strip(),
                'cena': lauki[6].text.strip(),
                'sludinajuma_saite': f"https://www.ss.lv{lauki[1].find('a')['href']}",
                'bilde': lauki[1].find('img')['src'] if lauki[1].find('img') else "Nav bildes",
            }
            dati.append(auto)
    except Exception as e:
        print(f"Error parsing {lapa}: {e}")
    return dati

def saglaba_datus(dati):
    """Save car data to a CSV file."""
    try:
        with open(DATI + "sslv.csv", "w", encoding="utf-8", newline='') as f:
            lauku_nosaukumi = ['modelis', 'gads', 'motors', 'nobraukums', 'cena', 'sludinajuma_saite', 'bilde']
            w = csv.DictWriter(f, fieldnames=lauku_nosaukumi)
            w.writeheader()
            for auto in dati:
                w.writerow(auto)
        print(f"Data saved to {DATI+'sslv.csv'}")
    except Exception as e:
        print(f"Error saving data: {e}")
    return

def dabut_info_daudz(skaits):
    """Extract car data from multiple pages."""
    visi_dati = []
    for i in range(1, skaits + 1):
        lapa = f"{LAPAS}lapa{i}.html"
        dati = dabut_info(lapa)
        visi_dati += dati
    return visi_dati

# Main execution
if __name__ == "__main__":
    lapu_skaits = 20  # Adjust the number of pages to scrape
    saglaba_visas_lapas(lapu_skaits)  # Fetch pages
    info = dabut_info_daudz(lapu_skaits)  # Extract data
    saglaba_datus(info)  # Save data to CSV
