from manim import (
    BLUE,
    DOWN,
    LEFT,
    LIGHT_GRAY,
    RIGHT,
    UP,
    DrawBorderThenFill,
    FadeIn,
    Group,
    ImageMobject,
    SurroundingRectangle,
    Tex,
)

from manim_presentation_template import DefaultSlide


# Chapters of the thesis.
class Slide7(DefaultSlide):

    def content(self):
        header = self.add_header("The Thesis", with_click=False)

        t1 = (
            Tex(
                "Explain empirical observations on real-world networks\\"
                "\\theoretically using the hyperbolic random graph model."
            )
            .shift(UP * 2.0)
            .scale(DefaultSlide.headerScale)
        )
        self.play(FadeIn(header, t1))
        self.wait()

        # First paper
        text_scale = 0.6
        small_scale = 0.5
        ref_color = LIGHT_GRAY
        shortest_paper = (
            ImageMobject("images/shortest-path.png")
            .scale(0.6)
            .shift(DOWN * 0.5)
            .shift(LEFT * 4.5)
        )
        t2 = (
            Tex("Shortest Paths")
            .scale(text_scale)
            .move_to(shortest_paper)
            .align_to(shortest_paper, DOWN)
            .shift(DOWN * 0.4)
        )
        t2_ref = (
            Tex("[ICALP '18]", color=ref_color)
            .scale(small_scale)
            .move_to(t2)
            .align_to(t2, DOWN)
            .shift(DOWN * 0.5)
        )
        self.play(FadeIn(shortest_paper, t2, t2_ref))
        self.wait()

        # Second paper
        routing_paper = (
            ImageMobject("images/routing.png")
            .scale(0.6)
            .shift(DOWN * 0.5)
            .shift(LEFT * 1.5)
        )
        t3 = (
            Tex("Greedy Routing")
            .scale(text_scale)
            .move_to(routing_paper)
            .align_to(t2, UP)
        )
        t3_ref = (
            Tex("[STACS '23]", color=ref_color)
            .scale(small_scale)
            .move_to(t3)
            .align_to(t2_ref, UP)
        )
        self.play(FadeIn(routing_paper, t3, t3_ref))
        self.wait()

        # Third paper
        exact_cover_paper = (
            ImageMobject("images/vc-exact.png")
            .scale(0.6)
            .shift(DOWN * 0.5)
            .shift(RIGHT * 1.5)
        )
        t4 = (
            Tex("Vertex Cover")
            .scale(text_scale)
            .move_to(exact_cover_paper)
            .align_to(t2, UP)
        )
        t4_ref = (
            Tex("[STACS '20]", color=ref_color)
            .scale(small_scale)
            .move_to(t4)
            .align_to(t2_ref, UP)
        )
        self.play(FadeIn(exact_cover_paper, t4, t4_ref))
        self.wait()

        # Fourth paper
        apx_cover_paper = (
            ImageMobject("images/vc-approx.png")
            .scale(0.6)
            .shift(DOWN * 0.5)
            .shift(RIGHT * 4.5)
        )
        t5 = (
            Tex("VC-Approximation")
            .scale(text_scale)
            .move_to(apx_cover_paper)
            .align_to(t2, UP)
        )
        t5_ref = (
            Tex("[ESA '21]", color=ref_color)
            .scale(small_scale)
            .move_to(t5)
            .align_to(t2_ref, UP)
        )
        self.play(FadeIn(apx_cover_paper, t5, t5_ref))
        self.wait()

        highlight_group = Group(exact_cover_paper, apx_cover_paper, t4, t5)
        highlight_rect = SurroundingRectangle(
            highlight_group, color=BLUE, z_index=-1
        ).set_fill(BLUE, opacity=0.5)

        self.play(DrawBorderThenFill(highlight_rect))
        self.wait()

        self.fade_out()
