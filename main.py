"""
发票OCR分类系统 - 主程序入口
Invoice OCR Classification System - Main Entry Point
"""

import argparse
import sys
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from src.invoice_processor import InvoiceProcessor
from src.config import setup_logging, DEFAULT_DUPLICATE_SENSITIVITY

# 初始化日志
logger = setup_logging()


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="发票OCR分类系统 - 自动识别发票文件、提取关键信息并生成Excel报表",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python main.py --input-dir ./Samples --output-file output.xlsx
  python main.py -i ./invoices -o report.xlsx --duplicate-sensitivity strict
        """
    )
    
    parser.add_argument(
        '-i', '--input-dir',
        required=True,
        help='输入目录路径（包含发票文件）'
    )
    
    parser.add_argument(
        '-o', '--output-file',
        required=True,
        help='输出Excel文件路径'
    )
    
    parser.add_argument(
        '--duplicate-sensitivity',
        choices=['strict', 'standard', 'loose'],
        default=DEFAULT_DUPLICATE_SENSITIVITY,
        help=f'重复检测灵敏度 (默认: {DEFAULT_DUPLICATE_SENSITIVITY})'
    )
    
    args = parser.parse_args()
    
    # 验证输入目录
    input_dir = Path(args.input_dir)
    if not input_dir.exists():
        logger.error(f"输入目录不存在: {args.input_dir}")
        sys.exit(1)
    
    if not input_dir.is_dir():
        logger.error(f"输入路径不是目录: {args.input_dir}")
        sys.exit(1)
    
    # 创建处理器并执行
    try:
        processor = InvoiceProcessor()
        processor.process_directory(
            input_dir=str(input_dir),
            output_file=args.output_file,
            duplicate_sensitivity=args.duplicate_sensitivity
        )
        
        logger.info("\n处理完成！")
        
    except KeyboardInterrupt:
        logger.info("\n用户中断处理")
        sys.exit(0)
        
    except Exception as e:
        logger.error(f"\n处理失败: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
