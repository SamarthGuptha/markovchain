from manim import *
import evolution_logic
import numpy as np


class FullPopulationEvolution(Scene):
    def construct(self):
        # --- Config ---
        pop_size = 20
        generations = 3
        cols = 5
        rows = 4

        # Calculate Grid Positions
        # Screen is roughly 14 units wide, 8 units high
        grid_positions = []
        start_x = -5.5
        start_y = 2.5
        gap_x = 14 / cols
        gap_y = 7 / rows

        for r in range(rows):
            for c in range(cols):
                pos = np.array([
                    start_x + (c * gap_x),
                    start_y - (r * gap_y),
                    0
                ])
                grid_positions.append(pos)

        # Initialize Population
        population = [evolution_logic.TreeDNA() for _ in range(pop_size)]

        title = Text("Evolutionary Process: Full Population", font_size=32).to_edge(UP)
        self.add(title)

        current_tree_mobjects = VGroup()

        for gen in range(1, generations + 1):

            # 1. Update Labels
            gen_label = Text(f"Generation {gen}", font_size=24, color=YELLOW).to_edge(LEFT, buff=0.5).shift(UP * 3)
            self.add(gen_label)

            # 2. Grow Trees (Math)
            # We pass the grid positions so they grow in their specific slots
            evolution_logic.grow_population_at_positions(
                population, grid_positions, max_depth=6
            )

            # 3. Create Mobjects (Visuals)
            generation_group = VGroup()
            tree_map = {}  # Map DNA object to its VGroup for later reference

            for i, dna in enumerate(population):
                tree_visual = VGroup()

                # Sort segments for organic growth
                sorted_segs = sorted(dna.segments, key=lambda x: x['depth'])

                # Color based on fitness potential (initially just brown/green)
                # We will recolor them after evaluation
                for seg in sorted_segs:
                    line = Line(seg['start'], seg['end'], stroke_width=2)
                    line.set_color(interpolate_color(color.BROWN, color.GREEN, seg['depth'] / 6))
                    tree_visual.add(line)

                generation_group.add(tree_visual)
                tree_map[id(dna)] = tree_visual

            # 4. Animate Growth ("The Birth")
            # We fade out the old and grow the new simultaneously or sequentially
            if gen > 1:
                self.play(
                    FadeOut(current_tree_mobjects),
                    Create(generation_group, lag_ratio=0.01),
                    run_time=2.5
                )
            else:
                self.play(Create(generation_group, lag_ratio=0.01), run_time=3)

            current_tree_mobjects = generation_group

            bestDNA = evolution_logic.evalPop(population)
            survivor_count = len(population)//2
            culls = population[survivor_count:]
            cullmObjects = VGroup(*[tree_map[id(d)] for d in culls])
            bestVisual = tree_map[id(bestDNA)]
            best_rect = SurroundingRectangle(bestVisual, color=GOLD, buff=0.1)
            self.play(Create(best_rect))
            self.play(cullmObjects.animate.set_opacity(0.2).set_color(GRAY), run_time=1)
            self.wait(0.5)
            population = evolution_logic.breedNextGen(population)
            self.play(FadeOut(best_rect), FadeOut(gen_label))
        final_text = Text("Evolution Complete", color=GREEN).scale(1.5)
        self.play(FadeOut(current_tree_mobjects), Write(final_text))
        self.wait(2)