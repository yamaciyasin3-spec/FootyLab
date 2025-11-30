# data_fetcher.py - Canlı skorlar + son 10 yıl
import requests
import pandas as pd
from datetime import datetime, timedelta
from config import BASE_URL, HEADERS

# Güncel takım ID'leri (2025)
TAKIM_ID = {
    "fenerbahce": 500, "fenerbahçe": 500, "fener": 500,
    "galatasaray": 501, "gs": 501,
    "besiktas": 502, "beşiktaş": 502, "bjk": 502,
    "trabzonspor": 503
}

def takımı_bul(takim_adi):
    takim_adi = takim_adi.lower().replace("ı", "i").replace("ş", "s")
    for anahtar, id in TAKIM_ID.items():
        if anahtar in takim_adi:
            return id, anahtar.title()
    return 500, "Fenerbahçe"  # Varsayılan

def maclari_cek(team_id, team_name, yil=10):
    url = f"{BASE_URL}/teams/{team_id}/matches"
    params = {"dateFrom": (datetime.now() - timedelta(days=yil*365)).strftime('%Y-%m-%d')}
    try:
        response = requests.get(url, headers=HEADERS, params=params)
        data = response.json()
        return data.get('matches', [])
    except:
        return []

def df_olustur(maclar, takim_adi):
    liste = []
    for m in maclar:
        if m['status'] != 'FINISHED':
            continue
        home = m['homeTeam']['name']
        away = m['awayTeam']['name']
        ev_sahibi = home.lower() == takim_adi.lower()
        rakip = away if ev_sahibi else home
        bizim_gol = m['score']['fullTime']['home'] if ev_sahibi else m['score']['fullTime']['away']
        rakip_gol = m['score']['fullTime']['away'] if ev_sahibi else m['score']['fullTime']['home']
        if bizim_gol is None:
            continue
        sonuc = "Galibiyet" if bizim_gol > rakip_gol else "Beraberlik" if bizim_gol == rakip_gol else "Mağlubiyet"
        liste.append({
            "Tarih": m['utcDate'][:10],
            "Rakip": rakip,
            "Skor": f"{bizim_gol}-{rakip_gol}",
            "Sonuç": sonuc,
            "Ev/Deplasman": "Ev" if ev_sahibi else "Deplasman",
            "Lig": m['competition']['name']
        })
    return pd.DataFrame(liste)