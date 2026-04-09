import fitz  # PyMuPDF
import os
import easyocr
import numpy as np

# Tải model OCR, hỗ trợ tiếng Việt và tiếng Anh
print("Đang tải model OCR (EasyOCR)...")
reader = easyocr.Reader(['vi', 'en'], gpu=False)

def process_pdf(pdf_path, output_dir="output"):
    # Tạo thư mục output
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(f"{output_dir}/images", exist_ok=True)
    os.makedirs(f"{output_dir}/pages", exist_ok=True)

    doc = fitz.open(pdf_path)
    full_text = []

    print(f"Đang xử lý: {pdf_path} ({len(doc)} trang)")

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        
        # 1. Trích xuất Text
        text = page.get_text().strip()
        
        # Dùng OCR nếu text xuất ra trống hoặc quá ngắn (khả năng là ảnh)
        if len(text) < 20:
            print(f"   -> Trang {page_num + 1} có vẻ là ảnh, đang chạy OCR...")
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            # Chuyển đổi pixmap sang dạng numpy array để dùng EasyOCR
            img_array = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
            
            # Trích xuất text từ ảnh bằng OCR
            ocr_result = reader.readtext(img_array, detail=0)
            text = "\n".join(ocr_result)
            
        full_text.append(f"--- Trang {page_num + 1} ---\n{text}")

        # 2. Trích xuất Hình ảnh gốc (Embedded Images)
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_filename = f"img_p{page_num+1}_{img_index}.{base_image['ext']}"
            with open(os.path.join(output_dir, "images", image_filename), "wb") as f:
                f.write(base_image["image"])

        # 3. Chụp lại toàn bộ trang (Dùng để lấy Diagram/Sơ đồ)
        # Tăng zoom lên 2.0 để hình ảnh sơ đồ sắc nét hơn
        mat = fitz.Matrix(2, 2) 
        pix = page.get_pixmap(matrix=mat)
        pix.save(os.path.join(output_dir, "pages", f"page_{page_num + 1}.png"))

    # Lưu toàn bộ text vào file
    with open(os.path.join(output_dir, "extracted_text.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(full_text))

    doc.close()
    print(f"Xử lý hoàn tất! Dữ liệu được lưu tại thư mục: {output_dir}")

if __name__ == "__main__":
    import sys
    import os
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        base_name = os.path.basename(pdf_path).replace('.pdf', '')
        output_dir = f"/Users/bean/AI/C401_E4_Day05/src/tools/output/{base_name}"
    else:
        pdf_path = "/Users/bean/AI/C401_E4_Day05/src/tools/B5.pdf"
        output_dir = "/Users/bean/AI/C401_E4_Day05/src/tools/output/B5"

    process_pdf(pdf_path, output_dir=output_dir)