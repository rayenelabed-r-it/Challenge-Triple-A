#!/usr/bin/env python3
"""
Script de monitoring système simplifié
Affiche les infos sur le CPU, la RAM, les processus et les fichiers
"""

# === IMPORTS : Bibliothèques nécessaires ===
import psutil        # Pour récupérer les infos système (CPU, RAM, processus)
import platform      # Pour les infos sur l'OS (Windows, Linux, Mac)
import socket        # Pour récupérer le nom de la machine
from datetime import datetime  # Pour afficher les dates et heures
import os            # Pour explorer les fichiers et dossiers


def afficher_cpu():
    """
    Affiche les informations sur le processeur
    - Nombre de cœurs physiques et logiques
    - Fréquence actuelle en MHz
    - Pourcentage d'utilisation
    """
    print("\n" + "="*50)  # Ligne de séparation visuelle
    print("PROCESSEUR")
    print("="*50)
    
    # Récupérer le nombre de cœurs
    # logical=False → cœurs physiques (ex: 4)
    # logical=True → cœurs logiques avec hyperthreading (ex: 8)
    coeurs = psutil.cpu_count(logical=False)
    coeurs_logiques = psutil.cpu_count(logical=True)
    
    # Récupérer la fréquence du CPU
    # Retourne un objet avec .current, .min, .max
    frequence = psutil.cpu_freq()
    
    # Mesurer l'utilisation CPU pendant 1 seconde
    # interval=1 → attend 1 seconde pour avoir une mesure précise
    utilisation = psutil.cpu_percent(interval=1)
    
    # Afficher les résultats
    print(f"Cœurs physiques : {coeurs}")
    print(f"Cœurs logiques : {coeurs_logiques}")
    print(f"Fréquence : {frequence.current:.0f} MHz")  # :.0f = 0 décimale
    print(f"Utilisation : {utilisation}%")


def afficher_memoire():
    """
    Affiche les informations sur la mémoire RAM
    - RAM utilisée et totale en GB
    - Pourcentage d'utilisation
    """
    print("\n" + "="*50)
    print("MÉMOIRE")
    print("="*50)
    
    # Récupérer les infos sur la RAM
    # Retourne un objet avec : .total, .used, .available, .percent
    mem = psutil.virtual_memory()
    
    # Convertir de bytes en GB
    # 1 GB = 1024 MB = 1024² KB = 1024³ bytes
    # Donc on divise par 1024**3 (= 1 073 741 824)
    ram_utilisee = mem.used / (1024**3)
    ram_totale = mem.total / (1024**3)
    
    # Afficher les résultats
    # :.2f = 2 chiffres après la virgule
    print(f"RAM utilisée : {ram_utilisee:.2f} GB")
    print(f"RAM totale : {ram_totale:.2f} GB")
    print(f"Pourcentage : {mem.percent}%")


