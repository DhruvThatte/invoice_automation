from pathlib import Path

import cv2
import pytesseract
from PIL import Image


def validate_image_path(
    image_path: str | Path,
) -> Path:

    image_path = Path(image_path)

    if not image_path.exists():
        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    if not image_path.is_file():
        raise ValueError(
            f"Path is not a file: {image_path}"
        )

    valid_extensions = {
        ".png",
        ".jpg",
        ".jpeg",
        ".tiff",
        ".tif",
        ".bmp",
        ".webp",
    }

    if image_path.suffix.lower() not in valid_extensions:
        raise ValueError(
            f"Unsupported image format: "
            f"{image_path.suffix}"
        )

    return image_path


def preprocess_image(
    image_path: str | Path,
):
    """
    Preprocess an invoice image before OCR.

    Steps:
        1. Read image
        2. Convert to grayscale
        3. Remove noise
        4. Apply thresholding
    """

    image_path = validate_image_path(
        image_path
    )

    image = cv2.imread(
        str(image_path)
    )

    if image is None:
        raise ValueError(
            f"Unable to read image: {image_path}"
        )

    # Convert to grayscale
    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY,
    )

    # Reduce small noise
    denoised = cv2.GaussianBlur(
        gray,
        (5, 5),
        0,
    )

    # Convert to black and white
    _, thresholded = cv2.threshold(
        denoised,
        0,
        255,
        cv2.THRESH_BINARY
        + cv2.THRESH_OTSU,
    )

    return thresholded


def extract_text_from_image(
    image_path: str | Path,
    preprocess: bool = True,
) -> str:
    """
    Extract text from an image using Tesseract OCR.
    """

    image_path = validate_image_path(
        image_path
    )

    try:

        if preprocess:
            image = preprocess_image(
                image_path
            )

            text = pytesseract.image_to_string(
                image
            )

        else:
            image = Image.open(
                image_path
            )

            text = pytesseract.image_to_string(
                image
            )

    except Exception as error:
        raise RuntimeError(
            f"OCR failed for: {image_path}"
        ) from error

    return text.strip()
def save_preprocessed_image(
    image_path: str | Path, 
    output_path: str | Path,
):
    """
    Preprocess an image and save the result.
    """

    processed = preprocess_image(
        image_path
    )

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    success = cv2.imwrite(
        str(output_path),
        processed,
    )

    if not success:
        raise RuntimeError(
            "Failed to save processed image."
        )

    return output_path