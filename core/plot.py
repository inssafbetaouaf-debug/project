import matplotlib.pyplot as plt


def plot_mst_layout(sequence, machine_lengths):
    """
    Visualisation de la disposition MST (une seule ligne)

    sequence : liste d'indices des machines
    machine_lengths : liste des longueurs des machines
    """

    x_pos = 0
    y_pos = 0

    fig, ax = plt.subplots(figsize=(10, 2))

    for idx in sequence:
        length = machine_lengths[idx]

        # Rectangle machine
        ax.add_patch(
            plt.Rectangle(
                (x_pos, y_pos),
                length,
                1,
                edgecolor="black",
                facecolor="lightblue"
            )
        )

        # Texte machine
        ax.text(
            x_pos + length / 2,
            y_pos + 0.5,
            f"M{idx + 1}",
            ha="center",
            va="center",
            fontsize=10
        )

        x_pos += length + 0.5  # espace entre machines

    ax.set_xlim(0, x_pos)
    ax.set_ylim(0, 2)
    ax.axis("off")
    ax.set_title("Disposition des machines – Méthode MST")

    return fig



def plot_slp_layout(layout):
    """
    Visualisation de la disposition SLP (grille)

    layout : dictionnaire {machine: (x, y)}
    """

    fig, ax = plt.subplots(figsize=(6, 6))

    for machine, (x, y) in layout.items():
        ax.add_patch(
            plt.Rectangle(
                (x, y),
                1,
                1,
                edgecolor="black",
                facecolor="lightgreen"
            )
        )

        ax.text(
            x + 0.5,
            y + 0.5,
            str(machine),
            ha="center",
            va="center"
        )

    ax.set_aspect("equal")
    ax.set_title("Disposition des machines – Méthode SLP")
    ax.axis("off")

    return fig

