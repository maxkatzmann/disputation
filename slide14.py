import copy

import numpy as np
from manim import (
    BLUE,
    DOWN,
    GREEN,
    LEFT,
    PI,
    RIGHT,
    UP,
    YELLOW,
    Create,
    DecimalNumber,
    FadeIn,
    Group,
    Rectangle,
    SurroundingRectangle,
    Text,
    Transform,
    VGroup,
)

from manim_presentation_template import DefaultSlide
from mextensions.recolorablebarchart import RecolorableBarChart


# Improved Approximation in Practice
class Slide14(DefaultSlide):

    def content(self):
        header = self.add_header(
            "Greedy Approximation in Practice", with_click=False
        ).shift(UP * 0.5)

        # We draw the table with the previous experiment results again.
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
        bar_names = [x for (x, _) in original_measures]

        y_label_positions = [0.0, 0.005, 0.01, 0.015, 0.02]
        chart = (
            RecolorableBarChart(
                values=original_values,
                bar_colors=[BLUE for _ in original_values],  # type: ignore
                y_range=[0.0, 0.02, 0.005],
                y_length=4,
                x_length=10,
                y_axis_config={
                    "numbers_to_exclude": y_label_positions,
                    "decimal_number_config": {"num_decimal_places": 3},
                },
                z_index=1,
            )
            .shift(UP * 1.0)
            .shift(RIGHT * 0.5)
        )

        x_axis, y_axis = chart.get_axes()
        y_labels = []
        for y_label_position in y_label_positions:
            y_labels.append(
                y_axis.get_number_mobject(y_label_position).set_value(
                    1.0 + y_label_position
                )
            )

        y_label = (
            Text("Ratio")
            .scale(0.66)
            .rotate(PI / 2)
            .next_to(chart, LEFT)
            .shift(LEFT)
        )

        def add_x_axis_labels():
            val_range = np.arange(
                0.5, len(bar_names), 1
            )  # 0.5 shifted so that labels are centered, not on ticks

            labels = VGroup()

            for i, (value, bar_name) in enumerate(zip(val_range, bar_names)):
                direction = DOWN
                bar_name_label = x_axis.label_constructor(bar_name)

                bar_name_label.font_size = x_axis.font_size
                bar_name_label.next_to(
                    x_axis.number_to_point(value),
                    direction=direction,
                ).rotate(PI / 2).align_to(x_axis, UP).rotate(
                    -PI / 4, about_point=x_axis.number_to_point(value)
                ).shift(
                    DOWN * 0.2
                )
                labels.add(bar_name_label)

            x_axis.labels = labels  # type: ignore
            x_axis.add(labels)

        # We override the right most rectangle,
        # as it is actually much larger than shown.
        # We add an extra label to make up for that.
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
        )

        override_label = (
            DecimalNumber(
                1.049,
                show_ellipsis=False,
                num_decimal_places=3,
                include_sign=False,
                color=BLUE,
            )
            .scale(0.5)
            .next_to(override_rect, RIGHT)
            .align_to(override_rect, UP)
            .shift(LEFT * 0.175)
            .shift(DOWN * 0.05)
        )

        add_x_axis_labels()

        self.play(
            FadeIn(
                header,
                chart,
                *y_labels,
                y_label,
                override_label,
                override_rect
            )
        )

        # The values obtained using the improved algorithm.
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

        # Somewhere below the `original_values` gets assigned the
        # `improved_values`.  Unclear to me where that happens, but to since we
        # need to be able to compare the original and improved values (by
        # having the original values transparent below the new ones), we make
        # a copy here.
        original_copy = copy.deepcopy(original_values)

        chart_copy = chart.copy().set_opacity(0.2).set_z_index(0)
        override_rect_copy = override_rect.copy().set_opacity(0.0)
        self.play(FadeIn(chart_copy, override_rect_copy))
        self.wait()

        # We want to morph the header to reference the improved algorithm now.
        new_header = (
            Text(
                "Improved Approximation in Practice",
                t2c={"Improved": GREEN},  # type: ignore
            )
            .scale(DefaultSlide.headerScale)
            .move_to(header)
        )

        self.play(Transform(header, new_header))
        self.wait()

        # Animate the table to shrink the bars to the new values.
        self.play(
            chart.animate.change_bar_values_and_color(improved_values, GREEN),
            override_rect.animate.set_opacity(0.2),
            override_rect_copy.animate.set_color(GREEN).set_opacity(0.7),
            override_label.animate.set_value(1.044).set_color(GREEN),
        )
        self.wait()

        # Mark graphs where we found the optimum
        highlight_bar_group = Group(*chart_copy.bars[3:7])
        highlight_rect = SurroundingRectangle(highlight_bar_group)
        self.play(Create(highlight_rect))
        self.wait()

        # Highlight halved bars.
        halved_bars = [
            bar
            for (index, bar) in enumerate(chart.bars)
            if improved_values[index] <= original_copy[index] / 2.0
        ]

        self.play(*[bar.animate.set_color(YELLOW) for bar in halved_bars])
        self.wait()

        self.fade_out()
