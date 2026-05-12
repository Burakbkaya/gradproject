import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from playwright.sync_api import sync_playwright
from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from scraper_trendyol import scrape_trendyol
from scraper_hepsiburada import scrape_hepsiburada
from scraper_n11 import scrape_n11

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

print("Model yükleniyor...")
duygu_analizi = pipeline("sentiment-analysis", model="savasy/bert-base-turkish-sentiment-cased", local_files_only=True)

class AnalizIstegi(BaseModel):
    url: str

def bot_filtresi(yorumlar):
    # 1. Aşama: 15 karakterden kısa yorumları en başta ele
    yorumlar = [y for y in yorumlar if len(y) >= 10]
    
    if len(yorumlar) < 5: 
        return yorumlar
    
    # 2. Aşama: Benzerlik analizi (0.95 eşiği)
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(yorumlar)
    benzerlik = cosine_similarity(tfidf)
    
    temiz = []
    silinen = set()
    for i in range(len(benzerlik)):
        if i in silinen: continue
        temiz.append(yorumlar[i])
        for j in range(i + 1, len(benzerlik)):
            # Akıllı botları yakalamak için 0.95 eşiği kullanıyoruz
            if benzerlik[i][j] > 0.95: 
                silinen.add(j)
    return temiz

@app.post("/analiz-et")
def analiz_et(istek: AnalizIstegi):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, channel="chrome")
        page = browser.new_page()
        
        try:
            url = istek.url.lower()
            if "trendyol.com" in url:
                raw_data = scrape_trendyol(page, url) 
            elif "hepsiburada.com" in url:
                raw_data = scrape_hepsiburada(page, url)
            elif "n11.com" in url:
                raw_data = scrape_n11(page, url)    
            else:
                browser.close()
                return {"hata": "Desteklenmeyen platform."}

            if not raw_data:
                browser.close()
                return {"hata": "Yorum bulunamadı."}

            # Gruplandırma
            satici_gruplari = {}
            for satici, metin in raw_data:
                if satici not in satici_gruplari: 
                    satici_gruplari[satici] = []
                satici_gruplari[satici].append(metin)

            tum_raporlar = []
            for satici, yorumlar in satici_gruplari.items():
                organik = bot_filtresi(yorumlar)
                negatif = 0
                
                # Duygu Analizi (BERT)
                for y in organik:
                    res = duygu_analizi(y[:512])[0]
                    if res['label'] == 'NEGATIVE' or (res['label'] == 'POSITIVE' and res['score'] < 0.6):
                        negatif += 1
                
                # 1. Temel Başarı Skoru (Sadece organik içerik kalitesi)
                temel_skor = ((len(organik) - negatif) / len(organik)) * 100 if organik else 0
                
                # 2. Spam Oranı Hesaplama
                toplam_y = len(yorumlar)
                spam_orani = (toplam_y - len(organik)) / toplam_y if toplam_y > 0 else 0
                
                # 3. Kademeli Ceza Sistemi (İstediğin terazi mantığı)
                if spam_orani < 0.05:
                    # %3 spam -> %99.7 gibi çok hafif ceza
                    ceza_orani = spam_orani * 0.1
                elif spam_orani < 0.10:
                    # %5-%10 arası -> Orta ceza
                    ceza_orani = spam_orani * 0.3
                else:
                    # %14 spam -> %93 gibi sert ceza (Spamın yarısı kadar kırıyoruz)
                    ceza_orani = spam_orani * 0.5
                
                # 4. Final Skoru Hesapla
                final_skor = int(max(0, temel_skor * (1 - ceza_orani)))

                tum_raporlar.append({
                    "id": f"s_{len(tum_raporlar)}",
                    "satici_adi": satici,
                    "toplam_yorum_sayisi": toplam_y,
                    "guvenilirlik_skoru": final_skor,
                    "detay_analiz": {
                        "bot_spam_orani": int(spam_orani * 100),
                        "gercek_yorum_orani": int((len(organik) / toplam_y) * 100) if toplam_y > 0 else 0
                    }
                })

            browser.close()
            return tum_raporlar

        except Exception as e:
            if 'browser' in locals(): browser.close()
            return {"hata": str(e)}