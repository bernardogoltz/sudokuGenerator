# Sudoku Generator - Makefile

.PHONY: help install run build docker-build docker-run docker-stop clean deploy

# Variáveis
IMAGE_NAME = sudoku-generator
CONTAINER_NAME = sudoku-generator
PORT = 8501

help: ## Mostra esta ajuda
	@echo "Sudoku Generator - Comandos Disponíveis:"
	@echo "========================================"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Instala dependências Python
	pip install -r requirements.txt

run: ## Executa aplicação localmente
	./run.sh

test: ## Executa testes básicos
	python -c "import streamlit; print('Streamlit OK')"
	python -c "import reportlab; print('ReportLab OK')"
	@echo "✅ Todas as dependências estão funcionando"

build: docker-build ## Constrói imagem Docker

docker-build: ## Constrói imagem Docker
	docker build -t $(IMAGE_NAME):latest .

docker-run: ## Executa container Docker
	docker run -d --name $(CONTAINER_NAME) -p $(PORT):8501 $(IMAGE_NAME):latest
	@echo "✅ Container executando em http://localhost:$(PORT)"

docker-stop: ## Para container Docker
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true

docker-logs: ## Mostra logs do container
	docker logs -f $(CONTAINER_NAME)

compose-up: ## Inicia com Docker Compose
	docker-compose up -d
	@echo "✅ Aplicação iniciada em http://localhost:$(PORT)"

compose-down: ## Para Docker Compose
	docker-compose down

clean: ## Remove containers e imagens
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true
	docker rmi $(IMAGE_NAME):latest || true
	docker-compose down || true

deploy-local: ## Deploy local
	./deploy.sh local

deploy-staging: ## Deploy staging
	./deploy.sh staging

deploy-production: ## Deploy produção
	./deploy.sh production

status: ## Status da aplicação
	./deploy.sh status

rollback: ## Rollback para versão anterior
	./deploy.sh rollback

# Comandos de desenvolvimento
dev: ## Modo desenvolvimento
	./docker-run.sh dev

shell: ## Acessa shell do container
	docker exec -it $(CONTAINER_NAME) bash

# Comandos de manutenção
prune: ## Remove containers, imagens e volumes não utilizados
	docker system prune -af
	docker volume prune -f

backup: ## Backup da imagem atual
	docker tag $(IMAGE_NAME):latest $(IMAGE_NAME):backup-$(shell date +%Y%m%d-%H%M%S)

# Comandos de monitoramento
health: ## Verifica saúde da aplicação
	curl -f http://localhost:$(PORT)/_stcore/health || echo "❌ Aplicação não está saudável"

stats: ## Estatísticas dos containers
	docker stats $(CONTAINER_NAME)

# Comandos utilitários
setup: ## Setup inicial completo
	chmod +x *.sh
	mkdir -p generated_pdfs
	mkdir -p .streamlit
	@echo "✅ Setup concluído"

quick-start: setup install docker-build compose-up ## Setup e execução rápida
	@echo "🎉 Aplicação pronta em http://localhost:$(PORT)"
