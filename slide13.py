import copy
import itertools

from hmanim import native
from manim import (
    BLUE,
    DOWN,
    GREEN,
    LEFT,
    ORANGE,
    PI,
    RED,
    RIGHT,
    UP,
    WHITE,
    YELLOW,
    AnimationGroup,
    ApplyMethod,
    BulletedList,
    Create,
    FadeIn,
    FadeOut,
    MathTex,
    PolarPlane,
    Restore,
)

from manim_presentation_template import (
    ContentTex,
    ContentText,
    DefaultSlide,
    SideNoteTex,
)


# Analysis
class Slide13(DefaultSlide):

    def content(self):
        header = self.add_header("Analysis", with_click=False).shift(UP * 0.2)

        # Write the theorem.
        t1 = ContentTex(
            "An approximate Vertex Cover of a Hyperbolic Random Graph \\"
            "\\ can be computed in time $\\mathcal{O}(m \log(n))$, such that "
            "the \\\\ approximation ratio is $(1 + o(1))$ asymptotically "
            "almost surely.",
            tex_environment="flushleft",
        ).next_to(header, DOWN, buff=0.15)
        t1_cite = (
            SideNoteTex(r"Bläsius, Friedrich \& K. ESA 2021")
            .next_to(t1, DOWN)
            .align_to(t1, LEFT)
        )
        self.play(FadeIn(header, t1, t1_cite))
        self.wait()

        # Draw the graph.
        graph_R = 12.0
        plane = PolarPlane(size=1.66).shift(RIGHT * 3.5).shift(DOWN * 1.4)
        graph = (
            native.Graph.from_files(
                edge_list_path="hrg-large.txt",
                coordinate_list_path="hrg-large.hyp",
                plane=plane,
                using_geodesic=False,
            )
            .set_vertex_color(WHITE)
            .set_vertex_radius(0.04)
            .set_edge_stroke_width(2.0)
            .set_edge_color(WHITE, 0.25)
        )
        self.play(FadeIn(graph))

        # Write out the proof steps.
        t2 = (
            ContentTex("1. Optimum is $\Omega(n)$")
            .next_to(t1, DOWN, buff=0.3)
            .align_to(t1, LEFT)
        )
        t2_cite = (
            SideNoteTex(
                "Chauhan, Friedrich \\& Rothenberger,\\\\Algorithmica 2020",
                tex_environment="flushleft",
            )
            .next_to(t2, DOWN, buff=0.15)
            .align_to(t2, LEFT)
        )
        self.play(FadeOut(t1_cite))
        self.play(FadeIn(t2, t2_cite))
        self.wait()

        t3 = (
            ContentTex("2. Find ", "radius", ":")
            .next_to(t2_cite, DOWN)
            .align_to(t2, LEFT)
        )
        t3[1].set_color(BLUE)
        t3b = (
            BulletedList(
                "$o(n)$ vertices inside",
                "removal decomposes graph",
                buff=0.2,
                height=0.25,
                width=5,
            )
            .next_to(t3, DOWN)
            .align_to(t3, LEFT)
            .shift(RIGHT * 0.5)
        )

        # Highlight the greedy and non-greedy vertices in the graph.
        greedy_radius = 10.0
        greedy_disk = native.Circle(
            center=native.Point(),
            radius=greedy_radius,
            plane=plane,
            z_index=4,
            color=BLUE,
        ).set_fill(BLUE, opacity=0.5)

        processed_vertices = []

        # Find greedily taken nodes.
        # TODO: Deal with code duplication (this BFS code is also in slide 12.)
        def nodes_seen_in_BFS_starting_at(start_vertex):
            if start_vertex in processed_vertices:
                return None

            state = [0 for _ in graph.vertices]
            state[start_vertex] = 1  # 0 = unseen, 1 = seen, 2 = processed
            seen_vertices = [start_vertex]  # we have seen the start_vertex
            for processed_vertex in processed_vertices:
                state[processed_vertex] = 2

            q = [start_vertex]

            while q:
                p = q.pop(0)
                state[p] = 2

                for v in mutable_graph_adjacencies[p]:
                    if state[v] == 1 or state[v] == 2:
                        continue

                    state[v] = 1
                    seen_vertices.append(v)
                    q.append(v)

            return seen_vertices

        small_size = 4
        greedy_vertices = []
        non_greedy_vertices = []

        sorted_vertices = []
        for index, dot in enumerate(graph.vertices):
            sorted_vertices.append((index, dot.center.radius))
        sorted_vertices.sort(key=lambda x: x[1])
        # Now we forget the radii, since we are only interested in
        # the vertex order.
        sorted_vertices = [x for (x, _) in sorted_vertices]

        # We want to be able to perform BFSs in the reduced graph
        mutable_graph_adjacencies = copy.deepcopy(graph.adjacencies)

        def remove_edges_incident_to(v):
            neighbors = mutable_graph_adjacencies[v]
            for neighbor in neighbors:
                mutable_graph_adjacencies[neighbor].remove(v)

            mutable_graph_adjacencies[v] = []

        for v in sorted_vertices:
            if v in processed_vertices:
                continue

            greedy_vertices.append(v)
            processed_vertices.append(v)
            remove_edges_incident_to(v)

            for neighbor in graph.adjacencies[v]:
                component = nodes_seen_in_BFS_starting_at(neighbor)
                if not component:
                    continue

                component_is_small = len(component) <= small_size
                if not component_is_small:
                    continue

                non_greedy_vertices += component
                processed_vertices += component

        greedy_dots = [
            native.Dot(
                graph.coordinates[v],
                radius=0.075,
                plane=plane,
                z_index=2,
                color=BLUE,
            )
            for v in greedy_vertices
        ]
        non_greedy_dots = [
            native.Dot(
                graph.coordinates[v],
                radius=0.075,
                plane=plane,
                z_index=1,
                color=YELLOW,
            )
            for v in non_greedy_vertices
        ]

        self.play(FadeIn(t3, t3b, greedy_disk, *greedy_dots, *non_greedy_dots))
        self.wait()

        # Remove the vertices inside the domination disk
        vertices_inside = [
            v
            for v in range(len(graph.vertices))
            if graph.coordinates[v].radius < greedy_radius
        ]
        edges_inside = set()
        for vertex_inside in vertices_inside:
            edges_inside.update(
                [
                    graph.get_edge(vertex_inside, neighbor)
                    for neighbor in graph.adjacencies[vertex_inside]
                ]
            )

        greedy_dots_inside = [
            dot for dot in greedy_dots if dot.center.radius < greedy_radius
        ]
        non_greedy_dots_inside = [
            dot for dot in non_greedy_dots if dot.center.radius < greedy_radius
        ]

        self.play(
            FadeOut(
                *greedy_dots_inside,
                *non_greedy_dots_inside,
                *[graph.vertices[v] for v in vertices_inside],
                *edges_inside,
            )
        )
        self.wait()

        t4 = (
            ContentTex(
                "3. At most $o(n)$ vertices in \\\\\hphantom{3.}",
                "non-small components",
            )
            .next_to(t3b, DOWN)
            .align_to(t3, LEFT)
        )
        t4[1].set_color(RED)

        # Find the greedy vertices outside of the domination disk
        greedy_vertices_outside = [
            v
            for v in greedy_vertices
            if graph.coordinates[v].radius > greedy_radius
        ]
        greedy_cover_dots_outside = [
            native.Dot(
                graph.coordinates[v],
                radius=0.075,
                plane=plane,
                color=BLUE,
                z_index=2,
            )
            for v in greedy_vertices_outside
        ]
        greedy_cover_borders_outside = [
            native.Dot(
                graph.coordinates[v],
                radius=0.075,
                plane=plane,
                fill_opacity=0.0,
                stroke_width=3.0,
                color=RED,
                z_index=2,
            )
            for v in greedy_vertices_outside
        ]
        self.play(
            FadeIn(
                t4, *greedy_cover_dots_outside, *greedy_cover_borders_outside
            )
        )
        self.wait()

        greedy_dots_outside = [
            dot for dot in greedy_dots if dot.center.radius > greedy_radius
        ]
        non_greedy_dots_outside = [
            dot for dot in non_greedy_dots if dot.center.radius > greedy_radius
        ]

        self.play(
            FadeOut(
                t1,
                *greedy_dots_outside,
                *non_greedy_dots_outside,
                *greedy_cover_dots_outside,
                *greedy_cover_borders_outside,
            )
        )

        # Diving into the last step of the proof. Before zooming in, we save
        # the camera state, so we can reset it later.
        self.camera.frame.save_state()  # type: ignore
        new_center_dot = native.Dot(
            native.Point(radius=greedy_radius, azimuth=PI / 2),
            radius=0.1,
            plane=plane,
        )
        self.play(
            self.camera.frame.animate.scale(0.25).move_to(  # type: ignore
                new_center_dot
            )
        )
        self.wait()

        # We draw the discretization
        disk = native.Arc(
            center=native.Point(),
            radius=graph_R,
            start_angle=PI,
            angle=0.0,
            plane=plane,
            stroke_width=1.0,
            color=WHITE,
        )
        angle_width = PI / 1.5
        number_of_sectors = 64
        sector_width = angle_width / number_of_sectors

        start_angle = PI / 2 + angle_width / 2 + sector_width - 0.01

        sector_bars = []

        for i in range(number_of_sectors):
            sector_bars.append(
                native.Line(
                    native.Point(),
                    native.Point(
                        radius=graph_R, azimuth=start_angle - i * sector_width
                    ),
                    plane=plane,
                    using_geodesic=False,
                    stroke_width=1.0,
                    stroke_color=WHITE,
                )
            )

        self.play(native.ArcStretchAngleInverse(disk, PI))
        self.wait()
        self.play(
            AnimationGroup(
                *[Create(bar) for bar in sector_bars], lag_ratio=0.025
            )
        )
        self.wait()

        # Color the sectors
        vertices_outside = [
            v
            for v in range(len(graph.vertices))
            if graph.coordinates[v].radius > greedy_radius
        ]

        # Collect groups of consecutive sectors
        empty_sectors = []
        runs = [[]]

        for i in range(number_of_sectors):
            sector_start = start_angle - (i + 1) * sector_width
            sector_end = sector_start - sector_width

            # Check if there is a vertex in that sector
            number_of_vertices_in_sector = 0
            for v in vertices_outside:
                coordinate = graph.coordinates[v]
                if (
                    coordinate.azimuth > sector_end
                    and coordinate.azimuth < sector_start
                ):
                    number_of_vertices_in_sector += 1

            sector = native.AnnularSector(
                center=native.Point(),
                inner_radius=greedy_radius,
                outer_radius=graph_R,
                start_angle=sector_start - sector_width,
                angle=sector_width,
                plane=plane,
                stroke_width=0,
                z_index=2,
            )

            # Empty sector
            if number_of_vertices_in_sector == 0:
                sector.set_fill(GREEN, opacity=0.75)
                empty_sectors.append(sector)
                runs.append([])  # Start a new run
            # Non-empty sector
            else:
                sector.set_fill(YELLOW, opacity=0.75)
                runs[-1].append(sector)

        # We are only interested in non-empty runs.
        runs = [run for run in runs if run]

        # Highlight empty sectors
        mini_buff = 0.025
        m0 = (
            ContentText("Components:")
            .scale(0.275)
            .next_to(disk, UP, buff=0.4)
            .shift(LEFT * 1.4)
        )
        m1 = (
            ContentText(
                "do not span empty sectors", t2c={"empty sectors": GREEN}
            )
            .scale(0.275)
            .next_to(m0, RIGHT, buff=mini_buff)
        )
        self.play(FadeIn(*empty_sectors, m1, m0))
        self.wait()

        # Explain what it means that a component cannot span beyond an empty
        # sector.
        special_sector_index = 48
        special_start_angle = (
            start_angle - (special_sector_index + 1) * sector_width
        )
        special_end_angle = special_start_angle + sector_width
        special_dot = native.Dot(
            native.Point(radius=greedy_radius, azimuth=special_end_angle),
            plane=plane,
            radius=0.05,
            color=YELLOW,
            z_index=4,
        )
        special_neighborhood = native.Circle(
            center=special_dot.center,  # type: ignore
            radius=graph_R / 1.05,
            plane=plane,
            color=YELLOW,
            stroke_width=1.05,
            z_index=4,
        )
        special_neighborhood.add_updater(
            lambda x: x.set_center(special_dot.center)
        )

        self.play(FadeIn(special_dot, special_neighborhood))
        self.wait()
        self.play(FadeOut(special_dot, special_neighborhood))
        self.wait()

        # Highlight
        special_narrow_run = runs[2]
        for sector in special_narrow_run:
            sector.set_fill(ORANGE, opacity=0.1)

        wide_runs = [run for run in runs if len(run) > 10]
        special_wide_run = wide_runs[1]
        for sector in special_wide_run:
            sector.set_fill(RED, opacity=0.1)

        m2 = (
            ContentText("are solved exactly", t2c={"solved exactly": YELLOW})
            .scale(0.275)
            .next_to(m1, DOWN, buff=mini_buff)
            .align_to(m1, LEFT)
        )
        all_non_empty_sectors = list(itertools.chain.from_iterable(runs))
        self.play(FadeIn(*all_non_empty_sectors, m2))
        self.wait()

        # Highlight narrow runs with many nodes
        m3 = (
            ContentText("contain many nodes", t2c={"many nodes": ORANGE})
            .scale(0.275)
            .next_to(m2, DOWN, buff=mini_buff)
            .align_to(m1, LEFT)
        )
        self.play(
            *[
                ApplyMethod(sector.set_opacity, 0.75)
                for sector in special_narrow_run
            ],
            FadeIn(m3),
        )
        self.wait()

        m4 = (
            ContentText("span many sectors", t2c={"many sectors": RED})
            .scale(0.275)
            .next_to(m3, DOWN, buff=mini_buff)
            .align_to(m1, LEFT)
        )
        self.play(
            *[
                ApplyMethod(sector.set_opacity, 0.75)
                for sector in special_wide_run
            ],
            FadeIn(m4),
        )
        self.wait()

        self.play(
            FadeOut(*all_non_empty_sectors, *empty_sectors, m0, m1, m2, m3, m4)
        )

        # Talk about the expected number of vertices in a sector
        expected = (
            MathTex(
                r"\mathbb{E}[|\{v \in \mathcal{S} \}|] = "
                r"n \int_\rho^R \int_0^\varphi \frac{\alpha \sinh(\alpha r)}"
                r"{2 \pi \cosh(\alpha R) - 1} \mathrm{d} \phi \mathrm{d} r",
                color=WHITE,
            )
            .scale(0.275)
            .next_to(disk, UP, buff=0.1)
        )

        special_sector = native.AnnularSector(
            center=native.Point(),
            inner_radius=greedy_radius,
            outer_radius=graph_R,
            start_angle=special_start_angle,
            angle=sector_width,
            plane=plane,
            stroke_width=0,
        )
        special_sector.set_fill(WHITE, opacity=0.75)

        self.play(FadeIn(expected, special_sector))
        self.wait()

        # Highlight the greedy radius
        self.play(ApplyMethod(expected[0][14:15].set_color, BLUE))
        self.wait()

        # Highlight the disk radius
        self.play(
            ApplyMethod(disk.set_color, YELLOW),
            ApplyMethod(expected[0][13:14].set_color, YELLOW),
        )
        self.wait()

        # Highlight angle phi
        angle_arc = native.AnnularSector(
            center=native.Point(),
            inner_radius=graph_R + 0.3,
            outer_radius=graph_R + 0.4,
            start_angle=special_start_angle,
            angle=sector_width,
            plane=plane,
            stroke_width=0,
            z_index=5,
        ).set_fill(RED, opacity=1)
        angle_arc_label_center = native.Dot(
            native.Point(
                radius=graph_R + 0.9,
                azimuth=special_start_angle + sector_width / 2.0,
            ),
            plane=plane,
            z_index=5,
        ).set_opacity(0.0)
        phi_tex = (
            MathTex(r"\varphi", color=RED, z_index=6)
            .scale(0.33)
            .move_to(angle_arc_label_center)
        )
        phi_tex.add_updater(lambda x: x.move_to(angle_arc_label_center))
        phi_tex.set_z_index(6)

        self.play(
            FadeIn(angle_arc, phi_tex),
            ApplyMethod(expected[0][16:17].set_color, RED),
        )
        self.wait()

        # R is fixed
        self.play(
            ApplyMethod(disk.set_color, WHITE),
            ApplyMethod(expected[0][13:14].set_color, WHITE),
        )
        self.wait()

        # The choice
        c0 = (
            ContentTex("Choose:")
            .scale(0.275)
            .align_to(m0, UP)
            .align_to(m0, LEFT)
        )
        c1 = (
            ContentTex(r"radius $\rho$ containing greedy vertices")
            .scale(0.275)
            .next_to(c0, RIGHT, buff=mini_buff * 2.0)
            .align_to(c0, UP)
        )
        c1[0][6:7].set_color(BLUE)

        c2 = (
            ContentTex(r"angle $\varphi$ defining the discretization")
            .scale(0.275)
            .next_to(c1, DOWN, buff=mini_buff)
            .align_to(c1, LEFT)
        )
        c2[0][5:6].set_color(RED)

        self.play(
            FadeOut(expected),
            FadeIn(
                *[graph.vertices[v] for v in vertices_inside],
                *edges_inside,
                c0,
                c1,
                c2,
            ),
        )
        self.wait()

        # We want to make rho small to avoid overestimating the number of
        # vertices that are taken greedily.
        greedy_scale_factor = 0.9
        special_sector_stretch = (
            native.AnnularSectorStretchRadiiAndAngleInverse(
                special_sector,
                inner_radius=greedy_radius * greedy_scale_factor,
            )
        )
        self.play(
            native.Scale(greedy_disk, greedy_scale_factor),
            special_sector_stretch,
        )
        self.wait()

        special_sector_unstretch = (
            native.AnnularSectorStretchRadiiAndAngleInverse(
                special_sector, inner_radius=greedy_radius
            )
        )
        self.play(
            native.Scale(greedy_disk, 1.0 / greedy_scale_factor),
            special_sector_unstretch,
        )
        self.wait()

        # Scale cells
        rotation_animations = []
        for index, bar in enumerate(sector_bars[:special_sector_index]):
            rotation_animations.append(
                native.Rotate(
                    bar, sector_width * (special_sector_index - index)
                )
            )
        for index, bar in enumerate(sector_bars[(special_sector_index + 1) :]):
            rotation_animations.append(
                native.Rotate(bar, -sector_width * (index + 1))
            )
        angle_arc_stretch = native.AnnularSectorStretchAngleInverse(
            angle_arc, 2.0 * sector_width
        )
        special_sector_stretch = (
            native.AnnularSectorStretchRadiiAndAngleInverse(
                special_sector,
                inner_radius=greedy_radius * greedy_scale_factor,
                angle=2.0 * sector_width,
            )
        )
        self.play(
            *rotation_animations,
            native.Rotate(
                angle_arc_label_center, -sector_width / 2.0  # type: ignore
            ),
            native.Scale(greedy_disk, greedy_scale_factor),
            angle_arc_stretch,
            special_sector_stretch,
        )
        self.wait()

        # Inverse rotations
        inverse_rotation_animations = []
        for index, bar in enumerate(sector_bars[:special_sector_index]):
            inverse_rotation_animations.append(
                native.Rotate(
                    bar, -sector_width * (special_sector_index - index)
                )
            )
        for index, bar in enumerate(sector_bars[special_sector_index + 1 :]):
            inverse_rotation_animations.append(
                native.Rotate(bar, sector_width * (index + 1))
            )

        # Reverse rotation
        angle_arc_reverse_stretch = native.AnnularSectorStretchAngleInverse(
            angle_arc, sector_width
        )
        special_sector_reverse_stretch = (
            native.AnnularSectorStretchRadiiAndAngleInverse(
                special_sector, inner_radius=greedy_radius, angle=sector_width
            )
        )

        self.play(
            *inverse_rotation_animations,
            native.Scale(
                greedy_disk, 1.0 / greedy_scale_factor
            ),  # type: ignore
            native.Rotate(
                angle_arc_label_center, sector_width / 2.0  # type: ignore
            ),
            angle_arc_reverse_stretch,  # type: ignore
            special_sector_reverse_stretch,  # type: ignore
        )
        self.wait()

        # Recall growing neighborhood
        self.play(FadeIn(special_dot, special_neighborhood))
        self.wait()

        # Rotate again
        self.play(
            *rotation_animations,
            native.Rotate(
                angle_arc_label_center, -sector_width / 2.0  # type: ignore
            ),
            native.Scale(greedy_disk, greedy_scale_factor),
            angle_arc_stretch,
            special_sector_stretch,
            native.DotSetRadialCoordinate(
                special_dot, greedy_radius * greedy_scale_factor
            ),
        )
        self.wait()

        self.play(
            FadeOut(
                phi_tex,
                angle_arc,
                special_sector,
                special_dot,
                special_neighborhood,
            ),
            native.Scale(greedy_disk, 1.0 / greedy_scale_factor),
            *inverse_rotation_animations,
        )
        self.play(FadeIn(*all_non_empty_sectors, *empty_sectors))
        self.wait()

        self.play(
            FadeIn(t1),
            Restore(self.camera.frame),  # type: ignore
            FadeOut(
                *all_non_empty_sectors,
                *empty_sectors,
                *sector_bars,
                c0,
                c1,
                c2,
                disk,
            ),
        )
        self.wait()

        self.fade_out()
