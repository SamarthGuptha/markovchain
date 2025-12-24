import pygame, mathutils
import numpy as np
from config import *

def lerpColor(c1, c2, t):
    r = int(c1[0] + (c2[0]-c1[0]) * t)
    g = int(c1[1] + (c2[1]-c1[1]) * t)
    b = int(c1[2] + (c2[2]-c1[2]) * t)
    return f'#{r:02x}{g:02x}{b:02x}'

class Tree:
    def __init__(self, dna):
        self.dna=dna
        self.segments=[]
        self.fitness=0
        self.minX=0
        self.maxX=0
        self.minY=0
        self.maxY=0
    def grow(self):
        self.segments=[]
        startVec = np.array([0, BRANCHLENGTH])
        stack=[(np.array([0.0, 0.0]), startVec, 0)]
        while stack:
            currentPos, currentDir, depth=stack.pop()
            if depth >= MAXDEPTH:continue
            endPos = currentPos+currentDir
            self.segments.append(((currentPos[0], currentPos[1]),(endPos[0], endPos[1]),depth))
            self.minX = min(self.minX, endPos[0])
            self.maxX = max(self.maxX, endPos[0])
            self.minY = min(self.minY, endPos[1])
            choice = np.random.choice(['SPLIT', 'STRAIGHT', 'STOP'], p=self.dna.probabilities)

            if choice == 'STOP':continue
            nextLenMult = self.dna.shrinkFactor
            if choice == 'STRAIGHT':
                wobble = mathutils.getRotationMatrix((np.random.rand() - 0.5) * 0.2)
                newDir = mathutils.transformVector(currentDir, wobble) * nextLenMult
                stack.append((endPos, newDir, depth + 1))
            elif choice == 'SPLIT':
                rotleft = mathutils.getRotationMatrix(-self.dna.angle)
                rotright = mathutils.getRotationMatrix(self.dna.angle)
                dirleft = mathutils.transformVector(currentDir, rotleft) * nextLenMult
                dirright = mathutils.transformVector(currentDir, rotright) * nextLenMult
                stack.append((endPos, dirleft, depth + 1))
                stack.append((endPos, dirright, depth + 1))

    def calculateFitness(self):
        heightScore = abs(self.minY) * 3.0
        widthScore = (self.maxX - self.minX) * 1.0
        intersections=0
        checks=3
        for i in range(0, len(self.segments), checks):
            for j in range(i + 2, len(self.segments), checks):
                s1p1, s1p2, _ = self.segments[i]
                s2p1, s2p2, _ = self.segments[j]
                if mathutils.linesIntersect(s1p1, s1p2, s2p1, s2p2): intersections += 1
        penalty = intersections * 50
        self.fitness = max(1, (heightScore + widthScore) - penalty)
        return self.fitness

    def drawonCanvas(self, canvas, offsetX, offsetY, limit=None):
        count = 0
        total = len(self.segments)
        limit = total if limit is None else limit

        for p1, p2, depth in self.segments:
            if count>=limit: break
            width = max(1, int((MAXDEPTH-depth) * 0.8))
            t = depth / MAXDEPTH
            hexColor = lerpColor(TRUNKCOLOR, LEAFCOLOR, t)

            canvas.createLine(
                p1[0]+offsetX, p1[1]+offsetY,
                p2[0]+offsetX, p2[1]+offsetY,
                width=width, fill = hexColor, capstyle = "round"
            )
            count += 1