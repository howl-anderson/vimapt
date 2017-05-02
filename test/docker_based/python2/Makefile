image = xiaoquankong/vimapt_py2
container = vimapt_py2

network = bridge

current_dir = $(shell pwd)

flags =  -it \
        -v $(current_dir)/../../../src/:/data \
        --net=$(network) \
        --name=$(container) \
        $(image)

.PHONY: build
build:
	docker build -t=$(image) .

.PHONY: build_without_cache
build_without_cache:
	docker build --no-cache -t=$(image) .

.PHONY: run
run:
	docker run -d $(flags)

.PHONY: start
start:
	docker start $(container)

.PHONY: stop
stop:
	docker stop $(container)


.PHONY: attach
attach:
	docker exec -it $(container) bash

