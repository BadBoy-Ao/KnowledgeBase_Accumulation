# Python Report Service

独立于原有 Java 工程的 Python 报备文档生成服务。

当前已经实现：
1. 山东 4 个模板
2. 北京 3 个模板
3. 统一模板注册与调度框架
4. `docx -> pdf -> jpg -> zip` 生成链路
5. 统一 API 入口
6. 本地直跑测试入口

## 功能

- 复用 Java 工程中的真实 `.docx` 模板
- 按模板类型统一调度生成
- 按 `entries` 批量生成多张图片
- 将多张图片打包为 ZIP
- 返回静态下载地址
- 通过印章接口自动下载真实印章图片

## 当前支持模板

### 山东

- `shandong_short_link_reporting`
- `shandong_multi_level_domain`
- `shandong_link_authorization`
- `shandong_phone_ownership_claim`

### 北京

- `beijing_link_authorization`
- `beijing_compliance_commitment`
- `beijing_number_ownership_claim`

## 目录

- `app/main.py`: FastAPI 入口与本地测试入口
- `app/models/report.py`: 通用请求/响应模型
- `app/routers/report.py`: 统一 API 路由
- `app/services/template_registry.py`: 模板注册表与样例数据
- `app/services/render_service.py`: 通用渲染、转换、打包服务
- `storage/`: 生成后的图片、ZIP、印章缓存
- `C:/temp/python-report-service-work/`: 中间 `docx` 和 `pdf` 文件

## 安装

```bash
pip install -r requirements.txt
```

## 运行方式

### 方式一：本地直跑

直接执行内置测试数据，不启动 FastAPI：

```bash
python -m app.main
```

### 方式二：启动 API

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

启动后可直接访问前端页面：

`http://127.0.0.1:8000/ui/`

## 通用请求结构

统一入口使用同一种请求格式：

```json
{
  "templateType": "shandong_short_link_reporting",
  "source": "山东移动",
  "entries": [
    {
      "signature": "放心借",
      "companyName": "全家福公司"
    }
  ],
  "sharedPayload": {
    "linkList": ["t.cn", "http://a.b.com", "c.d.cn"]
  }
}
```

字段说明：

- `templateType`: 模板类型
- `source`: 来源标识
- `entries`: 批量条目
- `sharedPayload`: 当前模板的共享参数

## API

### 1. 查询模板列表

`GET /api/v1/reports/templates`

返回示例：

```json
{
  "templates": [
    "beijing_compliance_commitment",
    "beijing_link_authorization",
    "beijing_number_ownership_claim",
    "shandong_link_authorization",
    "shandong_multi_level_domain",
    "shandong_phone_ownership_claim",
    "shandong_short_link_reporting"
  ]
}
```

### 2. 查询某个模板的请求样例

`GET /api/v1/reports/sample/{templateType}`

例如：

`GET /api/v1/reports/sample/shandong_short_link_reporting`

### 3. 统一生成入口

`POST /api/v1/reports/generate`

返回示例：

```json
{
  "taskName": "短链报备说明_放心借",
  "templateType": "shandong_short_link_reporting",
  "fileName": "短链报备说明_ab12cd34ef56.zip",
  "resultUrl": "http://127.0.0.1:8000/storage/zips/短链报备说明_ab12cd34ef56.zip",
  "imageCount": 1,
  "imageFiles": [
    "D:/数据/AI/公司Agent业务/SMS_CODE/python-report-service/storage/images/短链报备说明_放心借_1.jpg"
  ],
  "docxFiles": [
    "C:/temp/python-report-service-work/docx/shandong_short_link_reporting_1_xxxxx.docx"
  ],
  "pdfFiles": [
    "C:/temp/python-report-service-work/pdf/shandong_short_link_reporting_1_xxxxx.pdf"
  ]
}
```

### 4. 健康检查

`GET /health`

## 山东模板调用样例

### 1. 短链报备说明

