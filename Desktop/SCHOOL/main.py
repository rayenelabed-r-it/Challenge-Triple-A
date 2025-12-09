#!/usr/bin/env python3
"""
Script de monitoring système complet
Collecte et affiche diverses informations sur le système
"""
#psutil : Bibliothèque principale pour récupérer les infos système (CPU, RAM, processus, etc.)
#platform : Fournit des infos sur le système d'exploitation
#pocket : Permet de récupérer le nom de la machine et l'adresse IP
#datetime : Gestion des dates et heures (uptime, timestamp)
#os : Interactions avec le système de fichiers
#defaultdict : Dictionnaire qui crée automatiquement des valeurs par défaut (ici 0)

import psutil
import platform
import socket
from datetime import datetime, timedelta
import os
from collections import defaultdict


def get_cpu_info():
    """Récupère les informations sur le processeur"""
    print("\n" + "="*60)
    print("INFORMATIONS PROCESSEUR")
    print("="*60)


    #cpu_count(logical=False) : Nombre de cœurs physiques (ex: 4 cœurs)
    # #cpu_count(logical=True) : Nombre de cœurs logiques (ex: 8 avec hyperthreading)
    cpu_count = psutil.cpu_count(logical=False)
    cpu_count_logical = psutil.cpu_count(logical=True)
    cpu_freq = psutil.cpu_freq()
    cpu_percent = psutil.cpu_percent(interval=1)
    #Mesure l'utilisation CPU sur 1 seconde (le interval=1)
    
    print(f"Nombre de cœurs physiques : {cpu_count}")
    print(f"Nombre de cœurs logiques : {cpu_count_logical}")
    print(f"Fréquence actuelle : {cpu_freq.current:.2f} MHz")
    print(f"Fréquence maximale : {cpu_freq.max:.2f} MHz")
    print(f"Utilisation CPU : {cpu_percent}%")

#virtual_memory() retourne un objet avec plusieurs attributs :
# .total : RAM totale en bytes
# .used : RAM utilisée en bytes
# .available : RAM disponible
# .percent : Pourcentage d'utilisation
def get_memory_info():
    """Récupère les informations sur la mémoire"""
    print("\n" + "="*60)
    print("INFORMATIONS MÉMOIRE")
    print("="*60)
    
    mem = psutil.virtual_memory()
    
    ram_used_gb = mem.used / (1024**3)
    ram_total_gb = mem.total / (1024**3)
    ram_percent = mem.percent
    #1 GB = 1024 MB = 1024³
    # Donc on divise par 1024**3 (= 1 073 741 824)
    
    print(f"RAM utilisée : {ram_used_gb:.2f} GB")
    print(f"RAM totale : {ram_total_gb:.2f} GB")
    print(f"RAM disponible : {mem.available / (1024**3):.2f} GB")
    print(f"Pourcentage d'utilisation : {ram_percent}%")


