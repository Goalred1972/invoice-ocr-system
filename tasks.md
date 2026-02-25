# Implementation Plan: 发票OCR分类系统

## Overview

本实现计划将发票OCR分类系统分解为可执行的编码任务。系统采用管道式架构，支持多种发票格式（PDF、OFD、XML、图片），能够提取关键信息、检测重复并生成Excel报表。实现语言为Python。

## Tasks

- [x] 1. 设置项目结构和核心数据模型
  - 创建项目目录结构（src/、tests/、samples/）
  - 定义核心数据类：FileInfo, FileFormat, DocumentType, ExtractedContent, InvoiceData, ExtractionStatus, DuplicateSensitivity
  - 设置依赖管理文件（requirements.txt）：包括openpyxl、Pillow、PyPDF2、PaddleOCR、Hypothesis等
  - 创建基础配置文件和日志系统
  - _Requirements: 1.1, 1.2, 2.1, 2.2, 2.3, 2.4, 6.1_

- [ ]* 1.1 为核心数据模型编写属性测试
  - **Property 14: File Name Preservation with Extension**
  - **Validates: Requirements 5.1, 5.2**

- [ ] 2. 实现文件扫描和格式识别模块
  - [x] 2.1 实现FileScanner类
    - 实现scan_directory方法：扫描目录并返回文件列表
    - 实现identify_format方法：基于文件扩展名识别格式
    - 支持的格式：PDF, OFD, XML, JPG, PNG, TIFF
    - 对不支持的格式返回UNSUPPORTED并生成描述性错误消息
    - _Requirements: 1.1, 1.2, 1.3_

  - [ ]* 2.2 为格式识别编写属性测试
    - **Property 1: Format Identification Correctness**
    - **Validates: Requirements 1.1, 1.2, 1.3**

  - [x]* 2.3 编写文件扫描单元测试
    - 测试支持的格式识别（PDF、OFD、XML、图片）
    - 测试不支持格式的错误处理
    - 测试特殊字符文件名处理
    - _Requirements: 1.1, 1.2, 1.3_

- [ ] 3. 实现格式处理器基类和具体处理器
  - [x] 3.1 实现FormatProcessor抽象基类
    - 定义can_process和extract_content抽象方法
    - _Requirements: 1.4_

  - [x] 3.2 实现XMLProcessor
    - 解析XML结构并提取结构化数据
    - 处理中国电子发票标准格式（InvoiceNumber、TotalTax-includedAmount等节点）
    - 错误处理：XML格式不符合预期时返回错误
    - _Requirements: 1.4, 2.1, 2.2, 2.3, 2.4_

  - [ ]* 3.3 为XML处理器编写属性测试
    - **Property 5: XML Parsing Round Trip**
    - **Validates: Requirements 1.4, 2.1, 2.2, 2.3, 2.4**

  - [x] 3.4 实现PDFProcessor
    - 使用PyPDF2或pdfplumber提取PDF文本
    - 处理文本型PDF和图片型PDF（调用OCR）
    - _Requirements: 1.4_

  - [ ] 3.5 实现OFDProcessor
    - 使用odfpy或专门的OFD库处理OFD格式（中国电子发票标准格式）
    - 提取OFD文档中的文本和结构化数据
    - _Requirements: 1.4_

  - [ ] 3.6 实现ImageProcessor
    - 加载图片文件（JPG、PNG、TIFF）
    - 将图片数据传递给OCR引擎
    - _Requirements: 1.4_

  - [ ]* 3.7 为内容提取编写属性测试
    - **Property 2: Content Extraction Completeness**
    - **Validates: Requirements 1.4**

  - [ ]* 3.8 编写格式处理器单元测试
    - 测试XML解析（使用Samples目录中的高德电子发票）
    - 测试PDF文本提取
    - 测试OFD文档处理
    - 测试图片加载
    - 测试损坏文件处理
    - _Requirements: 1.4_

- [ ] 4. 实现文档类型分类器
  - [ ] 4.1 实现DocumentTypeClassifier类
    - 实现classify_document方法：判断文档是发票、非发票还是未知类型
    - 实现check_filename_keywords方法：检测文件名中的关键词（"行程单"、"明细单"、"附件"等）
    - 实现check_content_keywords方法：检测内容中的发票特征字段（"发票"、"发票号"、"发票代码"等）
    - 实现get_confidence_score方法：计算分类置信度
    - 分类决策：文件名关键词优先，然后检查内容关键词（至少2个发票特征字段）
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.8_

  - [ ]* 4.2 为文档类型分类编写属性测试
    - **Property 16: Document Type Classification Completeness**
    - **Validates: Requirements 6.1**

  - [ ]* 4.3 为文件名识别编写属性测试
    - **Property 17: Filename-Based Non-Invoice Detection**
    - **Validates: Requirements 6.2**

  - [ ]* 4.4 为内容识别编写属性测试
    - **Property 18: Content-Based Invoice Classification**
    - **Validates: Requirements 6.3, 6.4**

  - [ ]* 4.5 为未知类型警告编写属性测试
    - **Property 21: Unknown Type Warning Logging**
    - **Validates: Requirements 6.8**

  - [ ]* 4.6 编写文档类型分类器单元测试
    - 测试通过文件名识别行程单
    - 测试通过内容识别发票
    - 测试文件名和内容特征冲突情况
    - 测试低置信度情况（标记为未知类型）
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.8_

