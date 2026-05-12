import { useState } from "react"
import { X, Store, Star, MessageSquare, ArrowLeft } from "lucide-react"

type Seller = {
  id: string
  name: string
  rating: number
  comments: number
  spamPercent: number
  reliability: number
  category: string
}

function CircularProgress({
  percent, color, size = 80, strokeWidth = 6, label, showAnimation = true,
}: {
  percent: number; color: string; size?: number; strokeWidth?: number; label: string; showAnimation?: boolean
}) {
  const radius = (size - strokeWidth) / 2
  const circumference = radius * 2 * Math.PI
  const offset = circumference - (percent / 100) * circumference

  return (
    <div className="flex flex-col items-center">
      <div className="relative" style={{ width: size, height: size }}>
        <svg className="transform -rotate-90" width={size} height={size}>
          <circle cx={size / 2} cy={size / 2} r={radius} stroke="#e5e7eb" strokeWidth={strokeWidth} fill="none" />
          <circle
            cx={size / 2} cy={size / 2} r={radius} stroke={color} strokeWidth={strokeWidth} fill="none"
            strokeLinecap="round" strokeDasharray={circumference}
            strokeDashoffset={showAnimation ? offset : circumference}
            className="transition-all duration-1000 ease-out"
            style={{ filter: `drop-shadow(0 0 6px ${color}80)` }}
          />
        </svg>
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-lg font-bold text-gray-800">%{percent}</span>
        </div>
      </div>
      <span className="text-xs text-gray-500 mt-2 text-center">{label}</span>
    </div>
  )
}

const marketplaces = [
  {
    id: "trendyol",
    name: "Trendyol",
    logo: (
      <div className="w-20 h-20 bg-[#F27A1A] flex items-center justify-center rounded-lg shadow-inner">
        <span className="text-white font-bold text-sm">trendyol</span>
      </div>
    ),
    color: "#F27A1A",
    description: "Türkiye'nin lider e-ticaret platformu",
  },
  {
    id: "hepsiburada",
    name: "Hepsiburada",
    logo: (
      <div className="w-20 h-20 bg-[#FF6000] flex flex-col items-center justify-center rounded-lg shadow-inner border border-white/10">
        <span className="text-white font-black text-xs leading-none">hepsi</span>
        <span className="text-white font-black text-xs leading-none">burada</span>
      </div>
    ),
    color: "#FF6000",
    description: "Türkiye'nin en köklü pazar yeri platformu",
  },
  {
    id: "n11",
    name: "n11",
    logo: (
      <div className="w-20 h-20 bg-[#603996] flex items-center justify-center rounded-lg shadow-inner">
        <span className="text-white font-bold text-xl">n11</span>
      </div>
    ),
    color: "#603996",
    description: "Türkiye'nin uğurlu pazar yeri platformu",
}
]

