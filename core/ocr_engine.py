import pytesseract, cv2, sys, os

def extract_text(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return pytesseract.image_to_string(gray, lang="kor")

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller 임시폴더
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

pytesseract.pytesseract.tesseract_cmd = resource_path(
    "external/Tesseract-OCR/tesseract.exe"
)