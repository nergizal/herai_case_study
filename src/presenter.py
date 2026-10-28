from typing import List, Dict, Any, Optional

def display_local_analysis(
    active_devices: List[Dict[str, Any]],
    critical_devices: List[Dict[str, Any]],
    average_score: Optional[float] = None,
    warnings: Optional[List[str]] = None,
    api_posts: Optional[List[Dict[str, Any]]] = None,
    api_error: Optional[str] = None
) -> None:
    if warnings is None:
        warnings = []

    print("\n" + "="*45)
    print("      HERAI STUDIOS - CIHAZ ANALIZ RAPORU")
    print("="*45)
    
    if warnings:
        print("\n[UYARILAR / AYIKLANAN KAYITLAR]:")
        for w in warnings:
            print(f"  - {w}")
            
    print(f"\n[+] Aktif Cihaz Sayısı: {len(active_devices)}")
    print("[+] Aktif Cihaz Listesi:")
    for d in active_devices:
        is_crit = " [KRİTİK]" if d in critical_devices else ""
        print(f"    - {d.get('device_name')} (Skor: {d.get('threat_score')}){is_crit}")
        
    print(f"\n[+] Kritik Cihaz Sayısı (Skor >= 50): {len(critical_devices)}")
    if isinstance(average_score, (int, float)):
        avg_str = f"{average_score:.2f}"
    elif average_score is not None:
        avg_str = f"{average_score}"
    else:
        avg_str = "N/A"
    print(f"[+] Aktif Cihazlar Ortalama Tehdit Skoru: {avg_str}")
    
    print("\n" + "-"*50)
    print("      HARİCİ API ENTEGRASYONU (JSONPlaceholder)")
    print("-"*50)
    if api_error:
        print(f"[!] API Uyarı/Hata: {api_error} (Yerel analiz etkilenmedi)")
    elif api_posts:
        print("[+] İlk 5 Gönderi Başlığı:")
        for post in api_posts:
            print(f"    ({post['id']}) {post['title']}")
    print("="*50 + "\n")