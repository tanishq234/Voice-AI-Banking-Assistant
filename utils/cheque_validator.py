"""
Cheque Validator — OpenCV + PIL based image validation
Validates whether an uploaded image is a valid cheque.
"""
import io
from typing import Tuple


def validate_cheque_image(uploaded_file) -> Tuple[bool, str]:
    """
    Validate whether the uploaded file is a valid cheque image.

    Returns:
        (True, "Valid cheque") if validation passes
        (False, reason_string) if validation fails
    """
    try:
        if hasattr(uploaded_file, "read"):
            file_bytes = uploaded_file.read()
            if hasattr(uploaded_file, "seek"):
                uploaded_file.seek(0)
        else:
            file_bytes = bytes(uploaded_file)

        file_size = len(file_bytes)
        file_name = getattr(uploaded_file, "name", "unknown.jpg").lower()
        file_type = getattr(uploaded_file, "type", "image/jpeg").lower()

        if file_size < 5_000:  
            return False, "Image is too small. Please upload a clear, full-size cheque photo."

        if file_size > 15 * 1024 * 1024:  
            return False, "Image is too large. Please upload an image under 15 MB."

        allowed_types = ["image/jpeg", "image/jpg", "image/png", "application/pdf"]
        if file_type not in allowed_types:
            return False, "Unsupported file type. Please upload a JPG or PNG image."

        try:
            import numpy as np
            import cv2
            from PIL import Image

            img_pil = Image.open(io.BytesIO(file_bytes)).convert("RGB")
            img_np = np.array(img_pil)

            img_cv = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

            height, width = img_cv.shape[:2]

            if height < 50 or width < 50:
                return False, "Image resolution is too low. Please upload a higher quality image."

            aspect_ratio = width / height
            if aspect_ratio < 0.8:
                return False, "Image appears to be portrait orientation. Cheques are typically landscape."

            gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
            mean_brightness = float(np.mean(gray))

            if mean_brightness < 20:
                return False, "Image is too dark. Please upload a well-lit cheque photo."
            if mean_brightness > 250:
                return False, "Image is overexposed. Please upload a clear cheque photo."

            edges = cv2.Canny(gray, 50, 150)
            edge_density = float(np.sum(edges > 0)) / (height * width)

            if edge_density < 0.001:
                return False, "Image appears to be blank or have no content. Please upload a valid cheque."

            light_pixels = np.sum(gray > 150)
            light_ratio = light_pixels / (height * width)

            if light_ratio < 0.15:
                return False, "Image appears too dark to be a cheque. Please upload a clear scan."

            return True, "Valid cheque image"

        except ImportError:
            return _basic_validate(file_bytes, file_size)

        except Exception as cv_err:
            print(f"[Cheque CV Error] {cv_err}")
            return _basic_validate(file_bytes, file_size)

    except Exception as e:
        print(f"[Cheque Validation Error] {e}")
        return False, "Could not process the uploaded file. Please try again."


def _basic_validate(file_bytes: bytes, file_size: int) -> Tuple[bool, str]:
    """Basic validation without OpenCV — checks file headers."""
    if file_bytes[:3] == b'\xff\xd8\xff':
        return True, "Valid image (JPEG)"
    if file_bytes[:4] == b'\x89PNG':
        return True, "Valid image (PNG)"
    if file_bytes[:4] == b'%PDF':
        return True, "Valid PDF document"

    return False, "Unrecognized file format. Please upload a JPG or PNG cheque image."
