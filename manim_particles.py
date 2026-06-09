from manim import *
import typing
from PIL import Image

__all__ = ["Disintegrate", "Materialize"]


def to_grid(mob: VMobject, cell_size: float) -> VMobject:
    stroke_one_px = config.frame_width / config.pixel_width * 100
    stroke_width = 0.01 * mob.get_stroke_width()
    left, right, bottom, top = (
        mob.get_left()[0] - 0.5 * stroke_width,
        mob.get_right()[0] + 0.5 * stroke_width,
        mob.get_bottom()[1] - 0.5 * stroke_width,
        mob.get_top()[1] + 0.5 * stroke_width,
    )
    width, height = right - left, top - bottom
    resolution = (max(int(width / cell_size), 1), max(1, int(height / cell_size)))
    image = np.asarray(
        Image.fromarray(to_image(mob)).resize(size=resolution, resample=Image.Resampling.NEAREST)
    )
    cell_height, cell_width = height / image.shape[0], width / image.shape[1]
    image = np.flipud(image)
    return VGroup(
        Rectangle(
            width=cell_height,
            height=cell_width,
            stroke_width=stroke_one_px,
            color=ManimColor.from_rgba(pixel),
            fill_opacity=pixel[3],
            stroke_opacity=pixel[3],
        ).move_to((left + (x + 0.5) * cell_width, bottom + (y + 0.5) * cell_height, 0))
        for y in range(image.shape[0])
        for x in range(image.shape[1])
        if (pixel := image[y, x]) is not None and pixel[3] > 0
    )


def to_image(mob: VMobject) -> np.ndarray:
    stroke_offset = 0.5 * 0.01 * mob.get_stroke_width()
    width = mob.width + 2 * stroke_offset
    height = mob.height + 2 * stroke_offset
    if not width or not height:
        return np.zeros((0, 0, 4), dtype=np.uint8)
    image = np.asarray(mob.get_image(Camera(frame_center=mob.get_center(), background_opacity=0)))
    width_px = width * config.pixel_width / config.frame_width
    height_px = height * config.pixel_height / config.frame_height
    image = image[
        int((image.shape[0] - height_px) / 2) : int((image.shape[0] + height_px) / 2),
        int((image.shape[1] - width_px) / 2) : int((image.shape[1] + width_px) / 2),
    ]
    return image


class _Scatter(AnimationGroup):
    def __init__(
        self,
        vmobject: VMobject,
        fill_piece_size: float = 0.1,
        stroke_piece_size: float = 0.025,
        to_scale: typing.Callable[[], float] | None = lambda: 0,
        to_fade: typing.Callable[[], float] | None = lambda: 1,
        shift_strength: typing.Callable[[], float] = lambda: np.random.uniform(0.5, 1.5),
        x_shift: typing.Callable[[], float] = lambda: np.sin(np.random.uniform(0, 2 * PI)),
        y_shift: typing.Callable[[], float] = lambda: np.sin(np.random.uniform(0, 2 * PI)),
        z_shift: typing.Callable[[], float] = lambda: 0,
        **kwargs,
    ) -> None:
        pieces = [
            *to_grid(vmobject.copy().set_stroke(opacity=0), cell_size=fill_piece_size),
            *to_grid(vmobject.copy().set_fill(opacity=0), cell_size=stroke_piece_size),
        ]

        def animate_piece(piece: VMobject):
            animation = piece.animate.shift(
                (
                    shift_strength() * x_shift(),
                    shift_strength() * y_shift(),
                    shift_strength() * z_shift(),
                )
            )
            if to_scale is not None:
                animation = animation.scale(to_scale())
            if to_fade is not None:
                animation = animation.fade(to_fade())
            return animation

        animations = (animate_piece(piece) for piece in pieces)
        super().__init__(animations, **kwargs)


class Disintegrate(_Scatter):
    def __init__(self, vmobject: VMobject, **kwargs) -> None:
        self.vmobject = vmobject
        super().__init__(vmobject, **kwargs)

    def begin(self) -> None:
        self.vmobject.set_opacity(0)
        super().begin()

    def clean_up_from_scene(self, scene: Scene) -> None:
        scene.remove(self.vmobject)
        super().clean_up_from_scene(scene)


class Materialize(_Scatter):
    def __init__(self, vmobject: VMobject, **kwargs) -> None:
        rate_func = kwargs.get("rate_func", linear)
        kwargs["rate_func"] = lambda t: 1 - rate_func(t)
        self.vmobject = vmobject
        super().__init__(vmobject, **kwargs)

    def clean_up_from_scene(self, scene: Scene) -> None:
        scene.add(self.vmobject)
        return super().clean_up_from_scene(scene)
