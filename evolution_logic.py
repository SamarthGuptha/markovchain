import numpy as np
def getRotationMatrix(theta):
    c, s=np.cos(theta), np.sin(theta)
    return np.array(((c, -s), (s, c)))

def segmentsIntersect(p1, p2, p3, p4):
    a, b=p1[:2], p2[:2]
    c, d=p3[:2], p4[:2]

    if np.allclose(a, c)or np.allclose(a, d) or np.allclose(b, c) or np.allclose(b, d): return False
    def ccw(A, B, C): return(c[1]-A[1])*(B[0]-A[0])>(B[1]-A[1])*(C[0]-A[0])

    return ccw(a, c, d)!=ccw(b, c, d) and ccw(a, b, c) !=ccw(a, b, d)

class TreeDNA:
    def __init__(self, probs=None, angle=None):
        if probs is None:
            raw = np.random.rand(3)
            self.probs=raw/raw.sum()
        else: self.probs=probs
        if angle is None:
            self.angle=np.random.uniform(np.radians(15), np.radians(45))
        else: self.angle = angle
        self.segments=[]
        self.fitness=0
    def mutate(self):
        delta=np.random.uniform(-0.1, 0.1, 3)
        newProbs=self.probs+delta
        newProbs=np.clip(newProbs, 0.01, 1.0)
        self.probs=newProbs/newProbs.sum()
        self.angle+=np.random.uniform(-0.1, 0.1)
        self.angle=np.clip(self.angle, np.radians(10), np.radians(60))
def growTree(dna, origin, direction, length, depth, maxDepth):
    if depth==0: dna.segments=[]
    if depth>=maxDepth: return
    norm=np.linalg.norm(direction)
    if norm==0: return
    unitDir = direction/norm
    endPoint=origin+(unitDir*length)

    dna.segments.append({
        "start": origin,
        "end": endPoint,
        "depth": depth
    })
    newLen=length*0.75
    if depth==0: state=1
    else: state=np.random.choice([0, 1, 2], p=dna.probs)
    if state==0: return
    elif state==1:
        v2 = unitDir[:2]
        rotl = getRotationMatrix(dna.angle)
        dirl = np.array([*np.dot(rotl, v2), 0])
        growTree(dna, endPoint, dirl, newLen, depth+1, maxDepth)

        rotr = getRotationMatrix(-dna.angle)
        dirr = np.array([*np.dot(rotr, v2), 0])
        growTree(dna, endPoint, dirr, newLen, depth+1, maxDepth)

    elif state==2:
        wobble = np.radians(np.random.uniform(-5, 5))
        v2=unitDir[:2]
        rotw=getRotationMatrix(wobble)
        dirw=np.array([*np.dot(rotw, v2), 0])
        growTree(dna, endPoint, dirw, newLen, depth+1, maxDepth)
def calculateFitness(dna):
    if not dna.segments:
        dna.fitness=0
        return

    ys=[s['end'][1] for s in dna.segments]
    maxY=max(ys)

    xs=[s['end'][0] for s in dna.segments]
    width=max(xs)-min(xs)

    penalty=0
    segs=dna.segments
    count=len(segs)

    limitChecks=100
    checks=0
    intersectionCount=0

    for i in range(count):
        for j in range(i+2, count):
            if checks>limitChecks: break
            p1, p2 = segs[i]['start'], segs[i]['end']
            p3, p4 = segs[j]['start'], segs[j]['end']

            if segmentsIntersect(p1, p2, p3, p4):
              intersectionCount+=1
            checks+=1
    score=(maxY+4.0)*2.0+(width*1.5)-(intersectionCount*5.0)
    dna.fitness=max(0, score)

def runGeneration(population, generationID):
    for dna in population:
        growTree(dna, origin=np.array([0, -3, 0]), direction=np.array([0, 1, 0]), length=1.8, depth=0, maxDepth=7)
        calculateFitness(dna)
    population.sort(key=lambda x: x.fitness, reverse=True)
    bestDNA=population[0]
    print(f"Gen {generationID} Best Fitness: {bestDNA.fitness:.2f}")
    survivorsCount=len(population)//2
    survivors=population[:survivorsCount]

    nextGen = []
    nextGen.append(TreeDNA(survivors[0].probs.copy(), survivors[0].angle))
    while len(nextGen)<len(population):
        parent=np.random.choice(survivors)
        child=TreeDNA(parent.probs.copy(), parent.angle)
        child.mutate()
        nextGen.append(child)
    return nextGen, bestDNA