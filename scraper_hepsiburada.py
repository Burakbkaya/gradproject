import time
import random

def scrape_hepsiburada(page, url):
    print(f"Hepsiburada süreci başladı: {url}")
    
    # 1. Giriş ve Hazırlık
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(random.randint(1500, 3000))
        
        review_link = page.locator('[data-test-id="has-review"] a').first
        if review_link.is_visible():
            review_link.click()
            page.wait_for_timeout(random.randint(2000, 4000))
        elif "/yorumlari" not in url:
            hedef_url = url.split("-p-")[0] + "-yorumlari"
            page.goto(hedef_url, wait_until="networkidle")
    except Exception as e:
        print(f"Hepsiburada giriş hatası: {e}")

    # 2. Sıralama
    try:
        page.click('[class*="hermes-Sort-module-VANnZ3"]', timeout=5000)
        page.wait_for_timeout(random.randint(800, 1500))
        page.locator('text="En yeni değerlendirme"').first.click(force=True)
        page.wait_for_timeout(random.randint(2000, 4000))
    except:
        pass

    all_data = []
    seen_texts = set()
    current_page = 1 
    
    # 3. Sayfaları Gezerek Veri Toplama
    while True:
        print(f"Hepsiburada: Sayfa {current_page} taranıyor... (Mevcut: {len(all_data)})")
        
        # Sayfayı kaydır ve yorumların yüklenmesini bekle
        for _ in range(6):
            page.mouse.wheel(0, random.randint(700, 1300))
            page.wait_for_timeout(random.randint(400, 900))

        # Kartların DOM'da belirmesini bekle
        try:
            page.wait_for_selector('[class*="ReviewCard-module-dY_oaYMIo"]', timeout=5000)
        except:
            print("Hepsiburada: Bu sayfada yorum kartı bulunamadı, bitiriliyor.")
            break

        cards = page.locator('[class*="ReviewCard-module-dY_oaYMIo"]').all()
        
        for card in cards:
            try:
                metin_locator = card.locator('[class*="ReviewCard-module-KaU17Bb"]').first
                if metin_locator.count() > 0:
                    metin = metin_locator.inner_text().strip()
                    if len(metin) >= 15 and metin not in seen_texts:
                        try:
                            satici = card.locator('span[role="button"]').first.inner_text().strip()
                        except:
                            satici = "Hepsiburada Satıcısı"
                        all_data.append((satici, metin))
                        seen_texts.add(metin)
            except:
                continue

        # --- 4. KRİTİK DURMA NOKTASI (SENİN İSTEDİĞİN) ---
        target_page = current_page + 1
        # Bir sonraki sayfa rakamı (8, 9, 10...) var mı?
        next_page_btn = page.locator(f'div[class*="paginationBarHolder"] span:text-is("{target_page}")').first
        
        # EĞER BİR SONRAKİ RAKAM YOKSA DUR
        if not next_page_btn.is_visible(timeout=4000):
            print(f"Hepsiburada: {target_page}. sayfa rakamı bulunamadı. Tarama son sayfada (Sayfa {current_page}) bitti.")
            break
        
        # Rakam varsa tıkla
        print(f"Hepsiburada: {target_page}. sayfaya geçiliyor...")
        next_page_btn.scroll_into_view_if_needed()
        page.wait_for_timeout(random.randint(300, 700))
        next_page_btn.click(force=True)
        
        current_page = target_page
        page.wait_for_timeout(random.randint(3000, 5000)) # Yeni sayfanın yüklenmesi için zaman tanı
        page.keyboard.press("Home")

    # --- 5. DEĞERLENDİRME ÇIKTI ---
    print(f"\n--- TARAMA TAMAMLANDI ---")
    print(f"Toplam Çekilen Yorum: {len(all_data)}")
    return all_data