
   LET'S BREAK DOWN THE EARTH - Projet NSI 2026


Repository : Projet_NSI_Jeu_2026
Creation d'un jeu video pour le concours NSI 2026 sur le theme de la biodiversite.



LANCEMENT DU JEU


Prerequis :
  - Python 3.10 a 3.12 (recommande : Python 3.11)
  - Installer les dependances : pip install -r requirements.txt

Lancement complet :
  python main.py

Lancement par module :
  hub.py          -> Pour le hub
  intro.py        -> Pour l'intro
  game.py         -> Pour le jeu
  start_game.py   -> Pour le menu de tuto et d'infos avant le jeu
  endgame.py      -> Pour la scene de fin de jeu


STRUCTURE DU PROJET


Racine /
  main.py
  presentation.md
  sitotheque.txt
  LICENSE.md
  README.md
  Resume Projet.txt
  requirements.txt
  .gitignore
  .vscode/
  Source/

Dossier Source/
  animation.py
  best_score.txt
  case_brulee.py
  condamne.py
  data.py
  dico_info_game.py
  endgame.py
  flamme.py
  game.py
  grille.py
  hub.py
  intro.py
  jauge.py
  main.py
  meteo.py
  notification.py
  phrases_notif.py
  pollue.py
  pouvoir.py
  resp_tools.py
  save.py
  start_game.py
  ui_tools.py
  usine.py
  __pycache__/
  font/
  sound/
  sprite/



DESCRIPTION


Let's Break Down The Earth est un jeu video en pixel art developpe
en Python avec Pygame. Le joueur incarne le destructeur de la planete :
polluez, brulez, dechainez des catastrophes meteorologiques...
Un message moral vous attend a la fin.

"Et si on faisait un jeu sarcastique sur le rechauffement climatique ?"



FONCTIONNALITES


- Grille interactive avec propagation des flammes (flamme.py)
- Cases polluees et condamnees (pollue.py, condamne.py, case_brulee.py)
- Systeme de jauges avec degradation continue (jauge.py)
- Pouvoirs du joueur avec effets visuels (pouvoir.py)
- Effets meteorologiques dynamiques (meteo.py)
- Systeme de notifications en jeu (notification.py, phrases_notif.py)
- Sauvegarde des donnees de partie (save.py, best_score.txt)
- Interface responsive multi-resolutions (resp_tools.py)
- Animations optimisees (animation.py)
- Musique et effets sonores (sound/)
- Sprites pixel art (sprite/)



EQUIPE


Arthur Le Guludec       - Programmeur principal, compositeur, admin GitHub
Noah Debailleux         - Programmeur gameplay, graphiste, sound designer
Leana Weber             - Programmeuse gameplay, graphiste, directrice artistique
Leweline Collin-Montron - Programmeuse interface, graphiste, compositrice



COMPATIBILITE PYTHON


  Python 3.10  ->  Compatible
  Python 3.11  ->  Recommande (optimal)
  Python 3.12  ->  Compatible
  Python 3.13+ ->  Non teste, non recommande



CREDITS


- Sprites : PNGWing, Freepik (kjpargeter), CREASTA PIXEL
- SFX applaudissement : Pixabay
- Logo : genere par IA puis retravaille par l'equipe

Projet realise en ~5 semaines - 320 heures de travail - NSI 2026