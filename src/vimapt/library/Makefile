PKG_NAME = vimapt-library

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
	find_package=`pip list --format=legacy | grep "${PKG_NAME}" -c`; if [ $$find_package -eq "1" ]; then pip uninstall -y ${PKG_NAME}; fi
	find_package=`pip3 list --format=legacy | grep "${PKG_NAME}" -c`; if [ $$find_package -eq "1" ]; then pip3 uninstall -y ${PKG_NAME}; fi

.PHONY: bdist_and_install
bdist_and_install: bdist uninstall install
	# nothing to do here