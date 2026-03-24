I - Présentation globale du projet :

Naissance de l'idée
Pour ce qui est de la naissance de l'idée, en apprenant le sujet du concours qui serait la biodiversité, on a tout de suite 
voulu faire un jeu.  
Au début, on pensait à un jeu de gestion de construction de ville, mais en y réfléchissant, on s'est dit :  
« Et si on faisait un jeu sarcastique sur le réchauffement climatique ? »

Notre professeur a immédiatement accroché et on s'est lancé dans le projet.

Problématique initiale :

Notre problématique initiale, et qui est restée la même tout au long du projet, est la suivante :  
« Comment faire en sorte de faire vivre une expérience vidéoludique à un jeu de façon interactive sans que cela devienne 
redondant dans la forme ? »

Objectifs :
Dès le début du projet, nos objectifs étaient clairs : nous voulions faire un jeu où le but serait de détruire la planète et 
qu'à la fin, il y ait un message moral pour empêcher que cela se passe dans la vraie vie.

Nos objectifs étaient :

* Faire en sorte que le joueur s'amuse  
* Faire en sorte de faire passer un message clair  
* Être assez beau visuellement avec un style pixel art  
* Avoir un système de statistiques avec des jauges et des pouvoirs  
* Avoir une dégradation continue des jauges

II - Organisation du projet :

Présentation de l'équipe : 

* Arthur Le Guludec
* Noah Debailleux
* Leana Weber
* Leweline Collin-Montron

Rôle de chaque membre en répartition des tâches :

Arthur — Programmeur principal, compositeur musical et administrateur GitHub

* Programmation du hub, de l’introduction et de l’écran de fin de jeu
* Conception et implémentation du système de sauvegarde à l’aide d’un fichier texte
* Création des formules d’interaction entre les différentes jauges du jeu
* Développement des effets de glitch et du plan final avec les phrases de conclusion
* Mise en place et gestion du dépôt GitHub du projet
* Création et intégration du système de responsive pour l’interface
* Développement du module d’aide pour les interfaces utilisateur (ui_tools.py)
* Composition de la musique du hub, de la musique de fin et de certains bruitages
* Participation à la réalisation de la vidéo de présentation

Noah — Programmeur gameplay, graphiste et sound designer

* Programmation de la grille principale du jeu
* Programmation du système de jauges
* Implémentation de la propagation récursive des flammes et des cases polluées
* Développement d’une partie des effets météorologiques
* Création des sprites des cases et des jauges
* Conception de bruitages liés à la grille et aux interactions du joueur
* Gestion du système de sauvegarde des données d’une partie terminée via le fichier save.py
* Participation aux tests et à l’équilibrage du gameplay

Léana — Programmeuse gameplay, graphiste, compositrice et directrice artistique

* Conception et programmation des pouvoirs du joueur et de leurs effets
* Développement d’une partie des effets météorologiques
* Création des sprites des pouvoirs et de leur apparition dans le jeu
* Création des sprites des boutons de pouvoirs et de leur logique d’interaction
* Conception des logos et effets visuels liés à l’activation des pouvoirs
* Création des sprites du hub et de l’introduction
* Supervision de la direction artistique globale du jeu
* Composition d’une partie des éléments musicaux du jeu

Leweline — Programmeuse interface et graphiste

* Développement du menu principal “Start Game”
* Programmation de l’interface de pause permettant de quitter une partie
* Création et gestion du système de notifications
* Programmation de l’affichage des notifications en jeu
* Création des sprites liés aux effets météorologiques
* Composition de la musique du jeu principal
* Développement et gestion du chronomètre de jeu
* Participation à la création et à l’intégration d’éléments d’interface

Temps passé sur le projet :

Environ 5 semaines, soit à peu près 320 heures de travail en comptant le développement du programme ainsi que l’ensemble 
des fichiers et ressources associés.

III - Présentation des étapes du projet

Notre première idée était un jeu de gestion qui ressemblait un peu à un jeu de création de ville. Mais finalement on a 
préféré partir sur une sorte de simulation de réchauffement climatique.

On a ensuite imaginé la structure de notre jeu avec :

* Une intro avec le logo de notre groupe
* Un hub pour pouvoir lancer le jeu, afficher les stats de partie et les crédits
* Un menu Start avec toutes les règles du jeu et le rôle du joueur
* Une partie de jeu constituée d'une grille interactive, de jauges, de boutons de pouvoirs et d'une zone de notification 
qui donnera un peu de vie au monde
* Un écran de fin de jeu avec l'affichage de statistiques de la partie
* Un plan philosophique avec une morale à la fin

