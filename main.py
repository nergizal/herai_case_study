import sys
from typing import Optional, List
from src.data_loader import load_devices
from src.analyzer import run_device_analysis_pipeline
from src.api_client import fetch_first_five_posts
from src.presenter import display_local_analysis

DEFAULT_JSON_PATH = "data/devices.json"

def main(argv: Optional[List[str]] = None) -> int:
    """
    Uygulamanın ana giriş noktası.
    Başarılı durumlarda 0, kritik yerel hatalarda 1 döndürür.
    """
    if argv is None:
        argv = sys.argv

    file_path = argv[1] if len(argv) > 1 else DEFAULT_JSON_PATH
    
    # 1. Yerel Veri Okuma ve İşleme (Kritik Katman)
    try:
        raw_devices = load_devices(file_path)
        pipeline_res = run_device_analysis_pipeline(raw_devices)
    except (FileNotFoundError, ValueError) as e:
        print(f"\n[X] Kritik Hata: {e}\n", file=sys.stderr)
        return 1  # Çıkış kodu 1 (İşletim sistemine hatayı bildirir)
    except Exception as e:
        print(f"\n[X] Beklenmeyen Sistem Hatası: {e}\n", file=sys.stderr)
        return 1

    # 2. API Bağlantısı (İzole Katman - API çökse bile sistem 0 ile çıkar)
    api_posts = None
    api_error = None
    try:
        api_posts = fetch_first_five_posts()
    except RuntimeError as e:
        api_error = str(e)

    # 3. Konsol Ekranına Çıktı Verme
    display_local_analysis(
        active_devices=pipeline_res["active_devices"],
        critical_devices=pipeline_res["critical_devices"],
        average_score=pipeline_res["avg_score"],
        warnings=pipeline_res["warnings"],
        api_posts=api_posts,
        api_error=api_error
    )

    return 0  # Çıkış kodu 0 (Başarılı)

if __name__ == "__main__":
    sys.exit(main())