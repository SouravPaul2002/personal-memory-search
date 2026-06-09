from PIL import Image
import pytesseract

# Windows path
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe" #personal laptop
    # r"D:\sourav paul\New folder\tesseract.exe" #office laptop
)


def extract_text_from_image(image_path):

    try:

        image = Image.open(image_path)

        image = image.convert("L")

        image = image.resize(
            (image.width * 2,
            image.height * 2)
        )

        text = pytesseract.image_to_string(
            image,
            config="--psm 6"
        )

        return text

    except Exception as e:

        print(
            f"OCR Error: {e}"
        )

        return ""