Après avoir structuré le jeu nous avons tous commencé à coder et à designer nos parties de code respectives.

IV - Validation de l’opérationnalité du projet / de son fonctionnement

Etat d’avancement du projet au moment du dépôt :

Au moment du dépôt, le jeu est pratiquement fini, en effet on a réussi à incrémenter la plupart des éléments qu'on avait 
prévus. Nous avons aussi ajouté entre temps un système de météo pour plus de vie qu'on n'avait pas prévu au début du 
projet. Néanmoins il manque tout de même certains éléments comme des pouvoirs, ou même de meilleurs éléments de gameplay pour 
que le jeu soit plus plaisant.

Approches mises en œuvre pour vérifier l’absence de bugs :

Notre approche pour détecter rapidement et efficacement les "effets de bord", soit les bugs, a été de contrôler intégralement 
le jeu après chaque ajout. Utilisant GitHub, nous avons notamment pu revenir dans une version antérieure si un bug nous 
bloquait trop. Et les vérifications se faisaient après chaque commit dans GitHub. Et pour les "effets de bord", après chaque 
ajout nous testons tous le jeu dans les moindres détails pour être sûrs que chaque ajout convient bien avec la structure du jeu.

Difficultés rencontrées et les solutions apportées :

Nous avons rencontré plusieurs difficultés dans la création de notre jeu notamment :

* La gestion de la responsive, en effet nous avons commencé à coder dans notre lycée soit sur des écrans ayant une résolution 
de 1920 x 1080 mais chez nous, la plupart des membres du groupe avaient des écrans de PC portable donc avec une résolution 
plus faible (1366 x 768). Ce qui faisait que les éléments du jeu étaient complètement décalés. On a finalement réussi à régler 
le problème mais pas sans mal car nous n'avions pas les connaissances dans le domaine de la responsive pygame. On a 
donc effectivement remplacé dans le jeu les pixels x, y, l, h par des ratios convertis grâce à une classe resp.py

* La gestion des animations et frames. En effet il était assez difficile pour nous au début de bien incrémenter et comprendre 
le système de frame et de "Delta" pour que chaque animation s'adapte au nombre d'FPS du système. Notre structure n'a surtout 
pas été créée pour ça car on initialise les éléments graphiques dans des dictionnaires dans la méthode spéciale __init__, ce 
qui fait qu'on devait faire en sorte de modifier un attribut d'une classe héritée, notamment les classes UI_PNG et 
UI_screen présentes dans ui_tools.py

* L'optimisation des performances. Effectivement, après avoir beaucoup avancé dans notre projet, nous avons remarqué que les 
FPS du jeu chutaient énormément notamment à cause des animations. On a réussi à trouver la solution qui était de ne pas 
charger les images dans pygame à chaque frame d'animation, mais de toutes les charger dans une liste au début du programme 
et ensuite à chaque frame les interchanger avec un indice de la liste.

* La propagation responsive du feu et des cases polluées. Ce problème nous a demandé un moment de recherche pour trouver 
une solution mais c'est finalement en nous replongeant dans nos cours de NSI qu'on a trouvé la solution. En effet notre 
fonction de propagation est récursive ce qui veut dire que la propagation du feu par exemple se fait d'un coup. Mais 
visuellement ce n'est pas beau, on voulait que le feu se propage progressivement. On a donc utilisé une file. En effet on 
a transformé notre fonction récursive en fonction "semi-récursive". Alors au lieu d'appeler directement la fonction dans 
elle-même sans pouvoir la ralentir, on va stocker les appels de celle-ci dans une file et grâce à une fonction Update, on arrive 
à appeler les appels à un instant t progressivement.

V - Ouverture

Idées d'amélioration du projet :

* Notre projet peut s'améliorer dans beaucoup de domaines. Déjà dans la gestion de l'affichage des éléments graphiques. En 
effet notre système marche assez bien pour un plan ou un programme avec peu d'éléments à l'écran mais on s'est rendu compte 
que pour la classe Jeu, le nombre de dictionnaires et leur taille pour l'affichage d'éléments graphiques devenaient 
ingérables. Une amélioration pourrait donc être apportée dans la gestion des éléments graphiques ainsi que leur stockage

* De meilleurs graphiques. En effet même en faisant de notre mieux, certains graphiques sont tout de même assez rustiques et 
c'est un point que l'on peut améliorer pour rendre le jeu visuellement plus agréable. Notamment avec les effets graphiques de 
la météo