def afficher_systeme():
    """
    Affiche les informations générales du système
    - Nom de la machine
    - Système d'exploitation et version
    - Date/heure de démarrage
    - Temps écoulé depuis le démarrage (uptime)
    """
    print("\n" + "="*50)
    print("SYSTÈME")
    print("="*50)
    
    # Récupérer le nom de la machine (hostname)
    print(f"Machine : {socket.gethostname()}")
    
    # Récupérer l'OS et sa version
    # platform.system() → "Windows", "Linux", "Darwin" (Mac)
    # platform.release() → "10", "11", "5.15.0-92-generic"
    print(f"OS : {platform.system()} {platform.release()}")
    
    # Récupérer l'heure de démarrage du système
    # psutil.boot_time() → timestamp Unix (secondes depuis 1970)
    # datetime.fromtimestamp() → convertit en date lisible
    demarrage = datetime.fromtimestamp(psutil.boot_time())
    print(f"Démarrage : {demarrage.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Calculer l'uptime (temps écoulé depuis le démarrage)
    uptime = datetime.now() - demarrage
    
    # Extraire jours, heures, minutes
    jours = uptime.days  # Nombre de jours
    heures = uptime.seconds // 3600  # Division entière par 3600 (secondes dans 1h)
    minutes = (uptime.seconds % 3600) // 60  # Reste modulo 3600, puis diviser par 60
    
    # === UTILISATEURS CONNECTÉS ===
    # psutil.users() → retourne la liste des utilisateurs connectés
    # Chaque utilisateur a : .name (nom), .terminal (terminal), .host (machine distante)
    utilisateurs = psutil.users()
    print(f"\nUtilisateurs connectés : {len(utilisateurs)}")
    print(f"Uptime : {jours}j {heures}h {minutes}min")
    
       # Afficher chaque utilisateur
    for user in utilisateurs:
        # Si .host existe et n'est pas vide, l'afficher, sinon afficher "local"
        origine = user.host if user.host else "local"
        print(f"  → {user.name} (depuis {origine})")
    hostname=socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    print (ip_address)
    

def afficher_processus():
    """
    Affiche le top 5 des processus les plus gourmands
    - Triés par utilisation CPU
    - Triés par utilisation mémoire
    """
    print("\n" + "="*50)
    print("TOP 5 PROCESSUS")
    print("="*50)
    
    # Créer une liste vide pour stocker tous les processus
    processus = []
    
    # Parcourir tous les processus en cours
    # process_iter() → itère sur tous les processus
    # ['pid', 'name', ...] → les infos à récupérer pour chaque processus
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        # .info contient un dictionnaire avec les infos du processus
        processus.append(proc.info)
    
    # === TRI PAR CPU ===
    # sorted() → trie la liste
    # key=lambda x: x['cpu_percent'] → critère de tri (utilisation CPU)
    # or 0 → si la valeur est None, utiliser 0
    # reverse=True → tri décroissant (du plus grand au plus petit)
    processus_cpu = sorted(processus, key=lambda x: x['cpu_percent'] or 0, reverse=True)
    
    print("\nPar CPU :")
    # Afficher l'en-tête du tableau
    # <10 = aligné à gauche sur 10 caractères
    print(f"{'PID':<10} {'NOM':<25} {'CPU %':<10}")
    print("-" * 45)  # Ligne de séparation
    
    # Afficher les 5 premiers processus
    # [:5] = slice (découpe) des 5 premiers éléments
    for proc in processus_cpu[:5]:
        # [:24] = tronquer le nom à 24 caractères max
        print(f"{proc['pid']:<10} {proc['name'][:24]:<25} {proc['cpu_percent']:<10.1f}")
    
    # === TRI PAR MÉMOIRE ===
    processus_mem = sorted(processus, key=lambda x: x['memory_percent'] or 0, reverse=True)
    
    print("\nPar Mémoire :")
    print(f"{'PID':<10} {'NOM':<25} {'MEM %':<10}")
    print("-" * 45)
    
    for proc in processus_mem[:5]:
        print(f"{proc['pid']:<10} {proc['name'][:24]:<25} {proc['memory_percent']:<10.1f}")


def compter_fichiers(dossier):
    """
    Compte les fichiers dans un dossier par extension
    Analyse récursive de tous les sous-dossiers
    """
    print("\n" + "="*50)
    print("FICHIERS")
    print("="*50)
    
    # Vérifier si le dossier existe
    if not os.path.exists(dossier):
        print(f"Le dossier '{dossier}' n'existe pas")
        return  # Sortir de la fonction
    
    print(f"Dossier : {dossier}\n")
    
    # Dictionnaire pour compter les extensions
    # Clé = extension (.txt, .py, etc.), Valeur = nombre de fichiers
    compteurs = {'.txt': 0, '.py': 0, '.pdf': 0, '.jpg': 0}
    total = 0  # Compteur total de fichiers
    
    # Parcourir RÉCURSIVEMENT tous les fichiers et dossiers
    # os.walk() → parcourt le dossier et tous ses sous-dossiers
    # racine → chemin du dossier actuel
    # dossiers → liste des sous-dossiers dans ce dossier
    # fichiers → liste des fichiers dans ce dossier
    for racine, dossiers, fichiers in os.walk(dossier):
        for fichier in fichiers:
            total += 1  # Incrémenter le compteur total
            
            # Séparer le nom du fichier et son extension
            # os.path.splitext("photo.jpg") → ("photo", ".jpg")
            nom, ext = os.path.splitext(fichier)
            ext = ext.lower()  # Convertir en minuscules (.JPG → .jpg)
            
            # Si l'extension est dans notre dictionnaire, l'incrémenter
            if ext in compteurs:
                compteurs[ext] += 1
    
    print(f"Total de fichiers : {total}\n")
    
    # Afficher le tableau des résultats
    print(f"{'Extension':<15} {'Nombre':<10}")
    print("-" * 25)
    
    # Parcourir le dictionnaire et afficher chaque extension
    # .items() → retourne (clé, valeur) pour chaque élément
    for ext, nombre in compteurs.items():
        print(f"{ext:<15} {nombre:<10}")
    
    # Calculer le nombre de fichiers "autres" (non comptés)
    # sum() → additionne toutes les valeurs du dictionnaire
    autres = total - sum(compteurs.values())
    print(f"{'Autres':<15} {autres:<10}")


def main():
    """
    Fonction principale du programme
    Appelle toutes les autres fonctions dans l'ordre
    """
    # === EN-TÊTE DU PROGRAMME ===
    print("\n" + "="*50)
    print("MONITORING SYSTÈME")
    print("="*50)
    # Afficher la date et l'heure actuelles
    print(f"Date : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # === APPEL DES FONCTIONS DE MONITORING ===
    afficher_cpu()       # Info sur le processeur
    afficher_memoire()   # Info sur la RAM
    afficher_systeme()   # Info générales (OS, uptime, etc.)
    afficher_processus() # Top 5 des processus
    
    # === PARTIE INTERACTIVE : ANALYSE DE FICHIERS ===
    print("\n" + "="*50)
    # input() → demande à l'utilisateur de saisir du texte
    # .lower() → convertit en minuscules (O → o, N → n)
    reponse = input("Analyser un dossier ? (o/n) : ").lower()
    
    # Si l'utilisateur répond "o" (oui)
    if reponse == 'o':
        # Demander le chemin du dossier
        chemin = input("Chemin du dossier : ")
        
        # Si l'utilisateur a saisi un chemin, l'analyser
        if chemin:
            compter_fichiers(chemin)
        else:
            # Sinon, analyser le dossier home (~/ sur Linux/Mac, C:\Users\... sur Windows)
            compter_fichiers(os.path.expanduser("~"))
    
    # === FIN DU PROGRAMME ===
    print("\n" + "="*50)
    print("FIN")
    print("="*50 + "\n")


# === POINT D'ENTRÉE DU PROGRAMME ===
# Cette condition vérifie si le script est exécuté directement
# (et non importé comme module dans un autre script)
if __name__ == "__main__":
    main()  # Lancer la fonction principale