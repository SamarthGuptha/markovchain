import numpy as np
def getRotationMatrix(thetaRad):
    c, s=np.cos(thetaRad), np.sin(thetaRad)
    return np.array(((c, -s), (s, c)))
def transformVector(vector, rotationMatrix):
    return np.dot(rotationMatrix, vector)

def linesIntersect(p1, p2, p3, p4):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4

    denom = (y4-y3)*(x2-x1)-(x4-x3)*(y2-y1)
    if denom == 0: return False

    ua=((x4-x3)*(y1-y3)-(y4-y3)*(x1-x3))/denom
    ub=((x2-x1)*(y1-y3)-(y2-y1)*(x1-x3))/denom
    if 0<ua<1 and 0<ub<1: return True
    return False