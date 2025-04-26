#!/bin/bash

echo "====== Installation automatique du projet Raspberry Pi IOT ======"

# Mise à jour du système
echo "📦 Mise à jour du système..."
sudo apt update && sudo apt upgrade -y

# Installation des dépendances système
echo "📦 Installation des dépendances système..."
sudo apt install -y git python3-pip python3-venv

# Clonage du dépôt
echo "📂 Clonage du dépôt GitHub..."
git clone https://github.com/MaelMainsard/raspberry_script.git
cd raspberry_script

# Création et activation de l'environnement virtuel
echo "🐍 Configuration de l'environnement Python..."
python3 -m venv venv
source venv/bin/activate

# Installation des dépendances Python
echo "📦 Installation des dépendances Python..."
pip install -r requirements.txt

echo "✅ Installation terminée avec succès!"
echo "Pour exécuter le projet: cd raspberry_script && source venv/bin/activate && python3 main.py"