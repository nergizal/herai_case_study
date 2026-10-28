from typing import List, Dict, Any, Optional
from src.analyzer import CRITICAL_THRESHOLD

def display_local_analysis(
    active_devices: List[Dict[str, Any]], 
    critical_devices: List[Dict[str, Any]], 
    average_score: Optional[float],
    warnings: Optional[List[str]] = None,
    api_posts: Optional[List[Dict[str, Any]]] = None,
    api_error: Optional[str] = None
) -> None:
    """Yerel veri analizi ve API sonuçlarını konsola yazdırır."""
    
    print("\n" + "=" * 45)
    print("      HERAI STUDIOS - CIHAZ ANALIZ RAPORU")
    print("=" * 45)

    if warnings:
        print("\n[UYARILAR VE DOĞRULAMA HATALARI]")
        for w in warnings:
            print(f"  -> {w}")

    print("\n[TÜM AKTİF CİHAZLAR]")
    if not active_devices:
        print("  -> Aktif cihaz bulunmamaktadır.")
    else:
        for d in active_devices:
            status_tag = "[KRİTİK]" if d["threat_score"] >= CRITICAL_THRESHOLD else "[NORMAL]"
            print(f"  -> ID #{d.get('id', '?')}: {d.get('device_name', '?')} - Skor: {d['threat_score']} {status_tag}")

    print(f"\n[KRİTİK CİHAZLAR (Skor >= {CRITICAL_THRESHOLD})]")
    if not critical_devices:
        print("  -> Kritik seviyede aktif cihaz yok.")
    else:
        for d in critical_devices:
            print(f"  -> ID #{d.get('id', '?')}: {d.get('device_name', '?')} (Skor: {d['threat_score']})")

    print("\n[ÖZET İSTATİSTİK]")
    if average_score is not None:
        print(f"  -> Aktif Cihaz Ortalama Tehdit Skoru: {average_score:.2f}")
    else:
        print("  -> Aktif cihaz olmadığı için ortalama hesaplanamadı.")

    print("\n[HARİCİ API DUYURULARI (JSONPlaceholder - İlk 5)]")
    if api_error:
        print(f"   API Hatası: {api_error}")
        print("  (Yerel analiz başarıyla tamamlandı.)")
    elif api_posts:
        for post in api_posts:
            print(f"  [#{post.get('id', '?')}] {post.get('title', '?')}")
    else:
        print("  -> Gösterilecek API kaydı bulunamadı.")
        
    print("=" * 45 + "\n")