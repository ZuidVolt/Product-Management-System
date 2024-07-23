# Python development Makefile

.PHONY: mypy unittest pytest run format pylint ruff coverage install install_utility uninstall clean check full docs venv requirements freeze update_deps security_check build docker_build docker_run

mypy: # check for type errors
	mypy --check-untyped-defs utils.py tests.py user_management.py product_management.py order_management.py main.py inventory_management.py database.py
unittest: # runs unit tests on all files starting with test_
	python3 -m unittest discover -v -p "test_*.py"

pytest: # tests using pytest on all files starting with test_
	pytest -v test_*.py

run: # runs program from main
	python3 main.py

format: # formats using black
	ruff format --line-length 120 utils.py tests.py user_management.py product_management.py order_management.py main.py inventory_management.py database.py

pylint: # checks for errors and bad practices
	pylint --disable=C0116,C0114,C0301,W0611,C0303,E0602,W0612,C0413,C0305,C0415 utils.py tests.py user_management.py product_management.py order_management.py main.py inventory_management.py database.py

ruff: # checks for errors and bad practices
	ruff check --fix main.py .

coverage: # checks code coverage
	coverage run -m unittest discover
	coverage report
	coverage html

install: # installs all 3rd party libraries
	pip install -r requirements.txt

install_utility: # installs utilities for formatting and type checking
	pip install ruff mypy pylint coverage

uninstall: # uninstalls all 3rd party libraries
	pip uninstall -r requirements.txt -y

clean: # cleans temporary files
	find . -type f \( -name '*.pyc' -o -name '*.o' -o -name '*.out' -o -name '*.dSYM' -o -name '*.swp' -o -name '*.swo' -o -name '*.swn' \) -delete
	find . -type d \( -name '__pycache__' -o -name '.mypy_cache' -o -name '.pytest_cache' -o -name '.ruff_cache' -o -name 'build' -o -name '*.build' \) -exec rm -rf {} +
	find . -type f \( -name '*.gcda' -o -name '*.gcno' \) -delete
	rm -rf htmlcov
	rm -rf .build
	rm -rf *.xcodeproj
	rm -rf *.xcworkspace
	rm -rf *.dSYM

# combined commands
check: format mypy ruff unittest # does a quick check of code using linting, formatting, type checking, and unit testing

full: format mypy pytest ruff pylint # does a full check of code using linting, formatting, type checking, and unit testing

docs: # generate documentation using Sphinx
	cd docs && make html

venv: # create a virtual environment
	python3 -m venv venv
	@echo "To activate the virtual environment, run: source venv/bin/activate"
venv-a: # creates and actives the virtual environment
	python3 -m venv venv
	source venv/bin/activate
	@echo "Virtual environment activated."

requirements: # generate requirements.txt
	pip freeze > requirements.txt

freeze: requirements # alias for requirements

update_deps: # update all dependencies
	pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 pip install -U

security_check: # run security checks on dependencies
	safety check -r requirements.txt

build: # build the project (adjust as needed)
	python setup.py sdist bdist_wheel

# docker_build: # build Docker image (assuming Dockerfile exists)
# 	docker build -t my-python-app .

# docker_run: # run Docker container
# 	docker run -it --rm my-python-app