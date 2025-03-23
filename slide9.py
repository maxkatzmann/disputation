import math
import random

from colour import Color
from manim import (
    BLACK,
    BLUE,
    DOWN,
    LEFT,
    PI,
    RIGHT,
    UP,
    WHITE,
    YELLOW,
    Difference,
    DrawBorderThenFill,
    FadeIn,
    FadeOut,
    Group,
    Intersection,
    MoveAlongPath,
    PolarPlane,
    Restore,
    SurroundingRectangle,
    VMobject,
)

from hmanim import native
from manim_presentation_template import (
    ContentTex,
    ContentText,
    DefaultSlide,
    SideNoteTex,
)


# Domination in HRGs
class Slide9(DefaultSlide):

    def content(self):
        # Draw the native background gradient.
        background = native.Background(
            Color("#0021FF"), Color("#D13B1D"), expansion=0.25
        ).scale(2)
        header = self.add_header(
            "Dominance in Hyperbolic Random Graphs", with_click=False
        ).shift(UP * 0.35)
        self.play(FadeIn(background, header))
        self.wait()

        # The plane
        graph_R = 8.0
        plane = PolarPlane(size=3)

        # The disk
        disk = native.Circle(
            center=native.Point(), radius=graph_R, plane=plane, z_index=1
        )
        self.play(FadeIn(disk))
        self.wait()

        # We want to show a vertex with its neighborhood region and trace the
        # dominance region in it.

        # Start with the dominant vertex
        dominant_vertex = native.Dot(
            native.Point(radius=graph_R * 0.5, azimuth=0.0),
            plane=plane,
            color=BLUE,
            z_index=3,
        )

        # Draw its neighborhood disk
        dominant_neighborhood = native.Circle(
            center=dominant_vertex.center,  # type: ignore
            radius=graph_R,
            plane=plane,
            color=BLUE,
            z_index=3,
        )

        # Draw the intersection of the whole disk and the neighborhood disk
        dominant_neighborhood_disk_intersection = Intersection(
            disk, dominant_neighborhood, color=BLUE, fill_opacity=0.5
        )

        self.play(
            FadeIn(
                dominant_vertex,
                dominant_neighborhood,
                dominant_neighborhood_disk_intersection,
            )
        )
        self.wait()

        # Draw the dominated vertex with its neighborhood region.
        dominated_vertex = native.Dot(
            native.Point(radius=graph_R * 0.75, azimuth=0.0),
            plane=plane,
            color=YELLOW,
            z_index=4,
        )
        dominated_neighborhood = native.Circle(
            center=dominated_vertex.center,  # type: ignore
            radius=graph_R,
            plane=plane,
            color=YELLOW,
            z_index=4,
        )
        # Move the neighborhood together with the vertex.
        dominated_neighborhood.add_updater(
            lambda x: x.set_center(dominated_vertex.center)
        )

        # Draw the intersection of the whole disk and the neighborhood disk.
        dominated_neighborhood_disk_intersection = Intersection(
            disk, dominated_neighborhood, color=YELLOW, fill_opacity=0.5
        )
        self.play(
            FadeIn(
                dominated_vertex,
                dominated_neighborhood,
                dominated_neighborhood_disk_intersection,
            )
        )
        self.wait()

        # Fade out the intersections again.
        self.play(
            FadeOut(
                dominant_neighborhood_disk_intersection,
                dominated_neighborhood_disk_intersection,
            )
        )
        self.wait()

        # Function that gives us the maximum angle between the dominated and
        # dominant vertex, depending on their radii, such that the former is
        # indeed dominated by the latter.
        def delta_angle(dominant_radius, dominated_radius):
            return 2.0 * (
                math.exp(-dominant_radius / 2.0)
                - math.exp(-dominated_radius / 2.0)
            )

        # The dominance region is not a primitive hyperbolic shape. To draw it,
        # we sample points along its boundary.
        sample_points = 20
        domination_area_radius_range = [
            dominant_vertex.center.radius
            + (graph_R - dominant_vertex.center.radius)
            * float(x)
            / sample_points
            for x in range(sample_points + 1)
        ]
        domination_boundary_points_north = [
            native.Point(
                radius=r, azimuth=delta_angle(dominant_vertex.center.radius, r)
            )
            for r in domination_area_radius_range
        ]
        domination_boundary_points_south = [
            native.Point(p.radius, -p.azimuth)
            for p in domination_boundary_points_north
        ]

        domination_boundary_north = native.PolygonalChain(
            *domination_boundary_points_north,  # type: ignore
            using_geodesic=False,
            plane=plane
        )

        # Rotate the dominated vertex as far as possible such that it remains
        # dominated.
        self.play(native.DotSetRadialCoordinate(dominated_vertex, graph_R))
        self.wait()

        self.play(
            native.Rotate(
                dominated_vertex,  # type: ignore
                domination_boundary_points_south[-1].azimuth - 2 * PI,
            )
        )
        self.wait()

        # We now want to zoom in on that intersection. Before hand, we save the
        # current camera state, so that we can zoom back out easily afterwards.
        self.camera.frame.save_state()  # type: ignore
        self.play(
            self.camera.frame.animate.scale(0.25).move_to(  # type: ignore
                dominated_vertex
            )
        )
        self.wait()

        # Rotate the point even further so that it is no longer dominated.
        further_angle = -PI / 24
        self.play(
            native.Rotate(dominated_vertex, further_angle)  # type: ignore
        )

        # Highlight the region where vertices would be that make the dominated
        # vertex actually not-dominated.
        problem_zone = Difference(
            Intersection(dominated_neighborhood, disk),
            dominant_neighborhood,
            color=YELLOW,
            fill_opacity=0.9,
        )
        self.play(FadeIn(problem_zone))
        self.wait()

        # Fade out the problem region and zoom back out.
        self.play(FadeOut(problem_zone))
        self.play(
            native.Rotate(dominated_vertex, -further_angle),  # type: ignore
        )
        self.wait()

        # Highlight the intersections: Wherever we move the yellow circle, we
        # need to ensure that its intersection with the white circle does not
        # move outside the blue circle.  In fact, when we move the circle, the
        # intersections stay right on top of each other.
        intersection_highlight_dot = native.Dot(
            center=native.Point(
                radius=graph_R,
                azimuth=(
                    dominated_vertex.center.azimuth
                    - 2.0 * math.exp(-graph_R / 2.0)
                ),
                # Above we see a quick math-hack to get angle of intersection
                # by computing the maximum angular distance to be connected two
                # vertices at radius `graph_R`.
            ),
            plane=plane,
            color=WHITE,
            z_index=4,
        ).scale(0.75)
        self.play(FadeIn(intersection_highlight_dot))
        self.wait()

        # Trace the dominance area
        domination_area_boundary = VMobject(color=YELLOW)
        domination_area_boundary.set_points_as_corners(
            [
                dominated_vertex.get_center(),
                dominated_vertex.get_center(),
            ]  # type: ignore
        )

        def update_path(_):
            previous_path = domination_area_boundary.copy()
            previous_path.add_points_as_corners(
                [dominated_vertex.get_center()]
            )
            domination_area_boundary.become(previous_path)

        domination_area_boundary.add_updater(update_path)

        inverted_boundary_points_south = list(
            reversed(domination_boundary_points_south)
        )
        inverted_boundary_south = native.PolygonalChain(
            *inverted_boundary_points_south,  # type: ignore
            using_geodesic=False,
            plane=plane
        )

        self.play(FadeIn(domination_area_boundary, run_time=0.1))
        self.play(
            Restore(self.camera.frame, run_time=3),  # type: ignore
            MoveAlongPath(
                dominated_vertex, inverted_boundary_south, run_time=5
            ),
        )
        self.wait()

        # Remove the intersection highlight
        self.play(FadeOut(intersection_highlight_dot))
        self.wait()

        # Draw the other side of the domination area.
        self.play(
            MoveAlongPath(
                dominated_vertex, domination_boundary_north, run_time=3
            )
        )
        self.wait()

        self.play(FadeOut(dominated_vertex, dominated_neighborhood))

        # Domination area fill
        domination_fill = native.PolygonalChain(
            *inverted_boundary_points_south,  # type: ignore
            *domination_boundary_points_north,  # type: ignore
            native.Point(graph_R + 1, 0),  # type: ignore
            using_geodesic=False,
            plane=plane
        )
        domination_fill = Intersection(
            domination_fill, disk, color=YELLOW, fill_opacity=0.75, z_index=1
        )
        self.play(FadeIn(domination_fill))
        self.wait()

        # Draw the hyperbolic random graph into the disk.
        graph_plane = PolarPlane(size=2)
        graph_R = 12.0
        graph = (
            native.Graph.from_files(
                edge_list_path="hrg-large.txt",
                coordinate_list_path="hrg-large.hyp",
                plane=graph_plane,
                using_geodesic=False,
                z_index=2,
            )
            .set_vertex_color(WHITE)
            .set_vertex_radius(0.04)
            .set_edge_color(WHITE, 0.25)
        )
        self.play(FadeIn(graph))
        self.wait()

        self.play(
            FadeOut(
                domination_fill,
                domination_area_boundary,
                dominant_neighborhood,
                dominant_vertex,
            )
        )

        # Draw the disk containing all vertices in the graph that are likely to
        # dominate.
        domination_radius = 10.0
        domination_disk = (
            native.Circle(
                center=native.Point(),
                radius=domination_radius,
                plane=graph_plane,
                z_index=3,
            )
            .set_stroke(BLUE)
            .set_fill(BLUE, opacity=0.5)
        )
        self.play(DrawBorderThenFill(domination_disk))

        t1 = (
            ContentText("High-degree vertices dominate.")
            .next_to(graph, DOWN, buff=0.3)
            .shift(LEFT * 3.5)
        )
        self.play(FadeIn(t1))
        self.wait()

        # Remove "dominating" vertices and edges
        dominating_vertices = [
            vertex
            for vertex in range(len(graph.vertices))
            if graph.coordinates[vertex].radius < domination_radius
        ]
        non_dominating_vertices = [
            vertex
            for vertex in range(len(graph.vertices))
            if graph.coordinates[vertex].radius >= domination_radius
        ]
        dominating_edges = set()
        for dominating_vertex in dominating_vertices:
            neighbors = graph.adjacencies[dominating_vertex]
            for neighbor in neighbors:
                dominating_edge = graph.get_edge(dominating_vertex, neighbor)
                if dominating_edge is None:
                    continue

                dominating_edges.add(dominating_edge)
        non_dominating_edges = [
            edge for edge in graph.edges if edge not in dominating_edges
        ]

        self.play(
            FadeOut(
                *[graph.vertices[vertex] for vertex in dominating_vertices],
                *dominating_edges
            )
        )

        # To bound the pathwidth of the remainder, we introduced a circular arc
        # super graph. We now draw the corresponding arcs of the vertices.
        def arc_for_vertex(vertex):
            angle = 3 * 2 * math.exp(graph_R / 2.0 - vertex.center.radius)
            opacity = random.uniform(0.25, 1.0)
            return native.Arc(
                center=native.Point(),
                radius=vertex.center.radius,
                start_angle=vertex.center.azimuth - angle,
                angle=2 * angle,
                plane=graph_plane,
                color=YELLOW,
            ).set_opacity(opacity)

        arcs = [
            arc_for_vertex(graph.vertices[i]) for i in non_dominating_vertices
        ]
        self.play(
            FadeOut(
                domination_disk,
                *[graph.vertices[i] for i in non_dominating_vertices]
            ),
            FadeIn(*arcs),
        )

        t2 = (
            ContentText("Remainder has small path width.")
            .next_to(graph, DOWN, buff=0.3)
            .next_to(t1, RIGHT, buff=1.0)
        )
        self.play(FadeIn(t2))
        self.wait()

        # Theorem
        t3 = ContentTex(
            r"Vertex Cover can be solved in polynomial time on Hyperbolic"
            r"\\Random Graphs, with high probability.",
            tex_environment="flushleft",
        )
        t3_cite = (
            SideNoteTex(r"Bläsius, Friedrich, Fischbeck \& K., STACS 2020")
            .next_to(t3, DOWN)
            .align_to(t3, LEFT)
        )
        g3 = Group(t3, t3_cite).shift(DOWN * 1.6)
        b3 = (
            SurroundingRectangle(g3, buff=0.3)
            .set_z_index(2)
            .set_stroke(WHITE)
            .set_fill(BLACK, opacity=0.9)
        )
        t3.set_z_index(3)
        t3_cite.set_z_index(3)
        self.play(FadeIn(g3, b3))
        self.wait()

        self.play(FadeOut(g3, b3))
        self.play(FadeOut(header, t1, t2, disk, *non_dominating_edges, *arcs))
        self.play(FadeOut(background))
