import os
from datetime import datetime
import pytest

def pytest_configure(config):
    reports_dir = os.path.join(os.path.dirname(__file__), "reports")
    os.makedirs(reports_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_filename = f"test_report_{timestamp}.htm"
    report_path = os.path.join(reports_dir, report_filename)
    
    config.option.htmlpath = report_path
    config.option.self_contained_html = True