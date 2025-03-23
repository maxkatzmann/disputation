from manim import (
    DOWN,
    LEFT,
    PI,
    RIGHT,
    UP,
    WHITE,
    Elbow,
    FadeIn,
    Indicate,
    PolarPlane,
    Write,
)

from hmanim import native
from manim_presentation_template import ContentText, DefaultSlide


# Back to generative models
class Slide6(DefaultSlide):

    def content(self):
        header = self.add_header("Hyperbolic Random Graphs", with_click=False)

        # Draw the hyperbolic random graph again.
        plane = PolarPlane(size=3)
        straight_graph = (
            native.Graph.from_files(
                edge_list_path="hrg.txt",
                coordinate_list_path="hrg.hyp",
                plane=plane,
                using_geodesic=False,
                z_index=1,
            )
            .set_vertex_color(WHITE)
            .set_edge_color(WHITE, 0.8)
        )
        straight_graph.shift(RIGHT * 4.5).shift(UP * 1.5)
        straight_graph.scale(0.35)

        # Recall the desired properties.
        t1 = ContentText("Mathematically accessible")
        t1.shift(UP * 1.5).shift(LEFT * 2.5)

        t2 = ContentText("Realistic")
        t2.align_to(t1, LEFT)
        t2.shift(UP * 0.75)

        elbow_indicator = (
            Elbow(width=0.25, angle=3.0 * PI / 2.0)
            .flip()
            .shift(LEFT * 4.7)
            .shift(UP * 0.26)
        )

        t3 = (
            ContentText("Structural Properties")
            .align_to(t2, UP)
            .shift(DOWN * 0.75)
            .shift(LEFT * 2.5)
        )

        t4 = (
            ContentText("Algorithmic Properties")
            .align_to(t2, UP)
            .shift(DOWN * 0.75)
            .shift(RIGHT * 2.5)
        )

        self.play(
            FadeIn(header, straight_graph, t1, t2, elbow_indicator, t3, t4)
        )
        self.wait()

        # Structural Properties
        t5 = (
            ContentText("Degree Distribution")
            .align_to(t3, LEFT)
            .shift(DOWN * 0.6)
        )
        self.play(FadeIn(t5))
        self.wait()
        t6 = (
            ContentText("Clustering")
            .align_to(t5, LEFT)
            .align_to(t5, UP)
            .shift(DOWN * 0.6)
        )
        self.play(FadeIn(t6))
        self.wait()
        t7 = (
            ContentText("Diameter")
            .align_to(t6, LEFT)
            .align_to(t6, UP)
            .shift(DOWN * 0.6)
        )
        self.play(FadeIn(t7))
        self.wait()
        t8 = (
            ContentText("Components")
            .align_to(t7, LEFT)
            .align_to(t7, UP)
            .shift(DOWN * 0.6)
        )
        self.play(FadeIn(t8))
        self.wait()
        t9 = (
            ContentText("...")
            .align_to(t8, LEFT)
            .align_to(t8, UP)
            .shift(DOWN * 0.6)
        )
        self.play(FadeIn(t9))
        self.wait()

        # Algorithmic Properties
        t10 = ContentText("Generation").align_to(t4, LEFT).shift(DOWN * 0.6)
        self.play(FadeIn(t10))
        self.wait()
        t11 = (
            ContentText("Maximum Clique")
            .align_to(t10, LEFT)
            .align_to(t10, UP)
            .shift(DOWN * 0.6)
        )
        self.play(FadeIn(t11))
        self.wait()
        t12 = (
            ContentText("Tree Width")
            .align_to(t11, LEFT)
            .align_to(t11, UP)
            .shift(DOWN * 0.6)
        )
        self.play(FadeIn(t12))
        self.wait()
        t13 = (
            ContentText("Compression")
            .align_to(t12, LEFT)
            .align_to(t12, UP)
            .shift(DOWN * 0.6)
        )
        self.play(FadeIn(t13))
        self.wait()
        t14 = (
            ContentText("...")
            .align_to(t13, LEFT)
            .align_to(t13, UP)
            .shift(DOWN * 0.6)
        )
        self.play(FadeIn(t14))
        self.wait()

        # Highlight "Realistic" and add a question mark.
        self.play(Indicate(t2))
        question_mark = (
            ContentText("?")
            .scale(2.0)
            .move_to(t2)
            .align_to(t2, RIGHT)
            .shift(RIGHT * 0.5)
        )
        self.play(Write(question_mark))
        self.wait()

        self.fade_out()
