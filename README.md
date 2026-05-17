# Œstro-gen

- **Nom du groupe** : LGB-Team  

---


## Présentation du projet

**Œstro-gen** est un outil local et offline de génération de contenu pour Visual Novel, combinant plusieurs modèles d’IA afin de créer des personnages, des dialogues et des histoires complètes, exportables directement vers [Ren'Py](https://www.renpy.org/).

Ce projet s’appuie sur [EMF : Easy Model Fusion](https://github.com/easy-model-fusion), qui permet d’installer et d'utiliser plusieurs modèles génératifs (texte, image, musique) en local. Il s'inclut dans le concept du Gamelab. Le but d’un Gamelab est de créer un jeu/application avec un code réutilisable en petit groupe dans une periode définie. Le code issu du projet a pour but d’être réutilisable par de futurs étudiants, qui feront à leur tour une nouvelle version à partir de la nôtre. 

---

### Captures d'écran

**Écran principal d’Œstro-gen**  
A gauche le menu pour choisir le modèle d'IA, ainsi que d'autres réglages liés à la génération.
Au milieu ce trouve l'arbre de dialogue, modifiable par l'utilisateur.
![Fenêtre principale](/images/mainWindow.png)

**Écran principal - Version gestion de personnage**  
A gauche il est possible d'ajouter, supprimer et choisir les images des personnages. Il est possible d'avoir plusieurs images par personnage, pour représenter différentes expressions. A droite ce trouvent les personnages et fonds déjà existants.
![Fenêtre principale](/images/characterWindow.png)


**Fenêtre de dialogue et choix dans Ren’Py**  
![Dialogue dans l’application](/images/dialog.png)  
![Choix dans Ren’Py](/images/renpyscreen.png)

---

## Procédures d'installation et d'exécution

Pour l'installation complète du projet, suivez [ce lien dédié](/releases/oestro-gen_2.0/README.md).

---

## Cahier des charges

- Vous trouverez un [Wiki](https://git.unistra.fr/lgb-team/oestro-gen/-/wikis/home) où vous pourrez trouver toutes les informations relatives au projet Oestrogen :
- L'architecture du projet avec un diagramme UML
- Le cahier des charges
- La structure du projet
- Un changelog
- La procédure d'installation du projet
- Les perspectives d'amélioration que vous pourrez essayer d'implémenter

### Objectifs pédagogiques

- **Utiliser des modèles d’IA générative** : Savoir intégrer et exploiter des modèles d’IA en local pour différents types de contenus.
- **Exporter un projet complet** : Générer un projet Ren’Py à partir d’éléments créés dynamiquement.
- **Concevoir une application créative** : Offrir un outil utilisable par des créateurs de Visual Novel, sans compétences techniques.

#### Objectifs pédagogiques avancés

- **Travailler en équipe sur un projet modulaire** : Créer un logiciel avec des composants réutilisables et facilement modifiables par d’autres groupes.
- **Assurer une expérience totalement offline** : Aucun besoin de connexion Internet pour générer du contenu grâce à l’installation locale des modèles IA.

#### Références

- [Ren'Py](https://www.renpy.org/)
- [EMF - Easy Model Fusion](https://github.com/easy-model-fusion)

---

## Description des fonctionnalités

### Simulation

Le système permet la génération automatique de :

- personnages (visuels et caractéristiques)
- dialogues interactifs avec choix multiples
- scénarios de base

### Interface

- Studio de création de personnages
- Studio d’écriture de dialogues et de choix
- Interface principale pour organiser le contenu

### Actions de l’utilisateur

- Écrire des prompts pour générer du contenu
- Sélectionner et éditer les résultats générés
- Exporter le projet final au format compatible Ren’Py

---

## Scénarios

Un exemple de scénario utilisateur :

1. Lancer l’application Œstro-gen
2. Rédiger un prompt pour générer un personnage
3. Rédiger un prompt pour une scène narrative
4. Ajouter des choix pour le joueur
5. Exporter vers Ren’Py
6. Lancer le jeu dans Ren’Py

---

## Contraintes de développement

- Fonctionner entièrement hors-ligne
- Être basé sur EMF
- Rendre les composants facilement réutilisables pour d’autres groupes

---

## Fonctionnalités et scénarios avancés

- Gestion de la cohérence narrative entre scènes
- Génération conditionnelle selon les choix du joueur
