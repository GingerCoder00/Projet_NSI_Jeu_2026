# Projet : Let's Break Down The Earth
# Auteurs : ARTHUR LE GULUDEC, NOAH DEBAILLEUX, LEANA WEBER, LEWELINE COLLIN--MONTRON

import os

# Fonction qui charge les meilleurs scores depuis un fichier texte
def load_best_score_from_file():

        # Chemin vers le fichier contenant les meilleurs scores
        score_PATH = os.path.join(os.path.dirname(__file__), "best_score.txt")

        # Liste qui va stocker les valeurs récupérées
        best_score_file = []

        # Si le fichier n'existe pas, on retourne None
        if not os.path.exists(score_PATH):
            return None

        # Ouverture du fichier en lecture
        with open(score_PATH, "r") as f:

            # Lecture ligne par ligne
            for line in f:

                # On vérifie que la ligne contient bien une donnée du type "clé=valeur"
                if "=" in line:

                    # On récupère la valeur après le "="
                    value = line.strip().split("=")[1]

                    # Conversion de la valeur en nombre
                    # Si la valeur contient un ".", on suppose que c'est un float
                    try:
                        if "." in value:
                            best_score_file.append(float(value))
                        else:
                            best_score_file.append(int(value))

                    # En cas d'erreur de conversion, on ajoute 0 par défaut
                    except ValueError:
                        best_score_file.append(0)

        # Retour de la liste contenant tous les scores
        return best_score_file

# Liste des phrases affichées au début du jeu pour expliquer les règles
PHRASES_AIDE_START = [
    "RÈGLE DU JEU : Vous incarnez une méga corporation n'ayant que pour seul but d'engranger plus de profit, même si cela détruit la planète ! Vous devez être le plus rapide pour faire régner le capitalisme !",
    "Vous trouverez des jauges représentant plusieurs caractéristiques de la planète en temps réel ! Chaque taux sera compris entre 1 et 100.",
    "Vous aurez aussi à disposition plusieurs pouvoirs pour accroître votre empire économique ! Certains peuvent être posés sur la grille.",
    "Tandis que d'autres, comme par exemple la guerre commerciale, sont des pouvoirs immédiats qui n'ont pas besoin d'être posés sur la grille."
]

# Liste de phrases de désinformation affichées aléatoirement
PHRASES_DESINFORMATION = [
    "Les scientifiques confirment que tout va bien.",
    "Les feux actuels sont totalement naturels.",
    "La hausse des températures est un phénomène cyclique.",
    "Les usines améliorent la biodiversité locale.",
    "Les médias exagèrent la situation.",
    "Aucune preuve d'un lien entre pollution et climat.",
    "Les experts sont divisés sur la question.",
    "Les incendies stimulent la croissance économique.",
    "Tout est sous contrôle selon les autorités.",
    "Les citoyens soutiennent massivement les industries.",
    "Des études montrent que le réchauffement climatique est complètement absurde.",
    "Les scientifiques disent tous que notre planète se porte à merveille."
]

# Liste de messages affichés lorsque le joueur utilise un pouvoir
PHRASES_POUVOIR = [
    "Vous ne pouvez pas incendier ici...",
    "Vous ne pouvez pas construire une usine ici...",
    "Vous ne pouvez reverser malencontreusement du pétrole que dans l'eau.",
    "Malheureusement, vous n'avez pas assez de profit.",
    "Vous devez attendre avant de réutiliser ce pouvoir.",
    "Un incendie s'est déclaré dans la région.",
    "Une nouvelle usine est construite.",
    "Du pétrole est déversé dans la mer.",
    "Une guerre commerciale avec une entreprise voisine a commencé.",
    "Une grande vague de chaleur s'abat sur la région."
]

# Liste d'événements météorologiques pouvant apparaître dans le jeu
PHRASES_METEO = [
    "Une pluie battante s'abat sur la région.",
    "Une chaleur étouffante envahit la région.",
    "Un froid glacial recouvre la région d'un voile de givre.",
    "Un violent orage éclate, le tonnerre gronde et les éclairs frappent le sol.",
    "Une tornade dévastatrice traverse la région en arrachant tout sur son passage.",
    "Une montée brutale des eaux submerge les terres les plus basses.",
    "Un vaste programme de reforestation redonne vie aux forêts.",
    "Des écologistes interviennent pour limiter les dégâts environnementaux...",
    "Une sécheresse ciblée assèche certaines zones stratégiques.",
    "Une épidémie se propage rapidement et fragilise la population.",
    "Une météorite s'écrase violemment, laissant un cratère fumant."
]

# Messages affichés à la fin du jeu
PHRASES_FIN_DE_JEU = [
    "Vous avez détruit la Terre.",
    "Ce n'était qu'un jeu… mais pourquoi ce plaisir ?",
    "Chaque décision semblait naturelle.",
    "Détruire est plus simple que construire.",
    "Dans ce monde virtuel, personne ne souffre.",
    "Mais vous… ressentez-vous quelque chose ?",
    "Un léger malaise. Un frisson.",
    "Vous avez gagné.",
    "Éteignez l'écran. Regardez autour de vous.",
    "Respirez… et demandez-vous :",
    "Dans quel monde jouez-vous vraiment ?",
    "D'ailleurs, le secret est : 'CAPITALISME'"
]

# Messages affichés dans le hub (menu principal du jeu)
def get_phrases_hub():
    '''Recharge les scores depuis le fichier à chaque appel'''
    best_score = load_best_score_from_file()

    if best_score is None:
        score_texte = "Aucun score enregistré pour le moment."
    else:
        score_texte = (
            f"Meilleur Temps : {best_score[0]}\n\n",
            f"Meilleur Nombre d'incendies déclarés : {best_score[1]}\n\n",
            f"Meilleur Nombre de cases polluées : {best_score[2]}\n\n",
            f"Meilleur Nombre d'arbres brûlés : {best_score[3]}\n\n",
            f"Meilleur Nombre d'usines créées : {best_score[4]}\n\n",
            f"Meilleur Nombre de désinformations créées : {best_score[5]}\n\n",
            f"Meilleur Nombre de guerres déclarées : {best_score[6]}",
        )

    return [
        "Jeu développé par le groupe NATURE.EXE, constitué d'Arthur, Noah, Léana et Leweline dans le cadre des Trophées de NSI 2026 !",
        "Le saviez-vous ? Ce jeu n'est qu'une critique des méga-corporations !",
        score_texte
    ]
