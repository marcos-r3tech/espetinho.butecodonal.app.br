#!/bin/bash

# Inicializar Git se não existir
if [ ! -d ".git" ]; then
    echo "🔧 Inicializando repositório Git..."
    git init
    git remote add origin https://github.com/marcos-r3tech/marcos-r3tech.git
    git config user.name "Railway Bot"
    git config user.email "railway@buteco.com"
    echo "✅ Git configurado com sucesso!"
else
    echo "✅ Git já está configurado!"
fi

# Fazer pull do repositório
echo "🔄 Fazendo pull do GitHub..."
git pull origin main

# Iniciar aplicação
echo "🚀 Iniciando aplicação..."
python app_web.py
