import numpy as np


def generate_clearance_matrix(n, clearance_value=1.0):
    clearance = np.full((n, n), clearance_value)
    np.fill_diagonal(clearance, 0)
    return clearance


def modified_mst(flow_matrix, lengths, clearance_value=1.0):

    n = len(lengths)
    clearance_matrix = generate_clearance_matrix(n, clearance_value)

    weight = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            if i != j:
                weight[i, j] = flow_matrix[i, j] * (
                    clearance_matrix[i, j] + 0.5 * (lengths[i] + lengths[j])
                )
            else:
                weight[i, j] = -np.inf

    i_star, j_star = np.unravel_index(np.argmax(weight), weight.shape)

    sequence = [i_star, j_star]
    connected = {i_star, j_star}

    weight[i_star, j_star] = -np.inf
    weight[j_star, i_star] = -np.inf

    while len(connected) < n:
        best_value = -np.inf
        best_node = None
        attach_left = True

        for k in range(n):
            if k not in connected:
                if weight[i_star, k] > best_value:
                    best_value = weight[i_star, k]
                    best_node = k
                    attach_left = True

                if weight[j_star, k] > best_value:
                    best_value = weight[j_star, k]
                    best_node = k
                    attach_left = False

        if attach_left:
            sequence.insert(0, best_node)
            i_star = best_node
        else:
            sequence.append(best_node)
            j_star = best_node

        connected.add(best_node)

        for k in range(n):
            weight[best_node, k] = -np.inf
            weight[k, best_node] = -np.inf

    return sequence


def mst_total_distance(sequence, flow_matrix, lengths, clearance=0.5):
    """
    Calcule la distance totale parcourue pour la disposition MST
    (machines sur une seule ligne)
    """

    positions = {}
    x = 0

    for idx in sequence:
        center = x + lengths[idx] / 2
        positions[idx] = center
        x += lengths[idx] + clearance

    total_distance = 0
    n = len(sequence)

    for i in range(n):
        for j in range(n):
            if i != j:
                mi = sequence[i]
                mj = sequence[j]
                fij = flow_matrix[mi, mj]
                dij = abs(positions[mi] - positions[mj])
                total_distance += fij * dij

    return total_distance
