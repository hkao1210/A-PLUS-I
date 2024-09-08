from doctr.io import DocumentFile
from doctr.models import ocr_predictor, kie_predictor
import cv2
import os

model = ocr_predictor('db_resnet50', 'crnn_vgg16_bn', pretrained=True, assume_straight_pages=False)
modelv2 = kie_predictor(pretrained=True)


# PDF
pdf_doc = DocumentFile.from_pdf("./Andy_Deng_July_2024_Resume.pdf")

# # Image
# single_img_doc = DocumentFile.from_images("path/to/your/img.jpg")

# # Multiple page images
# multi_img_doc = DocumentFile.from_images(["path/to/page1.jpg", "path/to/page2.jpg"])


# def extract_words_and_predictions(result):
#     extracted_words = []
#     all_predictions = []

#     predictions = result.pages[0].predictions

#     return predictions.value()

# Class type prediction
result = model(pdf_doc)
# extracted_words = extract_words_and_predictions(result)
# print(f"Extracted words: {extracted_words}")

# predictions = result.pages[0].predictions["words"]

# List comprehension to extract the 'value' of each prediction
# extracted_words = [word.value for word in predictions]
print(result.render())

