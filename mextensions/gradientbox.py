from enum import Enum

import numpy as np
from colour import Color
from manim import ImageMobject, color_to_int_rgba, interpolate_color


# Helper Class
class GradientBox(ImageMobject):
    """A box that is filled with a gradient"""

    class Direction(Enum):
        horizontal = 1
        vertical = 2

    def __init__(
        self,
        inner_color: Color,
        outer_color: Color,
        direction: Direction = Direction.horizontal,
        width: int = 20,
        height: int = 20,
    ):
        """Creates an :class:`GradientLine` (which is an :class:`ImageMobject`)
        that shows a gradient with the `inner_color` on the left, that is
        interpolated to the `outer_color` towards right.

        The `size` determines the how many pixels are used to render the
        gradient.

        """
        x_start = 0
        x_end = 0

        y_start = 0
        y_end = 1

        if direction == GradientBox.Direction.vertical:
            x_start = 1
            x_end = 0
            y_start = 0
            y_end = 0

        x_axis = np.linspace(x_start, x_end, height)[:, None]
        y_axis = np.linspace(y_start, y_end, width)[None, :]

        intensities = x_axis + y_axis
        intensities = [[min(x, 1) for x in arr] for arr in intensities]

        pixel_array = np.uint8(
            [  # type: ignore
                [
                    color_to_int_rgba(
                        interpolate_color(
                            inner_color,  # type: ignore
                            outer_color,  # type: ignore
                            alpha,
                        )
                    )
                    for alpha in x
                ]
                for x in intensities
            ]
        )

        super().__init__(pixel_array)
