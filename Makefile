all: run

clean:
	rm -rf .venv build

venv:
	uv sync

run: venv
	uv run src/main.py $(ARGS)

test: venv
	uv run -m unittest discover -s src -p "test_*.py"

train: venv
	mkdir -p build
	uv run src/train.py

demo: venv
	uv run src/demo.py

package:
	rm -rf site
	mkdir -p site
	tar czvf site/pallanguzhi.tar.gz src/* build/*.pth Makefile pyproject.toml uv.lock
