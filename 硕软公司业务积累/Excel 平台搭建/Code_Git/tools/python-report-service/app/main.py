from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.config import APP_BASE_URL, APP_HOST, APP_PORT, BASE_DIR, STORAGE_DIR
from app.models.report import BatchReportRequest
from app.routers.report import router as report_router
from app.services.render_service import ReportRenderService


app = FastAPI(title="Python Report Service", version="1.0.0")
app.include_router(report_router)
app.mount("/storage", StaticFiles(directory=str(STORAGE_DIR)), name="storage")
app.mount("/ui", StaticFiles(directory=str(BASE_DIR / "web"), html=True), name="ui")


@app.get("/")
def home() -> RedirectResponse:
    return RedirectResponse(url="/ui/")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


def run_local_demo() -> None:
    request = BatchReportRequest(
        templateType="shandong_short_link_reporting",
        source="山东移动",
        entries=[{"signature": "吃得放心", "companyName": "阖家欢乐公司"}],
        sharedPayload={"linkList": ["t.cn", "http://a.b.com", "c.d.cn"]},
    )
    service = ReportRenderService()
    result = service.generate_zip(request)

    print(f"taskName: {result.task_name}")
    print(f"templateType: {result.template_type}")
    print(f"zipFile: {result.zip_path}")
    for index, docx_path in enumerate(result.docx_paths, start=1):
        print(f"docx{index}: {docx_path}")
    for index, pdf_path in enumerate(result.pdf_paths, start=1):
        print(f"pdf{index}: {pdf_path}")
    for index, image_path in enumerate(result.image_paths, start=1):
        print(f"image{index}: {image_path}")
    print(f"resultUrl: {APP_BASE_URL.rstrip('/')}/storage/zips/{result.file_name}")


if __name__ == "__main__":
    run_local_demo()
