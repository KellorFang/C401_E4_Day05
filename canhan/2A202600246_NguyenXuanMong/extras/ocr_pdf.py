"""
Slide PDF Parser — Trích xuất thông tin bài giảng dạng slide
=============================================================
Dành cho: PDF slide (mỗi trang = 1 ảnh, không có text layer)

Khả năng:
  ✅ OCR text từ toàn bộ slide
  ✅ Phát hiện và crop diagram / flowchart / sơ đồ
  ✅ Trích xuất text trong từng box của diagram
  ✅ Xuất Markdown có cấu trúc (text + ảnh diagram)
  ✅ Chạy hoàn toàn local, tối ưu cho M3

Thư viện cần:
  pip install rapidocr-onnxruntime  (đã cài)
  PyMuPDF, opencv-python-headless, Pillow  (đã cài)
"""

import os
import io
import json
import re
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field

import fitz          # PyMuPDF
import cv2
from PIL import Image


# ═══════════════════════════════════════════════════════════════════
# CẤU HÌNH
# ═══════════════════════════════════════════════════════════════════

DEFAULT_DPI   = 200       # Độ phân giải render slide (cao hơn = OCR chính xác hơn)
MIN_BOX_AREA  = 3000      # Diện tích tối thiểu để coi là 1 box diagram (px²)
MIN_DIAGRAM_BOXES = 2     # Số box tối thiểu để coi là vùng diagram
DIAGRAM_PADDING   = 15    # Pixel padding khi crop diagram


# ═══════════════════════════════════════════════════════════════════
# DATA STRUCTURES
# ═══════════════════════════════════════════════════════════════════

@dataclass
class DiagramRegion:
    """Một vùng diagram được phát hiện trong slide"""
    bbox: Tuple[int, int, int, int]   # (x, y, w, h) trong ảnh pixel
    boxes: List[Tuple]                # Các box nhỏ bên trong (bbox của từng node)
    image_path: str = ""              # Đường dẫn ảnh đã crop
    inner_texts: List[str] = field(default_factory=list)  # Text trong các box
    markdown_repr: str = ""           # Biểu diễn sơ bộ dạng markdown

    def to_markdown(self) -> str:
        if self.markdown_repr:
            return self.markdown_repr
        if self.inner_texts:
            lines = [f"```diagram\n"]
            for t in self.inner_texts:
                lines.append(f"  [ {t} ]\n")
            lines.append("```")
            return "".join(lines)
        return f"![Diagram]({self.image_path})"


@dataclass
class SlideContent:
    """Nội dung đầy đủ của 1 slide"""
    page: int
    full_text: str = ""                              # Toàn bộ text OCR của slide
    diagram_regions: List[DiagramRegion] = field(default_factory=list)
    slide_image_path: str = ""                       # Ảnh full slide
    metadata: Dict = field(default_factory=dict)

    def to_markdown(self) -> str:
        """Tạo Markdown gọn, chỉ chứa nội dung chính của slide"""
        lines = [f"## Slide {self.page}"]

        # ── Text chính từ OCR toàn slide ────────────────────────
        if self.full_text.strip():
            clean = re.sub(r"\n{3,}", "\n\n", self.full_text.strip())
            lines.append(clean)

        # ── Text bên trong các diagram (nếu OCR được) ───────────
        diagram_texts = []
        for region in self.diagram_regions:
            # Lọc lấy text trong diagram mà chưa nằm trong full_text
            for t in region.inner_texts:
                if t.strip() and t.strip() not in self.full_text:
                    diagram_texts.append(t.strip())

        if diagram_texts:
            lines.append("\n**Nội dung sơ đồ / diagram:**")
            for t in diagram_texts:
                lines.append(f"- {t}")

        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════
# OCR ENGINE (RapidOCR — local, không cần system deps)
# ═══════════════════════════════════════════════════════════════════

_ocr_engine = None

def get_ocr_engine():
    """Singleton OCR engine"""
    global _ocr_engine
    if _ocr_engine is None:
        from rapidocr_onnxruntime import RapidOCR
        _ocr_engine = RapidOCR()
    return _ocr_engine


