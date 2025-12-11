#!/usr/bin/env python3
"""
Script de monitoring système avec génération HTML
Compatible avec le template original utilisant {{placeholders}}
"""
import time
import psutil
import platform
import socket
from datetime import datetime
import os
from collections import defaultdict


def get_cpu_info():
    """Récupère les informations sur le processeur"""
    cpu_count = psutil.cpu_count(logical=False)
    cpu_freq = psutil.cpu_freq()
    cpu_percent = psutil.cpu_percent(interval=1)
    
    return {
        'cpu_count': cpu_count or 'N/A',
        'frequency': f"{cpu_freq.current:.2f} MHz" if cpu_freq else 'N/A',
        'cpu_percent': f"{cpu_percent}",  # Juste le nombre sans %
        'cpu_percent_display': f"{cpu_percent}%"  # Avec % pour l'affichage
    }


def get_memory_info():
    """Récupère les informations sur la mémoire"""
    mem = psutil.virtual_memory()
    
    return {
        'total_memory': f"{mem.total / (1024**3):.2f} GB",
        'used_memory': f"{mem.used / (1024**3):.2f} GB",
        'ram_percentage': f"{mem.percent:.1f}"
    }


def get_system_info():
    """Récupère les informations système générales"""
    hostname = socket.gethostname()
    os_info = f"{platform.system()} {platform.release()}"
    
    # Calcul de l'uptime
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.now() - boot_time
    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    uptime_str = f"{days}j {hours}h {minutes}min"
    
    # Nombre d'utilisateurs
    users = psutil.users()
    user_count = len(users)
    # Afficher chaque utilisateur
    for user in utilisateurs:
        # Si .host existe et n'est pas vide, l'afficher, sinon afficher "local"
        origine = user.host if user.host else "local"
        print(f"  → {user.name} (depuis {origine})")
    hostname=socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    print (ip_address)
    
  
    
    
    return {
        'name_pc': hostname,
        'name_systeme': os_info,
        'uptime': uptime_str,
        'user_nomber': user_count,
        'system_load': system_load,
        'ip_address': ip_address
    }


def get_process_info():
    """Récupère les informations sur les processus"""
    processes = []
    
    # Collecter les informations des processus
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    # Trier par utilisation CPU et prendre le top 3
    processes_by_cpu = sorted(
        processes, 
        key=lambda x: x['cpu_percent'] or 0, 
        reverse=True
    )
    
    top_3 = processes_by_cpu[:3]
    top_3_str = "\n".join([
        f"{p['name']} (PID: {p['pid']}) - {p['cpu_percent']:.1f}%"
        for p in top_3
    ])
    
    return {
        'process_count': len(processes),
        'top_3_processes': top_3_str
    }


def analyze_files(directory_path):
    """Analyse les fichiers dans un dossier"""
    if not os.path.exists(directory_path):
        return {'pourcentage': f"Erreur : dossier '{directory_path}' introuvable"}
    
    target_extensions = ['.txt', '.py', '.pdf', '.jpg']
    file_counts = defaultdict(int)
    total_files = 0
    
    # Parcourir tous les fichiers
    try:
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                total_files += 1
                _, ext = os.path.splitext(file)
                ext_lower = ext.lower()
                
                if ext_lower in target_extensions:
                    file_counts[ext_lower] += 1
    except PermissionError:
        return {'pourcentage': "Erreur : accès refusé au dossier"}
    
    # Créer le résumé
    if total_files == 0:
        return {'pourcentage': "Aucun fichier trouvé"}
    
    stats = [f"Total: {total_files} fichiers"]
    for ext in target_extensions:
        count = file_counts[ext]
        percentage = (count / total_files * 100) if total_files > 0 else 0
        if count > 0:
            stats.append(f"{ext}: {count} ({percentage:.1f}%)")
    
    return {'pourcentage': "\n".join(stats)}


def generate_html(data, template_path, output_path):
    """
    Génère le fichier HTML à partir du template
    Remplace les {{variable}} par les valeurs collectées
    """
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Remplacer chaque {{variable}} par sa valeur
        for key, value in data.items():
            placeholder = f"{{{{{key}}}}}"
            template_content = template_content.replace(placeholder, str(value))
        
        # Écrire le fichier HTML final
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(template_content)
        
        return True
    except FileNotFoundError:
        print(f"✗ Erreur : le fichier template '{template_path}' est introuvable")
        return False
    except Exception as e:
        print(f"✗ Erreur lors de la génération HTML : {e}")
        return False


def main():
    """Fonction principale qui génère le monitoring en boucle"""
    print("\n" + "="*60)
    print(" MONITORING SYSTÈME EN TEMPS RÉEL ".center(60, "="))
    print("="*60)
    print("Appuyez sur Ctrl+C pour arrêter\n")
    
    # Chemins des fichiers
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(script_dir, "template.html")
    output_path = os.path.join(script_dir, "monitoring.html")
    
    iteration = 0
    
    while True:
        iteration += 1
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Mise à jour #{iteration}...")
        
        # Timestamp actuel
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Collecter toutes les informations
        data = {'timestamp': timestamp}
        
        data.update(get_system_info())
        data.update(get_cpu_info())
        data.update(get_memory_info())
        data.update(get_process_info())
        
        # Analyse de fichiers (dossier personnel par défaut)
        home_dir = os.path.expanduser("~")
        data.update(analyze_files(home_dir))
        
        # Générer le HTML
        if generate_html(data, template_path, output_path):
            print(f"  ✓ Page mise à jour : CPU {data['cpu_percent_display']}, RAM {data['ram_percentage']}%")
        else:
            print(f"  ✗ Erreur lors de la génération")
        
        # Attendre 5 secondes avant la prochaine mise à jour
        time.sleep(5)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n" + "="*60)
        print(" MONITORING ARRÊTÉ ".center(60, "="))
        print("="*60 + "\n")
    except Exception as e:
        print(f"\nErreur inattendue : {e}")
        import traceback
        traceback.print_exc()
