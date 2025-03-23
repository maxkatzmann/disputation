import numpy as np
from manim import (
    BLUE,
    DOWN,
    LEFT,
    PI,
    RIGHT,
    UP,
    BarChart,
    FadeIn,
    Rectangle,
    Tex,
    Text,
    VGroup,
)

from manim_presentation_template import DefaultSlide, SideNoteTex


# Vertex Cover Approximation
class Slide11(DefaultSlide):

    def content(self):
        header = self.add_header(
            "Greedy Approximation in Practice", with_click=False
        ).shift(UP * 0.5)

        # Data to draw a chart with.
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
            # ("dblp-cite", 1.04859993562922) Replacing this value with a 1 for
            # visual reasons. We write the value next to the bar instead.
            ("dblp-cite", 1),
        ]

        original_values = [min(x - 1.0, 0.02) for (_, x) in original_measures]
        bar_names = [x for (x, _) in original_measures]

        y_label_positions = [0.0, 0.005, 0.01, 0.015, 0.02]
        chart = (
            BarChart(
                values=original_values,
                bar_colors=[BLUE for _ in original_values],  # type: ignore
                y_range=[0.0, 0.02, 0.005],
                y_length=4,
                x_length=10,
                y_axis_config={
                    "numbers_to_exclude": y_label_positions,
                    "decimal_number_config": {"num_decimal_places": 3},
                },
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
            .set_fill(BLUE, opacity=0.8)
        )

        override_label = (
            Tex("$1.049$", color=BLUE)
            .scale(0.5)
            .next_to(override_rect, RIGHT)
            .align_to(override_rect, UP)
            .shift(LEFT * 0.175)
            .shift(DOWN * 0.05)
        )

        add_x_axis_labels()

        cite = SideNoteTex(
            "da Silva, Gimenez-Lugo \\& da Silva, IJMPC 2013"
        ).shift(DOWN * 3.6)
        self.play(
            FadeIn(
                header,
                chart,
                *[y_label for y_label in y_labels],
                y_label,
                override_label,
                override_rect,
                cite
            )
        )
        self.wait()

        self.fade_out()
