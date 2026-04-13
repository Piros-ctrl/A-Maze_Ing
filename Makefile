# A-Maze-ing Makefile

run:
	python3 a_maze_ing.py config.txt

install:
	pip install -r requirements.txt

debug:
	python3 -m pdb a_maze_ing.py config.txt

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .mypy_cache -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name dist -exec rm -rf {} +
	find . -type d -name build -exec rm -rf {} +
	find . -name "*.pyc" -delete

lint:
	flake8 .
	mypy . --warn-return-any \
	       --warn-unused-ignores \
	       --ignore-missing-imports \
	       --disallow-untyped-defs \
	       --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict

package:
	pip install build
	python3 -m build mazegen/

.PHONY: install run debug clean lint lint-strict package