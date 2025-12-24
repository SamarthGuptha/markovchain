import numpy as np
import random
from config import MUTATIONRATE, MUTATIONSTRENGTH

class TreeDNA:
    def __init__(self):
        self.probabilities = np.array([0.7, 0.25, 0.05])
        self.angle = np.pi/6
        self.shrinkFactor = 0.75
    def normaliseProbs(self):
        total = np.sum(self.probabilities)
        if total == 0: self.probabilities = np.array([0.33, 0.33, 0.33])
        else: self.probabilities/=total

    def mutate(self):
        if random.random() < MUTATIONRATE:
            self.angle += (random.random() * 2 - 1) * MUTATIONSTRENGTH
            self.angle = np.clip(self.angle, 0.1, 1.5)
            idx = random.randint(0, 2)
            self.probabilities[idx] += (random.random() * 2 - 1) * MUTATIONSTRENGTH
            self.probabilities = np.clip(self.probabilities, 0.05, 1.0)
            self.normaliseProbs()
            self.shrinkFactor += (random.random() * 2 - 1) * (MUTATIONSTRENGTH * 0.5)
            self.shrinkFactor = np.clip(self.shrinkFactor, 0.6, 0.9)
    def clone(self):
        newDNA = TreeDNA()
        newDNA.probabilities = np.copy(self.probabilities)
        newDNA.angle = self.angle
        newDNA.shrinkFactor = self.shrinkFactor
        return newDNA