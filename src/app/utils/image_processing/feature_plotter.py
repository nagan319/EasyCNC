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
    
    def save_features(self):
        """
        Saves image with properties specified at initialization.
        Returns True if successful, False otherwise.
        """
        canvas = np.zeros((self.size.h, self.size.w, 3), dtype=np.uint8)
        canvas[:, :] = list(self.colors.background_color)

        """ Draw plate contour if available """
        if self.features.plate_contour is not None:
            try:
                self._draw_contour_points(canvas, self.features.plate_contour, self.colors.plate_color)
                logger.debug("Successfully plotted plate contour")
            except Exception as e:
                print("Exception occured during plate contour stage")
                raise e

        """ Draw other contours """
        if self.features.other_contours is not None:
            for idx, contour in enumerate(self.features.other_contours):
                color = self.colors.selected_element_color if idx == self.features.selected_contour_idx else self.colors.contour_color
                try:
                    self._draw_contour_points(canvas, contour, color)
                except Exception as e: 
                    logger.error("Exception occured during other contour stage")
                    raise e
                logger.debug("Successfully plotted other contours")

        """ Draw corners as individual points """
        if self.features.corners is not None:
            for idx, corner in enumerate(self.features.corners):
                radius = 5 
                color = self.colors.selected_element_color if idx == self.features.selected_corner_idx else self.colors.corner_color
                try:
                    cv2.circle(canvas, tuple(corner), radius, color, -1)  
                except Exception as e:
                    logger.error("Exception occured during corner stage")
                    raise e
            logger.debug("Successfully plotted corners")

        """ Save canvas to file """
        try:
            cv2.imwrite(self.dst_path, canvas)
            logger.debug("Successfully performed cv2.imwrite")
        except Exception as e:
            logger.error(f"Exception while performing cv2 imwrite: {e}")
            raise e

    def _draw_contour_points(self, canvas, contour, color):
        """
        Draw each point in the contour as a separate point on the canvas.
        """
        for i, point in enumerate(contour):
            x, y = int(point[0][0]), int(point[0][1])
            try:
                cv2.circle(canvas, (x, y), 1, color, -1)  
            except Exception as e:
                logger.error(f"Encountered exception while attempting to draw point number {i}, {(x, y)}: {e}")
                print(f"Encountered exception while attempting to draw point number {i}, {(x, y)}: {e}")
                raise e
