# Requirements Document

## Introduction

发票OCR分类系统是一个自动化工具，用于识别发票文件、提取关键信息并整理成结构化表格。该系统帮助报销人员快速处理大量发票，提高工作效率并减少人工错误。

## Glossary

- **System**: 发票OCR分类系统
- **Invoice_File**: 包含发票信息的数字文件（如PDF、图片等）
- **OCR_Engine**: 光学字符识别引擎，用于从图像中提取文本
- **Invoice_Data**: 从发票中提取的结构化信息（如金额、日期、供应商等）
- **Excel_Report**: 系统生成的Excel格式输出文件
- **Duplicate_Invoice**: 内容相同或高度相似的重复发票记录
- **Reimbursement_Staff**: 使用系统处理发票的报销人员
- **Non_Invoice_File**: 非发票文件，如行程单、明细单等附件
- **Document_Type**: 文档类型分类（发票或非发票）

## Requirements

### Requirement 1: 发票文件识别

**User Story:** 作为报销人员，我希望系统能够自动识别发票文件，以便我可以批量处理多个发票而无需手动分类。

#### Acceptance Criteria

1. WHEN an Invoice_File is uploaded, THE System SHALL identify the file format
2. THE System SHALL support PDF and common image formats (JPG, PNG, TIFF)
3. IF an unsupported file format is provided, THEN THE System SHALL return a descriptive error message
4. WHEN a valid Invoice_File is provided, THE System SHALL extract text using the OCR_Engine

### Requirement 2: 发票信息提取

**User Story:** 作为报销人员，我希望系统能够从发票中提取关键信息，以便我可以快速获取所需数据而无需手动输入。

#### Acceptance Criteria

1. WHEN text is extracted from an Invoice_File, THE System SHALL identify invoice number
2. WHEN text is extracted from an Invoice_File, THE System SHALL identify invoice date
3. WHEN text is extracted from an Invoice_File, THE System SHALL identify total amount
4. WHEN text is extracted from an Invoice_File, THE System SHALL identify vendor name
5. IF required information cannot be extracted, THEN THE System SHALL mark the field as incomplete and log the issue

### Requirement 3: 表格输出生成

**User Story:** 作为报销人员，我希望系统能够将提取的信息整理成Excel表格，以便我可以方便地查看、编辑和提交报销数据。

#### Acceptance Criteria

1. WHEN Invoice_Data is extracted, THE System SHALL generate an Excel_Report
2. THE Excel_Report SHALL contain columns for invoice number, date, amount, and vendor name
3. THE Excel_Report SHALL contain a column for the original Invoice_File name
4. WHEN multiple invoices are processed, THE System SHALL include all records in a single Excel_Report
5. THE System SHALL save the Excel_Report in a user-specified location

### Requirement 4: 重复发票排重

**User Story:** 作为报销人员，我希望系统能够识别和处理重复的发票，以便避免重复统计和重复报销。

#### Acceptance Criteria

1. WHEN processing multiple Invoice_Files, THE System SHALL compare invoice numbers to identify duplicates
2. WHEN a Duplicate_Invoice is detected, THE System SHALL mark it as duplicate in the Excel_Report
3. THE System SHALL include only one instance of each unique invoice in the final statistics
4. WHEN a Duplicate_Invoice is found, THE System SHALL log both the original and duplicate file names
5. THE Excel_Report SHALL contain a column indicating duplicate status for each invoice
6. WHERE duplicate detection is enabled, THE System SHALL allow Reimbursement_Staff to configure duplicate detection sensitivity

### Requirement 5: 文件名追溯

**User Story:** 作为报销人员，我希望在Excel表格中看到原始发票文件的名称，以便我可以快速定位和核对原始文件。

#### Acceptance Criteria

1. WHEN generating the Excel_Report, THE System SHALL include the original Invoice_File name for each record
2. THE System SHALL preserve the complete file name including file extension
3. WHEN a Duplicate_Invoice is detected, THE System SHALL list all associated file names
4. THE Excel_Report SHALL display the file name column in a clearly labeled format

### Requirement 6: 文档类型识别

**User Story:** 作为报销人员，我希望系统能够识别并区分发票文件和非发票文件，以便避免将行程单、明细单等非发票文件误处理为发票，产生错误数据。

#### Acceptance Criteria

1. WHEN a file is processed, THE System SHALL determine the Document_Type
2. THE System SHALL identify Non_Invoice_Files by checking file name for keywords such as "行程单", "明细单", "附件"
3. THE System SHALL identify Non_Invoice_Files by checking document content for absence of invoice-specific fields (invoice number, invoice code)
4. WHEN a file contains invoice-specific keywords ("发票", "发票号", "发票代码"), THE System SHALL classify it as Invoice_File
5. WHEN a Non_Invoice_File is detected, THE System SHALL mark it as "非发票文件" in the Excel_Report
6. WHEN a Non_Invoice_File is detected, THE System SHALL skip invoice information extraction for that file
7. THE Excel_Report SHALL contain a column indicating Document_Type for each processed file
8. WHEN a file cannot be confidently classified, THE System SHALL mark it as "未知类型" and log a warning
