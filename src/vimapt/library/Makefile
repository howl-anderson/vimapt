.PHONY: sdist
sdist:
	python setup.py sdist

.PHONY: bdist
bdist:
	python setup.py bdist_wheel --universal

.PHONY: clean

.PHONY: deb

.PHONY: install
intall:
	pip install dist/vimapt-*.whl
	pip3 install dist/vimapt-*.whl

.PHONY: uninstall
uninstall:
	pip uninstall -y vimapt
	pip3 uninstall -y vimapt

.PHONY: bdist_and_install
bdist_and_install: bdist uninstall intall
	# nothing to do here