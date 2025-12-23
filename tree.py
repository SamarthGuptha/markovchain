import pygame, mathutils
import numpy as np
from config import *

class Tree:
    def __init__(self, dna):
        self.dna=dna
        self.segments=[]
        self.fitness=0
        self.isDead=False
        self.color=GREEN
        self.minX=0
        self.maxX=0
        self.minY=0
        self.maxY=0
    def grow(self):
        self.segments=[]
        startVec=np.array([0, -BRANCHLENGTH])
        stack=[(np.array([0.0, 0.0]), startVec, 0)]

        while stack:
            currentPos, currentDir, depth=stack.pop()
            if depth>=MAXDEPTH: continue
            endPos=currentPos+currentDir
            p1 = (currentPos[0], currentPos[1])
            p2=(endPos[0], endPos[1])
            self.segments.append((p1, p2))
            self.minX = min(self.minX, endPos[0])
            self.maxX = max(self.maxX, endPos[0])
            self.minY = min(self.minY, endPos[1])
            choice = np.random.choice(['SPLIT', 'STRAIGHT', 'STOP'], p=self.dna.probabilities)
            if choice=='STOP': continue
            elif choice=='SPLIT':
                wobble=mathutils.getRotationMatrix((np.random.rand()-0.5)*0.1)
                newDir=mathutils.transformVector(currentDir, wobble)*0.9
                stack.append((endPos, newDir, depth+1))
            elif choice=='SPLIT':
                rotleft=mathutils.getRotationMatrix(-self.dna.angle)
                rotright=mathutils.getRotationMatrix(self.dna.angle)
                dirleft=mathutils.transformVector(currentDir, rotleft)*0.85
                dirright=mathutils.transformVector(currentDir, rotright)*0.85
                stack.append((endPos, dirleft, depth+1))
                stack.append((endPos, dirright, depth+1))

    def calculateFitness(self):
        heightScore = abs(self.minY)*2.0
        widthScore = (self.maxX-self.minY)*0.5
        intersections=0
        checks =2
        for i in range(0, len(self.segments), checks):
            for j in range(i+2, len(self.segments), checks):
                s1=self.segments[i]
                s2=self.segments[j]
                if mathutils.linesIntersect(s1[0], s1[1], s2[0], s2[1]): intersections+=1

        penalty = intersections*20
        self.fitness=max(0, (heightScore+widthScore)-penalty)
        return self.fitness
    def draw(self, surface, offsetX, offsetY, alpha=255):
        color = self.color if not self.isDead else RED
        drawColor = list(color)
        if self.isDead: pass

        for p1, p2 in self.segments:
            start=(p1[0]+offsetX, p1[1]+offsetY)
            end = (p2[0]+offsetX, p2[1]+offsetY)
            pygame.draw.line(surface, drawColor, start, end, 1)


