.PHONY: init run

init:
	chmod +x scripts/init.sh
	scripts/init.sh

run:
	chmod +x scripts/run.sh
	scripts/run.sh