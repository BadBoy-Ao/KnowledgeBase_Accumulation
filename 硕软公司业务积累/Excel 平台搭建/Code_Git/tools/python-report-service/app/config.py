from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BASE_DIR / "storage"
IMAGES_DIR = STORAGE_DIR / "images"
ZIPS_DIR = STORAGE_DIR / "zips"
SEALS_DIR = STORAGE_DIR / "seals"
WORK_DIR = Path(os.getenv("REPORT_WORK_DIR", "C:/temp/python-report-service-work"))
DOCX_DIR = WORK_DIR / "docx"
PDF_DIR = WORK_DIR / "pdf"

JAVA_SHORT_LINK_TEMPLATE = (
    BASE_DIR.parent
    / "sms"
    / "sms-parent"
    / "sms-admin"
    / "src"
    / "main"
    / "resources"
    / "template"
    / "report"
    / "shandon"
    / "shandong_mobile_short_link_reporting.docx"
)
JAVA_REPORT_TEMPLATE_ROOT = JAVA_SHORT_LINK_TEMPLATE.parent.parent

APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = int(os.getenv("APP_PORT", "8000"))
APP_BASE_URL = os.getenv("APP_BASE_URL", f"http://127.0.0.1:{APP_PORT}")
SEAL_API_BASE_URL = os.getenv("SEAL_API_BASE_URL", "http://59.36.76.123:3301")

DEFAULT_FONT_CANDIDATES = [
    "C:/Windows/Fonts/simfang.ttf",
    "C:/Windows/Fonts/FZFangSong-Z02S.ttf",
    "C:/Windows/Fonts/simsun.ttc",
    "C:/Windows/Fonts/msyh.ttc",
    "C:/Windows/Fonts/simhei.ttf",
    "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
]


for directory in (
    STORAGE_DIR,
    IMAGES_DIR,
    ZIPS_DIR,
    SEALS_DIR,
    WORK_DIR,
    DOCX_DIR,
    PDF_DIR,
):
    directory.mkdir(parents=True, exist_ok=True)
