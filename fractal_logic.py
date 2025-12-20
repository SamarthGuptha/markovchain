import numpy as np

STATE_SPLIT = "SPLIT"
STATE_STRAIGHT = "STRAIGHT"
STATE_TERMINATE = "TERMINATE"


def getRotationMatrix(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array(((c, -s), (s, c)))


def generateTreeData(origin, direction, length, depth, max_depth, segments_list=None):
    if segments_list is None: segments_list = []

    if depth >= max_depth: return segments_list
    if depth < 2:
        probabilities = [0.0, 1.0, 0.0]
    else:
        probabilities = [0.1, 0.6, 0.3]
    states = [STATE_TERMINATE, STATE_SPLIT, STATE_STRAIGHT]
    state = np.random.choice(states, p=probabilities)

    if state == STATE_TERMINATE: return segments_list

    norm = np.linalg.norm(direction)
    if norm == 0: return segments_list
    unit_direction = direction / norm
    end_point = origin + (unit_direction * length)
    segments_list.append({
        "start": origin,
        "end": end_point,
        "depth": depth
    })
    new_length = length * 0.75
    if state == STATE_SPLIT:
        angle_offset = np.radians(25)
        v2 = unit_direction[:2]

        rotleft = getRotationMatrix(angle_offset)
        newDir_left2D = np.dot(rotleft, v2)
        newDir_left = np.array([newDir_left2D[0], newDir_left2D[1], 0])
        generateTreeData(end_point, newDir_left, new_length, depth + 1, max_depth, segments_list)

        rotright = getRotationMatrix(-angle_offset)
        newDir_right2D = np.dot(rotright, v2)
        newDir_right = np.array([newDir_right2D[0], newDir_right2D[1], 0])

        generateTreeData(end_point, newDir_right, new_length, depth + 1, max_depth, segments_list)
    elif state == STATE_STRAIGHT:
        wobble = np.radians(np.random.uniform(-10, 10))
        v2 = unit_direction[:2]
        rotwobble = getRotationMatrix(wobble)
        newDir_2D = np.dot(rotwobble, v2)
        newDir = np.array([newDir_2D[0], newDir_2D[1], 0])

        generateTreeData(end_point, newDir, new_length, depth + 1, max_depth, segments_list)

    return segments_list
