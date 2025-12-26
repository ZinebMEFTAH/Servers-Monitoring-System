# AMS – Automated Monitoring System

## Présentation

AMS est un système de supervision distribué qui permet de collecter, stocker, visualiser et surveiller l'utilisation des ressources systèmes sur plusieurs machines (serveurs). Il est capable de détecter automatiquement des situations critiques et de notifier l’administrateur par email.

Le système est structuré en plusieurs modules : collecte, stockage, visualisation, détection de crise, alerte, et interface web.

---

## Options de fonctionnement

### Mode local (Serveur A)

Le projet peut fonctionner sur une seule machine :

- Collecte de métriques locales : CPU, RAM, Disque, Processus, Alerte CERT.
- Stockage dans un fichier `system_logs.json`.
- Visualisation des métriques sous forme de graphiques SVG avec Pygal.
- Interface web de consultation en Flask.
- Envoi automatique d’emails en cas de crise.

### Mode distribué (Serveur A + Serveur B)

Le système permet la supervision de plusieurs machines :

- Le serveur B collecte ses métriques et les stocke localement.
- Le serveur A récupère les logs de Server B automatiquement via `scp`.
- Les fichiers sont fusionnés pour afficher des données combinées et par serveur.
- Les graphiques sont générés pour :
  - toutes les machines combinées,
  - le serveur A uniquement,
  - le serveur B uniquement.

---

## Fonctionnalités développées

| Fonctionnalité               | Description |
|-----------------------------|-------------|
| Collecte de données système | CPU, RAM, Disque, Processus via `psutil` ou `bash`. |
| Détection de crise          | Détection automatique et déclenchement d’alerte. |
| Alerte par email            | Notification envoyée à l’administrateur via SMTP. |
| Graphiques dynamiques       | Visualisation de l’évolution des métriques en SVG. |
| Support multi-serveur       | Collecte distante depuis un serveur via SSH/SCP. |
| Interface web Flask         | Affichage centralisé des données et des alertes. |
| Automatisation (crontab)    | Tâches planifiées pour les sondes, alertes et backups. |
| Nettoyage & sauvegarde      | Suppression des vieux logs et backups journaliers. |

---

## Technologies utilisées

- Python 3 (psutil, pygal, flask)
- Bash
- Cron (pour l’automatisation)
- SCP/SSH (communication entre serveurs)
- JSON (format de stockage)
- HTML/CSS (interface web)

---

## Structure du projet
```bash
AMS_Project/
├── alerts/
│   └── crisis_detection.py
├── backups/
│   └── backup_json.py
├── graphs/
│   └── generate_graphs.py
├── sensors/
│   ├── log_cpu.sh
│   ├── log_ram.py
│   ├── log_disk.sh
│   ├── log_process.py
│   └── log_cert_alert.py
├── storage/
│   ├── system_logs.json
│   ├── remote/
│   │   └── serverb_logs.json
│   ├── cleanup_json.py
│   └── cleanup_alerts.py
├── web/
│   ├── app.py
│   ├── templates/
│   │   └── index.html
│   └── static/
│       └── style.css
├── logs/
│   └── flask.log
└── README.md
```


⸻

Instructions de lancement

1. Lancer manuellement

```bash
cd AMS_Project/web
./app.py

L’application sera accessible sur http://localhost:5050 ou via l’IP du serveur (shown in the terminal).

2. Utiliser crontab pour automatiser

Extrait d’exemple de crontab :

*/2  * * * * /bin/bash /chemin/vers/log_cpu.sh
*/5  * * * * /usr/bin/python3 /chemin/vers/log_ram.py
*/10 * * * * /bin/bash /chemin/vers/log_disk.sh
*/15 * * * * /usr/bin/python3 /chemin/vers/log_process.py
*/30 * * * * /usr/bin/python3 /chemin/vers/log_cert_alert.py
*/30 * * * * /usr/bin/python3 /chemin/vers/cleanup_json.py
0    * * * * /usr/bin/python3 /chemin/vers/backup_json.py
*/5  * * * * /usr/bin/python3 /chemin/vers/crisis_detection.py
*/30 * * * * /usr/bin/python3 /chemin/vers/cleanup_alerts.py
*/2  * * * * scp serverb@192.168.64.12:/home/serverb/AMS_Project/storage/system_logs.json /chemin/vers/remote/serverb_logs.json
@reboot /usr/bin/python3 /chemin/vers/web/app.py > /chemin/vers/logs/flask.log 2>&1 &
```
