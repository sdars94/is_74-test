import base64

import cv2
import numpy as np

from .conf import celery


@celery.task
def process_image(image_bytes: bytes | bytearray) -> bytes:
    image_np = convert_bytes_to_numpy(image_bytes)
    image_cv2 = decode_image(image_np)
    resized_image = resize_image(image_cv2, width=640, height=640)
    normalized_image = normalize_image(resized_image)
    image_base64 = encode_image_to_base64(normalized_image)
    return image_base64


def convert_bytes_to_numpy(image_bytes: bytes) -> np.ndarray:
    return np.frombuffer(image_bytes, dtype=np.uint8)


def decode_image(image_np: np.ndarray) -> np.ndarray:
    return cv2.imdecode(image_np, cv2.IMREAD_COLOR)


def resize_image(image: np.ndarray, width: int, height: int) -> np.ndarray:
    return cv2.resize(image, (width, height))


def normalize_image(image: np.ndarray) -> np.ndarray:
    normalized_image = np.copy(image)
    cv2.normalize(
        image,
        normalized_image,
        alpha=0,
        beta=255,
        norm_type=cv2.NORM_MINMAX,
        dtype=cv2.CV_8U,
    )
    return normalized_image


def encode_image_to_base64(image: np.ndarray) -> bytes:
    _, encoded_image = cv2.imencode(".jpg", image)
    return base64.b64encode(encoded_image.tobytes())
