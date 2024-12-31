all: run

clean:
	rm -rf .venv build

venv:
	python3 -m venv .venv
	./.venv/bin/pip install -r requirements.txt

run: venv
	./.venv/bin/python src/main.py $(ARGS)

test: venv
	./.venv/bin/python -m unittest discover -s src -p "test_*.py"

train: venv
	mkdir -p build
	./.venv/bin/python src/train.py

demo: venv
	./.venv/bin/python src/demo.py

package:
	rm -rf site
	mkdir -p site
	tar czvf site/pallanguzhi.tar.gz src/* build/*.pth Makefile requirements.txt
