import cv2 as cv
import numpy as np

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

def circle(
    img: np.array,
    top_offset: int,
    left_offset: int,
    field_resolution: int,
    field_padding: int,
    color: tuple
) -> None:
    center = (
        left_offset + int(field_resolution / 2),
        top_offset + int(field_resolution / 2)
    )
    size = (int(field_resolution / 2) - field_padding, int(field_resolution / 2) - field_padding)
    cv.ellipse(img, center, size, angle=0, startAngle=0, endAngle=360, color=color, thickness=-1)

def rectangle(
    img: np.array,
    top_offset: int,
    left_offset: int,
    field_resolution: int,
    field_padding: int,
    color: tuple
) -> None:
    top_left = (left_offset + field_padding, top_offset + field_padding)
    bottom_right = (left_offset + field_resolution - field_padding, top_offset + field_resolution - field_padding)
    cv.rectangle(img, pt1=top_left, pt2=bottom_right, color=color, thickness=-1)

def triangle(
    img: np.array,
    top_offset: int,
    left_offset: int,
    field_resolution: int,
    field_padding: int,
    color: tuple
) -> None:
    bottom_left = (left_offset + field_padding, top_offset + field_resolution - field_padding)
    bottom_right = (left_offset + field_resolution - field_padding, top_offset + field_resolution - field_padding)
    center_top = (left_offset + int(field_resolution / 2), top_offset + field_padding)
    pts=np.array([bottom_left, bottom_right, center_top])
    cv.fillPoly(img, pts=[pts], color=color)


colors = (RED, GREEN, BLUE)
shapes = (circle, rectangle, triangle)


def generate_shapes(permutations: np.array, field_resolution: int = 28, field_padding: int = 5, blur: float = 0.):
    shape_permutations = []
    size = int(np.sqrt(permutations.shape[1]))

    for p in permutations:
        image = np.zeros((field_resolution * size, field_resolution * size, size))
        for row in range(size):
            for col in range(size):
                permutation_index = row * size + col
                permutation_value = p[permutation_index]
                if (permutation_value >= permutations.shape[1]):
                    # Deletion occured at this position
                    continue
                perm_row, perm_col = (permutation_value // size, permutation_value % size)
                top_offset = row * field_resolution
                left_offset = col * field_resolution

                shapes[perm_row](image, top_offset, left_offset, field_resolution, field_padding, colors[perm_col])
        if blur != 0:
            image = cv.GaussianBlur(image, ksize=(5, 5), sigmaX=blur)
        shape_permutations.append(image)    
    return shape_permutations