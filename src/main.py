import os
import argparse
from src.parsing.classifier import ReportClassifier
from src.parsing.type_a_parser import TypeAParser
from src.parsing.type_b_parser import TypeBParser
from src.transformation.type_a_strategy import TypeAStrategy
from src.transformation.type_b_strategy import TypeBStrategy
from src.generation.excel_renderer import ExcelRenderer


def process_attendance_pdf(pdf_path: str, output_path: str) -> str:
    """
    Executes the full pipeline for a single attendance PDF file.
    """
    print(f"[1/4] Classifying PDF: {pdf_path}")
    report_type = ReportClassifier.classify(pdf_path)
    print(f"      Identified report type: {report_type}")

    print("[2/4] Parsing PDF data...")
    if report_type == "Type_A":
        parser = TypeAParser(pdf_path)
        strategy = TypeAStrategy()
    else:
        parser = TypeBParser(pdf_path)
        strategy = TypeBStrategy()

    parsed_report = parser.parse()

    print("[3/4] Generating variation (simulation)...")
    varied_report = strategy.transform(parsed_report)

    print(f"[4/4] Rendering Excel output to: {output_path}")
    renderer = ExcelRenderer()
    final_file = renderer.render(varied_report, output_path)

    print("Process completed successfully!")
    return final_file


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Attendance PDF Simulator and Excel Generator")
    parser.add_argument("--input", required=True, help="Path to input PDF file")
    parser.add_argument("--output", required=True, help="Path to output Excel (.xlsx) file")

    args = parser.parse_args()
    process_attendance_pdf(args.input, args.output)