- [ ] 5. Checkpoint - 确保格式识别和内容提取测试通过
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 6. 集成OCR引擎
  - [ ] 6.1 实现OCREngine类
    - 选择并集成PaddleOCR（推荐）或Tesseract
    - 实现recognize_text方法：识别图片中的文本
    - 实现recognize_with_layout方法：保留布局信息
    - 处理OCR失败和低置信度情况
    - _Requirements: 1.4_

  - [ ]* 6.2 编写OCR引擎单元测试
    - 测试文本识别功能
    - 测试低质量图片处理
    - 测试OCR引擎初始化失败处理
    - _Requirements: 1.4_

- [ ] 7. 实现发票信息解析器
  - [ ] 7.1 实现InvoiceParser类
    - 实现parse_invoice方法：从ExtractedContent提取InvoiceData
    - 实现extract_invoice_number：使用正则表达式匹配20位数字
    - 实现extract_date：支持多种日期格式（YYYY-MM-DD、YYYY/MM/DD等）
    - 实现extract_amount：匹配货币格式（小数点数字）
    - 实现extract_vendor：匹配"销售方"、"收款方"等关键词后的文本
    - 对于XML格式，直接从结构化数据提取
    - _Requirements: 2.1, 2.2, 2.3, 2.4_

  - [ ] 7.2 实现字段提取失败处理
    - 当必需字段无法提取时，标记为INCOMPLETE
    - 记录缺失字段到error_message
    - _Requirements: 2.5_

  - [ ]* 7.3 为字段提取编写属性测试
    - **Property 3: Field Extraction Consistency**
    - **Validates: Requirements 2.1, 2.2, 2.3, 2.4**

  - [ ]* 7.4 为不完整提取编写属性测试
    - **Property 4: Incomplete Extraction Marking**
    - **Validates: Requirements 2.5**

  - [ ]* 7.5 编写发票解析器单元测试
    - 测试从XML提取完整字段
    - 测试从文本提取各个字段
    - 测试缺少发票号的情况
    - 测试无效日期格式处理
    - 测试无效金额格式处理
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

- [ ] 8. 实现重复检测器
  - [ ] 8.1 实现DuplicateDetector类
    - 实现detect_duplicates方法：识别重复发票组
    - 实现mark_duplicates方法：标记重复发票并记录duplicate_files
    - 基于发票号进行精确匹配
    - 第一个出现的发票标记为非重复，后续相同发票号标记为重复
    - _Requirements: 4.1, 4.2, 4.3, 4.4_

  - [ ] 8.2 实现灵敏度配置
    - 实现configure_sensitivity方法
    - 支持STRICT（仅发票号）、STANDARD（发票号或日期+金额+供应商）、LOOSE（相似度阈值）模式
    - _Requirements: 4.6_

  - [ ]* 8.3 为重复检测编写属性测试
    - **Property 10: Duplicate Detection by Invoice Number**
    - **Validates: Requirements 4.1, 4.2**

  - [ ]* 8.4 为重复文件名记录编写属性测试
    - **Property 11: Duplicate File Name Recording**
    - **Validates: Requirements 4.4, 5.3**

  - [ ]* 8.5 为唯一发票计数编写属性测试
    - **Property 12: Unique Invoice Counting**
    - **Validates: Requirements 4.3**

  - [ ]* 8.6 为灵敏度配置编写属性测试
    - **Property 13: Sensitivity Configuration Effect**
    - **Validates: Requirements 4.6**

  - [ ]* 8.7 编写重复检测器单元测试
    - 测试精确重复检测
    - 测试不同灵敏度模式
    - 测试空发票号处理
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.6_

