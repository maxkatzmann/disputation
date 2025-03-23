from __future__ import annotations

from typing import Iterable, Sequence

from manim import DOWN, UP, BarChart, config


class RecolorableBarChart(BarChart):
    def __init__(
        self,
        values: Iterable[float],
        bar_names: Iterable[str] | None = None,
        y_range: Sequence[float] | None = None,
        x_length: float | None = None,
        y_length: float | None = config.frame_height - 4,
        bar_colors: str | Iterable[str] | None = [
            "#003f5c",
            "#58508d",
            "#bc5090",
            "#ff6361",
            "#ffa600",
        ],
        bar_width: float = 0.6,
        bar_fill_opacity: float = 0.7,
        bar_stroke_width: float = 3,
        **kwargs,
    ):
        super().__init__(
            values=values,
            bar_names=bar_names,
            y_range=y_range,
            x_length=x_length,
            y_length=y_length,
            bar_colors=bar_colors,
            bar_width=bar_width,
            bar_fill_opacity=bar_fill_opacity,
            bar_stroke_width=bar_stroke_width,
            **kwargs,
        )

    def change_bar_values_and_color(self, values: Iterable[float], new_color):
        """Updates the height of the bars of the chart and changes the color of the bars.

        Parameters
        ----------
        values
            The values that will be used to update the height of the bars.
            Does not have to match the number of bars.

        Examples
        --------
        .. manim:: ChangeBarValuesExample
            :save_last_frame:

            class ChangeBarValuesExample(Scene):
                def construct(self):
                    values=[-10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10]

                    chart = BarChart(
                        values,
                        y_range=[-10, 10, 2],
                        y_axis_config={"font_size": 24},
                    )
                    self.add(chart)

                    chart.change_bar_values(list(reversed(values)))
                    self.add(chart.get_bar_labels(font_size=24))
        """

        for i, (bar, value) in enumerate(zip(self.bars, values)):
            chart_val = self.values[i]

            if chart_val > 0:
                bar_lim = bar.get_bottom()
                aligned_edge = DOWN
            else:
                bar_lim = bar.get_top()
                aligned_edge = UP

            try:
                quotient = value / chart_val
                if quotient < 0:

                    aligned_edge = UP if chart_val > 0 else DOWN

                    # if the bar is already positive, then we now want to move it
                    # so that it is negative. So, we move the top edge of the bar
                    # to the location of the previous bottom

                    # if already negative, then we move the bottom edge of the bar
                    # to the location of the previous top

                bar.stretch_to_fit_height(quotient * bar.height)

            except ZeroDivisionError:
                bar.height = 0

            bar.move_to(bar_lim, aligned_edge)
            bar.set_color(new_color)

        self.values[: len(values)] = values
