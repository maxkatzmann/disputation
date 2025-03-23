from manim import (
    BLUE,
    DOWN,
    WHITE,
    ApplyMethod,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    Graph,
    Line,
    Tex,
)

from manim_presentation_template import DefaultSlide, SideNoteTex


# Vertex Cover Approximation
class Slide10(DefaultSlide):

    def content(self):
        header = self.add_header("Greedy Approximation", with_click=False)

        # Draw an exemplary graph again.
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
            vertex: [x + 0.5, y + 1.0, 0.0]
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
            vertex: {"radius": default_vertex_radius} for vertex in vertices
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
        self.play(FadeIn(*vertex_dots))
        self.wait()

        # Create the cover
        cover = [0, 1, 2, 3, 4, 5]
        non_cover_vertices = range(len(cover), len(vertices))

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

        all_cover_dots = []
        all_neighbor_edges = []
        fade_out_time = 0.4
        for cover_vertex in cover:
            cover_dot, neighbor_edges = dot_and_edges(cover_vertex)
            all_cover_dots.append(cover_dot)
            all_neighbor_edges += neighbor_edges
            self.play(
                Create(cover_dot), *[Create(edge) for edge in neighbor_edges]
            )

            self.play(
                *[
                    FadeOut(edge, run_time=fade_out_time)
                    for edge in graph.remove_edges(
                        *[
                            (cover_vertex, v)
                            for v in cover_neighbors[cover_vertex]
                        ]  # type: ignore
                    )
                ],
                FadeOut(
                    *graph.remove_vertices(cover_vertex),
                    run_time=fade_out_time
                ),
                FadeOut(vertex_dots[cover_vertex], run_time=fade_out_time),
                *[
                    ApplyMethod(edge.set_opacity, 0.25, run_time=fade_out_time)
                    for edge in all_neighbor_edges
                ],
                ApplyMethod(
                    cover_dot.set_opacity, 0.25, run_time=fade_out_time
                )
            )
            self.wait()

        self.play(
            FadeOut(graph),
            *[FadeOut(dot) for dot in all_cover_dots],
            *[FadeOut(vertex_dots[v]) for v in non_cover_vertices],
            *[FadeOut(edge) for edge in all_neighbor_edges]
        )

        # Next we display known results about vertex cover approximation.
        buff = 0.3
        mini_buff = 0.1
        t1 = Tex("$\\Omega(\\log(n))$").next_to(header, DOWN, buff=0.2)
        t1_cite = SideNoteTex("Johnson, J. Comput. Syst. Sci. 1974").next_to(
            t1, DOWN, buff=mini_buff
        )
        self.play(FadeIn(t1, t1_cite))
        self.wait()

        t2 = Tex("$2$").next_to(t1_cite, DOWN, buff=buff)
        t2_cite = SideNoteTex(
            "Gavril \\& Yannakakis. According to Papadimitriou \\"
            "& Steiglitz,\\\\Combinatorial Optimization: Algorithms"
            " and Complexity, Dover 1998"
        ).next_to(t2, DOWN, buff=mini_buff)
        self.play(FadeIn(t2, t2_cite))
        self.wait()

        t3 = Tex("$2 - \\Theta(\\log(n)^{-1/2})$").next_to(
            t2_cite, DOWN, buff=buff
        )
        t3_cite = SideNoteTex(
            "Karakostas, ACM Trans. Algorithms 2009"
        ).next_to(t3, DOWN, buff=mini_buff)
        self.play(FadeIn(t3, t3_cite))
        self.wait()

        t4 = Tex("$2 - \\varepsilon$").next_to(t3_cite, DOWN, buff=buff)
        t4_cite = SideNoteTex(
            "Khot \\& Regev, J. Comput. Syst. Sci. 2008"
        ).next_to(t4, DOWN, buff=mini_buff)
        self.play(FadeIn(t4, t4_cite))
        self.wait()

        t5 = Tex("$\sqrt{2}$").next_to(t4_cite, DOWN, buff=buff)
        t5_cite = SideNoteTex("Subhash, Minzer \\& Safra, FOCS 2008").next_to(
            t5, DOWN, buff=mini_buff
        )
        self.play(FadeIn(t5, t5_cite))
        self.wait()

        self.fade_out()
