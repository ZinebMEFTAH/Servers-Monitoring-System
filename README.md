# AMS — Système de Supervision de Serveurs

**AMS (Automated Monitoring System)** est un système de supervision distribué qui collecte, stocke, visualise et surveille l'utilisation des ressources sur une ou plusieurs machines. Il détecte automatiquement les situations critiques et alerte l'administrateur par email.

## Fonctionnalités

- **Collecte de métriques** — CPU, RAM, disque, processus
- **Stockage** des mesures (historique en `system_logs.json`)
- **Visualisation** sous forme de graphiques SVG (Pygal)
- **Détection de crise** automatique selon des seuils
- **Alertes email** à l'administrateur en cas d'anomalie
- **Interface web** de consultation (Flask)

## Modes de fonctionnement

- **Local (Serveur A)** — supervision d'une seule machine.
- **Distribué (Serveur A + Serveur B)** — le serveur A récupère automatiquement les logs du serveur B via `scp`, fusionne les données et génère des graphiques combinés et par serveur.

## Stack technique

- Python
- Flask (interface web)
- Pygal (graphiques SVG)
- scp (synchronisation en mode distribué)

## Installation & lancement

```bash
git clone https://github.com/ZinebMEFTAH/Servers-Monitoring-System.git
cd Servers-Monitoring-System
pip install -r requirements.txt
python web/app.py        # interface web de supervision
```

## Architecture

Modules : `sensors/` (collecte), `storage/` (stockage), `graphs/` (visualisation), `alerts/` (détection & email), `web/` (interface), `backups/` (sauvegardes), `config/` (configuration).

## Notes

Projet AMS de supervision système, du capteur jusqu'à l'alerte, fonctionnant aussi bien sur une machine que sur un parc distribué.
