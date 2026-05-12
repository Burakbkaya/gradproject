# Canlıya Alma Rehberi (Render & Vercel)

Projenizdeki gerekli kod değişikliklerini ve Playwright kurulum dosyasını (`render-build.sh`) sizin için oluşturdum. 

Aşağıdaki adımları sırasıyla takip ederek uygulamanızı canlıya alabilirsiniz.

## 1. Kodları GitHub'a Yükleme

Hem backend hem de frontend projelerinizi GitHub'a yüklemeniz gerekiyor. Bunu iki ayrı depo (repository) olarak yapmanız işinizi kolaylaştırır.

### Backend'i GitHub'a Yükleme:
1. GitHub'da `guven-backend` (veya istediğiniz bir isim) adında **yeni bir depo** oluşturun.
2. Projenizin ana dizininde (`C:\gradproject`) bir terminal açın ve şu komutları girin:
   ```bash
   git init
   git add .
   git commit -m "Ilk yukleme"
   git branch -M main
   git remote add origin https://github.com/KULLANICI_ADINIZ/guven-backend.git
   git push -u origin main
   ```

### Frontend'i GitHub'a Yükleme:
1. GitHub'da `guven-frontend` adında **yeni bir depo** oluşturun.
2. `C:\gradproject\guven-frontend` klasörüne gidin, yeni bir terminal açın ve şu komutları girin:
   ```bash
   git init
   git add .
   git commit -m "Frontend ilk yukleme"
   git branch -M main
   git remote add origin https://github.com/KULLANICI_ADINIZ/guven-frontend.git
   git push -u origin main
   ```

---

## 2. Backend'i Render Üzerinde Canlıya Alma

> [!WARNING]
> Render'ın ücretsiz planı **512MB RAM** sınırına sahiptir. Playwright ve Transformers (yapay zeka modeli) çok fazla bellek tüketebilir. Eğer Render kurulum sırasında veya analiz anında `Memory Limit Exceeded` (Out of Memory) hatası verirse daha yüksek bir plana geçmeniz veya farklı bir sunucu (örneğin DigitalOcean) kullanmanız gerekebilir.

1. [Render.com](https://dashboard.render.com/) adresine gidin ve hesabınıza giriş yapın.
2. Sağ üstten **New +** butonuna tıklayın ve **Web Service** seçin.
3. GitHub hesabınızı bağlayın ve oluşturduğunuz `guven-backend` reposunu seçin.
4. Karşınıza çıkan ekranda şu ayarları yapın:
   - **Name:** Projeniz için bir isim (örn: `guven-api`)
   - **Runtime:** `Python 3`
   - **Build Command:** `./render-build.sh`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Sayfanın alt kısımlarına doğru **Advanced** bölümünü genişletin.
6. **Add Environment Variable** (Ortam Değişkeni Ekle) butonuna tıklayın ve şunu ekleyin:
   - **Key:** `PYTHON_VERSION`
   - **Value:** `3.11.0` (Sisteminizdeki Python sürümü)
7. Sayfanın en altındaki **Create Web Service** butonuna tıklayın.

*Kurulum (Build) işlemi birkaç dakika sürebilir. Başarılı olduğunda sol üstte `https://guven-api.onrender.com` gibi bir link göreceksiniz. Bu linki kopyalayın, Vercel adımında lazım olacak.*

---

## 3. Frontend'i Vercel Üzerinde Canlıya Alma

1. [Vercel.com](https://vercel.com/) adresine gidin ve GitHub hesabınızla giriş yapın.
2. **Add New...** > **Project** seçeneğine tıklayın.
3. Çıkan listede `guven-frontend` reposunun yanındaki **Import** butonuna tıklayın.
4. Proje ayarları sayfasında:
   - **Framework Preset:** `Vite` olarak otomatik seçilmiş olmalıdır. Değilse seçin.
5. **Environment Variables** bölümünü genişletin ve Render'dan aldığınız API linkini buraya yapıştırın:
   - **Name:** `VITE_API_URL`
   - **Value:** Render uygulamanızın linki (örn: `https://guven-api.onrender.com` - **Sonunda `/` (slash) OLMASIN!**)
   - `Add` butonuna tıklayarak değişkeni kaydedin.
6. Son olarak **Deploy** butonuna tıklayın.

Kısa süre içinde Vercel sitenizi yayına alacak ve size bir ziyaret linki verecektir. Tüm işlemler bu kadar!
