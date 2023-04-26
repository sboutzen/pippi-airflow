dev:
	poetry env use 3.10 && poetry shell
clean:
	rm -rf dist/ && rm -rf dev/logs/
build: clean
build:
	poetry build
publish: build
publish:
	python -m twine upload --repository testpypi dist/*
dockerclean:
	docker compose -f dev/docker-compose.yml down --volumes --remove-orphans
dockerairflow:
	docker compose -f dev/docker-compose.yml up --build


