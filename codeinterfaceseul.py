from tkinter import Tk, Label, Button, Entry, Scale, HORIZONTAL, Frame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import threading
import time

# Création de la fenêtre principale
fenetre = Tk()
fenetre.title("Interface Utilisateurs")

# Configuration de la grille principale
fenetre.columnconfigure(0, weight=1)
fenetre.columnconfigure(1, weight=2)
fenetre.columnconfigure(2, weight=1)
fenetre.rowconfigure(0, weight=1)

# Création des frames pour les zones
frame_connexion = Frame(fenetre, bg="lightgrey")
frame_connexion.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
frame_mouvement = Frame(fenetre, bg="white")
frame_mouvement.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
frame_commande = Frame(fenetre, bg="lightgrey")
frame_commande.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)

# Variable pour contrôler le fil d'exécution de la mise à jour des graphiques
recevoir_donnees = False

# Zone "Connexion avec le robot"
Label(frame_connexion, text="Connexion avec le robot").grid(row=0, column=0, columnspan=2, pady=5)
Entry(frame_connexion).grid(row=1, column=0, columnspan=2, pady=5)
Button(frame_connexion, text="START", command=lambda: start_acquisition()).grid(row=2, column=0, columnspan=2, pady=5)
Button(frame_connexion, text="STOP", command=lambda: stop_acquisition()).grid(row=3, column=0, columnspan=2, pady=5)
icone_acquisition = Label(frame_connexion, text="Icône acquisition en cours", bg="grey", width=20)
icone_acquisition.grid(row=4, column=0, columnspan=2, pady=5)

# Zone "Mouvement du robot"
Label(frame_mouvement, text="Mouvement du robot").grid(row=0, column=0, columnspan=2, pady=5)

# Graphique de la vitesse linéaire et angulaire
fig_vitesse = plt.Figure(figsize=(5, 2.5), dpi=100)
ax_vitesse = fig_vitesse.add_subplot(111)
ax_vitesse.set_title("Vitesse Linéaire et Angulaire")
ax_vitesse.set_ylim(-1, 1)
canvas_vitesse = FigureCanvasTkAgg(fig_vitesse, master=frame_mouvement)
canvas_vitesse.get_tk_widget().grid(row=1, column=0, columnspan=2, pady=5)

# Graphique de la position relative
fig_position = plt.Figure(figsize=(5, 2.5), dpi=100)
ax_position = fig_position.add_subplot(111)
ax_position.set_title("Position Relative")
ax_position.set_xlim(-10, 10)
ax_position.set_ylim(-10, 10)
canvas_position = FigureCanvasTkAgg(fig_position, master=frame_mouvement)
canvas_position.get_tk_widget().grid(row=2, column=0, columnspan=2, pady=5)

# Zone "Commande"
Label(frame_commande, text="Commande").grid(row=0, column=0, columnspan=2, pady=5)
Button(frame_commande, text="Avancer", command=lambda: control_robot("avancer")).grid(row=1, column=0, columnspan=2, pady=5)
Button(frame_commande, text="Pivoter vers la gauche", command=lambda: control_robot("pivoter_gauche")).grid(row=2, column=0, pady=5)
Button(frame_commande, text="Pivoter vers la droite", command=lambda: control_robot("pivoter_droite")).grid(row=2, column=1, pady=5)
Button(frame_commande, text="Reculer", command=lambda: control_robot("reculer")).grid(row=3, column=0, columnspan=2, pady=5)

slider_vitesse_angulaire = Scale(frame_commande, from_=0, to=100, orient=HORIZONTAL)
slider_vitesse_angulaire.grid(row=4, column=0, pady=5)

slider_vitesse_lineaire = Scale(frame_commande, from_=0, to=100, orient=HORIZONTAL)
slider_vitesse_lineaire.grid(row=4, column=1, pady=5)

Label(frame_commande, text="Vitesse Angulaire").grid(row=5, column=0, pady=5)
Label(frame_commande, text="Vitesse Linéaire").grid(row=5, column=1, pady=5)

# Fonction pour démarrer l'acquisition des données
def start_acquisition():
    global recevoir_donnees
    recevoir_donnees = True
    icone_acquisition.config(bg="green")
    thread = threading.Thread(target=update_graph)
    thread.daemon = True
    thread.start()

# Fonction pour stopper l'acquisition des données
def stop_acquisition():
    global recevoir_donnees
    recevoir_donnees = False
    icone_acquisition.config(bg="grey")
    reset_position()

# Réinitialiser la position relative
def reset_position():
    ax_position.cla()
    ax_position.set_title("Position Relative")
    ax_position.set_xlim(-10, 10)
    ax_position.set_ylim(-10, 10)
    ax_position.plot([0], [0], 'ro')  # Placer le robot à la position (0,0)
    canvas_position.draw()

# Mise à jour des graphiques
def update_graph():
    global ax_vitesse, ax_position, canvas_vitesse, canvas_position
    while recevoir_donnees:
        # Simulation des nouvelles données pour la vitesse
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        ax_vitesse.cla()
        ax_vitesse.plot(x, y, label="Vitesse Linéaire")
        ax_vitesse.plot(x, np.cos(x), label="Vitesse Angulaire")
        ax_vitesse.legend()
        canvas_vitesse.draw()
        
        # Simulation des nouvelles données pour la position
        ax_position.cla()
        ax_position.set_title("Position Relative")
        ax_position.set_xlim(-10, 10)
        ax_position.set_ylim(-10, 10)
        ax_position.plot(np.random.rand(10) * 20 - 10, np.random.rand(10) * 20 - 10, 'o')
        canvas_position.draw()
        
        time.sleep(0.5)

# Contrôle du robot
def control_robot(action):
    if action == "avancer":
        print("Avancer")
    elif action == "pivoter_gauche":
        print("Pivoter vers la gauche")
    elif action == "pivoter_droite":
        print("Pivoter vers la droite")
    elif action == "reculer":
        print("Reculer")

# Lancement de la boucle principale
fenetre.mainloop()
