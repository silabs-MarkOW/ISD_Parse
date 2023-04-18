SCRIPTS = isd-parse.py
BINDIR = ~/bin

default :
	stat ${SCRIPTS}

install :
	install -m755 -d ${BINDIR}
	python3 install-backend.py -b ${BINDIR} ${SCRIPTS}
