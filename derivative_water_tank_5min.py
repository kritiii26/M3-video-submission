from manim import *
import numpy as np

# Kritika Pandey | URN: E25B070687
# M3 Linear Algebra & Calculus
# Topic: From Average Rate to Instantaneous Rate — Understanding Derivatives
# Original context: a rooftop water tank filling up.
# Designed for a clean 16:9 Manim render. Add voice-over during editing.

class DerivativeStory(Scene):
    def construct(self):
        # ---------- Theme ----------
        BG = BLACK
        WHITE = "#F4F6F8"
        MUTED = "#B8C0CC"
        TEAL = "#55D6BE"
        BLUE = "#4DA3FF"
        GOLD = "#FFD166"
        ORANGE = "#F4A261"
        PINK = "#EF709D"
        GREEN = "#8BD450"

        self.camera.background_color = BG

        def fit_width(mob, max_width=11.8):
            if mob.width > max_width:
                mob.scale_to_fit_width(max_width)
            return mob

        def title(text):
            mob = Text(text, font_size=30, weight=BOLD, color=TEAL)
            fit_width(mob, 11.8)
            mob.move_to(UP * 3.25)
            return mob

        def body(text, size=25, color=WHITE, max_width=11.5):
            mob = Text(text, font_size=size, color=color)
            fit_width(mob, max_width)
            return mob

        def show_title(text):
            t = title(text)
            self.play(FadeIn(t, shift=DOWN * 0.12), run_time=1.2)
            return t

        def clean_transition():
            # Removes the previous section completely, including its title.
            if self.mobjects:
                self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.8)

        def hold(seconds):
            self.wait(seconds)

        # ==================================================================
        # 1. OPENING / THE QUESTION (0:00–0:35)
        # ==================================================================
        opening = Text(
            "A Tank, a Rising Water Level,\nand One Instant",
            font_size=38, weight=BOLD, color=TEAL, line_spacing=0.85
        )
        fit_width(opening, 11.5)
        opening.move_to(UP * 1.65)

        subtitle = body(
            "How can we measure change at one exact moment?",
            size=24, color=MUTED
        ).move_to(UP * 0.35)

        # Simple tank illustration, safely grouped and positioned on right.
        tank_outline = RoundedRectangle(
            width=2.55, height=3.15, corner_radius=0.12,
            stroke_color=BLUE, stroke_width=4, fill_opacity=0
        )
        tank_outline.move_to(RIGHT * 3.25 + DOWN * 0.75)

        water = Rectangle(
            width=2.35, height=1.35, stroke_width=0,
            fill_color=BLUE, fill_opacity=0.55
        )
        water.align_to(tank_outline, DOWN).shift(UP * 0.12)
        water.move_to(tank_outline.get_bottom() + UP * 0.78)
        water.align_to(tank_outline, LEFT).shift(RIGHT * 0.10)

        pipe = Line(
            tank_outline.get_top() + LEFT * 0.65,
            tank_outline.get_top() + LEFT * 0.65 + UP * 0.65,
            color=MUTED, stroke_width=7
        )
        droplets = VGroup(*[
            Dot(pipe.get_top() + DOWN * (0.17 * k), radius=0.045, color=TEAL)
            for k in range(3)
        ])

        tank = VGroup(tank_outline, water, pipe, droplets)
        left_question = body(
            "Water is flowing in.\nThe level keeps rising.",
            size=27, color=GOLD, max_width=5.2
        ).move_to(LEFT * 2.55 + DOWN * 0.85)

        self.play(Write(opening), run_time=3)
        self.play(FadeIn(subtitle), run_time=1.5)
        self.play(Create(tank_outline), FadeIn(water), Create(pipe),
                  FadeIn(droplets), run_time=3)
        self.play(FadeIn(left_question), run_time=2)
        hold(25)

        # ==================================================================
        # 2. AVERAGE RATE (0:35–1:15)
        # ==================================================================
        clean_transition()
        t = show_title("1. Average Rate of Change")

        definition = MathTex(
            r"\text{Average rate}",
            r"=",
            r"\frac{\text{change in level}}{\text{change in time}}",
            font_size=34
        )
        definition[0].set_color(GOLD)
        definition[2].set_color(TEAL)
        fit_width(definition, 11.3)
        definition.move_to(UP * 1.45)

        example_label = body(
            "Imagine the tank's level changes from 10 cm to 18 cm.",
            size=23, color=MUTED
        ).move_to(UP * 0.35)

        calculation = MathTex(
            r"\frac{18-10}{6-2}",
            r"=",
            r"\frac{8}{4}",
            r"=",
            r"2\text{ cm/min}",
            font_size=38
        )
        calculation[0].set_color(BLUE)
        calculation[2].set_color(TEAL)
        calculation[4].set_color(GOLD)
        fit_width(calculation, 11.0)
        calculation.move_to(DOWN * 0.75)

        interpretation = body(
            "Over this 4-minute interval, the average rise is 2 cm each minute.",
            size=22, color=WHITE, max_width=11.2
        ).move_to(DOWN * 2.15)

        self.play(Write(definition), run_time=3)
        self.play(FadeIn(example_label), run_time=2)
        self.play(Write(calculation), run_time=3)
        self.play(FadeIn(interpretation), run_time=2)
        hold(29)

        # ==================================================================
        # 3. SECANT -> TANGENT (1:15–2:05)
        # ==================================================================
        clean_transition()
        t = show_title("2. From an Interval to One Instant")

        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 10, 2],
            x_length=7.3,
            y_length=4.0,
            axis_config={
                "color": MUTED,
                "include_numbers": True,
                "font_size": 18,
                "stroke_width": 2
            },
            tips=True
        )
        axes.move_to(DOWN * 0.45 + LEFT * 0.45)

        xlab = Text("time", font_size=20, color=MUTED)
        xlab.next_to(axes.x_axis, RIGHT, buff=0.18)
        ylab = Text("water level", font_size=20, color=MUTED)
        ylab.rotate(PI / 2)
        ylab.next_to(axes.y_axis, LEFT, buff=0.22)

        curve = axes.plot(
            lambda x: 0.35 * x**2 + 1,
            x_range=[0, 4.6],
            color=TEAL,
            stroke_width=4
        )

        # A=(2,2.4), B=(4,6.6) lie on the displayed curve.
        A = axes.c2p(2, 2.4)
        B = axes.c2p(4, 6.6)
        dot_a = Dot(A, color=GOLD, radius=0.085)
        dot_b = Dot(B, color=ORANGE, radius=0.085)
        label_a = MathTex("A", color=GOLD).scale(0.72).next_to(dot_a, DOWN, buff=0.12)
        label_b = MathTex("B", color=ORANGE).scale(0.72).next_to(dot_b, UP, buff=0.12)
        secant = Line(A, B, color=ORANGE, stroke_width=4)

        caption = body(
            "Secant line: average change between two points",
            size=21, color=ORANGE, max_width=11.5
        ).to_edge(DOWN, buff=0.18)

        self.play(Create(axes), FadeIn(xlab, ylab), run_time=2.5)
        self.play(Create(curve), run_time=2.5)
        self.play(FadeIn(dot_a, dot_b, label_a, label_b), Create(secant), run_time=2.5)
        self.play(FadeIn(caption), run_time=1.5)
        hold(13)

        # Move B gradually toward A; point A remains fixed.
        for x_value in [3.2, 2.75, 2.35, 2.12]:
            y_value = 0.35 * x_value**2 + 1
            new_point = axes.c2p(x_value, y_value)
            new_dot = Dot(new_point, color=ORANGE, radius=0.08)
            new_line = Line(A, new_point, color=ORANGE, stroke_width=4)
            new_label = MathTex("B", color=ORANGE).scale(0.72).next_to(
                new_dot, UP, buff=0.12
            )
            self.play(
                Transform(dot_b, new_dot),
                Transform(secant, new_line),
                Transform(label_b, new_label),
                run_time=1.3
            )
            hold(2.0)

        tangent = Line(
            axes.c2p(0.75, 0.72),
            axes.c2p(3.25, 4.08),
            color=GOLD,
            stroke_width=4
        )
        tangent_label = body(
            "Tangent line: slope at one point",
            size=21, color=GOLD, max_width=11.5
        ).to_edge(DOWN, buff=0.18)

        self.play(Transform(secant, tangent), FadeOut(caption),
                  FadeIn(tangent_label), run_time=2.5)

        limit_formula = MathTex(
            r"\text{Instantaneous rate}",
            r"=",
            r"\lim_{\Delta t\to0}\frac{\Delta L}{\Delta t}",
            font_size=31
        )
        limit_formula[0].set_color(WHITE)
        limit_formula[2].set_color(GOLD)
        fit_width(limit_formula, 11.2)
        limit_formula.move_to(UP * 2.35)
        self.play(Write(limit_formula), run_time=3)
        hold(9)

        # ==================================================================
        # 4. WORKED EXAMPLE ONE (2:05–2:45)
        # ==================================================================
        clean_transition()
        t = show_title("3. Example One: Find the Rate at t = 2")

        model = MathTex(r"L(t)=t^2", font_size=48, color=TEAL)
        model.move_to(UP * 2.15)

        description = body(
            "Use the limit definition of the derivative.",
            size=23, color=MUTED
        ).move_to(UP * 1.25)

        derivation = VGroup(
            MathTex(r"L'(t)=\lim_{h\to0}\frac{(t+h)^2-t^2}{h}"),
            MathTex(r"=\lim_{h\to0}\frac{2th+h^2}{h}"),
            MathTex(r"=\lim_{h\to0}(2t+h)=2t")
        ).arrange(DOWN, buff=0.38)
        derivation.scale(0.76)
        fit_width(derivation, 11.3)
        derivation.move_to(DOWN * 0.25)

        result = MathTex(
            r"L'(2)=4",
            r"\text{ level-units per minute}",
            font_size=35
        )
        result[0].set_color(GOLD)
        result[1].set_color(WHITE)
        fit_width(result, 11.2)
        result.move_to(DOWN * 2.25)

        self.play(Write(model), FadeIn(description), run_time=2.5)
        self.play(Write(derivation), run_time=5)
        self.play(Write(result), run_time=2.5)
        hold(27)

        # ==================================================================
        # 5. WORKED EXAMPLE TWO (2:45–3:25)
        # ==================================================================
        clean_transition()
        t = show_title("4. A Second Model")

        lead = body(
            "Suppose the level is described by:",
            size=24, color=MUTED
        ).move_to(UP * 2.15)

        model2 = MathTex(r"L(t)=3t^2+2t", font_size=44, color=TEAL)
        model2.move_to(UP * 1.25)

        rules = VGroup(
            MathTex(r"\frac{d}{dt}(3t^2)=6t", color=BLUE),
            MathTex(r"\frac{d}{dt}(2t)=2", color=GOLD)
        ).arrange(DOWN, buff=0.42)
        rules.scale(0.9)
        rules.move_to(ORIGIN + DOWN * 0.15)

        answer = MathTex(r"L'(t)=6t+2", font_size=42, color=GREEN)
        answer.move_to(DOWN * 1.85)

        explanation = body(
            "This formula gives the instantaneous rate at any time t.",
            size=21, color=WHITE, max_width=11.4
        ).move_to(DOWN * 2.7)

        self.play(FadeIn(lead), Write(model2), run_time=2.5)
        self.play(Write(rules), run_time=3.5)
        self.play(Write(answer), run_time=2.5)
        self.play(FadeIn(explanation), run_time=2)
        hold(27)

        # ==================================================================
        # 6. SECOND DERIVATIVE (3:25–4:05)
        # ==================================================================
        clean_transition()
        t = show_title("5. When the Rate Itself Changes")

        # Three distinct, centered rows. Never place a long equation on one line.
        level = MathTex(r"\text{Level: }L(t)", font_size=34, color=TEAL)
        first_arrow = MathTex(r"\Downarrow", font_size=30, color=MUTED)
        first_label = body("First derivative", size=20, color=MUTED)
        rate = MathTex(r"\text{Rate: }L'(t)", font_size=34, color=GOLD)
        second_arrow = MathTex(r"\Downarrow", font_size=30, color=MUTED)
        second_label = body("Second derivative", size=20, color=MUTED)
        rate_of_rate = MathTex(
            r"\text{Rate of rate: }L''(t)",
            font_size=32, color=ORANGE
        )
        sequence = VGroup(
            level,
            VGroup(first_arrow, first_label).arrange(RIGHT, buff=0.22),
            rate,
            VGroup(second_arrow, second_label).arrange(RIGHT, buff=0.22),
            rate_of_rate
        ).arrange(DOWN, buff=0.14)
        sequence.scale(0.78)
        sequence.move_to(UP * 0.55)
        fit_width(sequence, 10.8)

        example = VGroup(
            MathTex(r"L(t)=3t^2+2t", font_size=27, color=WHITE),
            MathTex(r"L'(t)=6t+2", font_size=27, color=GOLD),
            MathTex(r"L''(t)=6", font_size=27, color=ORANGE)
        ).arrange(RIGHT, buff=0.48)
        fit_width(example, 11.3)
        example.move_to(DOWN * 2.05)

        note = body(
            "The rate is increasing at a constant rate in this model.",
            size=19, color=MUTED, max_width=11.3
        ).move_to(DOWN * 2.8)

        self.play(Write(sequence), run_time=5)
        self.play(Write(example), run_time=3)
        self.play(FadeIn(note), run_time=2)
        hold(28)

        # ==================================================================
        # 7. SUMMARY AND PERSONAL CREDITS (4:05–5:00 approx.)
        # ==================================================================
        clean_transition()
        t = show_title("The Big Idea")

        summary_lines = [
            ("Average rate", "change across an interval", ORANGE),
            ("Instantaneous rate", "change at one moment", GOLD),
            ("First derivative", "slope of the tangent", TEAL),
            ("Second derivative", "how the rate changes", PINK)
        ]

        rows = VGroup()
        for label, meaning, color in summary_lines:
            row = VGroup(
                body(label + "  →", size=23, color=color, max_width=4.5),
                body(meaning, size=23, color=WHITE, max_width=6.8)
            ).arrange(RIGHT, buff=0.22, aligned_edge=DOWN)
            rows.add(row)

        rows.arrange(DOWN, buff=0.48, aligned_edge=LEFT)
        rows.scale(0.83)
        rows.move_to(ORIGIN + DOWN * 0.05)
        fit_width(rows, 11.4)

        self.play(LaggedStart(
            *[FadeIn(row, shift=UP * 0.12) for row in rows],
            lag_ratio=0.35
        ), run_time=5)
        hold(17)

        clean_transition()
        thanks = Text(
            "Thank You for Watching",
            font_size=38, weight=BOLD, color=TEAL
        )
        fit_width(thanks, 11.5)
        thanks.move_to(UP * 1.25)

        student = Text("Kritika Pandey", font_size=30, color=WHITE)
        urn = Text("URN: E25B070687", font_size=25, color=GOLD)
        course = Text("M3 • Linear Algebra & Calculus", font_size=22, color=MUTED)

        credits = VGroup(student, urn, course).arrange(DOWN, buff=0.42)
        credits.move_to(DOWN * 0.55)

        self.play(Write(thanks), run_time=2.5)
        self.play(FadeIn(credits), run_time=2.5)
        hold(16)
