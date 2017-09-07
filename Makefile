.PHONY: test run

test:
	nosetests3 test/

run:
	python3 -m gosmorewebapi.server

run-dev:
	cd src/python
	python3 -m gosmorewebapi.server
	cd ../..

install:
	cp -a src/python/* /usr/lib/python3/dist-packages/
	pip3 install -r requirements.txt

uninstall:
	rm -rf /usr/lib/python3/dist-packages/gosmorewebapi
