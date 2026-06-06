from backend.services.image_service import (
    extract_text_from_image
)
from backend.services.text_cleaner import clean_ocr_text

image_path = "data/images/test.jpeg"

text = extract_text_from_image(
    image_path
)
# text= clean_ocr_text(text) #not usefull 

print(text)