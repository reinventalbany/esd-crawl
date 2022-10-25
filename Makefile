all: lint types test

lint:
	flake8 --ignore E501

types:
	mypy esd_crawl tests

test:
	pytest --cov=esd_crawl --cov-report=html
	open htmlcov/index.html
