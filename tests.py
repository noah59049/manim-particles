from manim import *
from manim_particles import Materialize, Disintegrate

TESTS = [
    "test_00_null_test",
    "test_01_hello",
    "test_02_single_char",
    "test_03_blue_square",
    "test_04_line",
    "test_05_red_arrow",
    "test_06_curved_arrow",
    "test_07_purple_polygon",
    "test_08_cyan_pentagon",
    "test_09_orange_arc",
    "test_10_sine_curve",
    "test_11_number_line",
    "test_12_pink_star",
    "test_13_axes_parabola",
    "test_14_rainbow_text",
    "test_15_rainbow_mathtex",
    "test_16_solid_colored_squares",
    "test_17_mixed_filled_stroked_squares",
    "test_18_colored_circles",
    "test_19_multicolor_shapes",
    "test_20_stroke_squares_multicolor",
    "test_21_stroke_circles_multicolor",
    "test_22_stroke_shapes_multicolor",
    "test_23_stroke_lines_multicolor",
]

class TestScene(Scene):
    def construct(self):
        self.run_all_tests()
        # self.run_test_numbers(23)

    def run_test_numbers(self, *nums):
        for num in nums:
            getattr(self, TESTS[num])()
            self.clear()
    
    def run_all_tests(self):
        for name in TESTS:
            getattr(self, name)()
            self.clear()

    def test_00_null_test(self):
        pass

    def test_01_hello(self):
        text = Text("Hello", font_size=100).set_opacity(0.66).to_edge(UP)
        self.play(Materialize(text))
        self.wait(0.5)
        self.play(Disintegrate(text), run_time=1.4)
        self.wait(0.5)

    def test_02_single_char(self):
        text = Text("G", font_size=100).set_opacity(0.33)
        self.play(Materialize(text), run_time=1.4)
        self.wait(0.5)
        self.play(Disintegrate(text))
        self.wait(0.5)

    def test_03_blue_square(self):
        my_square = Square(fill_opacity=1).set_fill(BLUE_C)
        self.play(Materialize(my_square))
        self.wait(0.5)
        self.play(Disintegrate(my_square))
        self.wait(0.5)

    def test_04_line(self):
        my_line = Line().shift(UR * 1.3)
        self.play(Materialize(my_line))
        self.wait(0.5)
        self.play(Disintegrate(my_line))
        self.wait(0.5)

    def test_05_red_arrow(self):
        my_arrow = Arrow(LEFT * 2, RIGHT * 2, color=RED)
        self.play(Materialize(my_arrow))
        self.wait(0.5)
        self.play(Disintegrate(my_arrow))
        self.wait(0.5)

    def test_06_curved_arrow(self):
        my_curved_arrow = CurvedArrow(LEFT * 2 + DOWN, RIGHT * 2 + UP, color=BLUE_B).set_opacity(0.7).shift(LEFT)
        self.play(Materialize(my_curved_arrow))
        self.wait(0.5)
        self.play(Disintegrate(my_curved_arrow))
        self.wait(0.5)

    def test_07_purple_polygon(self):
        my_polygon = Polygon(
            UP * 2, RIGHT * 1.5 + UP * 0.5, RIGHT * 2 + DOWN, DOWN * 1.5, LEFT * 2
        ).set_fill(PURPLE, opacity=0.5).set_stroke(WHITE, width=2)
        self.play(Materialize(my_polygon))
        self.wait(0.5)
        self.play(Disintegrate(my_polygon))
        self.wait(0.5)

    def test_08_cyan_pentagon(self):
        my_pentagon = RegularPolygon(n=5).scale(2).set_stroke(PURE_CYAN, width=4).set_fill(opacity=0)
        self.play(Materialize(my_pentagon))
        self.wait(0.5)
        self.play(Disintegrate(my_pentagon))
        self.wait(0.5)

    def test_09_orange_arc(self):
        my_arc = Arc(radius=2, start_angle=0, angle=3 * PI / 2).set_stroke(ORANGE, width=5)
        self.play(Materialize(my_arc))
        self.wait(0.5)
        self.play(Disintegrate(my_arc))
        self.wait(0.5)

    def test_10_sine_curve(self):
        my_sine = FunctionGraph(lambda x: np.sin(x), x_range=[-PI, PI]).set_stroke(TEAL, width=4)
        self.play(Materialize(my_sine))
        self.wait(0.5)
        self.play(Disintegrate(my_sine))
        self.wait(0.5)

    def test_11_number_line(self):
        my_number_line = NumberLine(x_range=[-3, 3], length=8, color=YELLOW)
        self.play(Materialize(my_number_line))
        self.wait(0.5)
        self.play(Disintegrate(my_number_line))
        self.wait(0.5)

    def test_12_pink_star(self):
        my_star = Star(n=5, outer_radius=1.5).set_fill(PINK, opacity=1).set_stroke(width=0)
        self.play(Materialize(my_star))
        self.wait(0.5)
        self.play(Disintegrate(my_star))
        self.wait(0.5)

    def test_13_axes_parabola(self):
        my_axes = Axes(x_range=[-2, 2], y_range=[-1, 4], x_length=6, y_length=4)
        my_parabola = my_axes.plot(lambda x: x ** 2, color=MAROON)
        self.play(Materialize(VGroup(my_axes, my_parabola)))
        self.wait(0.5)
        self.play(Disintegrate(VGroup(my_axes, my_parabola)))
        self.wait(0.5)

    def test_14_rainbow_text(self):
        my_text = Text("Rainbow", font_size=100).set_color_by_gradient(RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE).to_corner(DL)
        self.play(Materialize(my_text))
        self.wait(0.5)
        self.play(Disintegrate(my_text))
        self.wait(0.5)

    def test_15_rainbow_mathtex(self):
        my_tex = MathTex(r"E = mc^2").scale(3).set_color_by_gradient(RED, YELLOW, GREEN, BLUE)
        self.play(Materialize(my_tex))
        self.wait(0.5)
        self.play(Disintegrate(my_tex))
        self.wait(0.5)

    def test_16_solid_colored_squares(self):
        squares = VGroup(
            Square(fill_opacity=1).set_fill(RED).set_stroke(width=0),
            Square(fill_opacity=1).set_fill(ORANGE).set_stroke(width=0),
            Square(fill_opacity=1).set_fill(YELLOW).set_stroke(width=0),
            Square(fill_opacity=1).set_fill(GREEN).set_stroke(width=0),
            Square(fill_opacity=1).set_fill(BLUE).set_stroke(width=0),
            Square(fill_opacity=1).set_fill(PURPLE).set_stroke(width=0),
        ).arrange(RIGHT, buff=0.2)
        self.play(Materialize(squares))
        self.wait(0.5)
        self.play(Disintegrate(squares))
        self.wait(0.5)

    def test_17_mixed_filled_stroked_squares(self):
        squares = VGroup(
            Square(fill_opacity=1).set_fill(RED_C).set_stroke(width=0),
            Square().set_stroke(GREEN, width=4).set_fill(opacity=0),
            Square(fill_opacity=0.6).set_fill(BLUE_C).set_stroke(YELLOW, width=2),
            Square().set_stroke(ORANGE, width=4).set_fill(opacity=0),
            Square(fill_opacity=1).set_fill(PURPLE).set_stroke(width=0),
            Square(fill_opacity=0.4).set_fill(TEAL).set_stroke(WHITE, width=3),
        ).arrange(RIGHT, buff=0.2)
        self.play(Materialize(squares))
        self.wait(0.5)
        self.play(Disintegrate(squares))
        self.wait(0.5)

    def test_18_colored_circles(self):
        circles = VGroup(
            Circle(radius=0.6, fill_opacity=1).set_fill(RED).set_stroke(width=0),
            Circle(radius=0.6, fill_opacity=1).set_fill(ORANGE).set_stroke(width=0),
            Circle(radius=0.6, fill_opacity=1).set_fill(YELLOW).set_stroke(width=0),
            Circle(radius=0.6, fill_opacity=1).set_fill(GREEN).set_stroke(width=0),
            Circle(radius=0.6, fill_opacity=1).set_fill(BLUE).set_stroke(width=0),
            Circle(radius=0.6, fill_opacity=1).set_fill(PURPLE).set_stroke(width=0),
        ).arrange(RIGHT, buff=0.15)
        self.play(Materialize(circles))
        self.wait(0.5)
        self.play(Disintegrate(circles))
        self.wait(0.5)

    def test_19_multicolor_shapes(self):
        shapes = VGroup(
            Triangle().scale(1.5).set_fill(RED_C, opacity=0.9).set_stroke(WHITE, width=1),
            RegularPolygon(n=6).scale(1.5).set_fill(GREEN_C, opacity=0.9).set_stroke(WHITE, width=1),
            Star(n=5, outer_radius=1.5).set_fill(YELLOW, opacity=0.9).set_stroke(WHITE, width=1),
            RegularPolygon(n=8).scale(1.5).set_fill(BLUE_C, opacity=0.9).set_stroke(WHITE, width=1),
        ).arrange(RIGHT, buff=0.3)
        self.play(Materialize(shapes))
        self.wait(0.5)
        self.play(Disintegrate(shapes))
        self.wait(0.5)

    def test_20_stroke_squares_multicolor(self):
        squares = VGroup(
            Square().set_stroke(RED,    width=6            ).set_fill(opacity=0),
            Square().set_stroke(ORANGE, width=6, opacity=0.8).set_fill(opacity=0),
            Square().set_stroke(YELLOW, width=6, opacity=0.6).set_fill(opacity=0),
            Square().set_stroke(GREEN,  width=6, opacity=0.4).set_fill(opacity=0),
            Square().set_stroke(BLUE,   width=6            ).set_fill(opacity=0),
            Square().set_stroke(PURPLE, width=6, opacity=0.7).set_fill(opacity=0),
        ).arrange(RIGHT, buff=0.2)
        self.play(Materialize(squares))
        self.wait(0.5)
        self.play(Disintegrate(squares))
        self.wait(0.5)

    def test_21_stroke_circles_multicolor(self):
        circles = VGroup(
            Circle(radius=0.6).set_stroke(TEAL,       width=3            ).set_fill(opacity=0),
            Circle(radius=0.6).set_stroke(PINK,       width=5, opacity=0.9).set_fill(opacity=0),
            Circle(radius=0.6).set_stroke(GOLD,       width=8, opacity=0.6).set_fill(opacity=0),
            Circle(radius=0.6).set_stroke(MAROON,     width=4, opacity=0.8).set_fill(opacity=0),
            Circle(radius=0.6).set_stroke(LIGHT_BROWN, width=6, opacity=0.5).set_fill(opacity=0),
        ).arrange(RIGHT, buff=0.25).to_corner(UL)
        self.play(Materialize(circles))
        self.wait(0.5)
        self.play(Disintegrate(circles))
        self.wait(0.5)

    def test_22_stroke_shapes_multicolor(self):
        shapes = VGroup(
            Triangle().scale(1.3).set_stroke(RED_C,        width=5            ).set_fill(opacity=0),
            RegularPolygon(n=5).scale(1.3).set_stroke(PURE_GREEN, width=4, opacity=0.7).set_fill(opacity=0),
            Star(n=5, outer_radius=1.3).set_stroke(YELLOW, width=3, opacity=0.5).set_fill(opacity=0),
            RegularPolygon(n=6).scale(1.3).set_stroke(BLUE_C,     width=6, opacity=0.9).set_fill(opacity=0),
            Arc(radius=1.2, angle=3*PI/2).set_stroke(ORANGE,      width=5, opacity=0.8).set_fill(opacity=0),
        ).arrange(RIGHT, buff=0.2)
        self.play(Materialize(shapes))
        self.wait(0.5)
        self.play(Disintegrate(shapes))
        self.wait(0.5)

    def test_23_stroke_lines_multicolor(self):
        lines = VGroup(
            Line(stroke_width = 23).scale(1.3).set_stroke(RED_C,        width=5            ).set_fill(opacity=0),
            Line().scale(1.3).set_stroke(PURE_GREEN, width=4, opacity=0.7).set_fill(opacity=0),
            Line().set_stroke(YELLOW, width=3, opacity=0.5).set_fill(opacity=0),
            Line().scale(1.3).set_stroke(BLUE_C,     width=6, opacity=0.9).set_fill(opacity=0),
            Line().set_stroke(ORANGE,      width=5, opacity=0.8).set_fill(opacity=0),
        ).arrange(DOWN, buff=0.2)
        self.play(Materialize(lines))
        self.wait(0.5)
        self.play(Disintegrate(lines))
        self.wait(0.5)


# --- Check that TESTS array is correct ---
_ALL_TESTS = sorted(name for name in vars(TestScene) if name.startswith("test_"))
_missing_from_list = set(_ALL_TESTS) - set(TESTS)
_missing_from_class = set(TESTS) - set(_ALL_TESTS)
if _missing_from_list or _missing_from_class:
    msg = "TESTS list is out of sync with TestScene methods."
    if _missing_from_list:
        msg += f"\n  Defined in class but absent from TESTS: {sorted(_missing_from_list)}"
    if _missing_from_class:
        msg += f"\n  Listed in TESTS but missing from class: {sorted(_missing_from_class)}"
    raise RuntimeError(msg)
