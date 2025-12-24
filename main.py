import pygame
import sys
import numpy as np
from config import *
from genetics import TreeDNA
from tree import Tree
pygame.init()

screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("Evolutionary Fractals")
clock = pygame.time.Clock()
fontUI = pygame.font.SysFont("segoeui", 20)
fontTitle = pygame.font.SysFont("segoeui", 40, bold=True)
def createInitialPopulation():
    pop = []
    for _ in range(POPULATIONSIZE):
        dna = TreeDNA()
        t = Tree(dna)
        t.grow()
        t.calculateFitness()
        pop.append(t)
    return pop
def evolvePopulation(population):
    population.sort(key=lambda t: t.fitness, reverse=True)
    cutoff = int(POPULATIONSIZE * ELITISM)
    survivors = population[:cutoff]
    nextGen = []
    nextGen.extend(survivors)
    while len(nextGen)<POPULATIONSIZE:
        parent = survivors[np.random.randint(0, len(survivors))]
        childDNA = parent.dna.clone()
        childDNA.mutate()
        child = Tree(childDNA)
        child.grow()
        child.calculateFitness()
        nextGen.append(child)
    return nextGen

def main():
    population = createInitialPopulation()
    champion = max(population, key=lambda t: t.fitness)
    currentGen = 1
    drawLimit = 0
    drawSpeed = 10
    targetSegments = len(champion.segments)
    evolutionTrigger = False
    running = True
    while running:
        screen.fill(BACKGROUND)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if event.type == pygame.MOUSEBUTTONDOWN: drawLimit = targetSegments
        if drawLimit < targetSegments: drawLimit += drawSpeed

        else:
            evolutionTrigger = True
        champion.draw(screen, STARTPOS[0], STARTPOS[1], drawLimit)
        if evolutionTrigger and currentGen < GENERATIONS:
            pygame.time.delay(100)
            population = evolvePopulation(population)
            newChamp = population[0]
            champion = newChamp
            currentGen += 1
            drawLimit = 0
            targetSegments = len(champion.segments)
            evolutionTrigger = False

        titleSurf = fontTitle.render(f"Generation {currentGen}", True, TEXTCOLOR)
        screen.blit(titleSurf, (20, 20))

        stats = [
            f"Fitness: {int(champion.fitness)}",
            f"Segments: {len(champion.segments)}",
            f"Angle: {int(np.degrees(champion.dna.angle))}°",
            f"Shrink: {champion.dna.shrinkFactor:.2f}"
        ]
        for i, line in enumerate(stats):
            s = fontUI.render(line, True, TEXTCOLOR)
            screen.blit(s, (20, 70 + i * 25))
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
    sys.exit()
if __name__ == "__main__":
    main()