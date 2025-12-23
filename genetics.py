import numpy as np
import random
from config import MUTATIONRATE, MUTATIONSTRENGTH

class TreeDNA:
    def __init__(self):
        self.probabilities = np.array([0.6, 0.3, 0.1])
        self.angle = np.pi/6
    def normaliseProbs(self):
        total = np.sum(self.probabilities)
        if total==0: self.probabilities=np.array([0.33, 0.33, 0.33])
        else: self.probabilities/=total

    def mutate(self):
        if random.random()<MUTATIONRATE:
            change=(random.random()*2-1)*MUTATIONSTRENGTH
            self.angle+=change
            self.angle=max(0.17, min(self.angle, 1.57))
            idx=random.randint(0, 2)
            self.probabilities[idx]+=change
            self.probabilities = np.clip(self.probabilities, 0.05, 1.0)
            self.normaliseProbs()
    def clone(self):
        newDNA = TreeDNA()
        newDNA.probabilities = np.copy(self.probabilities)
        newDNA.angle = self.angle
        return newDNA
