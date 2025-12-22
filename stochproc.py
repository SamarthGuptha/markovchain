from manim import *
import fractal_logic
import numpy as np

class stochasticFractalTree(Scene):
    def construct(self):
        origin = DOWN*3.5
        startDirection = UP
        startLength = 2.0
        maxRecursionDepth = 10

        self.camera.background_color = "#1a1a1a"
        tree_data = fractal_logic.generateTreeData(origin, startDirection, startLength, depth=0, max_depth=maxRecursionDepth)
        tree_data.sort(key=lambda x: x['depth'])

        tree_group=VGroup()
        base_color = ManimColor("#5D4037")
        tip_color = ManimColor("#4CAF50")

        for segment in tree_data:
            start=segment['start']
            end=segment['end']
            depth=segment['depth']
            branch=Line(start, end, stroke_width=4-(depth*0.3))
            alpha=depth/maxRecursionDepth

            branch.set_color(interpolate_color(base_color, tip_color, alpha))
            tree_group.add(branch)

        title=Text("Stochastic Markov Tree", font_size=36).to_edge(UP)
        details = Text(f"Segments: {len(tree_group)}|Depth: {maxRecursionDepth}", font_size=18, color=GRAY).next_to(title, DOWN)
        self.play(Write(title), FadeIn(details))
        self.play(Create(tree_group, lag_ratio=0.01, run_time=6, rate_func=linear))
        self.wait(2)