* L'ajout de meilleurs éléments de gameplay, pour rendre le jeu plus agréable à jouer et pour ajouter de la rejouabilité.

* Nous avons pensé aussi à une amélioration en rapport avec la rejouabilité, il s'agit d'un système de succès. Cela permettrait 
au joueur de jouer plusieurs parties et d'avoir des défis à relever.

* Ajout d'autres pouvoirs et d'amélioration de pouvoirs. Effectivement nous avons l'idée de prochainement ajouter plus de 
pouvoirs et un système d'amélioration pour rendre le jeu plus attractif et augmenter la durée de vie de celui-ci.

Analyse critique :

Dans l'ensemble nous sommes assez contents de notre projet, on a réussi à ajouter presque l'intégralité des fonctionnalités 
que l'on voulait. Néanmoins il reste tout de même des faiblesses assez conséquentes, comme par exemple la structure du code ou
même la mauvaise optimisation des fonctions utilisées. Notre code est assez bien mais aussi moyennement compréhensible à 
certains endroits. Il est aussi un peu redondant dans sa structure.

Compétences personnelles développées :

Nous avons tous appris énormément de choses pendant ce projet :

* L'utilisation et le fonctionnement de GitHub. Personne dans l'équipe ne savait utiliser de source control. On a dû apprendre 
le fonctionnement de Git et aussi de GitHub. Et nos compétences dans ce domaine se sont grandement améliorées.

* Le fonctionnement et comment créer un jeu vidéo. En effet, nous avions déjà expérimenté des logiciels comme Scratch, la 
création d'un jeu aussi conséquent nous a permis de comprendre et de bien utiliser les méthodes de création de jeu. Comme 
par exemple la boucle et le concept de Draw -> Update -> Draw.

* Nos compétences en programmation orientée objet et en récursivité se sont aussi notamment améliorées. Nous avons créé et 
utilisé beaucoup de classes. Nous avons aussi compris le système d'héritage de classe et d'importation de fichier Python 
externe dans un autre fichier.

* Nous avons aussi développé beaucoup de compétences dans le domaine de la musique ou de la création graphique pour faire 
les assets du jeu.

Démarche d'inclusion :

Nous avons essayé de rendre notre jeu accessible au plus grand nombre. L’interface a été conçue pour être claire et 
intuitive grâce à l’utilisation d’icônes, de notifications et d’un hub permettant de comprendre rapidement les mécaniques du 
jeu. De plus, un système de responsive interface a été développé afin que le jeu s’adapte à différentes tailles d’écran et 
résolutions. Ces choix permettent à des joueurs ayant différents niveaux d’expérience avec les jeux vidéo de comprendre 
et d’utiliser le jeu plus facilement. Nous avons aussi généralisé les chemins de fichier pour permettre d'éviter les bugs 
de lecteur de chemins.

VI - Modalités concernant l'intelligence artificielle et le code non original :

Pour la réalisation de notre projet, nous avons utilisé à la fois l’intelligence artificielle et certaines sources externes 
afin de nous assister dans la création du code.

En ce qui concerne les sources externes, nous n’avons pas utilisé de code provenant de tiers, à l’exception des 
bibliothèques Python standards comme pygame et Pillow. Ces sources nous ont surtout permis de mieux comprendre certains 
concepts inconnus et de les appliquer correctement dans notre projet.

L’intelligence artificielle a également été utilisée, principalement pour nous aider à déboguer certaines parties du code et 
pour proposer des solutions dans la création de quelques fonctionnalités. Nous avons veillé à limiter son utilisation autant 
que possible, et estimons que le code original représente environ 90 % du projet. Soit environ 10% de code aidé par 
intelligence artificielle.

Elle nous a aussi servi pour générer certains éléments graphiques, tels que le logo du jeu et du groupe. Bien entendu, nous 
avons retravaillé ces éléments pour leur donner notre style propre.

Nous avons utilisé quelques spritesheets provenant du site PNGWing, ainsi qu’une image libre de droit issue du site Freepik 
(créée par "kjpargeter") que nous avons pixelisée pour l’adapter au style du jeu.
Nous avons également intégré un sprite de tornade libre de droit, créé par CREASTA PIXEL.

Enfin nous avons utilisé un SFX libre de droit provenant du site Pixabay. Il s'agit du bruitage d'applaudissement à la fin du jeu.
