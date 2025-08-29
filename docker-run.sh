#!/bin/bash

# Sudoku Generator - Docker Run Script
# Este script constrói e executa o container Docker

set -e

echo "🐳 Sudoku Generator - Docker Deploy"
echo "===================================="

# Função para mostrar uso
show_usage() {
    echo "Uso: $0 [build|run|stop|logs|clean]"
    echo ""
    echo "Comandos:"
    echo "  build  - Constrói a imagem Docker"
    echo "  run    - Executa o container"
    echo "  stop   - Para o container"
    echo "  logs   - Mostra logs do container"
    echo "  clean  - Remove container e imagem"
    echo "  dev    - Executa em modo desenvolvimento"
    echo ""
    exit 1
}

# Verificar se Docker está instalado
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker não está instalado!"
        echo "Instale Docker: https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        echo "❌ Docker não está executando!"
        echo "Inicie o Docker e tente novamente."
        exit 1
    fi
    
    echo "✅ Docker está funcionando"
}

# Construir imagem
build_image() {
    echo "🔨 Construindo imagem Docker..."
    docker build -t sudoku-generator:latest .
    echo "✅ Imagem construída com sucesso!"
}

# Executar container
run_container() {
    echo "🚀 Iniciando container..."
    
    # Parar container existente se estiver executando
    docker stop sudoku-generator 2>/dev/null || true
    docker rm sudoku-generator 2>/dev/null || true
    
    # Criar diretório para PDFs
    mkdir -p generated_pdfs
    
    # Executar novo container
    docker run -d \
        --name sudoku-generator \
        -p 8501:8501 \
        -v "$(pwd)/generated_pdfs:/app/generated_pdfs" \
        --restart unless-stopped \
        sudoku-generator:latest
    
    echo "✅ Container iniciado!"
    echo "📍 Acesse: http://localhost:8501"
    echo "📝 Logs: docker logs -f sudoku-generator"
}

# Executar com docker-compose
run_compose() {
    echo "🚀 Iniciando com Docker Compose..."
    docker-compose up -d
    echo "✅ Aplicação iniciada!"
    echo "📍 Acesse: http://localhost:8501"
}

# Parar container
stop_container() {
    echo "🛑 Parando container..."
    docker-compose down 2>/dev/null || docker stop sudoku-generator 2>/dev/null || true
    echo "✅ Container parado!"
}

# Mostrar logs
show_logs() {
    echo "📋 Logs do container:"
    docker logs -f sudoku-generator
}

# Limpar tudo
clean_all() {
    echo "🧹 Limpando containers e imagens..."
    docker-compose down 2>/dev/null || true
    docker stop sudoku-generator 2>/dev/null || true
    docker rm sudoku-generator 2>/dev/null || true
    docker rmi sudoku-generator:latest 2>/dev/null || true
    echo "✅ Limpeza concluída!"
}

# Modo desenvolvimento
dev_mode() {
    echo "🔧 Modo desenvolvimento (com hot reload)..."
    docker stop sudoku-generator 2>/dev/null || true
    docker rm sudoku-generator 2>/dev/null || true
    
    docker run -it --rm \
        --name sudoku-generator-dev \
        -p 8501:8501 \
        -v "$(pwd):/app" \
        -v "$(pwd)/generated_pdfs:/app/generated_pdfs" \
        sudoku-generator:latest
}

# Main script
case "$1" in
    build)
        check_docker
        build_image
        ;;
    run)
        check_docker
        build_image
        run_compose
        ;;
    stop)
        stop_container
        ;;
    logs)
        show_logs
        ;;
    clean)
        clean_all
        ;;
    dev)
        check_docker
        build_image
        dev_mode
        ;;
    *)
        show_usage
        ;;
esac
