from typing import List, Tuple

import numpy as np


# Encode mask
def rle_encoding(x: np.array):
    """
    Encode binary mask to RLE

    Args:
        x (np.array): numpy array of shape (height, width), 1 - mask, 0 - background
    Returns run length as list
    """
    dots = np.where(x.flatten() == 1)[0]  # Order right-then-down
    run_lengths = []
    prev = -2
    for b in dots:
        if b > prev + 1:
            run_lengths.extend((b + 1, 0))
        run_lengths[-1] += 1
        prev = b
    return run_lengths


# Decode mask
def rle_decode(mask_rle: List[int], shape: Tuple[int]):
    """
    Decodes mask from RLE format to binary mask. Returns numpy array, 1 - mask, 0 - background

    Args:
        mask_rle (list): run-length as string formated (start length)
        shape (tuple): (width, height) of array to return
    """
    s = mask_rle
    starts, lengths = [np.asarray(x, dtype=int) for x in (s[0:][::2], s[1:][::2])]
    starts -= 1
    ends = starts + lengths
    shape = shape[1], shape[0]
    img = np.zeros(shape[0] * shape[1], dtype=np.uint8)
    for lo, hi in zip(starts, ends):
        img[lo:hi] = 1
    return img.reshape(shape)


def yolo2hasty(yolo_bbox: List[float], image_width: int, image_height: int):
    """
    Converts normalized YOLO bbox format (Xn_center, Yn_center, Wn, Hn) to Hasty format (x_min, y_min, x_max, y_max)

    Args:
         yolo_bbox (list of floats): Normalized coordinates [X_center, Y_center, W, H] example [0.3, 0.4, 0.1, 0.25]
         image_width (int): Image width
         image_height (int): Image height
    """
    bbox = [
        int((float(yolo_bbox[1]) - float(yolo_bbox[3]) / 2) * image_width),
        int((float(yolo_bbox[2]) - float(yolo_bbox[4]) / 2) * image_height),
        int((float(yolo_bbox[1]) + float(yolo_bbox[3]) / 2) * image_width),
        int((float(yolo_bbox[2]) + float(yolo_bbox[4]) / 2) * image_height),
    ]
    return bbox


def check_bbox_format(bbox):
    if len(bbox) != 4:
        return False
    if bbox[2] <= bbox[0]:
        return False
    if bbox[3] <= bbox[1]:
        return False
    return True


def check_rle_mask(bbox, mask):
    if bbox is None:
        return False
    if mask is None:
        return False
    bbox_area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
    rle_area = mask[-2] - 1 + mask[-1]
    if rle_area > bbox_area:
        return False
    return True


def polygon_area(polygon):
    np_poly = np.array(polygon)
    x, y = np_poly[:, 0], np_poly[:, 1]
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))


def polygon2box(polygon: List[List[int]]):
    """
    Converts polygon to bounding box [x_min, y_min, x_max, y_max]

    Args:
        polygon: List of x, y pairs [[x0, y0], [x1, y1], .... [x0, y0]]
    """
    min_x, min_y, max_x, max_y = [None] * 4

    for item in polygon:
        x, y = item[0], item[1]
        if min_x is None or x < min_x:
            min_x = x
        if min_y is None or y < min_y:
            min_y = y
        if max_x is None or x > max_x:
            max_x = x
        if max_y is None or y > max_y:
            max_y = y

    bbox = [min_x, min_y, max_x, max_y]
    assert all([b is not None for b in bbox]), "Empty sequence"
    return bbox