export default function App() {
  const [selectedMarketplace, setSelectedMarketplace] = useState<(typeof marketplaces)[0] | null>(null)
  const [showSellers, setShowSellers] = useState(false)
  const [activeDetailSeller, setActiveDetailSeller] = useState<Seller | null>(null)
  const [allSellers, setAllSellers] = useState<Seller[]>([])
  const [productLink, setProductLink] = useState("")
  const [isLoading, setIsLoading] = useState(false)

  const handleAnalyze = async () => {
    if (!productLink) {
      alert(`Lütfen bir ${selectedMarketplace?.name} ürün linki yapıştırın!`);
      return;
    }

    setIsLoading(true);
    try {
      const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';
      const response = await fetch(`${API_URL}/analiz-et`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: productLink })
      });

      const data = await response.json();

      if (data && Array.isArray(data)) {
        const formattedSellers = data.map((saticiVerisi: any) => ({
          id: Math.random().toString(),
          name: saticiVerisi?.satici_adi || "Bilinmeyen Satıcı",
          rating: Number((saticiVerisi?.guvenilirlik_skoru / 20).toFixed(1)), 
          comments: saticiVerisi?.toplam_yorum_sayisi || 0,
          spamPercent: saticiVerisi?.detay_analiz?.bot_spam_orani || 0,
          reliability: saticiVerisi?.guvenilirlik_skoru || 0,
          category: "Yapay Zeka Analiz Sonucu"
        }));

        setAllSellers(formattedSellers);
        setShowSellers(true);
      } else {
        alert("Analiz edilecek uygun veri bulunamadı.");
      }
    } catch (error) {
      console.error("Hata Detayı:", error);
      alert("Bağlantı veya Veri İşleme Hatası!");
    } finally {
      setIsLoading(false);
    }
  };

  const handleBack = () => {
    if (activeDetailSeller) setActiveDetailSeller(null);
    else setShowSellers(false);
  };

  const handleClose = () => {
    setSelectedMarketplace(null);
    setShowSellers(false);
    setAllSellers([]);
    setActiveDetailSeller(null);
    setProductLink("");
  };

  return (
  <div className="min-h-screen bg-[#F5F0E8] flex flex-col items-center justify-center p-8">
    {/* BAŞLIK BURADA GÜNCELLENDİ */}
    <h1 className="text-[#1A1A4E] font-serif text-center mb-8 leading-tight flex flex-col items-center">
        <div className="flex items-baseline justify-center">
          {/* MARKETPLACE Kısmı */}
          <span className="flex items-baseline">
            <span className="text-5xl md:text-6xl italic leading-none">M</span>
            <span className="text-xl md:text-2xl tracking-[0.3em] font-bold ml-1">ARKETPLACE</span>
          </span>

          <span className="mx-4">&nbsp;</span>

          {/* ANALYSIS Kısmı */}
          <span className="flex items-baseline">
            <span className="text-5xl md:text-6xl italic leading-none">A</span>
            <span className="text-xl md:text-2xl tracking-[0.3em] font-bold ml-1">NALYSIS</span>
          </span>
        </div>

        {/* Yeni Eklenen Alt Başlık */}
        <div className="mt-4 flex items-center justify-center gap-3 w-full">
          <div className="h-[1px] w-8 md:w-12 bg-[#1A1A4E]/20 hidden sm:block"></div>
          <span className="text-base md:text-xl font-light tracking-[0.25em] text-gray-500 italic uppercase whitespace-nowrap">
            AND RECOMMENDATION SYSTEM
          </span>
          <div className="h-[1px] w-8 md:w-12 bg-[#1A1A4E]/20 hidden sm:block"></div>
        </div>
      </h1>

      <p className="text-[#1A1A4E] text-sm md:text-base tracking-wider mb-12 uppercase">
        Lütfen analiz etmek istediğiniz platformu seçin
      </p>

      <div className="flex flex-wrap gap-8 justify-center items-center">
        {marketplaces.map((marketplace) => (
          <button
            key={marketplace.id}
            onClick={() => setSelectedMarketplace(marketplace)}
            className="transform transition-all duration-300 hover:scale-110 hover:shadow-2xl rounded-lg focus:outline-none"
          >
            {marketplace.logo}
          </button>
        ))}
      </div>

      {selectedMarketplace && (
        <div className="fixed inset-0 z-50 flex items-center justify-center transition-all duration-300" onClick={handleClose}>
          <div className="absolute inset-0 bg-black/60 backdrop-blur-sm"></div>

          <div
            className={`relative bg-white rounded-2xl shadow-2xl p-8 mx-4 transform transition-all duration-300 ${
              showSellers ? "max-w-3xl w-full max-h-[85vh] overflow-y-auto" : "max-w-md w-full"
            }`}
            onClick={(e) => e.stopPropagation()}
          >
            <div className="absolute top-4 right-4 flex gap-2">
              {showSellers && (
                <button onClick={handleBack} className="p-2 rounded-full hover:bg-gray-100">
                  <ArrowLeft className="w-5 h-5 text-gray-500" />
                </button>
              )}
              <button onClick={handleClose} className="p-2 rounded-full hover:bg-gray-100">
                <X className="w-5 h-5 text-gray-500" />
              </button>
            </div>

            {!showSellers ? (
              <div className="flex flex-col items-center text-center">
                <div className="mb-6 transform scale-150">{selectedMarketplace.logo}</div>
                <h2 className="text-2xl font-bold mb-2" style={{ color: selectedMarketplace.color }}>{selectedMarketplace.name}</h2>
                <p className="text-gray-600 mb-6">{selectedMarketplace.description}</p>

                <div className="w-full mb-6 text-left">
                  <label className="block text-sm font-medium text-gray-700 mb-2">Ürün Linki</label>
                  <div className="relative">
                    <input
                      type="url"
                      value={productLink}
                      onChange={(e) => setProductLink(e.target.value)}
                      placeholder={`${selectedMarketplace.name} ürün linkini yapıştırın...`}
                      className="w-full pl-4 pr-4 py-3 border-2 border-gray-200 rounded-lg focus:outline-none transition-colors"
                      style={{ borderColor: productLink ? selectedMarketplace.color : '#e5e7eb' }}
                    />
                  </div>
                </div>

                <button
                  onClick={handleAnalyze}
                  disabled={isLoading}
                  className="w-full py-3 rounded-lg text-white font-semibold transition-all disabled:opacity-50"
                  style={{ backgroundColor: selectedMarketplace.color }}
                >
                  {isLoading ? "Yapay Zeka Analiz Ediyor..." : "Analiz Et"}
                </button>
              </div>
            ) : (
              <div className="w-full">
                {!activeDetailSeller ? (
                  <div className="space-y-3 animate-in fade-in slide-in-from-bottom-4">
                    <h2 className="text-xl font-bold mb-4 flex items-center gap-2 text-gray-800">
                      <Store className="w-6 h-6" style={{ color: selectedMarketplace.color }} /> {selectedMarketplace.name} Satıcılar
                    </h2>
                    {allSellers.map((seller) => (
                    <div 
                      key={seller.id} 
                      onClick={() => setActiveDetailSeller(seller)}
                      className="bg-white rounded-xl p-4 shadow-sm border border-gray-100 flex items-center justify-between hover:border-gray-300 cursor-pointer group"
                      style={{ borderLeft: `4px solid ${selectedMarketplace.color}` }}
                    >
                      <div className="flex items-center gap-4">
                        <div 
                          className="w-12 h-12 rounded-full text-white flex items-center justify-center font-bold text-lg"
                          style={{ backgroundColor: selectedMarketplace.color }}
                        >
                          {seller.name.charAt(0)}
                        </div>
                        <div>
                          <h3 className="font-bold text-gray-800 group-hover:text-gray-600">{seller.name}</h3>
                          <p className="text-xs text-gray-500">{seller.category}</p>
                        </div>
                      </div>

                      {/* SAĞ TARAF: Puan, Yorum ve Güven Skoru */}
                      <div className="flex items-center gap-4 md:gap-6">
                        {/* Yıldız Puanı */}
                        <div className="flex items-center gap-1 text-sm font-medium text-gray-700">
                          <Star className="w-4 h-4 text-yellow-500 fill-current" /> 
                          {seller.rating}
                        </div>

                        {/* YENİ EKLENEN: Yorum Sayısı */}
                        <div className="flex items-center gap-1 text-sm font-medium text-gray-500">
                          <MessageSquare className="w-4 h-4 text-gray-400" />
                          {seller.comments.toLocaleString('tr-TR')}
                        </div>

                        {/* Güven Oranı (Sarı-Bej Arka Planlı) */}
                        <div 
                          className="px-3 py-1 rounded-full font-bold text-sm"
                          style={{ 
                            backgroundColor: '#FEF9C3', // Görseldeki açık sarı tonu
                            color: '#854D0E'           // Görseldeki koyu kahve/sarı yazı tonu
                          }}
                        >
                          %{seller.reliability}
                        </div>
                      </div>
                    </div>
                  ))}
                  </div>
                ) : (
                  <div className="animate-in zoom-in-95 duration-300">
                    <button onClick={() => setActiveDetailSeller(null)} className="flex items-center gap-2 text-sm text-gray-500 mb-6"><ArrowLeft className="w-4 h-4" /> Geri</button>
                    <div className="flex items-center gap-4 mb-8">
                      <div 
                        className="w-16 h-16 rounded-full text-white flex items-center justify-center font-bold text-2xl"
                        style={{ backgroundColor: selectedMarketplace.color }}
                      >
                        {activeDetailSeller.name.charAt(0)}
                      </div>
                      <div><h2 className="text-2xl font-bold">{activeDetailSeller.name}</h2><p className="text-gray-500">{activeDetailSeller.category}</p></div>
                    </div>
                    <div className="grid grid-cols-3 gap-6 mb-8 text-center bg-gray-50 p-4 rounded-xl">
                      <div><div className="font-bold text-xl">{activeDetailSeller.rating}</div><div className="text-xs text-gray-400">Puan</div></div>
                      <div><div className="font-bold text-xl">{activeDetailSeller.comments}</div><div className="text-xs text-gray-400">Yorum</div></div>
                      <div><div className="font-bold text-xl">%{activeDetailSeller.reliability}</div><div className="text-xs text-gray-400">Güven</div></div>
                    </div>
                    <div className="grid grid-cols-3 gap-4 mb-8">
                      <CircularProgress percent={activeDetailSeller.reliability} color="#22c55e" label="Güven" size={90} />
                      <CircularProgress percent={activeDetailSeller.spamPercent} color="#ef4444" label="Bot" size={90} />
                      <CircularProgress percent={100 - activeDetailSeller.spamPercent} color={selectedMarketplace.color} label="Gerçek" size={90} />
                    </div>
                    <button 
                       className="w-full py-4 text-white rounded-xl font-bold shadow-lg transition-transform active:scale-95"
                       style={{ backgroundColor: selectedMarketplace.color }}
                    >
                      Raporu İndir
                    </button>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}