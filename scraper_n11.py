import time
import random

def scrape_n11(page, url):
    print(f"n11 süreci başladı: {url}")
    
    # Zaman aşımını derin tarama için biraz artırdık (90 saniye)
    page.goto(url, wait_until="networkidle", timeout=90000)
    
    try:
        print("n11: Tüm yorumlar sayfasına geçiliyor...")
        page.click(".product-reviews__link", timeout=7000)
        page.wait_for_timeout(random.randint(2000, 4000))
    except Exception as e:
        print("n11: Yorumlar sekmesi zaten açık olabilir veya buton bulunamadı.")

    # --- AKILLI KAYDIRMA VE DERİN TARAMA BAŞLANGICI ---
    last_count = 0
    no_change_count = 0
    max_scroll = 50  # Yaklaşık 500 yorum için 50 kez kaydırma yeterli olacaktır
    
    print("n11: Derin ve dinamik tarama başlatıldı...")

    for i in range(max_scroll):
        page.keyboard.press("PageDown")
        
        # İnsan benzeri bekleme süresi
        page.wait_for_timeout(random.randint(800, 1800)) 
        
        # Sayfada kaç yorum kutusu var kontrol et
        current_count = page.locator(".review-card").count()
        
        if current_count > last_count:
            # Yeni yorumlar geldi, süreci devam ettir
            print(f"Yeni veriler yüklendi... Mevcut sayı: {current_count}")
            last_count = current_count
            no_change_count = 0 
        else:
            # Yeni veri gelmedi, internet yavaş olabilir. Ekstradan 2.5 saniye bekle.
            print("Yeni veri bekleniyor, bağlantı yavaş olabilir...")
            page.wait_for_timeout(random.randint(2000, 3500))
            no_change_count += 1
            
            # n11 özel: Bazen "Daha Fazla Göster" butonuna basmak gerekebilir
            try:
                more_button = page.locator("text='Daha Fazla Göster'")
                if more_button.is_visible():
                    more_button.click()
                    print("n11: 'Daha Fazla Göster' butonuna tıklandı.")
                    page.wait_for_timeout(random.randint(1500, 3000))
                    no_change_count = 0 # Butona basıldıysa sayacı sıfırla
            except:
                pass

        # Eğer 4 kez üst üste (yaklaşık 8-10 saniye) yeni veri gelmezse döngüyü kır
        if no_change_count >= 4:
            print("Sayfa sonuna ulaşıldı veya veri akışı durdu.")
            break

    # --- VERİ TOPLAMA ---
    cards = page.locator(".review-card").all()
    data = []
    
    try:
        ana_satici = page.locator(".shop-name, .seller-name").first.inner_text()
    except:
        ana_satici = "n11 Satıcısı"

    print(f"Analiz edilecek toplam yorum kutusu: {len(cards)}")

    for card in cards:
        try:
            metin = card.locator(".card-detail__contents").inner_text().strip()
            try:
                satici = card.locator(".card-detail__seller_nickname span").first.inner_text().strip()
            except:
                satici = ana_satici
                
            if len(metin) > 5:
                data.append((satici, metin))
        except:
            continue
            
    print(f"n11: Toplam {len(data)} yorum başarıyla toplandı.")
    return data