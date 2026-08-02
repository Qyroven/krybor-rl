PYTHON ?= python3

.PHONY: install check test smoke bandit plan

install:
	$(PYTHON) -m pip install -e .

check:
	$(PYTHON) -c 'import sys; assert sys.version_info >= (3, 11), "Krybor RL requires Python 3.11+"'
	PYTHONPATH=src $(PYTHON) -m compileall -q src tests
	PYTHONPATH=src $(PYTHON) -m unittest discover -s tests -v
	$(MAKE) smoke PYTHON=$(PYTHON)

test:
	PYTHONPATH=src $(PYTHON) -m unittest discover -s tests -v

smoke:
	PYTHONPATH=src $(PYTHON) -m krybor_rl bandit --steps 5 --runs 2 > /dev/null
	PYTHONPATH=src $(PYTHON) -m krybor_rl compare --theta 1e-8 > /dev/null
	PYTHONPATH=src $(PYTHON) -m krybor_rl run experiments/configs/ch04_value_iteration.toml > /dev/null

bandit:
	PYTHONPATH=src $(PYTHON) -m krybor_rl run experiments/configs/ch02_bandit.toml

plan:
	PYTHONPATH=src $(PYTHON) -m krybor_rl run experiments/configs/ch04_value_iteration.toml