def ocr_image(img: np.ndarray) -> str:
    """
    OCR một ảnh numpy array (BGR hoặc RGB), trả về text string.
    RapidOCR hỗ trợ tiếng Anh, Trung, và nhiều ký tự Latin (tiếng Việt cơ bản).
    """
    engine = get_ocr_engine()
    result, _ = engine(img)
    if not result:
        return ""
    # result = list of [bbox, text, confidence]
    texts = [line[1] for line in result if line[1].strip()]
    return "\n".join(texts)


def ocr_pil(pil_img: Image.Image) -> str:
    """OCR từ PIL Image"""
    arr = np.array(pil_img.convert("RGB"))
    return ocr_image(arr)


# ═══════════════════════════════════════════════════════════════════
# DIAGRAM DETECTOR (OpenCV-based)
# ═══════════════════════════════════════════════════════════════════

class DiagramDetector:
    """
    Phát hiện vùng diagram trong slide dùng OpenCV.

    Chiến lược kép:
    1. Tìm hình chữ nhật (box nodes của flowchart/diagram)
    2. Nếu không tìm thấy đủ box, tìm vùng "đặc" (dense edges) → likely diagram
    """

    def __init__(
        self,
        min_box_area: int = MIN_BOX_AREA,
        min_boxes_per_diagram: int = MIN_DIAGRAM_BOXES,
        padding: int = DIAGRAM_PADDING,
    ):
        self.min_box_area = min_box_area
        self.min_boxes = min_boxes_per_diagram
        self.padding = padding

    def detect(self, img_bgr: np.ndarray) -> List[DiagramRegion]:
        """
        Phát hiện tất cả diagram regions trong ảnh slide.
        """
        h, w = img_bgr.shape[:2]

        # ── Chiến lược 1: tìm hình chữ nhật ─────────────────────
        boxes = self._find_boxes(img_bgr)
        if len(boxes) >= self.min_boxes:
            clusters = self._cluster_boxes(boxes, max_gap=w * 0.20)
            regions = []
            for cluster in clusters:
                if len(cluster) >= self.min_boxes:
                    region_bbox = self._bounding_box_of_cluster(cluster, w, h)
                    # Bỏ qua region bao phủ quá nhiều slide (>70%)  
                    rx, ry, rw, rh = region_bbox
                    if rw * rh > 0.7 * w * h:
                        continue
                    regions.append(DiagramRegion(bbox=region_bbox, boxes=cluster))
            if regions:
                return regions

        # ── Chiến lược 2: tìm vùng có mật độ cạnh cao ───────────
        return self._find_dense_regions(img_bgr)

    def _find_boxes(self, img_bgr: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """Tìm hình chữ nhật trong slide"""
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape

        # Invert nếu background tối
        mean_val = gray.mean()
        if mean_val < 128:
            gray = cv2.bitwise_not(gray)

        # Adaptive threshold
        thresh = cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV, 15, 3
        )

        # Morphological closing để liên kết các đường gần nhau
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

        contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        boxes = []
        max_area = h * w * 0.60

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < self.min_box_area or area > max_area:
                continue

            x, y, bw, bh = cv2.boundingRect(cnt)
            aspect = bw / bh if bh > 0 else 0
            if 0.1 < aspect < 12:
                boxes.append((x, y, bw, bh))

        return boxes

    def _find_dense_regions(self, img_bgr: np.ndarray) -> List[DiagramRegion]:
        """
        Fallback: Tìm vùng có nhiều edges / đường kẻ → khả năng cao là diagram.
        Phân tích theo grid, tìm cell có mật độ edge cao.
        """
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape

        edges = cv2.Canny(gray, 30, 80)

        # Chia slide thành grid 6×4
        rows, cols = 4, 6
        cell_h, cell_w = h // rows, w // cols

        dense_cells = []
        edge_density_map = []

        for r in range(rows):
            for c in range(cols):
                y1, y2 = r * cell_h, (r + 1) * cell_h
                x1, x2 = c * cell_w, (c + 1) * cell_w
                cell = edges[y1:y2, x1:x2]
                density = cell.mean()
                edge_density_map.append((r, c, density, x1, y1, cell_w, cell_h))

        # Ngưỡng: top 25% cell có density cao nhất
        densities = [e[2] for e in edge_density_map]
        threshold = np.percentile(densities, 75)
        dense = [e for e in edge_density_map if e[2] > threshold and e[2] > 10]

        if not dense:
            return []

        # Cluster các cell liền kề → 1 region
        regions = []
        visited = set()

        def get_neighbors(r, c):
            return [(r-1,c),(r+1,c),(r,c-1),(r,c+1)]

        cell_set = {(e[0], e[1]) for e in dense}

        for entry in dense:
            r, c = entry[0], entry[1]
            if (r, c) in visited:
                continue

            # BFS để gom cluster
            cluster_cells = []
            queue = [(r, c)]
            while queue:
                cr, cc = queue.pop()
                if (cr, cc) in visited or (cr, cc) not in cell_set:
                    continue
                visited.add((cr, cc))
                cluster_cells.append((cr, cc))
                for nr, nc in get_neighbors(cr, cc):
                    if (nr, nc) not in visited and (nr, nc) in cell_set:
                        queue.append((nr, nc))

            if len(cluster_cells) < 2:
                continue

            # Tính bounding box của cluster
            rs = [cc[0] for cc in cluster_cells]
            cs_ = [cc[1] for cc in cluster_cells]
            min_r, max_r = min(rs), max(rs)
            min_c, max_c = min(cs_), max(cs_)

            x = max(0, min_c * cell_w - self.padding)
            y = max(0, min_r * cell_h - self.padding)
            x2 = min(w, (max_c + 1) * cell_w + self.padding)
            y2 = min(h, (max_r + 1) * cell_h + self.padding)

            # Bỏ qua region bao phủ quá nhiều slide
            if (x2 - x) * (y2 - y) > 0.65 * w * h:
                continue

            bbox = (x, y, x2 - x, y2 - y)
            regions.append(DiagramRegion(bbox=bbox, boxes=[]))

        return regions

    def _cluster_boxes(
        self, boxes: List[Tuple], max_gap: float
    ) -> List[List[Tuple]]:
        """Gộp các box gần nhau thành cluster"""
        if not boxes:
            return []

        clusters = []
        used = set()

        for i, box_i in enumerate(boxes):
            if i in used:
                continue
            cluster = [box_i]
            used.add(i)
            xi, yi, wi, hi = box_i

            for j, box_j in enumerate(boxes):
                if j in used:
                    continue
                xj, yj, wj, hj = box_j
                dist = max(
                    abs((xi + wi/2) - (xj + wj/2)),
                    abs((yi + hi/2) - (yj + hj/2))
                )
                if dist < max_gap:
                    cluster.append(box_j)
                    used.add(j)

            clusters.append(cluster)

        return clusters

    def _bounding_box_of_cluster(
        self, cluster: List[Tuple], img_w: int, img_h: int
    ) -> Tuple[int, int, int, int]:
        """Bounding box bao quanh toàn bộ cluster"""
        xs  = [b[0]        for b in cluster]
        ys  = [b[1]        for b in cluster]
        xe  = [b[0] + b[2] for b in cluster]
        ye  = [b[1] + b[3] for b in cluster]

        x  = max(0,     min(xs)  - self.padding)
        y  = max(0,     min(ys)  - self.padding)
        x2 = min(img_w, max(xe)  + self.padding)
        y2 = min(img_h, max(ye)  + self.padding)

        return (x, y, x2 - x, y2 - y)



