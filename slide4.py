from manim import (
    BLUE,
    DOWN,
    LEFT,
    PI,
    RIGHT,
    UP,
    YELLOW,
    Create,
    Dot,
    Elbow,
    FadeIn,
    FadeOut,
    Graph,
    Indicate,
)

from manim_presentation_template import ContentTex, ContentText, DefaultSlide


# Generative Models
class Slide4(DefaultSlide):

    def content(self):
        self.add_header("Generative Graph Models")
        self.wait()

        # We draw an example graph that initially consists of isolated vertices
        # only and add edges afterwards.
        vertices = [1, 2, 3, 4, 5]
        edges = []
        graph = (
            Graph(
                vertices,  # type: ignore
                edges,
                layout="circular",
                layout_scale=0.9,
            )
            .shift(RIGHT * 4.5)
            .shift(UP * 1.25)
        )

        self.play(Create(graph))
        self.wait()

        # Indicate first two vertices.
        vertex1_dot = Dot(color=BLUE, z_index=1).move_to(graph[1])
        vertex2_dot = Dot(color=BLUE, z_index=1).move_to(graph[2])
        self.play(
            Indicate(graph[1], color=BLUE, scale_factor=1.5),  # type: ignore
            Indicate(graph[2], color=BLUE, scale_factor=1.5),  # type: ignore
            Create(vertex1_dot),
            Create(vertex2_dot),
        )
        self.wait()

        # Flash first edge
        edge_flash_time = 0.33
        for _ in range(0, 3):
            self.play(
                FadeIn(graph.add_edges((1, 2)), run_time=edge_flash_time)
            )
            self.play(
                FadeOut(
                    graph.remove_edges((1, 2)),  # type: ignore
                    run_time=edge_flash_time,
                )
            )
        self.play(FadeIn(graph.add_edges((1, 2)), run_time=edge_flash_time))
        self.play(FadeOut(vertex1_dot), FadeOut(vertex2_dot))
        self.wait()

        # Indicate second two vertices
        vertex3_dot = Dot(color=BLUE, z_index=1).move_to(graph[3])
        self.play(
            Indicate(graph[2], color=BLUE, scale_factor=1.5),  # type: ignore
            Indicate(graph[3], color=BLUE, scale_factor=1.5),  # type: ignore
            Create(vertex2_dot),
            Create(vertex3_dot),
        )
        self.wait()

        # Flash second edge
        for _ in range(0, 3):
            self.play(
                FadeIn(graph.add_edges((2, 3)), run_time=edge_flash_time)
            )
            self.play(
                FadeOut(
                    graph.remove_edges((2, 3)),  # type: ignore
                    run_time=edge_flash_time,
                )
            )
        self.play(FadeOut(vertex2_dot, vertex3_dot))
        self.wait()

        # Add remaining edges
        self.play(FadeIn(graph.add_edges((3, 4), (1, 4), (2, 5), (2, 4))))
        self.wait()

        # Write out the properties that we wish for in a generative model.
        t1 = ContentText("Mathematically accessible")
        t1.shift(UP * 1.5).shift(LEFT * 2.5)
        self.play(FadeIn(t1))
        self.wait()

        t2 = ContentText("Realistic")
        t2.align_to(t1, LEFT)
        t2.shift(UP * 0.75)
        self.play(FadeIn(t2))
        self.wait()

        # Elaborate with respect to which properties we want to have realism.
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
        self.play(Create(elbow_indicator))
        self.play(FadeIn(t3, run_time=0.5))
        self.wait()

        t4 = (
            ContentText("Algorithmic Properties")
            .align_to(t2, UP)
            .shift(DOWN * 0.75)
            .shift(RIGHT * 2.5)
        )
        self.play(FadeIn(t4))
        self.wait()

        # Highlight Realistic and Algorithmic Properties
        t5 = ContentTex(
            r"Can we use Hyperbolic Random Graphs to understand\\"
            r"how algorithms perform on real-world networks?",
            color=YELLOW,
        ).shift(DOWN * 1.5)
        self.play(
            t4.animate().set_color(YELLOW),  # type: ignore
            t2.animate().set_color(YELLOW),  # type: ignore
            FadeIn(t5),
        )
        self.wait()

        self.fade_out()
