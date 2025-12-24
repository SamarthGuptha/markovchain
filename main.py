import tkinter as tk
from tkinter import ttk
import config
import numpy as np
from config import *
from genetics import TreeDNA
from tree import Tree

class EvolutionaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Evolutionary Fractals")
        self.root.geometry = (f"{CANVASWIDTH + SIDEBARWIDTH}x{CANVASHEIGHT}")
        self.root.resizable(False, False)
        self.population = []
        self.champion = None
        self.generation = 1
        self.isRunning = False
        self.animationProgress = 0
        self.createWidgets()
        self.animateLoop()
        self.createSliderr
        self.dagTIME
        self.ragTIME
    def createWidgets(self):
        self.canvas = tk.Canvas(
            self.root,
            width=CANVASWIDTH,
            height=CANVASHEIGHT,
            bg=COLORBG,
            highlightthickness=0
        )
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH)
        self.sidebar = tk.Frame(self.root, width=SIDEBARWIDTH, bg="#2d2d2d", padx=10, pady=10)
        self.sidebar.pack(side=tk.LEFT, fill=tk.BOTH)
        self.sidebar.pack_propagate(False)
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", background="#2d2d2d", foreground="white")
        style.configure("TButton", font=('Segoe UI', 10))
        lblTitle = ttk.Label(self.sidebar, text="Control Panel", font=("Segoe UI", 16, "bold"))
        lblTitle.pack(pady=(0, 20))
        self.btnRun = ttk.Button(self.sidebar, text="Start", command=self.toggleRun)
        self.btnRun.pack(fill=tk.X, pady=5)
        btnReset = ttk.Button(self.sidebar, text="Reset Population", command=self.resetPopulation)
        btnReset.pack(fill=tk.X, pady=5)
        self.createSlider("Mutation Rate", 0.0, 1.0, MUTATIONRATE, self.updateMutRate)
        self.createSlider("Mutation Strength", 0.0, 0.5, MUTATIONSTRENGTH, self.updateMutStrength)
        ttk.Separator(self.sidebar, orient='horizontal').pack(fill='x', pady=20)
        self.lblGen = ttk.Label(self.sidebar, text="Generation: 0", font=("Segoe UI", 12))
        self.lblGen.pack(anchor="w")
        self.lblFit = ttk.Label(self.sidebar, text="Best Fitness: 0")
        self.lblFit.pack(anchor="w")
        self.lblDNA = ttk.Label(self.sidebar, text="Angle: 0°")
        self.lblDNA.pack(anchor="w")

    def createSlider(self, label, minV, maxV, default, callback):
        frame = tk.Frame(self.sidebar, bg="#2d2d2d")
        frame.pack(fill=tk.X, pady=10)
        lbl = ttk.Label(frame, text=label)
        lbl.pack(anchor="w")

        scale = tk.Scale(frame, from_=minV, to=maxV, orient=tk.HORIZONTAL,
                         resolution=0.01, bg="#2d2d2d", fg="white", highlightthickness=0, command=callback)
        scale.set(default)
        scale.pack(fill=tk.X)

    def updateMutRate(self, val): config.MUTATIONRATE = float(val)
    def updateMutStrength(self, val): config.MUTATIONSTRENGTH = float(val)
    def toggleRun(self):
        self.isRunning = not self.isRunning
        self.btnRun.configure(text="Pause" if self.isRunning else "Resume")

    def resetPopulation(self):
        self.population = []
        for _ in range(POPULATIONSIZE):
            dna = TreeDNA()
            t=Tree(dna)
            t.grow()
            t.calculateFitness()
            self.population.append(t)

        self.champion = max(self.population, key=lambda t: t.fitness)
        self.generation = 1
        self.animationProgress = 0
        self.drawChampion()
        self.updateStats()
    def evolve(self):
        self.population.sort(key=lambda t: t.fitness, reverse=True)
        cutoff = int(POPULATIONSIZE*ELITISM)
        survivors = self.population[:cutoff]
        nextGen = survivors[:]
        while len(nextGen) < config.POPULATIONSIZE:
            parent = survivors[np.random.randint(0, len(survivors))]
            childDNA = parent.dna.clone()
            childDNA.mutate()
            child = Tree(childDNA)
            child.grow()
            child.calculateFitness()
            nextGen.append(child)

        self.population = nextGen
        self.champion = self.population[0]
        self.generation+=1
        self.updateStats()
        self.animationProgress = 0

    def updateStats(self):
        self.lblGen.config(text = f"Generation: {self.generation}")
        self.lblFit.config(text=f"Best Fitness: {self.champion.fitness}")
        self.lblDNA.config(text = f"Branch Angle: {np.degrees(self.champion.dna.angle)}")
    def drawChampion(self):
        self.canvas.delete("all")
        if not self.champion: return
        startX = CANVASWIDTH//1.75
        startY = CANVASHEIGHT//1.3
        limit = int(self.animationProgress)
        self.champion.drawonCanvas(self.canvas, startX, startY, limit)

    def animateLoop(self):
        if self.champion:
            totalSegments = len(self.champion.segments)
            if self.animationProgress < totalSegments:
                self.animationProgress+= 5 + (totalSegments / 50)
                self.drawChampion()
            elif self.isRunning: self.evolve()

        self.root.after(16, self.animateLoop)

if __name__ == "__main__":
    root = tk.Tk()
    app = EvolutionaryApp(root)
    root.mainloop()

