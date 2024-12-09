all: run

clean:
	rm -rf .venv

venv:
	python3 -m venv .venv
	./.venv/bin/pip install -r requirements.txt

run: venv
	./.venv/bin/python src/main.py

test: venv
	./.venv/bin/python -m unittest discover -s tests
