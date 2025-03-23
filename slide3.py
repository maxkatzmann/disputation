from colour import Color
from manim import (
    DEGREES,
    DOWN,
    GREEN,
    LEFT,
    RIGHT,
    UP,
    WHITE,
    YELLOW,
    AnimationGroup,
    Axes,
    Create,
    CurvesAsSubmobjects,
    Dot,
    FadeIn,
    Graph,
    Group,
    Line,
    Text,
    Triangle,
)

from manim_presentation_template import ContentText, DefaultSlide


# Complex Networks and their properties
class Slide3(DefaultSlide):

    def content(self):
        header = self.add_header("Complex Networks", with_click=False)

        # Draw a small network on which we can highlight the properties of
        # context networks.
        vertices = list(range(1, 18))
        edges = [
            (1, 2),
            (1, 3),
            (1, 4),
            (2, 3),
            (2, 4),
            (3, 4),
            (1, 5),
            (1, 6),
            (5, 6),
            (1, 7),
            (5, 7),
            (5, 8),
            (5, 9),
            (6, 10),
            (1, 11),
            (4, 12),
            (3, 12),
            (3, 12),
            (3, 13),
            (2, 14),
            (1, 15),
            (1, 16),
            (1, 17),
            (1, 7),
            (7, 1),
        ]
        layout = {
            node: [1.3 * x, 1.3 * y, 1.3 * z]
            for (node, [x, y, z]) in {
                1: [0, 0, 0],
                2: [-0.9, 0, 0],
                3: [-1, -0.7, 0],
                4: [-0.2, -1, 0],
                5: [0.7, -0.1, 0],
                6: [0.7, -0.5, 0],
                7: [0.9, 0.6, 0],
                8: [1.5, -0.4, 0],
                9: [1.3, -0.7, 0],
                10: [0.9, -1.1, 0],
                11: [0.2, -1.5, 0],
                12: [-1.3, -1.1, 0],
                13: [-1.6, -0.7, 0],
                14: [-1.75, 0.1, 0],
                15: [-1.6, 0.5, 0],
                16: [-0.95, 1.1, 0],
                17: [-0.45, 1.3, 0],
            }.items()
        }

        # We use different vertex colors to highlight certain properties.
        vertex_config = {
            1: {
                "fill_color": "#2874F6",
                "radius": 0.25,
            },
            2: {
                "fill_color": "#9F4B4B",
                "radius": 0.15,
            },
            3: {
                "fill_color": "#6F547D",
                "radius": 0.16,
            },
            4: {"fill_color": "#845066", "radius": 0.15},
            5: {"fill_color": "#6F547D", "radius": 0.18},
            6: {
                "fill_color": "#9F4B4B",
                "radius": 0.14,
            },
            7: {"fill_color": "#C1462C"},
            8: {"fill_color": "#C1462C"},
            9: {"fill_color": "#C1462C"},
            10: {"fill_color": "#C1462C"},
            11: {"fill_color": "#C1462C"},
            12: {"fill_color": "#C1462C"},
            13: {"fill_color": "#C1462C"},
            14: {"fill_color": "#C1462C"},
            15: {"fill_color": "#C1462C"},
            16: {"fill_color": "#C1462C"},
            17: {"fill_color": "#C1462C"},
        }
        graph = Graph(
            vertices,  # type: ignore
            edges,  # type: ignore
            layout=layout,  # type: ignore
            vertex_type=Dot,
            vertex_config=vertex_config,
        )
        graph.shift(RIGHT * 0.33)
        self.play(
            [
                FadeIn(header),
                AnimationGroup(
                    *[
                        FadeIn(mobject)
                        for mobject in [
                            Group(*graph.vertices.values()),
                            Group(*graph.edges.values()),
                        ]
                    ],
                    lag_ratio=0.35
                ),
            ]
        )
        self.wait()

        # Mention the first property.
        t1 = ContentText("Heterogeneity")
        t1.shift(LEFT * 3.5)
        t1.shift(UP * 2.0)
        self.play(FadeIn(t1))
        self.wait()

        # Draw a graph showing what a heterogeneous degree distribution looks
        # like.
        ax = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 10, 1],
            x_length=5,
            y_length=5,
            tips=True,
            axis_config={
                "include_numbers": False,
                "include_ticks": False,
                "tip_width": 0.15,
                "tip_height": 0.15,
            },
        )

        ax.shift(LEFT * 3.5)

        # Add axis labels to the plot.
        x_label = (
            Text("Degree")
            .scale(0.6)
            .shift(LEFT * 3.5)
            .align_to(ax, DOWN)
            .shift(DOWN * 0.5)
        )
        y_label = (
            Text("Fraction of Vertices")
            .rotate_about_origin(90 * DEGREES)
            .scale(0.6)
            .align_to(ax, LEFT)
            .shift(LEFT * 0.5)
        )

        self.play(FadeIn(ax, x_label, y_label))
        self.wait()

        # Plot the function.
        plot = ax.plot(
            lambda x: 5 / (x - 0.1), x_range=[0.68, 9], use_smoothing=False
        )
        gradient_plot = CurvesAsSubmobjects(plot)
        gradient_plot.set_color_by_gradient(
            Color("#C1462C"),  # type: ignore
            Color("#2874F6"),  # type: ignore
            Color("#2874F6"),  # type: ignore
        )

        self.play(Create(gradient_plot))
        self.wait()

        # Mention the second property.
        t2 = ContentText("Clustering")
        t2.shift(RIGHT * 4.0)
        t2.shift(UP * 2.0)
        self.play(FadeIn(t2))
        self.wait()

        # Highlight a node and its neighbors, with the appropriate edges.
        highlight_dot = Dot(radius=0.15, color=YELLOW).move_to(graph[4])
        self.play(Create(highlight_dot))
        self.wait()

        neighbor_dot_1 = Dot(radius=0.25, color=GREEN).move_to(graph[1])
        neighbor_dot_2 = Dot(radius=0.15, color=GREEN).move_to(graph[2])
        neighbor_dot_3 = Dot(radius=0.16, color=GREEN).move_to(graph[3])
        neighbor_dot_12 = Dot(color=GREEN).move_to(graph[12])
        self.play(
            Create(neighbor_dot_1),
            Create(neighbor_dot_2),
            Create(neighbor_dot_3),
            Create(neighbor_dot_12),
        )
        self.wait()

        highlight_edges = graph.add_edges(
            (1, 2),
            (1, 3),
            (2, 3),
            (3, 12),
            edge_config={
                (1, 2): {
                    "stroke_color": GREEN,
                    "stroke_width": 10,
                },
                (1, 3): {
                    "stroke_color": GREEN,
                    "stroke_width": 10,
                },
                (2, 3): {
                    "stroke_color": GREEN,
                    "stroke_width": 10,
                },
                (3, 12): {
                    "stroke_color": GREEN,
                    "stroke_width": 10,
                },
            },
        )
        self.play(Create(highlight_edges))
        self.wait()

        # Draw some triangles
        tri1 = Triangle(color=WHITE, stroke_width=7)
        tri1_dot1 = Dot(radius=0.15, color=YELLOW).shift(UP)
        tri1_dot2 = (
            Dot(radius=0.15, color=GREEN).shift(RIGHT * 0.85).shift(DOWN * 0.5)
        )
        tri1_dot3 = (
            Dot(radius=0.15, color=GREEN).shift(LEFT * 0.85).shift(DOWN * 0.5)
        )
        green_edge = Line(
            tri1_dot2,  # type: ignore
            tri1_dot3,  # type: ignore
            color=GREEN,
            stroke_width=7,
        )
        tri1.add(tri1_dot1)
        tri1.add(tri1_dot2)
        tri1.add(tri1_dot3)
        tri1.add(green_edge)

        tri1.rotate(15 * DEGREES).shift(RIGHT * 3.5).scale(0.9)
        tri2 = (
            tri1.copy()
            .rotate(35 * DEGREES)
            .shift(DOWN)
            .shift(RIGHT)
            .scale(0.8)
        )
        tri3 = (
            tri1.copy()
            .rotate(80 * DEGREES)
            .shift(RIGHT * 1.25)
            .shift(UP * 0.5)
            .scale(0.7)
        )
        self.play(FadeIn(tri1), FadeIn(tri2), FadeIn(tri3))
        self.wait()

        self.fade_out()