- [ ] 9. Checkpoint - 确保解析和重复检测测试通过
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 10. 实现Excel报表生成器
  - [ ] 10.1 实现ExcelGenerator类
    - 实现generate_report方法：创建Excel文件
    - 创建表头：序号、文件名、文档类型、发票号、发票日期、金额（元）、供应商名称、是否重复、重复文件、提取状态、备注
    - 填充数据行：每个InvoiceData对应一行
    - 对于非发票文件，在文档类型列显示"非发票文件"，发票字段留空
    - 实现format_worksheet方法：设置列宽、数字格式、日期格式
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 4.5, 5.1, 5.2, 5.4, 6.5, 6.7_

  - [ ] 10.2 实现输出路径处理
    - 验证输出路径有效性
    - 检查写权限
    - 保存Excel文件到指定位置
    - _Requirements: 3.5_

  - [ ]* 10.3 为Excel生成编写属性测试
    - **Property 6: Excel Generation Completeness**
    - **Validates: Requirements 3.1**

  - [ ]* 10.4 为Excel结构编写属性测试
    - **Property 7: Excel Schema Correctness**
    - **Validates: Requirements 3.2, 3.3, 4.5**

  - [ ]* 10.5 为批量处理编写属性测试
    - **Property 8: Batch Processing Completeness**
    - **Validates: Requirements 3.4**

  - [ ]* 10.6 为输出路径编写属性测试
    - **Property 9: Output Path Preservation**
    - **Validates: Requirements 3.5**

  - [ ]* 10.7 为文档类型列编写属性测试
    - **Property 20: Document Type Excel Column Presence**
    - **Validates: Requirements 6.5, 6.7**

  - [ ]* 10.8 编写Excel生成器单元测试
    - 测试Excel文件创建
    - 测试表头正确性（包含文档类型列）
    - 测试数据行数量
    - 测试文件名保留（含扩展名）
    - 测试非发票文件在Excel中的显示
    - 测试输出路径无效处理
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 5.1, 5.2, 6.5, 6.7_

- [ ] 11. 实现错误处理系统
  - [ ] 11.1 实现ErrorHandler类
    - 实现log_error方法：记录错误到日志文件
    - 实现get_error_summary方法：生成错误摘要
    - 支持不同错误级别：WARNING、ERROR、CRITICAL
    - _Requirements: 1.3, 2.5_

  - [ ] 11.2 集成错误处理到各个组件
    - 在文件扫描、格式处理、OCR、解析、重复检测中添加错误处理
    - 实现优雅降级：单个文件失败不影响批处理
    - 在Excel报表中记录错误信息（提取状态、备注列）
    - _Requirements: 1.3, 2.5_

  - [ ]* 11.3 为错误处理编写属性测试
    - **Property 15: Error Handling Idempotence**
    - **Validates: Requirements 2.5**

  - [ ]* 11.4 编写错误处理单元测试
    - 测试文件不存在错误
    - 测试不支持格式错误
    - 测试空文件处理
    - 测试损坏文件处理
    - _Requirements: 1.3, 2.5_

- [ ] 12. 实现主处理流程和批量处理器
  - [ ] 12.1 实现InvoiceProcessor主类
    - 实现process_directory方法：协调整个处理流程
    - 集成所有组件：FileScanner → FormatProcessor → DocumentTypeClassifier → InvoiceParser → DuplicateDetector → ExcelGenerator
    - 实现批量处理逻辑：遍历所有文件，收集结果
    - 对于非发票文件，跳过发票信息提取，直接标记文档类型
    - 处理每个文件时捕获异常，继续处理下一个
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 2.1, 2.2, 2.3, 2.4, 2.5, 3.4, 4.1, 4.2, 6.1, 6.6_

  - [ ] 12.2 实现命令行接口
    - 使用argparse创建CLI：接受输入目录、输出文件路径、配置选项
    - 添加参数：--input-dir, --output-file, --duplicate-sensitivity
    - 显示处理进度和摘要
    - _Requirements: 3.5, 4.6_

  - [ ]* 12.3 为非发票跳过提取编写属性测试
    - **Property 19: Non-Invoice Extraction Skipping**
    - **Validates: Requirements 6.6**

  - [ ]* 12.4 编写端到端集成测试
    - 测试完整处理流程（使用Samples目录）
    - 验证输出Excel文件存在且格式正确
    - 验证数据完整性和准确性
    - _Requirements: All_

- [ ] 13. Final Checkpoint - 确保所有测试通过
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 14. 添加文档和使用示例
  - [ ] 14.1 创建README.md
    - 项目简介和功能说明
    - 安装依赖说明
    - 使用示例和命令行参数说明
    - 支持的文件格式列表

  - [ ] 14.2 添加代码注释和文档字符串
    - 为所有公共类和方法添加docstring
    - 添加关键算法的注释说明
    - 添加使用示例

## Notes

- 任务标记为 `*` 的是可选测试任务，可以跳过以加快MVP开发
- 每个任务都引用了具体的需求条款，确保可追溯性
- Checkpoint任务确保增量验证
- 属性测试验证通用正确性属性，单元测试验证具体示例和边缘情况
- 使用Python实现，主要依赖：
  - openpyxl（Excel生成）
  - PaddleOCR或Tesseract（OCR引擎）
  - PyPDF2或pdfplumber（PDF处理）
  - odfpy或专门的OFD库（OFD处理）
  - Pillow（图片处理）
  - Hypothesis（属性测试）
  - xml.etree.ElementTree（XML解析）
- Samples目录包含真实的测试数据：
  - 高德打车/代驾电子发票（PDF、OFD、XML格式）
  - 电子行程单（非发票文件，用于测试文档类型识别）
  - 加油站发票、其他类型发票
- 文档类型识别是核心功能，需要正确区分发票和行程单，避免误处理
