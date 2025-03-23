from manim import (
    BLUE,
    DOWN,
    RIGHT,
    UP,
    WHITE,
    YELLOW,
    Create,
    Dot,
    DrawBorderThenFill,
    FadeIn,
    FadeOut,
    Graph,
    Line,
    Rectangle,
)

from manim_presentation_template import ContentText, DefaultSlide, SideNoteText


# Vertex Cover
class Slide8(DefaultSlide):

    def content(self):
        header = self.add_header("Vertex Cover", with_click=False)

        # Draw an exemplary graph.
        vertices = list(range(14))
        edges = [
            (0, 1),
            (0, 2),
            (0, 3),
            (0, 4),
            (0, 5),
            (0, 7),
            (0, 12),
            (1, 3),
            (1, 5),
            (1, 11),
            (1, 12),
            (1, 13),
            (2, 4),
            (2, 9),
            (2, 10),
            (2, 12),
            (3, 10),
            (3, 11),
            (3, 12),
            (4, 7),
            (4, 8),
            (5, 6),
        ]
        layout = {
            vertex: [x + 0.5, y + 2.2, 0.0]
            for (vertex, [x, y, z]) in {
                0: [0.0, 0.0, 0.0],
                1: [-1.5, -1.3, 0.0],
                2: [0.5, -1.2, 0.0],
                3: [-0.3, -1.9, 0.0],
                4: [1.5, -1.4, 0.0],
                5: [-2.0, -0.3, 0.0],
                6: [-3.1, -0.9, 0.0],
                7: [1.7, -0.4, 0.0],
                8: [2.4, -1.9, 0.0],
                9: [1.7, -2.9, 0.0],
                10: [0.3, -3.3, 0.0],
                11: [-1.15, -2.8, 0.0],
                12: [-0.7, -1.1, 0.0],
                13: [-2.8, -2.2, 0.0],
            }.items()
        }
        default_vertex_radius = 0.125
        vertex_config = {
            node: {"radius": default_vertex_radius} for node in vertices
        }
        edge_config = {edge: {"stroke_width": 5.0} for edge in edges}
        graph = Graph(
            vertices,  # type: ignore
            edges,  # type: ignore
            layout=layout,  # type: ignore
            vertex_config=vertex_config,
            edge_config=edge_config,
            labels=False,
        )
        self.play(FadeIn(header, graph))
        self.wait()

        cover_radius = 0.15

        # We place dots over all nodes to make sure edges are
        # not displayed above the nodes.
        vertex_dots = [
            Dot(
                layout[v],  # type: ignore
                color=WHITE,
                radius=default_vertex_radius,
                z_index=1,
            )
            for v in vertices
        ]
        self.play(*[FadeIn(dot, run_time=0.1) for dot in vertex_dots])
        self.wait()

        # Create the vertex cover
        cover = [0, 1, 2, 3, 4, 5]
        cover_neighbors = [
            [1, 2, 3, 4, 5, 7, 12],
            [5, 3, 11, 12, 13],
            [4, 9, 10, 12],
            [10, 11, 12],
            [7, 8],
            [6],
        ]

        def dot_and_edges(cover_vertex):
            cover_dot = Dot(
                layout[cover_vertex],  # type: ignore
                color=BLUE,
                z_index=2,
                radius=cover_radius,
            )
            neighbors = cover_neighbors[cover_vertex]
            neighbor_edges = [
                Line(
                    layout[cover_vertex],  # type: ignore
                    layout[neighbor],  # type: ignore
                    stroke_width=8.0,
                    color=BLUE,
                )
                for neighbor in neighbors
            ]
            return cover_dot, neighbor_edges

        # Add the first node to the cover
        dot0, edges0 = dot_and_edges(0)
        self.play(Create(dot0))
        self.play(*[Create(edge) for edge in edges0])
        self.wait()

        # Cover the remaining edges
        remaining_dots = []
        remaining_edges = []
        for cover_vertex in cover[1:]:
            dot, drawn_edges = dot_and_edges(cover_vertex)
            remaining_dots.append(dot)
            remaining_edges += drawn_edges

        self.play(
            *[Create(dot) for dot in remaining_dots],
            *[Create(edge) for edge in remaining_edges],
        )
        self.wait()

        # We briefly mention that removing the cover leaves
        # the graph edgeless.
        non_cover_vertices = range(len(cover), len(vertices))
        non_cover_dots = [
            Dot(
                layout[v],  # type: ignore
                color=WHITE,
                radius=default_vertex_radius,
                z_index=1,
            )
            for v in non_cover_vertices
        ]
        self.play(
            *[FadeOut(dot) for dot in remaining_dots],
            *[FadeOut(dot) for dot in vertex_dots],
            FadeOut(dot0),
            *[FadeOut(edge) for edge in remaining_edges],
            *[FadeOut(edge) for edge in edges0],
            FadeOut(graph),
            *[FadeIn(dot) for dot in non_cover_dots],
        )
        self.wait()

        # Get the graph back
        self.play(FadeIn(graph))
        self.wait()

        # Adding relevant known facts about the problem.

        # Akiba & Iwata
        t1 = ContentText("Reduction rules work well in practice.").shift(
            DOWN * 1.75
        )
        akiba_iwata_citation = (
            SideNoteText("Akiba & Iwata, Theor. Comput. Sci. 2016")
            .align_to(t1, UP)
            .shift(DOWN * 0.5)
        )
        self.play(FadeIn(t1, akiba_iwata_citation))
        self.wait()

        # Dominance Reduction Rule Header
        t2 = (
            ContentText("Dominance Reduction Rule")
            .align_to(akiba_iwata_citation, UP)
            .shift(DOWN * 0.6)
        )
        garfinkel_nemhauser_citation = (
            SideNoteText(
                "Garfinkel & Nemhauser, Integer Programming,"
                " John Wiley & Sons 1972"
            )
            .align_to(t2, UP)
            .shift(DOWN * 0.5)
        )
        self.play(FadeIn(t2, garfinkel_nemhauser_citation))
        self.wait()

        # Highlight neighborhood of 0
        self.play(FadeIn(dot0, *edges0, *vertex_dots))
        neighborhood0 = (
            Rectangle(width=4.5, height=2.7, color=BLUE, fill_opacity=0.15)
            .shift(UP * 1.25)
            .shift(RIGHT * 0.4)
        )
        self.play(DrawBorderThenFill(neighborhood0))
        self.wait()

        # Highlight the dominated node
        dominated_dot = Dot(
            layout[12],  # type: ignore
            color=YELLOW,
            z_index=2,
            radius=cover_radius,
        )
        self.play(Create(dominated_dot))
        self.wait()

        dominated_neighbors = [0, 1, 2, 3]
        dominated_lines = [
            Line(
                layout[12],  # type: ignore
                layout[v],  # type: ignore
                stroke_width=8.0,
                color=YELLOW,
            )
            for v in dominated_neighbors
        ]
        self.play(*[Create(line) for line in dominated_lines])
        self.wait()

        dominated_rect = Rectangle(
            width=2.5, height=2.5, color=YELLOW, fill_opacity=0.15
        ).shift(UP * 1.25)
        self.play(DrawBorderThenFill(dominated_rect))
        self.wait()

        # Show how we the instance has been reduced by removing the now covered
        # edges.
        self.play(
            FadeOut(
                dominated_dot,
                *dominated_lines,
                dominated_rect,
                neighborhood0,
            ),
        )
        self.wait()
        edges_to_fade = [graph.edges[edge] for edge in edges if 0 in edge]
        self.play(FadeOut(*edges_to_fade, *edges0))
        self.wait()

        self.fade_out()
