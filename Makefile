SRC_ROOT=src

.PHONY: clean_packages
clean_packages:
	find ${SRC_ROOT} -mindepth 1 -maxdepth 1 -type d ! -name 'vimapt' ! -name 'vimrc' -exec rm -r {} \;
	find ${SRC_ROOT} -mindepth 1 -maxdepth 1 -type f ! -name '.gitignore' -exec rm {} \;

.PHONY: helper_tool
helper_tool:
	$(MAKE) -C src/vimapt/tool build

.PHONY: install_vimapt
install_vimapt:
	$(MAKE) -C src/vimapt/library bdist_and_install

.PHONY: install_dependency
install_dependency:
	pip install -r ./src/vimapt/library/requirements.txt
	pip3 install -r ./src/vimapt/library/requirements.txt
