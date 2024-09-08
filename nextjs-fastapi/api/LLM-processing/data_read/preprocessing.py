# Preprocessing the document inputs
import cv2

def preprocess_image(image):
    # Convert grayscale
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Histogram Equalization
    img = cv2.equalizeHist(img)


    # Define alpha (contrast) and beta (brightness)
    alpha = 1.5 # Contrast control (1.0-3.0)
    beta = 50   # Brightness control (0-100)

    # Adjust the contrast and brightness
    adjusted = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

    return adjusted

if __name__ == "__main__":
    # Load an image
    image = cv2.imread("path/to/your/img.jpg")

    # Preprocess the image
    preprocessed_image = preprocess_image(image)

    # Display the preprocessed image
    cv2.imshow("Preprocessed Image", preprocessed_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()