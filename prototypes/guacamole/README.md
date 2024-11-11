# Guacamole


## Installation
### Dépendances : 
Ce prototype nécessite EMF-CLI, suivez les instructions d'installation via ce lien : [Lien vers EMF-CLI](https://easy-model-fusion.github.io/docs/installation.html)

Lien vers le github :  [EMF : Easy Model Fusion](https://github.com/easy-model-fusion)


### Mettre en place EMF-CLI

Une fois EMF-CLI installé et le prototype téléchargé, effectuez la commande suivante dans le dossier du prototype :
```
emf-cli install
```
Une fois que emf-cli a télécharger les modules nécéssaire au bon fonctionnement du prototype, vous n'avez plus qu'à lancer l'éxécutable main.py avec la commande :
(pour Windows):
```
.\venv\Scripts\python.exe main.py
```
(Pour linux)
```
./.venv/bin/python main.py
```


### Mise en place du launcher automatisé 

Ouvrir AppLauncher.bat 

```
@echo off
cmd /k "cd /d C:\Users\username\Desktop\oestro-gen\prototypes\guacamole\.venv\Scripts & .\activate & cd /d C:\Users\username\Desktop\oestro-gen & python .\main.py"
``` 

Remplacez le chemin d'accés par le votre.
Faite un clique droit sur le fichier AppLauncher.bat et faite "Creer un raccourci"
Deplacez le raccourci sur le bureau
Les proprietes du raccourci devrait être : 

Target: ```C:\Users\username\Desktop\oestro-gen\prototypes\guacamole\AppLauncher.bat``` 

Start In: ```C:\Users\username\Desktop\oestro-gen\prototypes\guacamole```

Shortcut Key: None

Start In: Normal Window


![Logo Guacamole](/prototypes/guacamole/images/guacamole.png) 
