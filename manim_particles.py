from manim import *
import typing
from PIL import Image

__all__ = ["Disintegrate", "Materialize"]


def _apparent_color(m: VMobject) -> np.ndarray:
    if m.get_fill_opacity() > 0:
        return color_to_rgb(m.get_fill_color())
    return color_to_rgb(m.get_stroke_color())


def _apparent_opacity(m: VMobject) -> float:
    return m.get_fill_opacity() or m.get_stroke_opacity()


def _ensure_filled(m: VMobject) -> VMobject:
    if m.get_fill_opacity() > 0:
        return m
    pts = m.points
    color = m.get_stroke_color()
    opacity = m.get_stroke_opacity() or 1
    stroke_radius = max(m.get_stroke_width() / 200, 0.02)
    is_closed = np.linalg.norm(pts[-1] - pts[0]) < 0.01
    n = 64
    if is_closed:
        path_pts = np.array(
            [m.point_from_proportion(t) for t in np.linspace(0, 1, n, endpoint=False)]
        )
        tangents = np.diff(np.vstack([path_pts, path_pts[0]]), axis=0)
        unit_t = tangents / np.maximum(np.linalg.norm(tangents, axis=1, keepdims=True), 1e-8)
        perps = np.c_[-unit_t[:, 1], unit_t[:, 0], np.zeros(n)]
        avg_perps = (perps + np.roll(perps, 1, axis=0)) / 2
    else:
        path_pts = np.array([m.point_from_proportion(t) for t in np.linspace(0, 1, n)])
        tangents = np.diff(path_pts, axis=0)
        unit_t = tangents / np.maximum(np.linalg.norm(tangents, axis=1, keepdims=True), 1e-8)
        perps = np.c_[-unit_t[:, 1], unit_t[:, 0], np.zeros(n - 1)]
        avg_perps = np.vstack([perps[:1], (perps[:-1] + perps[1:]) / 2, perps[-1:]])
    avg_perps /= np.maximum(np.linalg.norm(avg_perps, axis=1, keepdims=True), 1e-8)
    upper = path_pts + stroke_radius * avg_perps
    lower = path_pts - stroke_radius * avg_perps
    return (
        Polygon(*np.vstack([upper, lower[::-1]]))
        .set_stroke(width=0)
        .set_fill(color=color, opacity=opacity)
    )


def _flatten(mob: Mobject) -> VMobject:
    leaves = [_ensure_filled(m) for m in mob.get_family() if len(m.points) > 0]
    if not leaves:
        return mob
    if len(leaves) == 1:
        return leaves[0]
    return Union(*leaves)


def _to_grid(mob: VMobject, cell_size: float = 0.1) -> VMobject:
    def to_image(mob: VMobject) -> np.ndarray:
        width = mob.width + 0.01 * mob.get_stroke_width()
        height = mob.height + 0.01 * mob.get_stroke_width()
        if not width or not height:
            return np.zeros((0, 0, 4), dtype=np.uint8)
        scale = min(config.frame_width / width, config.frame_height / height)
        mob = mob.copy().scale(scale, scale_stroke=True)
        img = np.asarray(mob.get_image(Camera(frame_center=mob.get_center(), background_opacity=0)))
        mask = img[:, :, 3] > 0
        rows = np.where(np.any(mask, axis=1))[0]
        cols = np.where(np.any(mask, axis=0))[0]
        if len(rows) == 0 or len(cols) == 0:
            return np.zeros((0, 0, 4), dtype=np.uint8)
        img = img[rows[0] : rows[-1] + 1, cols[0] : cols[-1] + 1]
        return img

    stroke_one_px = config.frame_width / config.pixel_width * 100
    stroke_width = 0.01 * mob.get_stroke_width()
    left, bottom = mob.get_left()[0] - 0.5 * stroke_width, mob.get_bottom()[1] - 0.5 * stroke_width
    w, h = mob.width + stroke_width, mob.height + stroke_width
    res = (max(int(w / cell_size), 1), max(1, int(h / cell_size)))
    img = np.asarray(
        Image.fromarray(to_image(mob)).resize(size=res, resample=Image.Resampling.NEAREST)
    )
    c_w, c_h = w / img.shape[1], h / img.shape[0]
    img = np.flipud(img)
    rows, cols = np.where(img[:, :, 3] > 0)
    pixels = img[rows, cols]
    xs = left + (cols + 0.5) * c_w
    ys = bottom + (rows + 0.5) * c_h
    return VGroup(
        Rectangle(
            width=c_w,
            height=c_h,
            stroke_width=stroke_one_px,
            color=color,
            fill_opacity=pixel[3],
            stroke_opacity=pixel[3],
        ).move_to((x, y, 0))
        for x, y, pixel in zip(xs, ys, pixels, strict=True)
        if (color := ManimColor.from_rgb(pixel[:3])) is not None
    )


class _Scatter(AnimationGroup):
    def __init__(
        self,
        vmobject: VMobject,
        piece_size: tuple[float, float] = (0.1, 0.025),
        to_scale: typing.Callable[[], float] | None = lambda: 0,
        to_fade: typing.Callable[[], float] | None = lambda: 1,
        shift_strength: typing.Callable[[], float] = lambda: np.random.uniform(0.5, 1.5),
        x_shift: typing.Callable[[], float] = lambda: np.sin(np.random.uniform(0, 2 * PI)),
        y_shift: typing.Callable[[], float] = lambda: np.sin(np.random.uniform(0, 2 * PI)),
        z_shift: typing.Callable[[], float] = lambda: 0,
        **kwargs,
    ) -> None:
        pieces = [
            *_to_grid(vmobject.copy().set_stroke(opacity=0), cell_size=piece_size[0]),
            *_to_grid(vmobject.copy().set_fill(opacity=0), cell_size=piece_size[1]),
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
