import time
import random

def scrape_trendyol(page, url):
    print(f"Trendyol süreci başladı: {url}")
    
    # 1. Sayfaya Giriş ve "Tüm Yorumları Göster" Butonuna Geçiş
    try:
        # Sayfayı yükle
        page.goto(url, wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(random.randint(2000, 4000))
        
        # Pop-up temizliği
        page.keyboard.press("Escape")

        # === TÜM YORUMLARI GÖSTER BUTONU ===
        try:
            print("Trendyol: 'Tüm Yorumları Göster' butonu aranıyor...")

            selectors = [
                'a[data-testid="show-more-button"]',
                '.show-more-button',
                'a.show-more-button',
                'span:has-text("TÜM YORUMLARI GÖSTER")'
            ]

            clicked = False

            for selector in selectors:
                try:
                    locator = page.locator(selector).first

                    if locator.count() > 0:
                        locator.scroll_into_view_if_needed()
                        page.wait_for_timeout(random.randint(1000, 2500))

                        try:
                            # Normal click
                            locator.click(timeout=5000, force=True)
                        except:
                            # JS click
                            handle = locator.element_handle()
                            page.evaluate("(el) => el.click()", handle)

                        print(f"Buton tıklandı -> {selector}")
                        clicked = True
                        break

                except Exception as inner_e:
                    print(f"Selector başarısız: {selector} -> {inner_e}")

            # Eğer buton bulunamazsa direkt yorum URL'sine git
            if not clicked:
                print("Buton bulunamadı. Direkt yorum sayfasına gidiliyor...")

                if "/yorumlar" not in page.url:
                    base_url = url.split("?")[0]

                    if not base_url.endswith("/yorumlar"):
                        review_url = base_url + "/yorumlar"

                        print(f"Hedef URL: {review_url}")

                        page.goto(review_url, wait_until="networkidle")
                        page.wait_for_timeout(random.randint(2500, 4500))

        except Exception as e:
            print(f"Buton tıklama hatası: {e}")

    except Exception as e:
        print(f"Trendyol giriş/geçiş aşamasında hata: {e}")

    # 2. Sıralama İşlemleri
    try:
        page.wait_for_selector(".sort-dropdown-button", timeout=10000)

        page.click(".sort-dropdown-button")
        page.wait_for_timeout(1000)

        page.click("[data-testid='sort-option-newest']")

        print("Trendyol: Sıralama başarıyla değiştirildi.")

        page.wait_for_timeout(random.randint(2000, 4000))

    except Exception as e:
        print(f"Trendyol: Sıralama yapılamadı (Yorum yok veya buton bulunamadı).")

    # 3. Sayfayı Aşağı Kaydır
    last_count = 0

    for i in range(1, 151):

        # İnsan benzeri kaydırma: rastgele mesafe ve hız
        page.mouse.wheel(0, random.randint(1800, 3200))

        page.wait_for_timeout(random.randint(800, 1800))

        if i % 5 == 0:

            current_count = page.locator(".review, .rnr-com-w").count()

            print(f"Şu anki yorum sayısı: {current_count}")

            # Daha geç kır
            if i > 20 and current_count > 0 and current_count == last_count:
                print(f"Trendyol: Yeni yorum yüklenmiyor, döngü {i}. adımda kırıldı.")
                break

            last_count = current_count

    # 4. Veri Toplama
    cards = page.locator(".review, .rnr-com-w").all()

    data = []

    try:
        ana_satici = page.locator(".seller-name-text, .merchant-name").first.inner_text()

    except:
        ana_satici = "Trendyol Satıcısı"

    print(f"Tespit edilen {len(cards)} yorum kutusu inceleniyor...")

    for card in cards:

        try:
            metin_locator = card.locator(".review-comment, .comment-text, span, p")

            metin = ""

            for p in metin_locator.all():

                t = p.inner_text().strip()

                if len(t) > len(metin):
                    metin = t

            try:
                satici = card.locator(".seller-name-wrapper strong").inner_text()

            except:
                try:
                    satici = card.locator(".seller-name, .merchant-name").first.inner_text()

                except:
                    satici = ana_satici

            if len(metin) > 10:
                data.append((satici.strip(), metin.strip()))

        except:
            continue

    print(f"Başarılı! {len(data)} yorum ve satıcı bilgisi eşleştirildi.")

    return data