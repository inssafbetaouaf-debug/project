import streamlit as st
import numpy as np
import pandas as pd

from flux import compute_flux_matrices
from slp import generate_slp_layout, slp_total_distance
from mst import modified_mst
from plot import plot_mst_layout, plot_slp_layout


st.set_page_config(page_title="Facilities Layout Simulator", layout="wide")

st.title("Plateforme interactive d’aménagement d’atelier")
st.write("Simulation des méthodes SLP et MST – Facilities Design")


st.header("1. Saisie des données")

n_machines = st.number_input("Nombre de machines", min_value=2, value=3)

machines = [f"M{i+1}" for i in range(n_machines)]

st.subheader("Dimensions des machines (longueur)")
lengths = []
for i in range(n_machines):
    l = st.number_input(f"Longueur de la machine {i+1}", min_value=0.5, value=2.0)
    lengths.append(l)

st.subheader("Routage des produits")
st.write("Exemple : M1 → M2 → M3")

n_products = st.number_input("Nombre de produits", min_value=1, value=2)

routings = []
for p in range(n_products):
    routing_str = st.text_input(
        f"Routage du produit {p+1}",
        value="M1,M2,M3"
    )
    routing = routing_str.replace(" ", "").split(",")
    routings.append(routing)


if st.button("Calculer la matrice de flux"):

    flow_np, flow_df = compute_flux_matrices(machines, routings)

    st.subheader("Matrice de flux")
    st.dataframe(flow_df)

    st.header("2. Méthode SLP")

    slp_layout = generate_slp_layout(machines)
    slp_distance = slp_total_distance(flow_df, slp_layout)

    fig_slp = plot_slp_layout(slp_layout)
    st.pyplot(fig_slp)

    st.write(f"Distance totale SLP : **{slp_distance:.2f}**")

 
    st.header("3. Méthode MST")

    clearance = st.number_input(
        "Clearance (distance de sécurité entre machines)",
        min_value=0.0,
        value=1.0
    )

    sequence = modified_mst(flow_np, lengths, clearance)

    fig_mst = plot_mst_layout(sequence, lengths)
    st.pyplot(fig_mst)

  
    st.header("4. Comparaison des solutions")

    st.write("Séquence MST :", [machines[i] for i in sequence])

    st.success("La solution avec la distance totale minimale est considérée comme la meilleure.")

