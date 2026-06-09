# manim-particles

Particle disintegration and materialization animations for [Manim Community](https://www.manim.community/).

Objects shatter into hundreds of small pieces that scatter outward (`Disintegrate`), or the reverse — pieces fly in from all directions and assemble into an object (`Materialize`). Colors and opacity are sampled per-particle from a rendered image of the original object, so multicolor and gradient objects work correctly.

## Installation

```bash
pip install git+https://github.com/noah59049/manim-particles
```

Developed and tested against Manim Community v0.20.1. Requires Python 3.10+.


## Quick start

```python
from manim import *
from manim_particles import Disintegrate, Materialize

class ExampleScene(Scene):
    def construct(self):
        text = Text(
            "Hello World",
            font_size=100,
            fill_color=[RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE],
        )
        self.play(Materialize(text))
        self.wait(0.5)
        self.play(Disintegrate(text))
        self.wait(0.5)
```

[Example Scene](https://github.com/user-attachments/assets/fdfa3e8c-6c97-4795-967a-f618aa5c7886)

## Usage

Both classes accept any `VMobject` or `VGroup` and all standard Manim animation kwargs (`run_time`, `rate_func`, `lag_ratio`, …).

```python
# Materialize — pieces converge into the object, then the object appears
self.play(Materialize(my_mob, run_time=2))

# Disintegrate — the object disappears, pieces fly outward
self.play(Disintegrate(my_mob, run_time=1.5))
```

### Parameters

Both classes share the same keyword arguments beyond standard Manim kwargs:

|    Parameter     |        Default        |                                           Description                                           |
|:----------------:|:---------------------:|:-----------------------------------------------------------------------------------------------:|
|    `vmobject`    |                       |                                  The object to the scattered.                                   |
|   `piece_size`   |         `0.1`         | The size for each square. A tuple can be passed to handle the fill and stroke areas separately. |
|    `to_scale`    |          `0`          |                       Callable returning the target scale for each piece.                       |
|    `to_fade`     |          `1`          |                       Callable returning the target fade for each piece.                        |
| `scatter_distance` |  `uniform(0.5, 1.5)`  |                     Callable returning the travel distance for each piece.                      |
|    `x_shift`     | `sin(uniform(0, 2π))` |                    Callable returning the shift x-component for each piece.                     |
|    `y_shift`     | `sin(uniform(0, 2π))` |                    Callable returning the shift y-component for each piece.                     |


All callables are invoked independently per piece, so passing a lambda with `random` gives a different value for each piece.

### Examples

```python
# Slower, bigger pieces
self.play(Disintegrate(mob, piece_size=0.2, run_time=3))

# Pieces fly only upward
self.play(Disintegrate(mob, y_shift=lambda: 1, x_shift=lambda: 0))

# Pieces don't shrink or fade — just drift
self.play(Disintegrate(mob, to_scale=None, to_fade=None))

# Pieces explode outward with more spread
self.play(Disintegrate(mob, scatter_distance=lambda: np.random.uniform(2, 4)))
```

## Supported object types

Works with any 2D `VMobject` or `VGroup`, including:

- **Text / MathTex / Tex** — including gradient and multicolor text
- **Filled shapes** — `Square`, `Circle`, `Triangle`, `Polygon`, `Star`, …
- **Stroke-only shapes** — outlines, `RegularPolygon` with no fill, `Arc`, …
- **Open paths** — `Line`, `Arrow`, `CurvedArrow`, `FunctionGraph`, …
- **Compound objects** — `Axes`, `NumberLine`, `VGroup` of mixed shapes
- **Semi-transparent objects** — opacity is preserved per particle
- ...

Does not work with 3D objects.

## How it works

1. Prerenders the object with either the fill or the stroke area.
2. Resizes the rendered image to match the size of grid.
3. Creates the grid out of `Square`s.
    * Skips pixels where the prerendered image doesn't have a color.
    * Sets the color based on the pixel in the rendered image.
4. Animates each square.

## Credits

Created by [Noah](https://github.com/noah59049) and [GniLudio](https://github.com/GniLudio).
Additional contributions by uwezi.