# ═══════════════════════════════════════════════════════════════════
# SLIDE PDF PARSER
# ═══════════════════════════════════════════════════════════════════

class SlidesPDFParser:
    """
    Parser tối ưu cho PDF bài giảng dạng slide.

    Mỗi trang slide được:
    1. Render thành ảnh (PyMuPDF)
    2. OCR toàn bộ để lấy text
    3. Phân tích bằng OpenCV để tìm diagram
    4. Crop + lưu các diagram regions
    5. OCR text bên trong từng diagram
    6. Xuất Markdown có cấu trúc
    """

    def __init__(
        self,
        pdf_path: str,
        output_dir: str = "slide_output",
        dpi: int = DEFAULT_DPI,
        detect_diagrams: bool = True,
        save_slide_images: bool = False,  # Lưu toàn bộ ảnh slide (tốn ổ đĩa)
    ):
        self.pdf_path = pdf_path
        self.output_dir = Path(output_dir)
        self.dpi = dpi
        self.detect_diagrams = detect_diagrams
        self.save_slide_images = save_slide_images

        self.pdf_name = Path(pdf_path).stem
        self.doc = fitz.open(pdf_path)
        self.detector = DiagramDetector()

        # Tạo thư mục lưu kết quả
        self.diagrams_dir = self.output_dir / "diagrams" / self.pdf_name
        self.slides_dir   = self.output_dir / "slides"   / self.pdf_name
        self.diagrams_dir.mkdir(parents=True, exist_ok=True)
        if save_slide_images:
            self.slides_dir.mkdir(parents=True, exist_ok=True)

        total = len(self.doc)
        print(f"📚 Đã mở: {Path(pdf_path).name}  ({total} slide)")

    # ─────────────────────────────────────────────────────────────
    # PUBLIC API
    # ─────────────────────────────────────────────────────────────

    def parse(
        self,
        start_page: int = 1,
        end_page: Optional[int] = None,
    ) -> List[SlideContent]:
        """
        Parse từ start_page đến end_page.
        Trả về danh sách SlideContent.
        """
        if end_page is None or end_page > len(self.doc):
            end_page = len(self.doc)

        print(f"🚀 Parse slide {start_page} → {end_page}...\n")

        # Khởi động OCR engine trước (tải model 1 lần)
        print("🔧 Khởi động OCR engine...")
        get_ocr_engine()
        print("✅ OCR sẵn sàng!\n")

        results = []
        for page_idx in range(start_page - 1, end_page):
            page_num = page_idx + 1
            content = self._parse_slide(page_idx, page_num)
            results.append(content)

            diag_info = f", {len(content.diagram_regions)} diagram" if content.diagram_regions else ""
            text_chars = len(content.full_text.strip())
            print(f"  ✅ Slide {page_num:3d}: {text_chars:5d} ký tự{diag_info}")

        return results

    def save_markdown(
        self,
        slides: List[SlideContent],
        output_file: Optional[str] = None,
    ) -> str:
        """Lưu toàn bộ kết quả ra file Markdown"""
        if output_file is None:
            output_file = str(self.output_dir / f"{self.pdf_name}.md")

        Path(output_file).parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"# {self.pdf_name}\n\n")

            for slide in slides:
                f.write(slide.to_markdown())
                f.write("\n\n---\n\n")

        print(f"\n💾 Đã lưu: {output_file}")
        return output_file

    def save_json(
        self,
        slides: List[SlideContent],
        output_file: Optional[str] = None,
    ) -> str:
        """Lưu metadata JSON"""
        if output_file is None:
            output_file = str(self.output_dir / f"{self.pdf_name}_meta.json")

        data = [
            {
                "page": s.page,
                "text": s.full_text,
                "diagrams": [
                    {
                        "bbox": d.bbox,
                        "image": d.image_path,
                        "texts_in_boxes": d.inner_texts,
                    }
                    for d in s.diagram_regions
                ],
            }
            for s in slides
        ]

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"💾 Đã lưu JSON: {output_file}")
        return output_file

    def close(self):
        self.doc.close()

    # ─────────────────────────────────────────────────────────────
    # INTERNAL: PARSE 1 SLIDE
    # ─────────────────────────────────────────────────────────────

    def _parse_slide(self, page_idx: int, page_num: int) -> SlideContent:
        """Xử lý đầy đủ 1 slide: render → OCR → diagram detection"""
        page = self.doc[page_idx]

        # ── 1. Render slide → PIL Image ──────────────────────────
        mat = fitz.Matrix(self.dpi / 72, self.dpi / 72)
        pix = page.get_pixmap(matrix=mat, colorspace=fitz.csRGB)
        img_bytes = pix.tobytes("png")
        pil_img = Image.open(io.BytesIO(img_bytes))
        img_bgr = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

        content = SlideContent(page=page_num)

        # ── 2. Lưu ảnh toàn slide (nếu cần) ─────────────────────
        if self.save_slide_images:
            slide_path = str(self.slides_dir / f"slide_{page_num:03d}.png")
            pil_img.save(slide_path)
            content.slide_image_path = slide_path

        # ── 3. OCR toàn bộ slide ─────────────────────────────────
        full_text = ocr_image(img_bgr)
        content.full_text = full_text

        # ── 4. Phát hiện Diagram ──────────────────────────────────
        if self.detect_diagrams:
            regions = self.detector.detect(img_bgr)

            for r_idx, region in enumerate(regions):
                x, y, rw, rh = region.bbox

                # Crop vùng diagram
                crop_bgr = img_bgr[y:y+rh, x:x+rw]
                crop_pil = Image.fromarray(cv2.cvtColor(crop_bgr, cv2.COLOR_BGR2RGB))

                # Lưu ảnh diagram
                diag_filename = f"slide{page_num:03d}_diagram{r_idx+1:02d}.png"
                diag_path = str(self.diagrams_dir / diag_filename)
                crop_pil.save(diag_path)
                region.image_path = diag_path

                # OCR text trong từng box nhỏ của diagram
                inner_texts = []
                for (bx, by, bw, bh) in region.boxes:
                    # Tọa độ tương đối trong crop
                    rx = max(0, bx - x)
                    ry = max(0, by - y)
                    box_crop = crop_bgr[ry:ry+bh, rx:rx+bw]
                    if box_crop.size == 0:
                        continue
                    box_text = ocr_image(box_crop).strip()
                    if box_text and len(box_text) > 1:
                        inner_texts.append(box_text)

                region.inner_texts = inner_texts

                # Tạo biểu diễn Markdown của diagram
                region.markdown_repr = self._build_diagram_markdown(inner_texts)

                content.diagram_regions.append(region)

        return content

    def _build_diagram_markdown(self, texts: List[str]) -> str:
        """
        Tạo biểu diễn sơ bộ hình thức markdown/ASCII cho diagram.
        Mỗi text (node) được biểu diễn là 1 khối.
        """
        if not texts:
            return ""

        lines = []
        n = len(texts)

        if n == 1:
            return f"[ {texts[0]} ]"

        # Heuristic: sắp xếp theo luồng (flow diagram)
        # Nếu <= 5 node → hiển thị theo hàng ngang
        # Nếu > 5 node → hiển thị dạng danh sách
        if n <= 5:
            parts = [f"[ {t} ]" for t in texts]
            return " → ".join(parts)
        else:
            lines.append("Flowchart / Sơ đồ các bước:")
            for i, t in enumerate(texts, 1):
                lines.append(f"  {i}. {t}")
            return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import time

    PDF_PATH   = "/Users/mong/Documents/ComputerScience/AI4SE/AI_ThucChien/lesson_docs/B3.pdf"
    OUTPUT_DIR = "slide_output"

    print("=" * 60)
    print("  Slide PDF Parser — Local, M3 Optimized")
    print("=" * 60)

    t0 = time.time()

    parser = SlidesPDFParser(
        pdf_path          = PDF_PATH,
        output_dir        = OUTPUT_DIR,
        dpi               = 200,    # 200 DPI cho OCR chính xác
        detect_diagrams   = True,   # Phát hiện diagram
        save_slide_images = False,  # Không lưu ảnh toàn slide (tiết kiệm ổ đĩa)
    )

    # Parse slide 5–10 (đổi end_page=None để parse toàn bộ)
    slides = parser.parse(start_page=1, end_page=None)

    # Chỉ lưu 1 file .md
    md_path = parser.save_markdown(slides)
    parser.close()

    elapsed = time.time() - t0

    print(f"\n{'='*60}")
    print(f"  ⏱️  Tổng thời gian  : {elapsed:.1f}s ({elapsed/len(slides):.1f}s/slide)")
    print(f"  📝 Text trích xuất : {sum(len(s.full_text) for s in slides):,} ký tự")
    print(f"  📊 Diagram phát hiện: {sum(len(s.diagram_regions) for s in slides)}")
    print(f"  📄 Output           : {md_path}")
    print(f"{'='*60}")

    # Preview slide đầu tiên
    if slides:
        print(f"\n📖 Preview Slide {slides[0].page}:")
        print("-" * 40)
        preview = slides[0].to_markdown()
        print(preview[:600])