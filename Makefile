PYTHON := ./venv/bin/python

$(PYTHON):
	python3.10 -m venv venv
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt

.PHONY: clean

clean:
	rm -rf venv
