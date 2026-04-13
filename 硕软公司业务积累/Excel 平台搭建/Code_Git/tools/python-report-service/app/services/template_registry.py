from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class TemplateConfig:
    template_type: str
    task_prefix: str
    zip_prefix: str
    file_prefix: str
    template_path: Path
    required_shared_fields: tuple[str, ...]
    summary_field: str
    default_shared_payload: dict[str, Any]
    multiline_fields: tuple[str, ...]
    seal_company_field: str


def _today_text() -> str:
    today = date.today()
    return f"{today.year}年{today.month}月{today.day}日"


def build_shandong_registry(template_root: Path) -> dict[str, TemplateConfig]:
    shandong_root = template_root / "shandon"
    return {
        "shandong_short_link_reporting": TemplateConfig(
            template_type="shandong_short_link_reporting",
            task_prefix="短链报备说明",
            zip_prefix="短链报备说明",
            file_prefix="短链报备说明",
            template_path=shandong_root / "shandong_mobile_short_link_reporting.docx",
            required_shared_fields=("linkList",),
            summary_field="signature",
            default_shared_payload={"time": _today_text},
            multiline_fields=("linkList",),
            seal_company_field="companyName",
        ),
        "shandong_multi_level_domain": TemplateConfig(
            template_type="shandong_multi_level_domain",
            task_prefix="多级域名报备",
            zip_prefix="多级域名报备",
            file_prefix="多级域名报备",
            template_path=shandong_root / "shandong_mobile_multi_level_domain.docx",
            required_shared_fields=("linkList",),
            summary_field="signature",
            default_shared_payload={"time": _today_text, "businessUsage": "宣传推广"},
            multiline_fields=("linkList",),
            seal_company_field="companyName",
        ),
        "shandong_link_authorization": TemplateConfig(
            template_type="shandong_link_authorization",
            task_prefix="域名授权书",
            zip_prefix="域名授权书",
            file_prefix="域名授权书",
            template_path=shandong_root / "shandong_mobile_link_authorization.docx",
            required_shared_fields=("linkList", "linkCompanyName"),
            summary_field="companyName",
            default_shared_payload={
                "time": _today_text,
                "businessUsage": "宣传推广",
                "authStartTime": _today_text,
                "authEndTime": lambda: f"{date.today().year + 3}年{date.today().month}月{date.today().day}日",
            },
            multiline_fields=("linkList",),
            seal_company_field="linkCompanyName",
        ),
        "shandong_phone_ownership_claim": TemplateConfig(
            template_type="shandong_phone_ownership_claim",
            task_prefix="电话归属权声明",
            zip_prefix="电话归属权声明",
            file_prefix="电话归属权声明",
            template_path=shandong_root / "shandong_mobile_phone_ownership_claim.docx",
            required_shared_fields=("phoneNumbers",),
            summary_field="signature",
            default_shared_payload={"time": _today_text, "phoneUsage": "客户服务等"},
            multiline_fields=("phoneNumbers",),
            seal_company_field="companyName",
        ),
    }


def build_beijing_registry(template_root: Path) -> dict[str, TemplateConfig]:
    beijing_root = template_root / "lgi"
    return {
        "beijing_link_authorization": TemplateConfig(
            template_type="beijing_link_authorization",
            task_prefix="域名授权申明函",
            zip_prefix="域名授权申明函",
            file_prefix="域名授权申明函",
            template_path=beijing_root
            / "bjyd_link_shrinking_authorization_declaration_letter.docx",
            required_shared_fields=("linkList", "linkCompanyName"),
            summary_field="companyName",
            default_shared_payload={
                "businessScope": "",
                "authStartTime": _today_text,
                "authEndTime": lambda: f"{date.today().year + 3}年{date.today().month}月{date.today().day}日",
            },
            multiline_fields=("linkList",),
            seal_company_field="linkCompanyName",
        ),
        "beijing_compliance_commitment": TemplateConfig(
            template_type="beijing_compliance_commitment",
            task_prefix="引流合规承诺书",
            zip_prefix="引流合规承诺书",
            file_prefix="引流合规承诺书",
            template_path=beijing_root / "bjyd_compliance_commitment_letter.docx",
            required_shared_fields=("lgiItems",),
            summary_field="companyName",
            default_shared_payload={"businessScope": "金融业务", "time": _today_text},
            multiline_fields=(),
            seal_company_field="companyName",
        ),
        "beijing_number_ownership_claim": TemplateConfig(
            template_type="beijing_number_ownership_claim",
            task_prefix="号码归属声明",
            zip_prefix="号码归属声明",
            file_prefix="号码归属声明",
            template_path=beijing_root / "bjyd_number_ownership_claim.docx",
            required_shared_fields=("numberList",),
            summary_field="signature",
            default_shared_payload={"time": _today_text},
            multiline_fields=(),
            seal_company_field="companyName",
        ),
    }


def build_shandong_samples() -> dict[str, dict[str, Any]]:
    return {
        "shandong_short_link_reporting": {
            "templateType": "shandong_short_link_reporting",
            "source": "山东移动",
            "entries": [
                {"signature": "放心借", "companyName": "全家福公司"},
                {"signature": "吃得放心", "companyName": "阖家欢乐公司"},
            ],
            "sharedPayload": {
                "linkList": ["t.cn", "http://a.b.com", "c.d.cn"],
            },
        },
        "shandong_multi_level_domain": {
            "templateType": "shandong_multi_level_domain",
            "source": "山东移动",
            "entries": [
                {"signature": "放心借", "companyName": "全家福公司"},
            ],
            "sharedPayload": {
                "linkList": ["a.b.com", "m.a.b.com"],
                "businessUsage": "宣传推广",
            },
        },
        "shandong_link_authorization": {
            "templateType": "shandong_link_authorization",
            "source": "山东移动",
            "entries": [
                {"companyName": "阖家欢乐公司"},
            ],
            "sharedPayload": {
                "linkCompanyName": "全家福公司",
                "linkList": ["a.b.com", "c.d.cn"],
                "businessUsage": "宣传推广",
            },
        },
        "shandong_phone_ownership_claim": {
            "templateType": "shandong_phone_ownership_claim",
            "source": "山东移动",
            "entries": [
                {"signature": "放心借", "companyName": "全家福公司"},
            ],
            "sharedPayload": {
                "phoneNumbers": ["13800000000", "13900000000"],
                "phoneUsage": "客户服务等",
            },
        },
    }


def build_beijing_samples() -> dict[str, dict[str, Any]]:
    return {
        "beijing_link_authorization": {
            "templateType": "beijing_link_authorization",
            "source": "北京移动",
            "entries": [{"companyName": "阖家欢乐公司"}],
            "sharedPayload": {
                "linkCompanyName": "全家福公司",
                "linkList": ["a.b.com", "c.d.cn"],
                "businessScope": "金融业务",
            },
        },
        "beijing_compliance_commitment": {
            "templateType": "beijing_compliance_commitment",
            "source": "北京移动",
            "entries": [{"companyName": "全家福公司"}],
            "sharedPayload": {
                "businessScope": "金融业务",
                "lgiItems": [
                    {"content": "a.b.com", "type": 1},
                    {"content": "13800000000", "type": 2},
                ],
            },
        },
        "beijing_number_ownership_claim": {
            "templateType": "beijing_number_ownership_claim",
            "source": "北京移动",
            "entries": [{"signature": "放心借", "companyName": "全家福公司"}],
            "sharedPayload": {
                "numberList": ["13800000000", "13900000000"],
            },
        },
    }
