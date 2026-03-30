# Nature.EXE — Présentation du projet

---

## I — Présentation globale

### Naissance de l'idée

En apprenant que le thème du concours serait la **biodiversité**, l'équipe a immédiatement voulu créer un jeu.
L'idée initiale d'un jeu de gestion de ville a rapidement évolué vers une question plus audacieuse :

> *« Et si on faisait un jeu sarcastique sur le réchauffement climatique ? »*

Le professeur a immédiatement accroché, et le projet a démarré.

---

### Problématique

> *« Comment faire en sorte de faire vivre une expérience vidéoludique de façon interactive sans que cela devienne redondant dans la forme ? »*

---

### Objectifs

- Faire en sorte que le joueur s'amuse
- Faire passer un message clair
- Être beau visuellement avec un style **pixel art**
- Avoir un système de statistiques avec des jauges et des pouvoirs
- Avoir une dégradation continue des jauges

---

## II — Organisation du projet

### Présentation de l'équipe

| Membre | Rôle principal |
|--------|---------------|
| **Arthur Le Guludec** | Programmeur principal, compositeur, admin GitHub |
| **Noah Debailleux** | Programmeur gameplay, graphiste, sound designer |
| **Léana Weber** | Programmeuse gameplay, graphiste, directrice artistique |
| **Leweline Collin-Montron** | Programmeuse interface, graphiste |

---

### Répartition des tâches

<details>
<summary><strong>Arthur</strong> — Programmeur principal, compositeur & admin GitHub</summary>

- Programmation du hub, de l'intro et de l'écran de fin
- Système de sauvegarde via fichier texte
- Formules d'interaction entre les jauges
- Effets de glitch et plan final avec phrases de conclusion
- Mise en place et gestion du dépôt GitHub
- Système de responsive interface
- Module d'aide UI (`ui_tools.py`)
- Composition de la musique du hub, de fin, et de certains bruitages
- Participation à la vidéo de présentation

</details>

<details>
<summary><strong>Noah</strong> — Programmeur gameplay, graphiste & sound designer</summary>

- Programmation de la grille principale
- Système de jauges
- Propagation récursive des flammes et cases polluées
- Effets météorologiques (partie)
- Sprites des cases et des jauges
- Bruitages liés à la grille et aux interactions
- Gestion de la sauvegarde via `save.py`
- Tests et équilibrage du gameplay

</details>

<details>
<summary><strong>Léana</strong> — Programmeuse gameplay, graphiste, compositrice & DA</summary>

- Conception et programmation des pouvoirs et de leurs effets
- Effets météorologiques (partie)
- Sprites des pouvoirs, boutons et logos associés
- Sprites du hub et de l'introduction
- Supervision de la direction artistique globale
- Composition d'éléments musicaux

</details>

<details>
<summary><strong>Leweline</strong> — Programmeuse interface & graphiste</summary>

- Menu principal "Start Game"
- Interface de pause
- Système de notifications et leur affichage en jeu
- Sprites des effets météorologiques
- Composition de la musique du jeu principal
- Chronomètre de jeu

</details>

---

### Temps passé

> Environ **5 semaines**, soit approximativement **320 heures** de travail au total (développement + ressources associées).

---

## III — Étapes du projet

La structure finale du jeu comprend :

1. **Intro** — Logo du groupe
2. **Hub** — Lancer le jeu, voir les stats et les crédits
3. **Menu Start** — Règles du jeu et rôle du joueur
4. **Partie** — Grille interactive, jauges, pouvoirs, zone de notifications
5. **Écran de fin** — Statistiques de la partie
6. **Plan philosophique** — Morale finale

---

## IV — Validation et fonctionnement

### État d'avancement au moment du dépôt

Le jeu est **pratiquement terminé**. La quasi-totalité des fonctionnalités prévues ont été implémentées.
Un système de **météo** a été ajouté en cours de route pour apporter plus de vie, sans avoir été prévu initialement.
Il manque néanmoins quelques pouvoirs et certains éléments de gameplay pour affiner l'expérience.

---

### Approche anti-bugs

- Vérification intégrale du jeu **après chaque ajout**
- Tests approfondis **après chaque commit GitHub**
- Possibilité de revenir à une version antérieure grâce à **Git**

---

### Difficultés rencontrées

| Problème | Solution apportée |
|----------|------------------|
| **Responsive** (résolutions 1920×1080 vs 1366×768) | Remplacement des valeurs px fixes par des **ratios** via une classe `resp.py` |
| **Animations & frames** (système de delta/FPS) | Modification des attributs des classes héritées `UI_PNG` et `UI_screen` |
| **Optimisation des performances** (chute de FPS) | Pré-chargement de toutes les images en liste au démarrage, échange par indice |
| **Propagation du feu** (récursivité trop rapide) | Transformation en fonction "semi-récursive" avec une **file** et une fonction `Update` |

---

## V — Ouverture

### Idées d'amélioration

- Refonte de la gestion des éléments graphiques (dictionnaires trop lourds dans la classe `Jeu`)
- Amélioration des graphismes, notamment les effets météo
- Ajout d'éléments de gameplay pour plus de rejouabilité
- Système de **succès** pour encourager les parties multiples
- Nouveaux pouvoirs et système d'**amélioration de pouvoirs**

---

### Analyse critique

Le projet est globalement satisfaisant : presque toutes les fonctionnalités prévues ont été intégrées.
Les principales faiblesses identifiées sont :

- Structure du code perfectible (redondances, lisibilité)
- Optimisation des fonctions à revoir

---

### Compétences développées

- **GitHub & Git** — Source control appris de zéro
- **Création de jeu vidéo** — Boucle Draw → Update → Draw
- **POO & récursivité** — Classes, héritage, importation de modules
- **Musique & graphisme** — Création d'assets originaux

---

### Démarche d'inclusion

- Interface claire avec **icônes, notifications et hub explicatif**
- Système de **responsive** adapté à différentes résolutions
- **Chemins de fichiers généralisés** pour éviter les bugs multi-OS

---

## VI — IA & Code non original

| Élément | Détail |
|---------|--------|
| **Bibliothèques externes** | `pygame`, `Pillow` uniquement |
| **Code original** | ~**90 %** du projet |
| **Code assisté par IA** | ~**10 %** (débogage et quelques fonctionnalités) |
| **Éléments graphiques IA** | Logo du jeu et du groupe (retravaillés dans notre style) |
| **Sprites tiers** | PNGWing · Freepik (*kjpargeter*, pixelisé) · Tornade par *CREASTA PIXEL* |
| **SFX tiers** | Bruitage d'applaudissement libre de droit — Pixabay |
