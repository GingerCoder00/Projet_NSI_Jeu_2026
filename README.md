# Let's Break Down The Earth
### *Projet Trophées NSI 2026 — Nature.EXE*

> Création d'un jeu vidéo pour le concours Trophées NSI 2026 sur le thème de la **biodiversité**.  
> 📁 Repository : `Projet_Trophees_NSI_2026`

---

## Lancement du jeu

Dans le dossier, vous pouvez soit lancer le jeu via l'exécutable, ce qui permet de tester le jeu sans rien avoir à installer. Si vous voulez tester des parties **distinctes** du programme, il faudra installer la bonne version de Python ainsi que les bonnes dépendances.

### Prérequis

| Élément | Détail |
|---------|--------|
| **Python** | 3.10 à 3.12 — recommandé : **Python 3.11** |
| **Dépendances** | `pip install -r requirements.txt` |

### Lancement
```bash
# Lancement complet via un fichier Python (depuis le dossier Source/)
cd Source
python main.py

# Lancement complet via l'exécutable
"Let's Break Down The Earth.exe"
```

| Module | Fichier | Description |
|--------|---------|--------------|
| Hub | `hub.py` | Écran d'accueil principal |
| Intro | `intro.py` | Séquence d'introduction |
| Jeu | `game.py` | Partie principale |
| Menu | `start_game.py` | Tutoriel et infos avant le jeu |
| Fin | `endgame.py` | Scène de fin de jeu |

---

## 🗂️ Structure du projet
```
📁 Projet_NSI_Jeu_2026/
│
├── presentation.md
├── Let's Break Down The Earth.exe
├── logo_jeu.ico
├── sitotheque.txt
├── LICENSE.md
├── README.md
├── résumé_Projet.txt
├── requirements.txt
├── .gitignore
│
└── 📁 Sources/
    ├── animation.py
    ├── best_score.txt
    ├── case_brulee.py
    ├── condamne.py
    ├── data.py
    ├── dico_info_game.py
    ├── endgame.py
    ├── flamme.py
    ├── game.py
    ├── grille.py
    ├── hub.py
    ├── intro.py
    ├── jauge.py
    ├── main.py
    ├── meteo.py
    ├── notification.py
    ├── phrases_notif.py
    ├── pollue.py
    ├── pouvoir.py
    ├── resp_tools.py
    ├── save.py
    ├── start_game.py
    ├── ui_tools.py
    ├── usine.py
    ├── 📁 font/
    ├── 📁 sound/
    └── 📁 sprite/
```

---

## Description

**Let's Break Down The Earth** est un jeu vidéo **pixel art** développé en Python avec Pygame.  
Le joueur incarne le destructeur de la planète : polluez, brûlez, déchaînez des catastrophes météorologiques...  
Un message moral vous attend à la fin.

> *« Et si je faisais un jeu sarcastique sur le réchauffement climatique ? »*

---

## Fonctionnalités

| Fonctionnalité | Fichier(s) |
|----------------|-----------|
| Grille interactive avec propagation des flammes | `flamme.py` |
| Cases polluées et condamnées | `pollue.py` · `condamne.py` · `case_brulee.py` |
| Jauges avec dégradation continue | `jauge.py` |
| Pouvoirs du joueur avec effets visuels | `pouvoir.py` |
| Effets météorologiques dynamiques | `meteo.py` |
| Système de notifications en jeu | `notification.py` · `phrases_notif.py` |
| Sauvegarde des données de partie | `save.py` · `best_score.txt` |
| Interface responsive multi-résolutions | `resp_tools.py` |
| Animations optimisées | `animation.py` |
| Musique et effets sonores | `sound/` |
| Sprites pixel art | `sprite/` |

## Compatibilité Python

| Version | Statut |
|---------|--------|
| Python 3.10 | ✅ Compatible |
| Python 3.11 | ⭐ Recommandé (optimal) |
| Python 3.12 | ✅ Compatible |
| Python 3.13+ | ❌ Non testé, non recommandé |

---

## 🏆 Crédits

- **Sprites** — PNGWing · Freepik (*kjpargeter*) · CREASTA PIXEL
- **SFX applaudissement** — Pixabay
- **Logo** — Généré par IA, retravaillé par l'équipe

---

*Projet réalisé en ~**8 semaines** — **320 heures** de travail — NSI 2026* 🏅
