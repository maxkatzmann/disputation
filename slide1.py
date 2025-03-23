from manim import (
    BLACK,
    BLUE,
    Circle,
    Dot,
    FadeIn,
    FadeOut,
    MoveAlongPath,
    PolarPlane,
    linear,
    interpolate_color,
)

from hmanim import native
from manim_presentation_template import DefaultSlide


# Title Slide
class Slide1(DefaultSlide):

    def content(self):
        # We draw a hyperbolic random graph and afterwards move the center of
        # projection in a circular motion which makes for a nice animation.

        # The center of the projection which will move along the circle.
        center_of_projection_dot = Dot().set_opacity(0.0)

        # The plane in which all the content is drawn.
        plane = PolarPlane(size=5)

        # Conversion from the Euclidean plane to the hyperbolic plane.
        def get_hyperbolic_center_of_projection():
            return native.Point(
                *plane.point_to_polar(
                    center_of_projection_dot.get_center()  # type: ignore
                )
            )

        TRANSPARENT_BLUE = interpolate_color(BLACK, BLUE, 0.5)

        # Read the hyperbolic random graph from the files.
        graph = (
            native.Graph.from_files(
                edge_list_path="hrg.txt",
                coordinate_list_path="hrg.hyp",
                plane=plane,
            )
            .set_vertex_color(TRANSPARENT_BLUE)
            .set_edge_color(TRANSPARENT_BLUE)
        )

        # Trigger graph redrawing upon center of projection change.
        graph.add_updater(
            lambda x: x.set_center_of_projection(
                get_hyperbolic_center_of_projection()
            )
        )

        # Create the circle along which we rotate
        circle_radius = 1.5
        rotation_circle = Circle(radius=circle_radius)

        # Move the center of the projection onto the circle.
        translation_target = native.Point(
            circle_radius, 0.0
        ).to_point_in_plane(plane)
        center_of_projection_dot.set_center(translation_target)

        self.play(FadeIn(graph))

        self.add_title(
            [
                "About the Analysis of Algorithms on Networks",
                "with Underlying Hyperbolic Geometry",
            ],
            subtitle="Maximilian Katzmann",
        )

        # Actually start playing the animation.
        self.play(
            MoveAlongPath(center_of_projection_dot, rotation_circle),
            # run_time=5,
            run_time=54,
            rate_func=linear,
        )

        # Fade out the graph, then fade out everything else.
        self.play(FadeOut(graph))
        self.fade_out()
