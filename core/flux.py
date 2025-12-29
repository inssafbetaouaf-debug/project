import numpy as np
import pandas as pd


def compute_flux_matrices(machines, routings):
   
    n = len(machines)

    # Initialisation de la matrice de flux (numpy)
    flow_np = np.zeros((n, n))

    # Association machine → indice
    machine_to_index = {machine: i for i, machine in enumerate(machines)}

    # Calcul des flux à partir des routages
    for routing in routings:
        for k in range(len(routing) - 1):
            i = machine_to_index[routing[k]]
            j = machine_to_index[routing[k + 1]]

            # Flux symétrique
            flow_np[i, j] += 1
            flow_np[j, i] += 1

    # Conversion en DataFrame pour SLP
    flow_df = pd.DataFrame(flow_np, index=machines, columns=machines)

    return flow_np, flow_df
