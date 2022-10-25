#!/bin/bash

set -e
set -x


flake8 --ignore E501

mypy esd_crawl tests

pytest --cov=esd_crawl --cov-report=html
open htmlcov/index.html
