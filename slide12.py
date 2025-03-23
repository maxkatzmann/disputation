import copy

from colour import Color
from manim import (
    BLUE,
    DOWN,
    LEFT,
    RED,
    RIGHT,
    UP,
    WHITE,
    YELLOW,
    Create,
    DrawBorderThenFill,
    FadeIn,
    FadeOut,
    PolarPlane,
    Text,
    Transform,
)

from hmanim import native
from manim_presentation_template import ContentTex, ContentText, DefaultSlide


# Greedy Vertex Cover in HRGs
class Slide12(DefaultSlide):

    def content(self):
        # Draw the native background gradient.
        background = native.Background(
            Color("#0021FF"), Color("#D13B1D"), expansion=0.25
        ).scale(2)
        background.set_z_index(-1)
        header = self.add_header(
            "Greedy Approximation in Hyperbolic Random Graphs",
            with_click=False,
        ).shift(UP * 0.35)

        # The Graph
        graph_R = 12.0
        plane = PolarPlane(size=2)
        graph = (
            native.Graph.from_files(
                edge_list_path="hrg-large.txt",
                coordinate_list_path="hrg-large.hyp",
                plane=plane,
                using_geodesic=False,
            )
            .set_vertex_color(WHITE)
            .set_vertex_radius(0.04)
            .set_edge_color(WHITE, 0.25)
        )
        self.play(FadeIn(background, header, graph))
        self.wait()

        # We want the vertex with the smallest radius. To this end,
        # we first sort all vertices by radius.  (We need the sorted
        # order later anyways.)
        sorted_vertices = []
        for index, dot in enumerate(graph.vertices):
            sorted_vertices.append((index, dot.center.radius))
        sorted_vertices.sort(key=lambda x: x[1])
        # Now we forget the radii, since we are only interested in
        # the vertex order.
        sorted_vertices = [x for (x, _) in sorted_vertices]

        # Draw the disk containing all vertices that are likely to dominate.
        domination_radius = 10.0
        domination_disk = native.Circle(
            center=native.Point(),
            radius=domination_radius,
            plane=plane,
            color=BLUE,
        ).set_fill(BLUE, opacity=0.5)
        self.play(DrawBorderThenFill(domination_disk))
        self.wait()

        # We highlight the neighborhood of the vertex with smallest
        # radius.
        high_degree_vertex = sorted_vertices[0]
        high_degree_highlight_dot = native.Dot(
            graph.coordinates[high_degree_vertex],
            radius=0.1,
            plane=plane,
            color=YELLOW,
            z_index=2,
        )
        high_degree_circle = native.Circle(
            center=graph.coordinates[high_degree_vertex],
            radius=graph_R - 0.1,
            plane=plane,
            color=YELLOW,
            z_index=2,
        )

        # Draw the incident edges of the high-degree vertex.
        high_degree_neighbors = graph.adjacencies[high_degree_vertex]
        high_degree_edges = []
        high_degree_dots = []
        for v in high_degree_neighbors:
            edge = native.Line(
                graph.coordinates[high_degree_vertex],
                graph.coordinates[v],
                plane=plane,
                using_geodesic=False,
                stroke_width=2.0,
                color=YELLOW,
                z_index=2,
            )
            high_degree_edges.append(edge)
            dot = native.Dot(
                graph.coordinates[v],
                radius=0.04,
                plane=plane,
                color=YELLOW,
                z_index=2,
            )
            high_degree_dots.append(dot)

        self.play(
            FadeIn(
                high_degree_highlight_dot,
                high_degree_circle,
                *high_degree_dots,
            ),
            *[Create(edge) for edge in high_degree_edges],
        )
        self.wait()

        t1 = (
            ContentText("Greedy prefers safe vertices ")
            .next_to(graph, DOWN, buff=0.3)
            .shift(LEFT * 3.6)
        )
        self.play(FadeIn(t1))
        self.wait()

        # Remove "dominating" vertices and edges
        dominating_vertices = [
            vertex
            for vertex in range(len(graph.vertices))
            if graph.coordinates[vertex].radius < domination_radius
        ]
        dominating_edges = set()
        for dominating_vertex in dominating_vertices:
            neighbors = graph.adjacencies[dominating_vertex]
            for neighbor in neighbors:
                dominating_edge = graph.get_edge(dominating_vertex, neighbor)
                if dominating_edge is None:
                    continue

                dominating_edges.add(dominating_edge)

        self.play(
            FadeOut(
                *[graph.vertices[vertex] for vertex in dominating_vertices],
                *dominating_edges,
                high_degree_highlight_dot,
                high_degree_circle,
                *high_degree_edges,
                *high_degree_dots,
                domination_disk,
            )
        )

        t2 = ContentText("and picks low degree vertices at random.").next_to(
            t1, RIGHT, buff=0.15
        )
        self.play(FadeIn(t2))
        self.wait()

        t3 = ContentText(
            "and picks low degree vertices at random.", t2c={"random": YELLOW}
        ).next_to(t1, RIGHT, buff=0.15)
        self.play(Transform(t2, t3))
        self.wait()

        # Improved Greedy
        new_header = (
            Text("Improved Greedy in Hyperbolic Random Graphs")
            .scale(DefaultSlide.headerScale)
            .move_to(header)
        )
        self.play(
            Transform(header, new_header),
            FadeIn(
                *[graph.vertices[vertex] for vertex in dominating_vertices],
                *dominating_edges,
            ),
            FadeOut(t1, t2, t3),
        )
        self.wait()

        # How the improved greedy works

        # Iterate vertices in order of increasing radius,
        # meaning increasing distance from the center
        start_radius = 0.001

        # Closer look at the algorithm.
        # Start with the vertex closest to the center.

        v0 = sorted_vertices[0]
        processed_vertices = [
            v0
        ]  # We keep track of the vertices we have processed already.
        solved_vertices = []

        start_radius = 0.001
        radius_circle = native.Circle(
            center=native.Point(), radius=start_radius, plane=plane, color=BLUE
        )
        self.play(FadeIn(radius_circle))
        self.play(
            native.Scale(
                radius_circle,
                factor=graph.coordinates[v0].radius / start_radius,
            )
        )

        v0_dot = native.Dot(
            graph.coordinates[v0],
            radius=0.1,
            plane=plane,
            color=BLUE,
            z_index=3,
        )
        self.play(Create(v0_dot))
        self.play(FadeOut(radius_circle))
        self.wait()

        # Identify its neighbors
        v0_neighbors = graph.adjacencies[v0]
        v0_neighbors_dots = [
            native.Dot(
                graph.coordinates[v],
                radius=0.1,
                plane=plane,
                color=RED,
                z_index=1,
            )
            for v in v0_neighbors
        ]
        self.play(FadeIn(*v0_neighbors_dots))
        self.wait()

        # Remove its edges
        all_edges = []
        v0_edges = [
            edge
            for v in v0_neighbors
            if (edge := graph.get_edge(v0, v)) is not None
        ]
        all_edges += v0_edges
        self.play(FadeOut(*v0_edges))
        self.wait()

        # Find small components

        # We want to be able to perform BFSs in the reduced graph
        mutable_graph_adjacencies = copy.deepcopy(graph.adjacencies)

        def remove_edges_incident_to(v):
            neighbors = mutable_graph_adjacencies[v]
            for neighbor in neighbors:
                mutable_graph_adjacencies[neighbor].remove(v)

            mutable_graph_adjacencies[v] = []

        remove_edges_incident_to(v0)

        def nodes_seen_in_BFS_starting_at(start_vertex):
            if start_vertex in processed_vertices:
                return None

            state = [0 for _ in graph.vertices]
            state[start_vertex] = 1  # 0 = unseen, 1 = seen, 2 = processed
            seen_vertices = [start_vertex]  # we have seen the start_node
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

        # Find small components
        small_size = 4
        small_dots = []

        for neighbor in graph.adjacencies[v0]:
            component = nodes_seen_in_BFS_starting_at(neighbor)
            component_is_small = len(component) <= small_size  # type: ignore
            if not component_is_small:
                continue

            solved_vertices += component  # type: ignore
            component_dots = [
                native.Dot(
                    graph.coordinates[v],
                    radius=0.1,
                    plane=plane,
                    color=YELLOW,
                    z_index=2,
                )
                for v in component  # type: ignore
            ]
            small_dots += component_dots

        t4 = (
            ContentTex(
                "Solve components of small size that "
                "get separated in the process.",
            )
            .scale(0.9)
            .next_to(graph, DOWN)
        )
        self.play(FadeIn(*small_dots), FadeOut(*v0_neighbors_dots), FadeIn(t4))
        self.wait()

        # Do the same with the next vertex
        v1 = sorted_vertices[1]
        self.play(FadeIn(radius_circle))
        self.play(
            native.Scale(
                radius_circle,
                factor=graph.coordinates[v1].radius
                / graph.coordinates[v0].radius,
            )
        )

        v1_dot = native.Dot(
            graph.coordinates[v1],
            radius=0.1,
            plane=plane,
            color=BLUE,
            z_index=3,
        )
        self.play(Create(v1_dot))
        self.play(FadeOut(radius_circle))
        self.wait()

        v1_neighbors = mutable_graph_adjacencies[v1]
        v1_neighbors_dots = [
            native.Dot(
                graph.coordinates[v],
                radius=0.1,
                plane=plane,
                color=RED,
                z_index=1,
            )
            for v in v1_neighbors
        ]
        self.play(FadeIn(*v1_neighbors_dots))
        self.wait()

        v1_edges = [
            edge
            for v in v1_neighbors
            if (edge := graph.get_edge(v1, v)) is not None
        ]
        all_edges += v1_edges
        self.play(FadeOut(*v1_edges))
        self.wait()
        remove_edges_incident_to(v1)

        v1_small_dots = []
        for neighbor in graph.adjacencies[v1]:
            component = nodes_seen_in_BFS_starting_at(neighbor)
            if component is None:
                continue

            component_is_small = len(component) <= small_size
            if not component_is_small:
                continue

            solved_vertices += component
            component_dots = [
                native.Dot(
                    graph.coordinates[v],
                    radius=0.1,
                    plane=plane,
                    color=YELLOW,
                    z_index=2,
                )
                for v in component
            ]
            v1_small_dots += component_dots

        self.play(FadeIn(*v1_small_dots))
        self.wait()
        small_dots += v1_small_dots

        self.play(FadeOut(*v1_neighbors_dots))
        self.wait()
        processed_vertices.append(v1)

        # The rest of the graph.
        fast_animation_time = 0.1

        def process_vertex(v, solved_vertices):
            if v in solved_vertices:
                return [], []

            v_dot = native.Dot(
                graph.coordinates[v], radius=0.1, plane=plane, color=BLUE
            )

            v_neighbors = mutable_graph_adjacencies[v]
            v_edges = [graph.get_edge(v, u) for u in v_neighbors]
            remove_edges_incident_to(v)

            v_small_dots = []

            for neighbor in graph.adjacencies[v]:
                component = nodes_seen_in_BFS_starting_at(neighbor)
                if not component:
                    continue

                component_is_small = len(component) <= small_size
                if not component_is_small:
                    continue

                solved_vertices += component

                component_dots = [
                    native.Dot(
                        graph.coordinates[v],
                        radius=0.1,
                        plane=plane,
                        color=YELLOW,
                    )
                    for v in component
                ]
                v_small_dots += component_dots

            processed_vertices.append(v)
            return [v_dot] + v_small_dots, v_edges

        # Seems like the animation time cannot be set arbitrarily small.
        # Therefore, we group vertices and groups and animate them
        # simultaneously.
        max_group_size = 1
        # The group size should start small and then increase in the process.
        # That is, every `max_group_size_increase_rate` the `max_group_size`
        # increases by `max_group_size_increase_step`.
        current_step = 0
        max_group_size_increase_rate = 3
        max_group_size_increase_step = 2

        current_dot_group = []
        current_edge_group = []
        current_group_size = 0

        for v in sorted_vertices[2:]:
            new_dots, edges = process_vertex(v, solved_vertices)
            small_dots += new_dots
            all_edges += edges

            current_dot_group += new_dots
            current_edge_group += edges

            current_group_size += 1

            if current_group_size < max_group_size:
                continue

            current_step += 1
            if current_step % max_group_size_increase_rate == 0:
                max_group_size *= max_group_size_increase_step

            # Animate the group
            if current_dot_group and current_edge_group:
                self.play(
                    FadeIn(
                        *[dot for dot in current_dot_group],
                        run_time=fast_animation_time,
                    ),
                    FadeOut(*current_edge_group, run_time=fast_animation_time),
                )
            elif current_dot_group:
                self.play(
                    FadeIn(
                        *[dot for dot in current_dot_group],
                        run_time=fast_animation_time,
                    )
                )
            elif current_edge_group:
                self.play(
                    FadeOut(*current_edge_group, run_time=fast_animation_time)
                )

            current_dot_group = []
            current_edge_group = []
            current_group_size = 0

        # Make sure, we animate the dots that did not fill up the last group.
        # Animate the group
        if current_dot_group and current_edge_group:
            self.play(
                FadeIn(
                    *[dot for dot in current_dot_group],
                    run_time=fast_animation_time,
                ),
                FadeOut(*current_edge_group, run_time=fast_animation_time),
            )
        elif current_dot_group:
            self.play(
                FadeIn(
                    *[dot for dot in current_dot_group],
                    run_time=fast_animation_time,
                )
            )
        elif current_edge_group:
            self.play(
                FadeOut(*current_edge_group, run_time=fast_animation_time)
            )
        self.click()

        # Finally, we show the domination disk again.
        domination_radius = 10.0
        domination_disk = native.Circle(
            center=native.Point(),
            radius=domination_radius,
            plane=plane,
            color=BLUE,
            z_index=4,
        ).set_fill(BLUE, opacity=0.5)
        self.play(FadeIn(domination_disk))
        self.wait()

        visible_edges = [edge for edge in graph.edges if edge not in all_edges]

        self.remove(*graph.vertices)
        self.play(
            FadeOut(*visible_edges, run_time=0.25),
            FadeOut(
                domination_disk,
                header,
                v0_dot,
                v1_dot,
                t4,
                *small_dots,
            ),
        )
        self.play(FadeOut(background))
