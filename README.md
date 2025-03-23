# disputation

The code used to generate the slides for my disputation and the corresponding
video. The main frameworks used are [manim](https://www.manim.community) and
the hyperbolic extension thereof, called
[hmanim](https://maxkatzmann.github.io/hmanim/).

## Installation

Create a virtual Python environment and install the required packages using

``` bash
pip install -r requirements.txt
```

## Rendering

Following the installation, you can render the video file representing a slide using

``` bash
python -m manim -p slide2.py Slide2
```

For other slides just replace the `2`s above with the corresponding slide
number. I recommend **not** starting with slide 1, since that is rather
expensive to render.
