# Projet : Let's Break Down The Earth
# Auteurs : ARTHUR LE GULUDEC, NOAH DEBAILLEUX, LEANA WEBER, LEWELINE COLLIN--MONTRON

import os

def load_best_score_from_file():
        score_PATH = os.path.join(os.path.dirname(__file__), "best_score.txt")
        best_score_file = []

        if not os.path.exists(score_PATH):
            return None

        with open(score_PATH, "r") as f:
            for line in f:
                if "=" in line:
                    value = line.strip().split("=")[1]

                    # Convertir en float si c'est un nombre décimal, sinon en int
                    try:
                        if "." in value:
                            best_score_file.append(float(value))
                        else:
                            best_score_file.append(int(value))
                    except ValueError:
                        best_score_file.append(0)  # valeur par défaut en cas de problème

        return best_score_file

best_score = load_best_score_from_file()

PHRASES_AIDE_START = [
    "RÈGLE DU JEU : Vous incarnez une méga corporation n'ayant que pour seul but d'engranger plus de profit, même si cela détruit la planète ! Vous devez être le plus rapide pour faire régner le capitalisme !",
    "Vous trouverez des jauges représentant plusieurs caractéristiques de la planète en temps réel ! Chaque taux sera compris entre 1 et 100.",
    "Vous aurez aussi à disposition plusieurs pouvoirs pour accroître votre empire économique ! Certains peuvent être posés sur la grille.",
    "Tandis que d'autres, comme par exemple la guerre commerciale, sont des pouvoirs immédiats qui n'ont pas besoin d'être posés sur la grille."
]

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
    "Dans quel monde jouez-vous vraiment ?"
]

PHRASES_HUB = [
    "Jeu développé par le groupe NATURE.EXE, constitué d'Arthur, Noah, Léana et Lewiline dans le cadre des Trophées de NSI 2026 !",
    "Le saviez-vous ? Ce jeu n'est qu'une critique des méga-corporations !",
    f"""Meilleur Temps : {best_score[0]} \n \n Meilleur Nombre d'incendies déclarés : {best_score[1]} \n \n Meilleur Nombre de cases polluées : {best_score[2]} \n \n Meilleur Nombre d'arbres brûlés : {best_score[3]} \n \n Meilleur Nombre d'usines créées : {best_score[4]} \n \n Meilleur Nombre de désinformations créées : {best_score[5]} \n \n Meilleur Nombre de guerres déclarées : {best_score[6]}"""
]