def get_system_info():
    """Récupère les informations système générales"""
    print("\n" + "="*60)
    print("INFORMATIONS SYSTÈME GÉNÉRALES")
    print("="*60)
    
    # Nom de la machine
    hostname = socket.gethostname()
    print(f"Nom de la machine : {hostname}")
    
    # Système d'exploitation
    os_info = platform.system()
    os_release = platform.release()
    os_version = platform.version()
    
    print(f"Système d'exploitation : {os_info}")
    print(f"Version : {os_release}")
    
    # Essayer d'obtenir la distribution Linux
    try:
        import distro
        dist_name = distro.name(pretty=True)
        print(f"Distribution : {dist_name}")
    except ImportError:
        if os_info == "Linux":
            print("(Installer 'distro' pour plus de détails: pip install distro)")
    
    # Heure de démarrage
    #psutil.boot_time() retourne un timestamp Unix (nombre de secondes depuis 1970)
    # fromtimestamp() convertit en objet datetime lisible
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    print(f"Heure de démarrage : {boot_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Uptime
    #divmod(a, b) : Retourne (quotient, reste)
    #ivmod(7384, 3600) → (2, 184) → 2 heures, reste 184 secondes
    uptime = datetime.now() - boot_time
    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    print(f"Uptime : {days} jours, {hours}h {minutes}min {seconds}s")
    
    # Utilisateurs connectés
    users = psutil.users()
    print(f"Nombre d'utilisateurs connectés : {len(users)}")
    for user in users:
        print(f"  - {user.name} (depuis {user.host if user.host else 'local'})")
    
    # Adresse IP principale
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        print(f"Adresse IP principale : {ip_address}")
    except Exception:
        print("Adresse IP principale : Non disponible")


def get_process_info():
    """Récupère les informations sur les processus"""
    print("\n" + "="*60)
    print("INFORMATIONS PROCESSUS")
    print("="*60)
    
    processes = []
    
    # Collecter les informations des processus
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    # Trier par utilisation CPU
    processes_by_cpu = sorted(processes, key=lambda x: x['cpu_percent'] or 0, reverse=True)
    
    print("\n--- TOP 10 PROCESSUS PAR UTILISATION CPU ---")
    print(f"{'PID':<10} {'NOM':<30} {'CPU %':<10}")
    print("-" * 50)
    for proc in processes_by_cpu[:10]:
        print(f"{proc['pid']:<10} {proc['name'][:29]:<30} {proc['cpu_percent']:<10.2f}")
    
    # Trier par utilisation mémoire
    processes_by_mem = sorted(processes, key=lambda x: x['memory_percent'] or 0, reverse=True)
    
    print("\n--- TOP 10 PROCESSUS PAR UTILISATION MÉMOIRE ---")
    print(f"{'PID':<10} {'NOM':<30} {'MEM %':<10}")
    print("-" * 50)
    for proc in processes_by_mem[:10]:
        print(f"{proc['pid']:<10} {proc['name'][:29]:<30} {proc['memory_percent']:<10.2f}")
    
    # Top 3 des processus les plus gourmands (combiné CPU + MEM)
    print("\n--- TOP 3 PROCESSUS LES PLUS GOURMANDS (CPU + MEM) ---")
    print(f"{'PID':<10} {'NOM':<30} {'CPU %':<10} {'MEM %':<10}")
    print("-" * 60)
    
    # Calculer un score combiné
    for proc in processes:
        cpu = proc['cpu_percent'] or 0
        mem = proc['memory_percent'] or 0
        proc['combined_score'] = cpu + (mem * 2)  # Pondération mémoire x2
    
    processes_combined = sorted(processes, key=lambda x: x['combined_score'], reverse=True)
    
    for proc in processes_combined[:3]:
        print(f"{proc['pid']:<10} {proc['name'][:29]:<30} {proc['cpu_percent']:<10.2f} {proc['memory_percent']:<10.2f}")


def analyze_files(directory_path):
    """Analyse les fichiers dans un dossier"""
    print("\n" + "="*60)
    print("ANALYSE DE FICHIERS")
    print("="*60)
    
    if not os.path.exists(directory_path):
        print(f"Erreur : Le dossier '{directory_path}' n'existe pas.")
        return
    
    print(f"Analyse du dossier : {directory_path}")
    
    # Extensions à compter
    target_extensions = ['.txt', '.py', '.pdf', '.jpg']
    file_counts = defaultdict(int)
    total_files = 0
    
    # Parcourir tous les fichiers
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            total_files += 1
            _, ext = os.path.splitext(file)
            ext_lower = ext.lower()
            
            if ext_lower in target_extensions:
                file_counts[ext_lower] += 1
    
    print(f"\nNombre total de fichiers analysés : {total_files}")
    print("\n--- RÉPARTITION PAR EXTENSION ---")
    print(f"{'Extension':<15} {'Nombre':<15} {'Pourcentage':<15}")
    print("-" * 45)
    
    for ext in target_extensions:
        count = file_counts[ext]
        percentage = (count / total_files * 100) if total_files > 0 else 0
        print(f"{ext:<15} {count:<15} {percentage:<14.2f}%")
    
    # Fichiers autres
    counted_files = sum(file_counts.values())
    other_files = total_files - counted_files
    other_percentage = (other_files / total_files * 100) if total_files > 0 else 0
    
    print(f"{'Autres':<15} {other_files:<15} {other_percentage:<14.2f}%")


def main():
    """Fonction principale"""
    print("\n" + "="*60)
    print(" MONITORING SYSTÈME COMPLET ".center(60, "="))
    print("="*60)
    print(f"Date et heure : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Collecter toutes les informations
    get_cpu_info()
    get_memory_info()
    get_system_info()
    get_process_info()
    
    # Analyse de fichiers
    # Modifier le chemin selon vos besoins
    home_dir = os.path.expanduser("~")
    
    # Vous pouvez choisir un dossier spécifique
    folder_to_analyze = home_dir  # ou home_dir + "/Documents"
    
    print("\n" + "="*60)
    choice = input("Voulez-vous analyser un dossier ? (o/n) : ").strip().lower()
    
    if choice == 'o':
        custom_path = input(f"Entrez le chemin du dossier (défaut: {folder_to_analyze}) : ").strip()
        if custom_path:
            folder_to_analyze = custom_path
        
        analyze_files(folder_to_analyze)
    
    print("\n" + "="*60)
    print(" FIN DU MONITORING ".center(60, "="))
    print("="*60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nMonitoring interrompu par l'utilisateur.")
    except Exception as e:
        print(f"\nErreur inattendue : {e}")
        import traceback
        traceback.print_exc()