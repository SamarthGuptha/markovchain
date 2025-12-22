from manim import *
import evolution_logic
import numpy as np


class EvolutionaryFractals(Scene):
    def construct(self):
        pop_size = 20
        generations = 3
        population = [evolution_logic.TreeDNA() for _ in range(pop_size)]
        title = Text("Evolutionary Fractal Trees", font_size=36).to_edge(UP)
        gen_text = Text("Initializing...", font_size=24, color=YELLOW).next_to(title, DOWN)
        self.play(Write(title), Write(gen_text))
        prev_tree_group = None
        for gen in range(1, generations + 1):
            new_gen_text = Text(f"Generation: {gen} | Pop: {pop_size}", font_size=24, color=YELLOW).next_to(title, DOWN)
            self.play(Transform(gen_text, new_gen_text), run_time=0.5)
            population, best_dna = evolution_logic.runGeneration(population, gen)
            tree_group = VGroup()
            sorted_segments = sorted(best_dna.segments, key=lambda x: x['depth'])
            base_color = ManimColor("#795548")
            tip_color = ManimColor("#8BC34A")
            for seg in sorted_segments:
                line = Line(seg['start'], seg['end'], stroke_width=4 - (seg['depth'] * 0.4))
                alpha = seg['depth'] / 7.0
                line.set_color(interpolate_color(base_color, tip_color, alpha))
                tree_group.add(line)
            p_split = best_dna.probs[1]
            p_str = best_dna.probs[2]
            angle_deg = np.degrees(best_dna.angle)
            stats_str = f"Fitness: {best_dna.fitness:.1f}\nSplit Prob: {p_split:.2f}\nAngle: {angle_deg:.1f}°"
            stats_text = Text(stats_str, font_size=20, line_spacing=1.2).to_corner(UL).shift(DOWN * 1)
            if prev_tree_group:
                self.play(
                    FadeOut(prev_tree_group),
                    FadeOut(prev_stats),
                    run_time=0.5
                )
            self.play(
                Create(tree_group, lag_ratio=0.01),
                Write(stats_text),
                run_time=3.5  # Fast growth
            )
            self.wait(1)
            prev_tree_group = tree_group
            prev_stats = stats_text
        final_text = Text("Evolution Complete", color=GREEN).next_to(tree_group, DOWN)
        self.play(Write(final_text))
        self.wait(2)