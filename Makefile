py_dirs := .
py_files = $(wildcard *.py)

.PHONY: test
test: check
	env/bin/python -m unittest discover $(py_dirs) -p "*.py" -v

.PHONY: fmt
fmt: env_ok
	env/bin/isort --sp .isort.cfg $(py_files)
	env/bin/black $(py_files)

.PHONY: check
check: env_ok
	env/bin/python -m mypy \
		--no-implicit-optional \
		--check-untyped-defs \
		--ignore-missing-imports \
		$(py_dirs)
	env/bin/python -m flake8 --exclude env --select F $(py_dirs)
	env/bin/isort --sp .isort.cfg --check $(py_files)
	env/bin/black --check $(py_files)

env_ok: requirements.txt
	rm -rf env env_ok
	python3 -m venv env
	env/bin/pip install --upgrade pip
	env/bin/pip install -r requirements.txt
	touch env_ok

roadmap.gv: project_spec.py roadmap.py env_ok
	env/bin/python roadmap.py gv > roadmap.gv.tmp
	mv roadmap.gv.tmp roadmap.gv

README.md: project_spec.py roadmap.py env_ok README.template.md
	env/bin/python roadmap.py table > table.tmp
	cat README.template.md table.tmp > README.md
	rm table.tmp

svg_targets := roadmap.gv.svg

%.gv.svg: %.gv
	dot -Tsvg -O $<

.PHONY: build
build: README.md $(svg_targets)

.PHONY: clean
clean:
	rm -rf env env_ok table.tmp
