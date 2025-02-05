project_name := Nezbut Portfolio
author := nezbut

backend_version := $(shell grep -oP '^version = "\K[^"]+' backend/pyproject.toml || echo "0.1.0")
frontend_version := $(shell grep -oP '"version":\s*"\K[^"]+' frontend/package.json || echo "0.1.0")

backend_image := $(author)/portfolio-backend:$(backend_version)
frontend_image := $(author)/portfolio-frontend:$(frontend_version)

backend_image_latest := $(author)/portfolio-backend:latest
frontend_image_latest := $(author)/portfolio-frontend:latest

# =================================================================================================
# Dependencies
# =================================================================================================

.PHONY: install-deps-backend
install-deps-backend:
	cd backend && poetry install --with test

.PHONY: install-deps-frontend
install-deps-frontend:
	cd frontend && npm install

.PHONY: update-deps-backend
update-deps-backend:
	cd backend && poetry update --with test

.PHONY: install-deps-backend-unix
install-deps-backend-unix:
	cd backend && poetry install --with test,unix

.PHONY: update-deps-backend-unix
update-deps-backend-unix:
	cd backend && poetry update --with test,unix

# =================================================================================================
# Project Info
# =================================================================================================

.PHONY: info
info:
	@echo ""
	@echo "=============================================="
	@echo "        $(project_name) - Project Info"
	@echo "=============================================="
	@echo " Backend Version:  $(backend_version)"
	@echo " Frontend Version: $(frontend_version)"
	@echo "----------------------------------------------"
	@echo " Backend Image:  $(backend_image)"
	@echo " Frontend Image: $(frontend_image)"
	@echo "=============================================="
	@echo ""

# =================================================================================================
# Linters (Backend)
# =================================================================================================

.PHONY: lint-backend
lint-backend:
	@echo "Linting $(project_name) backend..."
	cd backend && \
		echo "Running Ruff:" && poetry run ruff check . && \
		echo "Running Mypy:" && poetry run mypy .

# =================================================================================================
# Docker: Backend
# =================================================================================================

.PHONY: build-backend
build-backend:
	@echo "Building backend Docker image: $(backend_image)..."
	docker buildx build -f Dockerfile-backend -t $(backend_image) .

.PHONY: rebuild-backend
rebuild-backend:
	@echo "Rebuilding backend Docker image: $(backend_image)..."
	@if [ -n "$$(docker images -q $(backend_image))" ]; then \
	  echo "Removing existing backend image $(backend_image)..."; \
	  docker rmi $(backend_image) || echo "Image $(backend_image) not found, skipping removal."; \
	fi
	$(MAKE) build-backend

.PHONY: push-backend
push-backend:
	@echo "Pushing backend Docker image to Docker Hub..."
	docker tag $(backend_image) $(backend_image_latest)
	docker push $(backend_image)
	docker push $(backend_image_latest)

# =================================================================================================
# Docker: Frontend
# =================================================================================================

.PHONY: build-frontend
build-frontend:
	@echo "Building frontend Docker image: $(frontend_image)..."
	docker buildx build -f Dockerfile-frontend -t $(frontend_image) .

.PHONY: rebuild-frontend
rebuild-frontend:
	@echo "Rebuilding frontend Docker image: $(frontend_image)..."
	@if [ -n "$$(docker images -q $(frontend_image))" ]; then \
	  echo "Removing existing frontend image $(frontend_image)..."; \
	  docker rmi $(frontend_image) || echo "Image $(frontend_image) not found, skipping removal."; \
	fi
	$(MAKE) build-frontend

.PHONY: push-frontend
push-frontend:
	@echo "Pushing frontend Docker image to Docker Hub..."
	docker tag $(frontend_image) $(frontend_image_latest)
	docker push $(frontend_image)
	docker push $(frontend_image_latest)

# =================================================================================================
# Combined: Rebuild and Push All
# =================================================================================================

.PHONY: rebuild-all
rebuild-all: rebuild-backend rebuild-frontend
	@echo "All images rebuilt successfully!"

.PHONY: push-all
push-all: push-backend push-frontend
	@echo "All images pushed to Docker Hub!"