`templateType = shandong_short_link_reporting`

```json
{
  "templateType": "shandong_short_link_reporting",
  "source": "山东移动",
  "entries": [
    {
      "signature": "放心借",
      "companyName": "全家福公司"
    },
    {
      "signature": "吃得放心",
      "companyName": "阖家欢乐公司"
    }
  ],
  "sharedPayload": {
    "linkList": ["t.cn", "http://a.b.com", "c.d.cn"]
  }
}
```

### 2. 多级域名报备

`templateType = shandong_multi_level_domain`

```json
{
  "templateType": "shandong_multi_level_domain",
  "source": "山东移动",
  "entries": [
    {
      "signature": "放心借",
      "companyName": "全家福公司"
    }
  ],
  "sharedPayload": {
    "linkList": ["a.b.com", "m.a.b.com"],
    "businessUsage": "宣传推广"
  }
}
```

### 3. 域名授权书

`templateType = shandong_link_authorization`

```json
{
  "templateType": "shandong_link_authorization",
  "source": "山东移动",
  "entries": [
    {
      "companyName": "阖家欢乐公司"
    }
  ],
  "sharedPayload": {
    "linkCompanyName": "全家福公司",
    "linkList": ["a.b.com", "c.d.cn"],
    "businessUsage": "宣传推广"
  }
}
```

### 4. 电话归属权声明

`templateType = shandong_phone_ownership_claim`

```json
{
  "templateType": "shandong_phone_ownership_claim",
  "source": "山东移动",
  "entries": [
    {
      "signature": "放心借",
      "companyName": "全家福公司"
    }
  ],
  "sharedPayload": {
    "phoneNumbers": ["13800000000", "13900000000"],
    "phoneUsage": "客户服务等"
  }
}
```

说明：

- `phoneNumbers` 支持数组输入。
- 渲染到模板时会按英文逗号 `,` 拼接，例如：`13800000000,13900000000`。

## 北京模板调用样例

### 1. 域名授权申明函

`templateType = beijing_link_authorization`

```json
{
  "templateType": "beijing_link_authorization",
  "source": "北京移动",
  "entries": [
    {
      "companyName": "阖家欢乐公司"
    }
  ],
  "sharedPayload": {
    "linkCompanyName": "全家福公司",
    "linkList": ["a.b.com", "c.d.cn"],
    "businessScope": "金融业务"
  }
}
```

### 2. 引流合规承诺书

`templateType = beijing_compliance_commitment`

```json
{
  "templateType": "beijing_compliance_commitment",
  "source": "北京移动",
  "entries": [
    {
      "companyName": "全家福公司"
    }
  ],
  "sharedPayload": {
    "businessScope": "金融业务",
    "lgiItems": [
      {
        "content": "a.b.com",
        "type": 1
      },
      {
        "content": "13800000000",
        "type": 2
      }
    ]
  }
}
```

### 3. 号码归属声明

`templateType = beijing_number_ownership_claim`

```json
{
  "templateType": "beijing_number_ownership_claim",
  "source": "北京移动",
  "entries": [
    {
      "signature": "放心借",
      "companyName": "全家福公司"
    }
  ],
  "sharedPayload": {
    "numberList": ["13800000000", "13900000000"]
  }
}
```

## 说明

- 当前返回的是服务自身暴露的静态文件地址，用来模拟 OSS 地址。
- 如果后续接真实 OSS，只需要在 ZIP 生成后替换上传逻辑即可。
- 中间 `docx` 和 `pdf` 文件输出到 `C:/temp/python-report-service-work/`。
- 当前依赖本机安装 Microsoft Word，用于 `docx -> pdf`。
- 当前印章来源为真实印章接口：`POST /api/seal/download`。

## 已实现状态

- 山东 4 个模板：已可生成
- 北京 3 个模板：已可生成
- 统一 API：已提供
- 每个模板样例：已提供
- 本地直跑测试：已提供
