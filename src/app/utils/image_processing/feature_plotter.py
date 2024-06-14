import numpy as np
import cv2

from .utils import Size, Colors
from .features import Features

from ...logging import logger

class FeaturePlotter:
    """
    Saves features as an image.

    ### Parameters:
    - dst_path: Image save path.
    - size: Output image resolution.
    - features: Features to be mapped.
    - colors: Color palette to be used when saving.
    """
    def __init__(self, dst_path: str, size: Size, features: Features, colors: Colors = Colors()):
        self.dst_path = dst_path
        self.size = size
        self.features = features
        self.colors = colors
    
    def save_features(self) -> bool:
        """
        Saves image with properties specified at initialization.
        Returns True if successful, False otherwise.
        """
        try:
            canvas = np.zeros((self.size.h, self.size.w, 3), dtype=np.uint8)
            canvas[:, :] = list(self.colors.background_color)

            """ Thickness and colors vary for selected features. """
            if self.features.plate_contour is not None:
                contours = [self.features.plate_contour.reshape((-1, 1, 2))]
                thickness = 8 
                color = (*self.colors.plate_color, 100)
                cv2.drawContours(canvas, contours, -1, color, thickness, cv2.LINE_AA)

            if self.features.other_contours is not None:
                for idx, contour in enumerate(self.features.other_contours):
                    contour = contour.reshape((-1, 1, 2))
                    thickness = 16 if idx == self.features.selected_contour_idx else 8
                    color = self.colors.selected_element_color if idx == self.features.selected_contour_idx else self.colors.contour_color
                    cv2.drawContours(canvas, [contour], -1, color, thickness, cv2.LINE_AA)

            for idx, corner in enumerate(self.features.corners):
                radius = 76
                color = (*self.colors.selected_element_color, 200) if idx == self.features.selected_corner_idx else (*self.colors.corner_color, 100)
                thickness = 16 if idx == self.features.selected_corner_idx else 8
                cv2.circle(canvas, corner, radius=radius, color=color, thickness=thickness)
                cv2.circle(canvas, corner, radius = 1, color=color, thickness=32)

            cv2.imwrite(self.dst_path, canvas)
            return True
        except Exception as e:
            print(f"Error saving features: {e}")
            return False
