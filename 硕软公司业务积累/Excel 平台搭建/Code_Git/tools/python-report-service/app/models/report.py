from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, field_validator


class ReportEntry(BaseModel):
    signature: str | None = Field(default=None, description="短信签名")
    companyName: str = Field(..., min_length=1, description="公司名称")


class BatchReportRequest(BaseModel):
    templateType: str = Field(..., description="模板类型")
    source: str = Field(default="", description="来源")
    entries: list[ReportEntry] = Field(..., min_length=1, description="批量条目")
    sharedPayload: dict[str, Any] = Field(
        default_factory=dict, description="模板共享参数"
    )

    @field_validator("templateType")
    @classmethod
    def validate_template_type(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("templateType 不能为空")
        return value


class BatchReportResponse(BaseModel):
    taskName: str
    templateType: str
    fileName: str
    resultUrl: str
    imageCount: int
    imageFiles: list[str]
    docxFiles: list[str]
    pdfFiles: list[str]


class TemplateSampleResponse(BaseModel):
    templateType: str
    sample: dict[str, Any]
