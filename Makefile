SRC_ROOT=src

.PHONY: clean_packages
clean_packages:
	find ${SRC_ROOT} -mindepth 1 -maxdepth 1 -type d ! -name 'vimapt' ! -name 'vimrc' -exec rm -r {} \;
	find ${SRC_ROOT} -mindepth 1 -maxdepth 1 -type f ! -name '.gitignore' -exec rm {} \;

.PHONY: helper_tool
helper_tool:
	cd src/vimapt/bin & debuild -i -us -uc -b

.PHONY: python_vimapt
python_vimpapt:
	# this is a placeholder for build vimapt's python package

.PHONY: install_dependency
install_dependency:
	pip install -r ./src/vimapt/library/requirements.txt
	pip3 install -r ./src/vimapt/library/requirements.txt
