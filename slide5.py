import math

from colour import Color
from hmanim import native
from hmanim.native.scale import Scale
from manim import (
    BLUE,
    DEGREES,
    DOWN,
    LEFT,
    RIGHT,
    TAU,
    UP,
    WHITE,
    YELLOW,
    ApplyMethod,
    Axes,
    Create,
    CurvesAsSubmobjects,
    Dot,
    FadeIn,
    FadeOut,
    Group,
    Indicate,
    Line,
    MoveAlongPath,
    PolarPlane,
    ShowIncreasingSubsets,
    Text,
    Triangle,
    smooth,
)

from manim_presentation_template import DefaultSlide, SideNoteTex


# Introduction hyperbolic space & HRGs
class Slide5(DefaultSlide):

    def content(self):
        # The center of our projection.
        center_of_projection_dot = Dot().set_opacity(0.0)

        def get_hyperbolic_center_of_projection():
            return native.Point(
                *plane.point_to_polar(
                    center_of_projection_dot.get_center()  # type: ignore
                )
            )

        # Draw the gradient background.
        background = native.Background(
            Color("#0021FF"), Color("#D13B1D"), expansion=0.25
        ).scale(2)
        background.add_updater(
            lambda x: x.move_to(center_of_projection_dot.get_center())
        )
        self.play(FadeIn(background))
        self.wait()

        # The plane that all our hyperbolic objects live in.
        plane = PolarPlane(size=5)

        # Show a plot comparing polynomial and exponential expansion.
        axes = Axes(
            x_range=[0, 5.3, 1],
            y_range=[0, 80, 20],
            x_length=3,
            y_length=2.5,
            tips=True,
            axis_config={
                "tip_width": 0.15,
                "tip_height": 0.15,
            },
        )
        axes.shift(RIGHT * 4.25)

        # Add labels
        x_label = Text("Radius", font_size=24).next_to(axes, DOWN)
        y_label = (
            Text("Area", font_size=24).rotate(90 * DEGREES).next_to(axes, LEFT)
        )

        # Create polynomial growth curve
        polynomial_curve = axes.plot(
            lambda x: x**1.9,
            x_range=[0, 5.3],
            color=BLUE,
        )

        plot_group = Group(axes, x_label, y_label, polynomial_curve)

        self.play(FadeIn(plot_group))
        self.wait()

        # Create exponential growth curve
        exponential_curve = axes.plot(
            lambda x: math.exp(x - 1),
            x_range=[0, 5.3],
            color=YELLOW,
        )

        # Create a circle that grows together with the curve.
        growing_circle = native.Circle(
            center=native.Point(),
            radius=0.01,
            plane=plane,
            color=YELLOW,
        )
        growing_run_time = 2
        growing_rate = smooth
        self.play(FadeIn(growing_circle))
        self.play(
            Create(
                exponential_curve,
                run_time=growing_run_time,
                rate_func=growing_rate,
            ),
            native.Scale(
                growing_circle,
                factor=250,
                run_time=growing_run_time,
                rate_func=growing_rate,
            ),
        )
        self.wait()

        # Clean up if needed
        self.play(FadeOut(plot_group, exponential_curve, growing_circle))
        self.wait()

        # Draw the circle center.
        center_dot = native.Dot(native.Point(), plane=plane, z_index=4)
        center_dot.add_updater(
            lambda x: x.set_center_of_projection(
                get_hyperbolic_center_of_projection()
            )
        )

        # Draw the circle.
        circle = native.Circle(
            center=center_dot.center,  # type: ignore
            radius=5.0,
            plane=plane,
            color=WHITE,
            z_index=3,
        )
        self.play(FadeIn(center_dot, circle))
        self.wait()

        # Make sure the circle moves together with the circle center.
        circle.add_updater(lambda x: x.set_center(center_dot.center))
        circle.add_updater(
            lambda x: x.set_center_of_projection(
                get_hyperbolic_center_of_projection()
            )
        )

        # Draw the semi circle.
        semi_circle = native.Arc(
            center_dot.center,  # type: ignore
            circle.radius,
            start_angle=0.75 * TAU,
            angle=TAU / 2,
            plane=plane,
            is_closed=True,
            color=WHITE,
            fill_opacity=0.5,
            z_index=2,
        )
        semi_circle.add_updater(lambda x: x.set_center(center_dot.center))
        semi_circle.add_updater(
            lambda x: x.set_center_of_projection(
                get_hyperbolic_center_of_projection()
            )
        )
        self.play(FadeIn(semi_circle))
        self.wait()

        # Translate the circle horizontally.
        translation_distance = 4.0
        self.play(native.Translate(center_dot, translation_distance))
        self.wait()

        # Show the other half of the circle.
        semi_circle2 = native.Arc(
            center_dot.center,  # type: ignore
            circle.radius,
            start_angle=0.25 * TAU,
            angle=TAU / 2,
            plane=plane,
            is_closed=True,
            color=BLUE,
            fill_opacity=0.66,
            z_index=1,
        )
        semi_circle2.add_updater(lambda x: x.set_center(center_dot.center))
        self.play(FadeIn(semi_circle2))
        self.wait()

        # Hide the other half of the circle again.
        self.play(FadeOut(semi_circle2))
        self.wait()

        # Get the points that represent the north and south poles of the
        # circle.
        highlight_color = BLUE
        north_dot = native.Dot(
            native.Point(), plane=plane, color=highlight_color, z_index=5
        )
        north_dot.add_updater(
            lambda x: x.set_center(
                native.Point(circle.radius, 0.25 * TAU)
                .translated_by(center_dot.center.radius)
                .rotated_by(center_dot.center.azimuth)
            )
        )
        north_dot.add_updater(
            lambda x: x.set_center_of_projection(
                get_hyperbolic_center_of_projection()
            )
        )

        south_dot = native.Dot(
            native.Point(), plane=plane, color=highlight_color, z_index=5
        )
        south_dot.add_updater(
            lambda x: x.set_center(
                native.Point(circle.radius, 0.75 * TAU)
                .translated_by(center_dot.center.radius)
                .rotated_by(center_dot.center.azimuth)
            )
        )
        south_dot.add_updater(
            lambda x: x.set_center_of_projection(
                get_hyperbolic_center_of_projection()
            )
        )

        self.play(FadeIn(north_dot, south_dot))
        self.wait()

        # Get the geodesic between them.
        line = native.Line(
            north_dot.center,  # type: ignore
            south_dot.center,  # type: ignore
            plane=plane,
            color=highlight_color,
            z_index=5,
        )
        line.add_updater(
            lambda x: x.move_to(
                north_dot.center,  # type: ignore
                south_dot.center,  # type: ignore
            )
        )
        line.add_updater(
            lambda x: x.set_center_of_projection(
                get_hyperbolic_center_of_projection()
            )
        )
        self.play(Create(line), FadeOut(semi_circle))
        self.wait()

        # Get the Euclidean geodesic between them, but in hyperbolic space.
        euclidean_north = north_dot.center.to_point_in_plane(plane)
        euclidean_south = south_dot.center.to_point_in_plane(plane)
        # Interpolate between the two.
        samples = 100.0
        euclidean_line_points = []
        for t in range(int(samples)):
            alpha = t / samples
            euclidean_line_points.append(
                (1 - alpha) * euclidean_north  # type: ignore
                + alpha * euclidean_south  # type: ignore
            )

        euclidean_line_points.append(euclidean_south)
        fake_geodesic = native.PolygonalChain(
            *[
                native.Point(*plane.point_to_polar(p))  # type: ignore
                for p in euclidean_line_points
            ],
            plane=plane,
            using_geodesic=False
        ).set_color(YELLOW)
        fake_geodesic.add_updater(
            lambda x: x.set_center_of_projection(
                get_hyperbolic_center_of_projection()
            )
        )
        self.play(Create(fake_geodesic))
        self.wait()

        # Move the center of the projection.
        translation_line = Line(
            native.Point().to_point_in_plane(plane),  # type: ignore
            native.Point(4.0, 0.0).to_point_in_plane(plane),  # type: ignore
        )
        self.play(
            MoveAlongPath(
                center_of_projection_dot, translation_line, run_time=4
            )
        )

        # Reset the center of the projection, after fading out the objects.
        self.play(
            FadeOut(
                fake_geodesic, line, north_dot, south_dot, circle, center_dot
            )
        )
        self.wait()

        back_translation_line = Line(
            native.Point(4.0, 0.0).to_point_in_plane(plane),  # type: ignore
            native.Point().to_point_in_plane(plane),  # type: ignore
        )
        self.play(
            MoveAlongPath(
                center_of_projection_dot, back_translation_line, run_time=3
            )
        )
        self.wait()

        # How to HRG
        plane = PolarPlane(size=3)
        graph_R = 8.6
        center_dot = native.Dot(native.Point(), plane=plane, z_index=4)
        circle = native.Circle(
            center=center_dot.center,  # type: ignore
            radius=graph_R,
            plane=plane,
            color=WHITE,
            z_index=3,
        )

        # Draw the citation.
        hrg_cite = SideNoteTex(
            "Krioukov, Papadopoulos, Kitsak, Vahdat \& Boguñá,",
            " Phys. Rev. E 2010",
        ).next_to(circle, DOWN)
        self.play(FadeIn(hrg_cite))
        self.wait()

        # Draw the disk again and the graph.
        self.play(FadeIn(circle))
        self.wait()

        graph = (
            native.Graph.from_files(
                edge_list_path="hrg.txt",
                coordinate_list_path="hrg.hyp",
                plane=plane,
                z_index=1,
            )
            .set_vertex_color(WHITE, 1.0)
            .set_edge_color(WHITE, 1.0)
        )

        vertex_group = Group(*graph.vertices)
        self.play(ShowIncreasingSubsets(vertex_group))
        self.wait()

        # Draw edges of high-degree node.
        # highlight_vertex = 89
        highlight_vertex = 18
        highlight_vertex_point = graph.vertices[highlight_vertex].center
        highlight_vertex_dot = native.Dot(
            center=highlight_vertex_point,  # type: ignore
            color=BLUE,
            plane=plane,
            z_index=2,
        )
        self.play(
            FadeIn(highlight_vertex_dot),
            *[
                ApplyMethod(vertex.set_opacity, 0.1)
                for vertex in graph.vertices
            ]
        )
        self.play(Indicate(highlight_vertex_dot, color=BLUE))  # type: ignore
        self.wait()

        # Highlight the neighborhood of a vertex, by first redrawing the disk
        # boundary and moving it to the vertex afterwards.
        highlight_vertex_circle = native.Circle(
            center=native.Point(),
            radius=graph_R,
            plane=plane,
            stroke_width=5.0,
            color=BLUE,
            z_index=3,
        )
        self.play(Create(highlight_vertex_circle, run_time=3))
        self.wait()

        self.play(
            native.RotatedTranslate(
                highlight_vertex_circle,
                highlight_vertex_point.radius,
                highlight_vertex_point.azimuth,
            )
        )
        self.wait()

        # Highlight the neighbors of the vertex.
        neighbor_points = [
            graph.vertices[v].center
            for v in graph.adjacencies[highlight_vertex]
        ]
        neighbor_dots = [
            native.Dot(p, plane=plane, z_index=2, color=WHITE)
            for p in neighbor_points
        ]
        self.play(FadeIn(*neighbor_dots))
        self.wait()

        # Draw edges to neighbors.
        highlight_vertex_incident_edges = [
            native.Line(
                highlight_vertex_point,  # type: ignore
                p,
                plane=plane,
                stroke_color=WHITE,
                z_index=0,
            )
            for p in neighbor_points
        ]
        self.play(*[Create(edge) for edge in highlight_vertex_incident_edges])
        self.wait()

        self.play(
            # FadeIn nodes and edges in the graph
            FadeIn(*graph.edges),
            *[ApplyMethod(node.set_opacity, 1.0) for node in graph.vertices],
            # FadeOut highlight vertex, circle, its neighbors and edges.
            FadeOut(*highlight_vertex_incident_edges),
            FadeOut(
                *neighbor_dots, highlight_vertex_dot, highlight_vertex_circle
            )
        )
        self.wait()

        # Draw the graph using straight lines instead of bent ones.
        straight_graph = (
            native.Graph.from_files(
                edge_list_path="hrg.txt",
                coordinate_list_path="hrg.hyp",
                plane=plane,
                using_geodesic=False,
                z_index=1,
            )
            .set_vertex_color(WHITE, 1.0)
            .set_edge_color(WHITE, 1.0)
        )

        self.play(native.SetCurvature(graph, -0.001))
        self.add(straight_graph)
        self.remove(graph)
        self.wait()

        # Showing that the graph has the properties we want.  We start by
        # highlighting the neighborhood of the low-degree vertex again.
        straight_neighbor_edges = [
            native.Line(
                highlight_vertex_point,  # type: ignore
                p,
                plane=plane,
                using_geodesic=False,
                z_index=1,
            ).set_stroke(WHITE)
            for p in neighbor_points
        ]

        self.play(
            FadeOut(hrg_cite),
            FadeIn(
                highlight_vertex_dot,
                highlight_vertex_circle,
                *neighbor_dots,
                *straight_neighbor_edges,
                run_time=2
            ),
            *[
                ApplyMethod(node.set_opacity, 0.1)
                for node in straight_graph.vertices
            ],
            *[
                ApplyMethod(edge.set_opacity, 0.1)
                for edge in straight_graph.edges
            ]
        )

        # Move the circle to a large degree node.
        high_degree_vertex = 89
        high_degree_vertex_point = graph.vertices[high_degree_vertex].center
        highlight_circle_translation_distance = (
            high_degree_vertex_point.radius - highlight_vertex_point.radius
        )
        highlight_circle_rotation_angle = (
            high_degree_vertex_point.azimuth - highlight_vertex_point.azimuth
        )

        highlight_vertex_dot.add_updater(
            lambda x: x.set_center(highlight_vertex_circle.center)
        )

        # FadeOut the neighbors
        self.play(FadeOut(*neighbor_dots, *straight_neighbor_edges))
        self.wait()

        # Move the circle to the high-degree vertex
        self.play(
            native.TranslateAndRotate(
                highlight_vertex_circle,
                highlight_circle_translation_distance,
                highlight_circle_rotation_angle,
            )
        )
        self.wait()

        # Show the edges of the high-degree vertex
        high_degree_vertex_neighbors = straight_graph.adjacencies[
            high_degree_vertex
        ]
        high_vertex_straight_neighbor_edges = [
            native.Line(
                high_degree_vertex_point,  # type: ignore
                graph.vertices[v].center,
                plane=plane,
                using_geodesic=False,
                z_index=1,
            ).set_stroke(WHITE)
            for v in high_degree_vertex_neighbors
        ]
        high_vertex_straight_neighbor_dots = [
            straight_graph.vertices[v] for v in high_degree_vertex_neighbors
        ]
        self.play(
            FadeIn(*high_vertex_straight_neighbor_edges),
            *[
                ApplyMethod(vertex.set_opacity, 1.0)
                for vertex in high_vertex_straight_neighbor_dots
            ]
        )
        self.wait()

        # Draw the power-law plot
        ax = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 10, 1],
            x_length=3,
            y_length=3,
            tips=True,
            axis_config={
                "include_numbers": False,
                "include_ticks": False,
                "tip_width": 0.15,
                "tip_height": 0.15,
            },
        )

        ax.shift(LEFT * 4.75)

        x_label = (
            Text("Degree")
            .scale(0.5)
            .shift(LEFT * 4.75)
            .align_to(ax, DOWN)
            .shift(DOWN * 0.5)
        )
        y_label = (
            Text("Fraction of Vertices")
            .rotate_about_origin(90 * DEGREES)
            .scale(0.5)
            .align_to(ax, LEFT)
            .shift(LEFT * 0.375)
        )

        plot = ax.plot(
            lambda x: 5 / (x - 0.1), x_range=[0.69, 8.5], use_smoothing=False
        )
        gradient_plot = CurvesAsSubmobjects(plot)
        self.play(FadeIn(gradient_plot, ax, x_label, y_label))
        self.wait()

        # Draw the edges among the neighbors of the high-degree vertex.
        edges_among_neighbors = []
        for neighbor in high_degree_vertex_neighbors:
            neighbor_neighbors = straight_graph.adjacencies[neighbor]
            for neighbor_neighbor in neighbor_neighbors:
                if neighbor_neighbor not in high_degree_vertex_neighbors:
                    continue

                edges_among_neighbors.append(
                    native.Line(
                        straight_graph.vertices[neighbor].center,
                        straight_graph.vertices[neighbor_neighbor].center,
                        plane=plane,
                        using_geodesic=False,
                        z_index=1,
                    ).set_stroke(WHITE)
                )

        self.play(
            FadeIn(*edges_among_neighbors),
            FadeOut(*high_vertex_straight_neighbor_edges),
        )

        # Draw the triangles again.
        tri1 = Triangle(color=WHITE, stroke_width=7)
        tri1_dot1 = Dot(radius=0.15).shift(UP)
        tri1_dot2 = Dot(radius=0.15).shift(RIGHT * 0.85).shift(DOWN * 0.5)
        tri1_dot3 = Dot(radius=0.15).shift(LEFT * 0.85).shift(DOWN * 0.5)
        tri1.add(tri1_dot1)
        tri1.add(tri1_dot2)
        tri1.add(tri1_dot3)

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
        tri1.shift(RIGHT * 0.75)
        tri2.shift(RIGHT * 0.75)
        tri3.shift(RIGHT * 0.75)
        self.play(FadeIn(tri1, tri2, tri3))
        self.wait()

        self.play(
            *[
                ApplyMethod(obj.set_opacity, 0.0)
                for obj in straight_graph.vertices
                + straight_graph.edges
                + [circle, highlight_vertex_circle, highlight_vertex_dot]
                + edges_among_neighbors
                + [
                    gradient_plot,
                    ax,
                    x_label,
                    y_label,
                    tri1,
                    tri2,
                    tri3,
                ]
            ]
        )
        self.play(FadeOut(background))
