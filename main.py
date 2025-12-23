import sys, pygame
from config import *
from genetics import TreeDNA
from tree import Tree
import numpy as np


pygame.init()
screen=pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption('Evolutionary Fractals')
clock=pygame.time.Clock()

font=pygame.font.SysFont("monospace", 16)
largeFont = pygame.font.SysFont("monospace", 32)
def getGridCenter(index):
    col=index%GRID_COLS
    row=index//GRID_COLS
    cellW = SCREENWIDTH//GRID_COLS
    cellH = SCREENHEIGHT//GRID_ROWS
    x=col*cellW+(cellW//2)
    y=row*cellH+(cellH-20)
    return y, x

def main():
    population = []
    for _ in range(POPULATIONSIZE):
        dna=TreeDNA()
        tree = Tree(dna)
        tree.grow()
        population.append(tree)
    generationCount=1
    state="GROWING"
    timer=0
    running=True
    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running=False

        if state=="GROWING":
            timer+=1
            if timer>TIMETOGROW:
                state="EVALUATING"
                timer=0
        elif state=="EVALUATING":
            scores=[t.calculateFitness() for t in population]
            population.sort(key=lambda t: t.fitness, reverse=True)
            state="DYING"
        elif state=="DYING":
            cutoff=int(POPULATIONSIZE*ELITISM)
            for i in range(cutoff, POPULATIONSIZE): population[i].isDead = True
            timer+=1

            if timer>TIMETOKILL:
                if generationCount<GENERATIONS:
                    state="REPRODUCING"
                else:
                    state="FINISHED"
                timer=0
        elif state=="REPRODUCING":
            survivors = [t for t in population if not t.isDead]
            nextGen=[]
            while len(nextGen)<POPULATIONSIZE:
                parent = survivors[np.random.randint(0, len(survivors))]
                childDNA = parent.dna.clone()
                childDNA.mutate()
                childTree = Tree(childDNA)
                childTree.grow()
                nextGen.append(childTree)
            population = nextGen
            generationCount+=1
            state="GROWING"

        cellW= SCREENWIDTH//GRID_COLS
        cellH = SCREENHEIGHT//GRID_ROWS
        for x in range(0, SCREENWIDTH, cellW):
            pygame.draw.line(screen, (20, 20, 20), (x, 0), (x, SCREENHEIGHT))
        for y in range(0, SCREENHEIGHT, cellH):
            pygame.draw.line(screen, (20, 20, 20), (0, y), (SCREENWIDTH, y))

        for i, tree in enumerate(population):
            cx, cy = getGridCenter(i)
            tree.draw(screen, cx, cy)
            scoreColor = GOLD if i==0 and state!="GROWING" else GRAY
            text = font.render(f"Fit: {int(tree.fitness)}", True, scoreColor)
            screen.blit(text, (cx-30, cy-10))

        genText = largeFont.render(f"Generation: {generationCount} / {GENERATIONS}", True, WHITE)
        stateText = font.render(f"State: {state}", True, WHITE)
        screen.blit(genText, (20, 20))
        screen.blit(stateText, (20, 60))

        if state == "FINISHED":
            finText = largeFont.render("SIMULATION COMPLETE", True, GREEN)
            screen.blit(finText, (SCREENWIDTH//2-150, SCREENHEIGHT//2))

        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
    sys.exit()
if __name__ == "__main__": main()