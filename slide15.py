from colour import Color
from manim import (
    BLUE,
    DOWN,
    GREEN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    WHITE,
    AnimationGroup,
    FadeIn,
    Group,
    ImageMobject,
    PolarPlane,
    Rectangle,
    SurroundingRectangle,
    Tex,
    Write,
)

from hmanim import native
from manim_presentation_template import DefaultSlide
from mextensions.layout import Layout
from mextensions.recolorablebarchart import RecolorableBarChart


# Summary
class Slide15(DefaultSlide):

    def content(self):
        self.add_header("Summary")

        # Investigated the relationship between complex networks and underlying
        # geometry with a focus on algorithmic properties
        background = native.Background(
            Color("#0021FF"),
            Color("#D13B1D"),
            width=270,
            height=150,
            expansion=0.5,
        ).scale(0.35)
        r1 = SurroundingRectangle(background, buff=0.0, color=WHITE)
        plane = PolarPlane(size=1).move_to(background)
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
            .scale(0.8)
        )
        g1 = Group(background, plane, graph, r1)

        # To this end, we took several problems where prior empirical analyses
        # hinted at a huge gap between theoretical worst-case bounds and
        # the performance on real-world instances and used the relation between
        # complex networks and hyperbolic geometry in order to explain the
        # observed phenomena.
        r2 = SurroundingRectangle(r1, buff=0.0, color=WHITE).next_to(r1, RIGHT)
        image_scale = 0.266
        image_buff = 0.1
        image_offset = 0.25
        shortest_paper = ImageMobject("images/shortest-path.png").scale(
            image_scale
        )
        routing_paper = (
            ImageMobject("images/routing.png")
            .scale(image_scale)
            .next_to(shortest_paper, RIGHT, buff=image_buff)
            .shift(DOWN * image_offset)
        )
        exact_cover_paper = (
            ImageMobject("images/vc-exact.png")
            .scale(image_scale)
            .next_to(routing_paper, RIGHT, buff=image_buff)
            .shift(DOWN * image_offset)
        )
        apx_cover_paper = (
            ImageMobject("images/vc-approx.png")
            .scale(image_scale)
            .next_to(exact_cover_paper, RIGHT, buff=image_buff)
            .shift(DOWN * image_offset)
        )

        Layout.move_arranged_mobjects_to(
            shortest_paper,
            routing_paper,
            exact_cover_paper,
            apx_cover_paper,
            target=r2,
        )
        g2 = Group(
            r2,
            shortest_paper,
            routing_paper,
            exact_cover_paper,
            apx_cover_paper,
        )

        # In particular, for the problem of efficiently computing vertex cover
        # approximations, we were able to use what we learned on the model, to
        # derive a new algorithm which yielded better solutions in practice.

        r3 = SurroundingRectangle(r1, buff=0.0, color=WHITE).next_to(r1, DOWN)
        original_measures = [
            ("ego-facebook", 1),
            ("ego-gplus", 1),
            ("munmun\\_twitter\\_social", 1),
            ("as-caida20071105", 1.00162910670649),
            ("bio-CE-LC", 1.0027027027027),
            ("as20000102", 1.00285171102662),
            ("bn-mouse-kasthuri\\_graph\\_v4", 1.00584795321637),
            ("topology", 1.00307869924957),
            ("com-dblp", 1.00180055653566),
            ("as-22july06", 1.00181653042688),
            ("ca-AstroPh", 1.0028305028305),
            ("wordnet-words", 1.00412575788379),
            ("youtube-links", 1.00816179775281),
            ("com-youtube", 1.00820018415209),
            ("youtube-u-growth", 1.00853867580887),
            ("soc-Epinions1", 1.00628366247756),
            ("flixster", 1.00212838855031),
            ("ca-cit-HepTh", 1.00352519966951),
            ("ca-cit-HepPh", 1.00380716277834),
            ("moreno\\_names", 1.00682926829268),
            ("com-amazon", 1.01074698404179),
            ("as-skitter", 1.00954862266681),
            ("web-Google", 1.0085407199019),
            ("bio-yeast-protein-inter", 1.00638977635783),
            ("moreno\\_propro", 1.00798722044728),
            ("bio-CE-HT", 1.01593137254902),
            ("petster-carnivore", 1.00750561034944),
            ("digg-friends", 1.00865259130808),
            ("petster-friendships-cat", 1.00926939639442),
            ("loc-brightkite\\_edges", 1.01449673023277),
            ("citeseer", 1.01507546960918),
            ("loc-gowalla\\_edges", 1.01434304576002),
            ("bio-DM-HT", 1.01691542288557),
            ("advogato", 1.01315789473684),
            ("bn-fly-drosophila\\_medulla\\_1", 1.01612903225806),
            ("hyves", 1.00792126971875),
            ("cfinder-google", 1.00831443688587),
            ("petster-friendships-dog", 1.0145153446978),
            ("livemocha", 1.01844474635595),
            ("p2p-Gnutella31", 1.00974956987192),
            ("petster-friendships-hamster", 1.01355013550136),
            #             ("dblp-cite", 1.04859993562922)
            ("dblp-cite", 1),
        ]

        original_values = [min(x - 1.0, 0.02) for (_, x) in original_measures]
        chart = RecolorableBarChart(
            values=original_values,
            bar_colors=[BLUE for _ in original_measures],  # type: ignore
            y_range=[0.0, 0.02, 0.005],
            y_length=4,
            x_length=10,
            y_axis_config={"numbers_to_exclude": [0.005, 0.01, 0.015, 0.02]},
            z_index=1,
        ).set_opacity(0.2)

        # We override the right most rectangle,
        # as it is actually much larger than shown.
        override_rect = (
            Rectangle(
                width=0.14,
                height=5.0,
                stroke_width=3.0,
                z_index=-1,
                color=BLUE,
            )
            .align_to(chart, DOWN)
            .align_to(chart, RIGHT)
            .shift(LEFT * 0.05)
            .shift(UP * 0.1)
            .set_fill(BLUE, opacity=0.7)
            .set_opacity(0.2)
        )
        chart_group = Group(chart, override_rect).scale(0.45).move_to(r3)

        improved_measures = [
            ("ego-facebook", 1),
            ("ego-gplus", 1),
            ("munmun_twitter_social", 1),
            ("as-caida20071105", 1),
            ("bio-CE-LC", 1),
            ("as20000102", 1),
            ("bn-mouse-kasthuri_graph_v4", 1),
            ("topology", 1.0001924187031),
            ("com-dblp", 1.00020612431721),
            ("as-22july06", 1.00060551014229),
            ("ca-AstroPh", 1.0008325008325),
            ("wordnet-words", 1.00105236722833),
            ("youtube-links", 1.0014202247191),
            ("com-youtube", 1.00142627597537),
            ("youtube-u-growth", 1.00145465800062),
            ("soc-Epinions1", 1.00148114901257),
            ("flixster", 1.00153659270949),
            ("ca-cit-HepTh", 1.00159735610025),
            ("ca-cit-HepPh", 1.00163796538138),
            ("moreno_names", 1.0019512195122),
            ("com-amazon", 1.00200335765239),
            ("as-skitter", 1.00247416014529),
            ("web-Google", 1.00295462742552),
            ("bio-yeast-protein-inter", 1.00319488817891),
            ("moreno_propro", 1.00319488817891),
            ("bio-CE-HT", 1.00367647058824),
            ("petster-carnivore", 1.00398988116566),
            ("digg-friends", 1.00404025957774),
            ("petster-friendships-cat", 1.0051577743717),
            ("loc-brightkite_edges", 1.00521333516257),
            ("citeseer", 1.00554181889754),
            ("loc-gowalla_edges", 1.00575859039206),
            ("bio-DM-HT", 1.00597014925373),
            ("advogato", 1.0068058076225),
            ("bn-fly-drosophila_medulla_1", 1.00733137829912),
            ("hyves", 1.00787302812485),
            ("cfinder-google", 1.00806248425296),
            ("petster-friendships-dog", 1.00835348428226),
            ("livemocha", 1.0090266424114),
            ("p2p-Gnutella31", 1.0091760657618),
            ("petster-friendships-hamster", 1.00948509485095),
            #             ("dblp-cite", 1.04441583521081),
            ("dblp-cite", 1),
        ]
        improved_values = [min(x - 1.0, 0.02) for (_, x) in improved_measures]

        chart_copy = chart.copy().set_z_index(1).set_opacity(1.0)
        override_override_rect = (
            override_rect.copy()
            .set_fill(GREEN, opacity=1.0)
            .set_stroke(GREEN, opacity=1.0)
            .set_z_index(1)
        )

        g3 = Group(r3, chart_group, chart_copy, override_override_rect)

        # Thank you
        #
        # With that, I hope that the thesis can be used to convince people
        # that modelling networks with an underlying geometry can serve as a
        # powerful framework for analyzing algorithms on scale-free real-world
        # networks.

        r4 = SurroundingRectangle(r1, buff=0.0, color=WHITE).next_to(r2, DOWN)
        thank_you = Tex(r"Thank\\You!").scale(2).move_to(r4)
        g4 = Group(r4, thank_you)

        # Align everything such that it is centered in the slide.
        Layout.move_arranged_mobjects_to(g1, g2, g3, g4, target=ORIGIN).shift(
            DOWN * 0.5
        )

        # Fade in r1
        self.play(FadeIn(background, graph, r1))
        self.wait()

        # Fade in r2
        self.play(
            FadeIn(r2),
            AnimationGroup(
                *[
                    FadeIn(image)
                    for image in [
                        shortest_paper,
                        routing_paper,
                        exact_cover_paper,
                        apx_cover_paper,
                    ]
                ],
                lag_ratio=0.33
            ),
        )
        self.wait()

        # Fade in r3
        self.play(
            FadeIn(r3, chart_group, chart_copy),
            chart_copy.animate(
                run_time=2
            ).change_bar_values_and_color(  # type: ignore
                improved_values, GREEN
            ),
            FadeIn(override_override_rect, run_time=2),
        )
        self.wait()

        # Write thank you
        self.play(FadeIn(r4), Write(thank_you))
        self.wait()

        self.fade_out()
