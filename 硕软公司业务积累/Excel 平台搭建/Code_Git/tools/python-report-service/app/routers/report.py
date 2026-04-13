from fastapi import APIRouter, HTTPException, Request

from app.config import APP_BASE_URL
from app.models.report import (
    BatchReportRequest,
    BatchReportResponse,
    TemplateSampleResponse,
)
from app.services.render_service import ReportRenderService
from app.services.template_registry import build_beijing_samples, build_shandong_samples


router = APIRouter(prefix="/api/v1/reports", tags=["reports"])
service = ReportRenderService()
SAMPLES = {**build_shandong_samples(), **build_beijing_samples()}


@router.get("/templates")
def list_templates() -> dict[str, list[str]]:
    return {"templates": sorted(service.registry.keys())}


@router.get("/sample/{template_type}", response_model=TemplateSampleResponse)
def get_template_sample(template_type: str) -> TemplateSampleResponse:
    if template_type not in SAMPLES:
        raise HTTPException(status_code=404, detail=f"未配置示例: {template_type}")
    return TemplateSampleResponse(
        templateType=template_type, sample=SAMPLES[template_type]
    )


@router.post("/generate", response_model=BatchReportResponse)
def generate_report(
    request_body: BatchReportRequest, request: Request
) -> BatchReportResponse:
    result = service.generate_zip(request_body)
    base_url = (
        str(request.base_url).rstrip("/")
        if request.base_url
        else APP_BASE_URL.rstrip("/")
    )
    return BatchReportResponse(
        taskName=result.task_name,
        templateType=result.template_type,
        fileName=result.file_name,
        resultUrl=f"{base_url}/storage/zips/{result.file_name}",
        imageCount=len(result.image_paths),
        imageFiles=[str(path) for path in result.image_paths],
        docxFiles=[str(path) for path in result.docx_paths],
        pdfFiles=[str(path) for path in result.pdf_paths],
    )
