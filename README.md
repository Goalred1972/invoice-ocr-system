# 发票OCR分类系统

自动识别发票文件、提取关键信息并生成Excel报表的智能系统。

## 功能特性

- ✅ **多格式支持**: PDF、OFD、XML、JPG、PNG、TIFF
- ✅ **智能分类**: 自动区分发票和非发票文件（如行程单、明细单）
- ✅ **信息提取**: 自动提取发票号、日期、金额、供应商名称
- ✅ **重复检测**: 基于发票号识别重复发票
- ✅ **Excel报表**: 生成结构化的Excel报表
- ✅ **文件追溯**: 保留原始文件名，便于核对

## 安装依赖

### 1. 安装Python依赖

```bash
pip install -r requirements.txt
```

### 2. OCR引擎

系统使用PaddleOCR作为OCR引擎（已包含在requirements.txt中）。

如果需要使用Tesseract，请额外安装：
- Windows: 下载 [Tesseract-OCR](https://github.com/UB-Mannheim/tesseract/wiki)
- Linux: `sudo apt-get install tesseract-ocr tesseract-ocr-chi-sim`
- macOS: `brew install tesseract tesseract-lang`

## 使用方法

### 基本用法

```bash
python main.py --input-dir ./Samples --output-file output.xlsx
```

### 完整参数

```bash
python main.py \
  --input-dir ./Samples \
  --output-file report.xlsx \
  --duplicate-sensitivity standard
```

### 参数说明

- `-i, --input-dir`: 输入目录路径（必需）
- `-o, --output-file`: 输出Excel文件路径（必需）
- `--duplicate-sensitivity`: 重复检测灵敏度
  - `strict`: 严格模式（仅发票号完全相同）
  - `standard`: 标准模式（默认）
  - `loose`: 宽松模式

## 支持的文件格式

| 格式 | 扩展名 | 处理方式 |
|------|--------|----------|
| PDF | .pdf | 文本提取 + OCR |
| OFD | .ofd | OCR |
| XML | .xml | 结构化解析 |
| 图片 | .jpg, .jpeg, .png, .tiff, .tif | OCR |

## Excel报表结构

生成的Excel报表包含以下列：

1. 序号
2. 文件名
3. 文档类型（发票/非发票文件/未知类型）
4. 发票号
5. 发票日期
6. 金额（元）
7. 供应商名称
8. 是否重复
9. 重复文件
10. 提取状态（完整/不完整/失败）
11. 备注

## 文档类型识别

系统会自动识别文档类型：

- **发票**: 包含"发票"、"发票号"等关键字的文件
- **非发票文件**: 包含"行程单"、"明细单"、"附件"等关键字的文件
- **未知类型**: 无法确定类型的文件

非发票文件会被标记但不会提取发票信息。

## 项目结构

```
.
├── main.py                 # 主程序入口
├── requirements.txt        # Python依赖
├── pytest.ini             # 测试配置
├── README.md              # 项目文档
├── src/                   # 源代码
│   ├── __init__.py
│   ├── config.py          # 配置管理
│   ├── models.py          # 数据模型
│   ├── file_scanner.py    # 文件扫描器
│   ├── format_processors.py  # 格式处理器
│   ├── document_classifier.py  # 文档分类器
│   ├── ocr_engine.py      # OCR引擎
│   ├── invoice_parser.py  # 发票解析器
│   ├── duplicate_detector.py  # 重复检测器
│   ├── excel_generator.py  # Excel生成器
│   ├── error_handler.py   # 错误处理器
│   └── invoice_processor.py  # 主处理器
├── tests/                 # 测试代码
│   ├── __init__.py
│   └── test_file_scanner.py
├── Samples/               # 示例文件
└── logs/                  # 日志文件

```

## 运行测试

```bash
# 运行所有测试
pytest

# 运行单元测试
pytest -m unit

# 运行集成测试
pytest -m integration

# 查看测试覆盖率
pytest --cov=src --cov-report=html
```

## 日志

系统会自动生成日志文件：
- 位置: `logs/invoice_ocr.log`
- 包含: 处理过程、错误信息、调试信息

## 常见问题

### 1. OCR识别效果不好

- 确保图片清晰度足够
- 尝试调整图片大小和对比度
- 考虑使用更高质量的扫描件

### 2. XML解析失败

- 检查XML文件是否符合中国电子发票标准格式
- 查看日志文件了解具体错误信息

### 3. 内存占用过高

- 减少单次处理的文件数量
- 分批处理大量文件

## 技术栈

- Python 3.8+
- PaddleOCR - OCR识别
- openpyxl - Excel生成
- PyPDF2 - PDF处理
- Pillow - 图片处理
- pytest - 测试框架
- Hypothesis - 属性测试

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 联系方式
goal.red@hotmail.com

如有问题或建议，请提交Issue。
