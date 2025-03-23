from manim import (
    BLUE,
    DOWN,
    LEFT,
    RIGHT,
    UP,
    BraceBetweenPoints,
    Create,
    FadeIn,
    Graph,
    Group,
    Transform,
)

from manim_presentation_template import ContentText, DefaultSlide


# Real-World Networks
class Slide2(DefaultSlide):

    def content(self):
        self.add_header("Real-World Networks")

        # We start by drawing a representation of a road network.
        # The nodes are roughly placed like this.
        #
        #    1                   9      14
        #
        #    2     6      7      10     15
        #       3
        #          5      8      11
        # 4               12
        #
        #                        13

        road_vertices = list(range(1, 16))
        road_edges = [
            (1, 2),
            (2, 3),
            (3, 4),
            (3, 5),
            (3, 6),
            (5, 7),
            (6, 8),
            (7, 10),
            (7, 11),
            (7, 8),
            (8, 9),
            (8, 12),
            (9, 13),
            (11, 14),
            (12, 15),
        ]
        # Defining the positions of the vertices.
        road_layout = {
            vertex: [0.25 * x, 0.25 * y, 0.25 * z]
            for (vertex, [x, y, z]) in {
                1: [-4, 4, 0],
                2: [-4, 2, 0],
                3: [-3, 1, 0],
                4: [-5, -1, 0],
                5: [-2, 2, 0],
                6: [-2, 0, 0],
                7: [0, 2, 0],
                8: [0, 0, 0],
                9: [0, -1, 0],
                10: [2, 4, 0],
                11: [2, 2, 0],
                12: [2, 0, 0],
                13: [2, -3, 0],
                14: [4, 4, 0],
                15: [4, 2, 0],
            }.items()
        }

        road = Graph(
            road_vertices, road_edges, layout=road_layout  # type: ignore
        )
        road.shift(3.8 * LEFT)

        self.play(Create(road, run_time=2))
        self.wait()

        # The next network is supposed to represent a brain.
        #
        #            1          2
        #   15                       3
        #  14      16                   4
        #    13                17     5
        #         12                 6
        #                  11       7
        #                     10   8
        #                        9

        brain_vertices = list(range(1, 18))
        brain_edges = (
            [(i, i + 1) for i in range(1, 15)]
            + [(15, 1)]
            + [
                (16, 1),
                (16, 15),
                (16, 12),
                (16, 11),
                (16, 17),
                (17, 1),
                (17, 2),
                (17, 4),
                (17, 7),
                (17, 11),
                (11, 17),
            ]
        )
        brain_layout = {
            1: [0, 0, 0],
            2: [1, 0, 0],
            3: [1.5, -0.25, 0],
            4: [1.7, -0.5, 0],
            5: [1.65, -0.75, 0],
            6: [1.5, -1, 0],
            7: [1.25, -1.25, 0],
            8: [1.2, -1.5, 0],
            9: [1.3, -1.75, 0],
            10: [1.0, -1.5, 0],
            11: [0.7, -1.25, 0],
            12: [-0.5, -1.0, 0],
            13: [-0.75, -0.9, 0],
            14: [-0.75, -0.7, 0],
            15: [-0.5, -0.25, 0],
            16: [-0.2, -0.65, 0],
            17: [1.0, -0.8, 0],
        }
        brain = Graph(
            brain_vertices, brain_edges, layout=brain_layout  # type: ignore
        )
        brain.shift(UP)
        brain.shift(LEFT * 0.5)

        self.play(Create(brain, run_time=2))
        self.wait()

        # The last network should represent a globe.
        #         1
        #  2   3  4  5   6
        # 7   8   9   10  11
        #  12  13 14 15  16
        #         17
        web_vertices = list(range(1, 18))
        web_edges = [
            (1, 6),
            (6, 11),
            (11, 16),
            (16, 17),
            (17, 12),
            (12, 7),
            (7, 2),
            (2, 1),
            (1, 3),
            (3, 8),
            (8, 13),
            (13, 17),
            (1, 4),
            (4, 9),
            (9, 14),
            (14, 17),
            (1, 5),
            (5, 10),
            (10, 15),
            (15, 17),
            (2, 3),
            (3, 4),
            (4, 5),
            (5, 6),
            (7, 8),
            (8, 9),
            (9, 10),
            (10, 11),
            (12, 13),
            (13, 14),
            (14, 15),
            (15, 16),
            (16, 15),
        ]
        web_layout = {
            1: [0, 1.25, 0],
            2: [-1.0, 0.8, 0],
            3: [-0.65, 0.7, 0],
            4: [0, 0.6, 0],
            5: [0.65, 0.7, 0],
            6: [1.0, 0.8, 0],
            7: [-1.25, 0.0, 0],
            8: [-0.8, 0.0, 0],
            9: [0.0, 0.0, 0],
            10: [0.8, 0.0, 0],
            11: [1.25, 0.0, 0],
            12: [-1.0, -0.8, 0],
            13: [-0.65, -0.7, 0],
            14: [0, -0.6, 0],
            15: [0.65, -0.7, 0],
            16: [1.0, -0.8, 0],
            17: [0.0, -1.25, 0],
        }

        web = Graph(web_vertices, web_edges, layout=web_layout)  # type: ignore
        web.shift(RIGHT * 4)
        self.play(Create(web, run_time=2))
        self.wait()

        # Next, we draw a distinction between two groups of networks, using
        # braces.
        brace_group_one = BraceBetweenPoints(
            [-5.25, -1.5, 0.0], [-2.75, -1.5, 0.0]
        )
        t1 = ContentText("Group 1").next_to(brace_group_one, DOWN)

        brace_scale_free = BraceBetweenPoints(
            [-1.5, -1.5, 0.0], [5.5, -1.5, 0.0]
        )
        t2 = ContentText("Group 2").next_to(brace_scale_free, DOWN)

        # Fade in the two braces.
        g = Group(brace_group_one, t1, brace_scale_free, t2)
        self.play(FadeIn(g))
        self.wait()

        # Change the text of the second group to "Complex Networks".
        self.play(
            Transform(
                t2,
                ContentText("Complex Networks", t2c={"Complex": BLUE}).move_to(
                    t2
                ),
            )
        )
        self.wait()

        self.fade_out()
