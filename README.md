# Get Started
Pour installer rapidement ce projet sur votre Raspberry Pi, vous pouvez utiliser le script d'installation automatique ci-dessous.

## Etape 1 : Installation
```bash
    curl -sSL https://raw.githubusercontent.com/MaelMainsard/raspberry_script/main/install.sh | bash
```
## Etape 2 : Lancement du script
```bash
    cd raspberry_script
    source venv/bin/activate
    python3 main.py
```
## Etape 3 : Lancement au démarage
Pour exécuter le script automatiquement au démarrage du Raspberry Pi :

```bash
  crontab -e
```

Puis ajoutez cette ligne :
```
@reboot cd /chemin/complet/vers/raspberry_script && source venv/bin/activate && python main.py
```



