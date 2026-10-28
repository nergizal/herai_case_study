import sys
from pathlib import Path
from typing import Optional, List

sys.path.append(str(Path(__file__).resolve().parent))

from src.data_loader import load_devices
from src.analyzer import run_device_analysis_pipeline
from src.api_client import fetch_first_five_posts
from src.presenter import display_local_analysis
from src.exceptions import DeviceAnalysisError

DEFAULT_DATA_PATH = "data/devices.json"

def main(argv: Optional[List[str]] = None) -> int:
    if argv is None:
        argv = sys.argv

    file_path = argv[1] if len(argv) > 1 else DEFAULT_DATA_PATH
    
    try:
        raw_devices = load_devices(file_path)
        pipeline_res = run_device_analysis_pipeline(raw_devices)
    except DeviceAnalysisError as e:
        print(f"\n[X] Analiz Kritik Hatası: {e}\n", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"\n[X] Analiz Kritik Hatası: {e}\n", file=sys.stderr)
        return 1

    api_posts = None
    api_error = None
    try:
        api_posts = fetch_first_five_posts()
    except Exception as e:
        api_error = str(e)

    display_local_analysis(
        active_devices=pipeline_res["active_devices"],
        critical_devices=pipeline_res["critical_devices"],
        average_score=pipeline_res["avg_score"],
        warnings=pipeline_res["warnings"],
        api_posts=api_posts,
        api_error=api_error
    )

    return 0

if __name__ == "__main__":
    sys.exit(main())