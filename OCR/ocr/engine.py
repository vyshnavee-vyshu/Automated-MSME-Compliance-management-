"""PaddleOCR PP-OCRv5 mobile wrapper — CPU-only, low compute/memory footprint.

Mobile det/rec models trade a small amount of accuracy for size/speed vs the
server variants; doc orientation classification + unwarping are enabled
because source documents arrive as phone photos (per project spec), not
flat scans.
"""
from paddleocr import PaddleOCR

_engine = None


def get_engine() -> PaddleOCR:
    global _engine
    if _engine is None:
        _engine = PaddleOCR(
            lang="en",
            ocr_version="PP-OCRv5",
            text_detection_model_name="PP-OCRv5_mobile_det",
            text_recognition_model_name="PP-OCRv5_mobile_rec",
            device="cpu",
            enable_mkldnn=False,  # True crashes on this Paddle build: oneDNN
            # rejects ConvertPirAttribute2RuntimeAttribute for ArrayAttribute<DoubleAttribute>
            use_doc_orientation_classify=True,
            use_doc_unwarping=True,
            use_textline_orientation=True,
        )
    return _engine


def run_ocr(file_path: str) -> list[list[dict]]:
    """Runs OCR on an image or PDF path (PaddleOCR rasterizes PDF pages
    internally). Returns one list of line results per page:
    [[{"text": str, "confidence": float, "bbox": [[x,y], ...]}, ...], ...]
    """
    engine = get_engine()
    results = engine.predict(file_path)

    pages = []
    for page_result in results:
        texts = page_result.get("rec_texts", [])
        scores = page_result.get("rec_scores", [])
        polys = page_result.get("rec_polys", [])
        lines = [
            {
                "text": text,
                "confidence": float(score),
                "bbox": poly.tolist() if hasattr(poly, "tolist") else poly,
            }
            for text, score, poly in zip(texts, scores, polys)
        ]
        pages.append(lines)
    return pages
