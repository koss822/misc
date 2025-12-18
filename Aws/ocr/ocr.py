import os
from pathlib import Path
import boto3

def ocr_image_local(file_path: Path) -> str:
    """Run OCR with Amazon Textract on a local JPG file and return recognized text line by line."""
    textract = boto3.client("textract")

    # Read the file into memory as bytes.
    with open(file_path, "rb") as f:
        image_bytes = f.read()

    response = textract.detect_document_text(
        Document={"Bytes": image_bytes}
    )

    lines = []
    for block in response.get("Blocks", []):
        if block.get("BlockType") == "LINE":
            lines.append(block.get("Text", ""))

    return "\n".join(lines)


def main():
    # Directory where this script is located
    script_dir = Path(__file__).resolve().parent

    # All .jpg files in the script directory (non-recursive)
    jpg_files = sorted(script_dir.glob("*.jpg"))

    if not jpg_files:
        print("No .jpg files found in the script directory.")
        return

    for img_path in jpg_files:
        print(f"Processing: {img_path.name}")
        text = ocr_image_local(img_path)

        # Create a text file name based on the image name.
        # Example: image.jpg -> image.txt
        txt_name = img_path.with_suffix(".txt")

        with open(txt_name, "w", encoding="utf-8") as out_f:
            out_f.write(text)

        print(f"Saved to: {txt_name.name}")


if __name__ == "__main__":
    main()