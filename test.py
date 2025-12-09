#!/usr/bin/env python3
"""
Script de monitoring système simplifié
"""
#psutil : Bibliothèque principale pour récupérer les infos système (CPU, RAM, processus, etc.)
#platform : Fournit des infos sur le système d'exploitation
#socket : Permet de récupérer le nom de la machine et l'adresse IP
#datetime : Gestion des dates et heures (uptime, timestamp)
#os : Interactions avec le système de fichiers
import psutil
import platform
import socket
from datetime import datetime
import os


def afficher_cpu():
    """Affiche les infos CPU"""
    print("\n" + "="*50)
    print("PROCESSEUR")
    print("="*50)
    
    #cpu_count(logical=False) : Nombre de cœurs physiques (ex: 4 cœurs)
    # #cpu_count(logical=True) : Nombre de cœurs logiques (ex: 8 avec hyperthreading)
    coeurs = psutil.cpu_count(logical=False)
    coeurs_logiques = psutil.cpu_count(logical=True)
    frequence = psutil.cpu_freq()
    utilisation = psutil.cpu_percent(interval=1)
    
    print(f"Cœurs physiques : {coeurs}")
    print(f"Cœurs logiques : {coeurs_logiques}")
    print(f"Fréquence : {frequence.current:.0f} MHz")
    print(f"Utilisation : {utilisation}%")

#virtual_memory() retourne un objet avec plusieurs attributs :
# .total : RAM totale en bytes
# .used : RAM utilisée en bytes
# .available : RAM disponible
# .percent : Pourcentage d'utilisation
def afficher_memoire():
    """Affiche les infos mémoire"""
    print("\n" + "="*50)
    print("MÉMOIRE")
    print("="*50)
    
    mem = psutil.virtual_memory()
    
    ram_utilisee = mem.used / (1024**3)
    ram_totale = mem.total / (1024**3)
    ram_percent = mem.percent
     #1 GB = 1024 MB = 1024³
    # Donc on divise par 1024**3 (= 1 073 741 824)
    
    print(f"RAM utilisée : {ram_utilisee:.2f} GB")
    print(f"RAM totale : {ram_totale:.2f} GB")
    print(f"Pourcentage : {mem.percent}%")


def afficher_systeme():
    """Affiche les infos système"""
    print("\n" + "="*50)
    print("SYSTÈME")
    print("="*50)
    
    print(f"Machine : {socket.gethostname()}")
    print(f"OS : {platform.system()} {platform.release()}")
    
    demarrage = datetime.fromtimestamp(psutil.boot_time())
    print(f"Démarrage : {demarrage.strftime('%Y-%m-%d %H:%M:%S')}")
    
    uptime = datetime.now() - demarrage
    jours = uptime.days
    heures = uptime.seconds // 3600
    minutes = (uptime.seconds % 3600) // 60
    print(f"Uptime : {jours}j {heures}h {minutes}min")


def afficher_processus():
    """Affiche le top 5 des processus"""
    print("\n" + "="*50)
    print("TOP 5 PROCESSUS")
    print("="*50)
    
    processus = []
    
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        processus.append(proc.info)
    
    processus_cpu = sorted(processus, key=lambda x: x['cpu_percent'] or 0, reverse=True)
    
    print("\nPar CPU :")
    print(f"{'PID':<10} {'NOM':<25} {'CPU %':<10}")
    print("-" * 45)
    
    for proc in processus_cpu[:5]:
        print(f"{proc['pid']:<10} {proc['name'][:24]:<25} {proc['cpu_percent']:<10.1f}")
    
    processus_mem = sorted(processus, key=lambda x: x['memory_percent'] or 0, reverse=True)
    
    print("\nPar Mémoire :")
    print(f"{'PID':<10} {'NOM':<25} {'MEM %':<10}")
    print("-" * 45)
    
    for proc in processus_mem[:5]:
        print(f"{proc['pid']:<10} {proc['name'][:24]:<25} {proc['memory_percent']:<10.1f}")


def compter_fichiers(dossier):
    """Compte les fichiers par extension"""
    print("\n" + "="*50)
    print("FICHIERS")
    print("="*50)
    
    if not os.path.exists(dossier):
        print(f"Le dossier '{dossier}' n'existe pas")
        return
    
    print(f"Dossier : {dossier}\n")
    
    compteurs = {'.txt': 0, '.py': 0, '.pdf': 0, '.jpg': 0}
    total = 0
    
    for racine, dossiers, fichiers in os.walk(dossier):
        for fichier in fichiers:
            total += 1
            nom, ext = os.path.splitext(fichier)
            ext = ext.lower()
            
            if ext in compteurs:
                compteurs[ext] += 1
    
    print(f"Total de fichiers : {total}\n")
    
    print(f"{'Extension':<15} {'Nombre':<10}")
    print("-" * 25)
    
    for ext, nombre in compteurs.items():
        print(f"{ext:<15} {nombre:<10}")
    
    autres = total - sum(compteurs.values())
    print(f"{'Autres':<15} {autres:<10}")


def main():
    """Fonction principale"""
    print("\n" + "="*50)
    print("MONITORING SYSTÈME")
    print("="*50)
    print(f"Date : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    afficher_cpu()
    afficher_memoire()
    afficher_systeme()
    afficher_processus()
    
    print("\n" + "="*50)
    reponse = input("Analyser un dossier ? (o/n) : ").lower()
    
    if reponse == 'o':
        chemin = input("Chemin du dossier : ")
        if chemin:
            compter_fichiers(chemin)
        else:
            compter_fichiers(os.path.expanduser("~"))
    
    print("\n" + "="*50)
    print("FIN")
    print("="*50 + "\n")


if __name__ == "__main__":
    main()