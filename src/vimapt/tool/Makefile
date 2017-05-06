.PHONY: build
build:
	debuild -i -us -uc -b

PKG_NAME = vimapt_tools

.PHONY: sdist
sdist:
	python setup.py sdist

.PHONY: bdist
bdist:
	python setup.py bdist_wheel --universal

.PHONY: clean

.PHONY: deb

.PHONY: install
install:
	pip install dist/*.whl
	pip3 install dist/*.whl

.PHONY: uninstall
uninstall:
	pip uninstall -y ${PKG_NAME}
	pip3 uninstall -y ${PKG_NAME}

.PHONY: bdist_and_install
bdist_and_install: bdist uninstall install
	# nothing to do here