import argparse
from pdf2image import convert_from_path
import os

def convert_pdf_to_png(pdf_path, dpi=400, output_dir=None):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    images = convert_from_path(pdf_path, dpi=dpi)
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]

    if output_dir is None:
        output_dir = os.getcwd()
    os.makedirs(output_dir, exist_ok=True)

    for i, img in enumerate(images):
        output_path = os.path.join(output_dir, f"{base_name}_page_{i+1}.png")
        img.save(output_path, "PNG")
        print(f"Images saved: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Convert PDF to PNG")
    parser.add_argument("pdf", help="Path to the PDF file")
    parser.add_argument("-d", "--dpi", type=int, default=400, help="DPI for conversion (default: 400)")
    parser.add_argument("-o", "--output", help="Output directory for PNG file (default: current directory)")

    args = parser.parse_args()
    convert_pdf_to_png(args.pdf, dpi=args.dpi, output_dir=args.output)

if __name__ == "__main__":
    main()
