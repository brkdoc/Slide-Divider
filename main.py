import fitz  # PyMuPDF
import os


def split_4up_to_1up(input_path, output_path):
    try:
        src_doc = fitz.open(input_path)
        out_doc = fitz.open()

        for page in src_doc:
            rect = page.rect
            w = rect.width
            h = rect.height

            # Define the 4 quadrants (Top-Left, Top-Right, Bottom-Left, Bottom-Right)
            # Standard Z-order layout
            quadrants = [
                fitz.Rect(0, 0, w / 2, h / 2),  # Top-Left
                fitz.Rect(w / 2, 0, w, h / 2),  # Top-Right
                fitz.Rect(0, h / 2, w / 2, h),  # Bottom-Left
                fitz.Rect(w / 2, h / 2, w, h)  # Bottom-Right
            ]

            for quad in quadrants:
                # Copy the original page to the new document
                out_doc.insert_pdf(src_doc, from_page=page.number, to_page=page.number)
                # Get the newly added page
                new_page = out_doc[-1]
                # Crop the page to the specific quadrant
                new_page.set_cropbox(quad)

        out_doc.save(output_path)
        out_doc.close()
        print(f"[OK] Converted: {output_path}")

    except Exception as e:
        print(f"[ERROR] Error processing {input_path}: {e}")


def process_all_pdfs_in_folder(folder_path):
    # List all files in the directory
    files = [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]

    if not files:
        print("No PDF files found in the folder.")
        return

    print(f"Found {len(files)} PDFs, starting process...\n" + "-" * 40)

    count = 0
    for filename in files:
        # Skip previously generated files (containing "_split" in the name)
        # to prevent recursive processing
        if "_split" in filename:
            continue

        input_full_path = os.path.join(folder_path, filename)

        # Output filename format: original_name_split.pdf
        output_filename = f"{os.path.splitext(filename)[0]}_split.pdf"
        output_full_path = os.path.join(folder_path, output_filename)

        split_4up_to_1up(input_full_path, output_full_path)
        count += 1

    print("-" * 40)
    print(f"Process complete. Total {count} files converted.")


# Usage:
# Use "." if the script is in the same folder as the PDFs.
# Otherwise, provide the full path: r"C:\Users\You\Documents\Slides"
target_folder = "."

if __name__ == "__main__":
    process_all_pdfs_in_folder(target_folder)