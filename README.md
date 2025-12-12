  Chalange triple A
               Dashboard de Monitoring 



Ce projet est un dashboard de monitoring système qui collecte et affiche des informations en temps réel sur l'état d'un serveur ou d'une machine. Il utilise Python pour la collecte des données système et génère une page HTML statique mise à jour dynamiquement





## Prérequis
- Python 3.7+ installé sur le système
- pip (gestionnaire de paquets Python)
- psutil 
- Système d'exploitation : Linux
- distro 
## Installation

Cloner le repository :
```bash
git clone https://github.com/prenom-nom/AAA.git
cd AAA
```

Installer les dépendances Python :
```bash
pip install psutil 
pip freeze 
pip install distro
```

## Utilisation

Lancer le script de monitoring :
```bash
python monitor.py
```
Le script va :
1. Collecter les données système
2. Générer le fichier index.html
3. Afficher un message de confirmation

### Visualiser le dashboard

**Option 1 - Double-clic sur le fichier**
- Ouvrez le dossier du projet
- Double-cliquez sur index.html

**Option 2 - Ligne de commande**
```bash
# Linux/macOS
open index.html

# Windows
start index.html
```

### Actualisation automatique

Pour mettre à jour le dashboard toutes les 60 secondes :

**Linux/macOS :**
```bash
watch -n 60 python monitor.py
```

**Windows PowerShell :**
```bash
while($true) { python monitor.py; Start-Sleep -Seconds 60 }
```

**Ou manuellement :**
- Relancez `python monitor.py`
- Cliquez sur "Actualiser" dans le navigateur

## Fonctionnalités
- Collecte de données système en temps réel
- Interface responsive et moderne
- Mise à jour automatique
- Indicateurs visuels colorés
- Export des données possible

## Captures d'écran
Voir le dossier screenshots/ pour les captures terminal.png et index.png
![organisation](https://github.com/rayenelabed-r-it/Challenge-Triple-A/blob/main/screenshot/organisation.png)
![planing](https://github.com/rayenelabed-r-it/Challenge-Triple-A/blob/main/screenshot/planning.png)
![zonning](https://github.com/rayenelabed-r-it/Challenge-Triple-A/blob/main/screenshot/zooning.png)
![wireframe](https://github.com/rayenelabed-r-it/Challenge-Triple-A/blob/main/screenshot/WIREFRAMe%20(2).png)
![page_index](https://github.com/rayenelabed-r-it/Challenge-Triple-A/blob/main/screenshot/page_index.png)

## Difficultés rencontrées
- Optimisation du rafraîchissement des données
- creation de la jauge en css 

## Améliorations possibles
- Ajout de graphiques historiques
- Notifications en cas de seuils dépassés
- Mode sombre/clair


## Auteur
LABED Rayene 
MAHAMOUD  Mohamed 
GUIRADO jean pierre 

