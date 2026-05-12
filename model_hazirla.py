from transformers import AutoTokenizer, AutoModelForSequenceClassification
import os

model_adi = "savasy/bert-base-turkish-sentiment-cased"
kayit_yolu = "./yerel_model"

print("🚀 Operasyon Başladı: Yapay zeka modeli indiriliyor...")

try:
    # İnternetten çek
    tokenizer = AutoTokenizer.from_pretrained(model_adi)
    model = AutoModelForSequenceClassification.from_pretrained(model_adi)

    # Klasör yoksa oluştur
    if not os.path.exists(kayit_yolu):
        os.makedirs(kayit_yolu)

    # Bilgisayarına (proje klasörüne) fiziksel olarak kaydet
    tokenizer.save_pretrained(kayit_yolu)
    model.save_pretrained(kayit_yolu)

    print(f"✅ BAŞARILI: Model '{kayit_yolu}' klasörüne hapsedildi.")
    print("Artık sunumda internet olmasa bile yapay zeka çalışacak!")
except Exception as e:
    print(f"❌ HATA: Model indirilemedi. İnternetini kontrol et: {e}")