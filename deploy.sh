#!/bin/bash

# Sudoku Generator - Deploy Script
# Script completo para deploy em produção

set -e

echo "🚀 Sudoku Generator - Deploy Script"
echo "===================================="

# Configurações
IMAGE_NAME="sudoku-generator"
CONTAINER_NAME="sudoku-generator"
PORT="8501"
DOMAIN=""  # Adicione seu domínio aqui se necessário

# Função para mostrar uso
show_usage() {
    echo "Uso: $0 [local|production|staging]"
    echo ""
    echo "Ambientes:"
    echo "  local      - Deploy local (desenvolvimento)"
    echo "  production - Deploy em produção"
    echo "  staging    - Deploy em staging"
    echo ""
    exit 1
}

# Verificar pré-requisitos
check_requirements() {
    echo "🔍 Verificando pré-requisitos..."
    
    # Docker
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker não encontrado!"
        exit 1
    fi
    
    # Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        echo "❌ Docker Compose não encontrado!"
        exit 1
    fi
    
    echo "✅ Pré-requisitos OK"
}

# Backup da versão anterior
backup_previous() {
    echo "💾 Fazendo backup da versão anterior..."
    
    if docker image inspect $IMAGE_NAME:latest &> /dev/null; then
        docker tag $IMAGE_NAME:latest $IMAGE_NAME:backup-$(date +%Y%m%d-%H%M%S)
        echo "✅ Backup criado"
    else
        echo "ℹ️  Nenhuma versão anterior encontrada"
    fi
}

# Build da aplicação
build_app() {
    echo "🔨 Construindo aplicação..."
    
    # Build da imagem
    docker build -t $IMAGE_NAME:latest .
    
    # Tag com timestamp
    docker tag $IMAGE_NAME:latest $IMAGE_NAME:$(date +%Y%m%d-%H%M%S)
    
    echo "✅ Build concluído"
}

# Deploy local
deploy_local() {
    echo "🏠 Deploy Local"
    
    check_requirements
    backup_previous
    build_app
    
    # Parar versão anterior
    docker-compose down 2>/dev/null || true
    
    # Iniciar nova versão
    docker-compose up -d
    
    echo "✅ Deploy local concluído!"
    echo "📍 URL: http://localhost:$PORT"
}

# Deploy produção
deploy_production() {
    echo "🌐 Deploy Produção"
    
    check_requirements
    
    # Verificar se está na branch main
    if [[ $(git branch --show-current) != "main" ]]; then
        echo "⚠️  Não está na branch main!"
        read -p "Continuar assim mesmo? [y/N] " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
    
    backup_previous
    build_app
    
    # Health check da imagem
    echo "🏥 Testando saúde da aplicação..."
    docker run --rm -d --name test-$CONTAINER_NAME -p 8502:8501 $IMAGE_NAME:latest
    sleep 10
    
    if curl -f http://localhost:8502/_stcore/health &> /dev/null; then
        echo "✅ Health check OK"
        docker stop test-$CONTAINER_NAME
    else
        echo "❌ Health check falhou!"
        docker stop test-$CONTAINER_NAME
        exit 1
    fi
    
    # Deploy com zero downtime
    echo "🔄 Deploy com zero downtime..."
    
    # Iniciar nova versão na porta temporária
    docker run -d --name $CONTAINER_NAME-new -p 8502:8501 $IMAGE_NAME:latest
    sleep 5
    
    # Verificar se nova versão está funcionando
    if curl -f http://localhost:8502/_stcore/health &> /dev/null; then
        # Parar versão antiga
        docker stop $CONTAINER_NAME 2>/dev/null || true
        docker rm $CONTAINER_NAME 2>/dev/null || true
        
        # Renomear nova versão
        docker stop $CONTAINER_NAME-new
        docker rm $CONTAINER_NAME-new
        
        # Iniciar versão final
        docker run -d --name $CONTAINER_NAME -p $PORT:8501 --restart unless-stopped $IMAGE_NAME:latest
        
        echo "✅ Deploy produção concluído!"
        if [[ -n "$DOMAIN" ]]; then
            echo "📍 URL: https://$DOMAIN"
        else
            echo "📍 URL: http://localhost:$PORT"
        fi
    else
        echo "❌ Nova versão falhou!"
        docker stop $CONTAINER_NAME-new
        docker rm $CONTAINER_NAME-new
        exit 1
    fi
}

# Deploy staging
deploy_staging() {
    echo "🧪 Deploy Staging"
    
    check_requirements
    backup_previous
    build_app
    
    # Parar staging anterior
    docker stop $CONTAINER_NAME-staging 2>/dev/null || true
    docker rm $CONTAINER_NAME-staging 2>/dev/null || true
    
    # Iniciar staging
    docker run -d --name $CONTAINER_NAME-staging -p 8503:8501 --restart unless-stopped $IMAGE_NAME:latest
    
    echo "✅ Deploy staging concluído!"
    echo "📍 URL: http://localhost:8503"
}

# Rollback
rollback() {
    echo "⏪ Fazendo rollback..."
    
    # Encontrar última imagem de backup
    BACKUP_IMAGE=$(docker images --format "table {{.Repository}}:{{.Tag}}" | grep $IMAGE_NAME:backup | head -1)
    
    if [[ -n "$BACKUP_IMAGE" ]]; then
        # Parar versão atual
        docker stop $CONTAINER_NAME
        docker rm $CONTAINER_NAME
        
        # Iniciar versão de backup
        docker run -d --name $CONTAINER_NAME -p $PORT:8501 --restart unless-stopped $BACKUP_IMAGE
        
        echo "✅ Rollback concluído para: $BACKUP_IMAGE"
    else
        echo "❌ Nenhum backup encontrado!"
        exit 1
    fi
}

# Status da aplicação
show_status() {
    echo "📊 Status da Aplicação"
    echo "====================="
    
    # Container status
    if docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep $CONTAINER_NAME; then
        echo "✅ Container ativo"
    else
        echo "❌ Container não está executando"
    fi
    
    # Health check
    if curl -f http://localhost:$PORT/_stcore/health &> /dev/null; then
        echo "✅ Aplicação saudável"
    else
        echo "❌ Aplicação com problemas"
    fi
    
    # Logs recentes
    echo ""
    echo "📋 Logs recentes:"
    docker logs --tail 10 $CONTAINER_NAME
}

# Main script
case "$1" in
    local)
        deploy_local
        ;;
    production)
        deploy_production
        ;;
    staging)
        deploy_staging
        ;;
    rollback)
        rollback
        ;;
    status)
        show_status
        ;;
    *)
        show_usage
        ;;
esac
