- ***前提*：**创建新的 Excel_A.xlse，将 A中 需要修改的文件 + 不需要修改的文件，写入 新的ZIP包 Excel_B.zip，并修改后缀，成Excel_B.xlse。完成向表格其中嵌入图片

- ***缺失文件***：

  - xl/media【放图片文件】

  - xl/_rels/cellimages.xml.rels【图片映射路径 rid 】

  - xl/cellimages.xml【图片格式 + uuid + rid】

- ***修改文件***：
  - xl/worksheets【新增单元格-有库能直接操作-写入单元格内容与计算公式=DISPIMG(uuid)】
  - xl/_rels/workbook.xml.rels【供sheet去查询，单元格内的映射-新增一行，增加xl/cellimages.xml】
  - [Content_Types].xml【可能需要修改，也可能wps会自主判断并增加所需**总映射规则**】

- ***代码大致流程***：

  1. 所需参数，图片集-字典列表，文本集-字典，输出文件路径

  2. 先将 文本 和 图片 DISPIMG(uuid)_自创 写入 xl/worksheets/sheet1 表中

  3. 将 图片 写入 xl/media 中，并记录 相对路径 relative_path（代码中不是这样的写，但基本逻辑一样）

  4. 创建 xl/cellimages.xml，写入图片xml属性，uuid，rid

  5. 创建 xl/_rels/cellimages.xml.rels，写入映射规则——rid，relative_path

  6. 修改 xl/_rels/workbook.xml.rels，新增一行——id（不重复，即可。我是连续），新增映射路径 xl/cellimages.xml

  7. [Content_Type].xml【我这里是处理了的。之前做对比的时候，发现这地方不用管也是可以的，因为这是总映射规则合集】

  8. 【基于前提】创建新的 ZIP 文件，并写入上述内容，完成嵌入

- [代码具体位置](./Json2Excel_Function.py)

```python
import os
import uuid
import zipfile
import json
from openpyxl import Workbook
import xml.etree.ElementTree as ET
import io import BytesIO
import shutil

def create_cellimages_xml(updated_pics_data):
    # 定义命名空间 URI
    NS_ETC = "http://www.wps.cn/officeDocument/2017/etCustomData"
    NS_XDR = "http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing"
    NS_A = "http://schemas.openxmlformats.org/drawingml/2006/main"
    NS_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    
    # 注册命名空间前缀
    ET.register_namespace("etc", NS_ETC)
    ET.register_namespace("xdr", NS_XDR)
    ET.register_namespace("a", NS_A)
    ET.register_namespace("r", NS_R)
    
    # 创建根元素
    root = ET.Element(f"{{NS_ETC}}cellImages")
    
    # 子元素：全部使用 {uri} 格式
    for i, pic_info in enumerate(updated_pics_data):
        cell_image = ET.SubElement(root, f"{{{NS_ETC}}}cellImage")
        pic = ET.SubElement(cell_image, f"{{{NS_XDR}}}pic")

        nvPr = ET.SubElement(pic, f"{{{NS_XDR}}}cNvPr")
        cNvPr = ET.SubElement(nvPr, f"{{{NS_XDR}}}cNvPr")
        cNvPr.set("id", f"{i + 1}")
        cNvPr.set("name", pic_info["disp_id"])
        ET.SubElement(nvPr, f"{{{NS_XDR}}}cNvPicPr")

        blipFill = ET.SubElement(pic, f"{{{NS_XDR}}}blipFill")
        blip = ET.SubElement(blipFill, f"{{{NS_A}}}blip")
        blip.set(f"{{{NS_R}}}embed", f"rId{i + 1}")
        stretch = ET.SubElement(blipFill, f"{{{NS_A}}}stretch")
        ET.SubElement(stretch, f"{{{NS_A}}}fillRect")

        spPr = ET.SubElement(pic, f"{{{NS_XDR}}}spPr")
        xfrm = ET.SubElement(spPr, f"{{{NS_A}}}xfrm")
        off_a = ET.SubElement(xfrm, f"{{{NS_A}}}off")
        off_a.set("x", "0")
        off_a.set("y", "0")
        ext_a = ET.SubElement(xfrm, f"{{{NS_A}}}ext")
        ext_a.set("cx", "5000000") # 高度
        ext_a.set("cy", "3000000") # 宽度
        prstGeom = ET.SubElement(spPr, f"{{{NS_A}}}prstGeom")
        prstGeom.set("prst", "rect")
        ET.SubElement(prstGeom, f"{{{NS_A}}}avLst")
    
    # 输出 XML 字符串
    xml_str = ET.tostring(root, encoding="unicode")
    return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' + xml_str

def create_cellimage_xml_rels(updated_pics_data):
    NS = "http://schemas.openxmlformats.org/package/2006/relationships"
    ET.register_namespace('', NS)
    
    root = ET.Element("Relationships", xmlns=NS)
    for i, disp_info in enumerate(updated_pics_data):
        rel = ET.SubElement(root, "Relationship")
        rel.set("Id", f"rId{i + 1}")
        rel.set("Type", "http://schemas.openxmlformats.org/officeDocument/2006/relationship/image")
    
    return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' + ET.tostring(root, encoding='unicode')

def write_pics_data_to_excel(sheet, pics_data, json_data, current_dir, start_col=1):
    """
    将 图片数据 和 JSON数据 写入 Excel 工作表
    第一行：图片类型 + JSON键
    第二行：图片公式 + JSON值
    同时将生成的 UUID 存储到 pics_data 中
    """
    col = start_col
    
    # 写入 JSON 数据
    for key, value in json_data.items():
        sheet.cell(row=1, column=col, value=key) # 第一行写入键
        sheet.cell(row=2, column=col, value=value) # 第二行写入值
        col += 1
    # 写入图片数据    
    for i, pic_info in enumerate(pics_data):
        pic_type = pic_info["图片类型"]
        sheet.cell(row=1, column=col, value=pic_type) # 第一行写入图片类型
        
        # 生成唯一的图片ID 并写入公式
        disp_id = f"ID_{uuid.uuid4().hex.upper()}"
        sheet.cell(row=2, column=col, value=f'DISPIMG("{disp_id}",1)') # 第二行写入公式
        
        # 将生成的 UUID 存储到 pics_data 中
        pic_info["disp_id"] = disp_id
        
        # 修改文件路径
        pic_info["图片文件路径"]  = os.path.join(current_dir, pic_info["图片文件路径"])
        col += 1
    return pics_data, col # 返回更新后的图片信息和下一列的列号

def JSON2EXCEL_Function(pics_data, json_data, output_xlsx):
    # todo 还没写完，md，没必要，直接超链接
```



