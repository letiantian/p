PREFIX ?= /usr/local/bin

install: bin/p.py
	cp $< $(PREFIX)/p
	chmod +x $(PREFIX)/p

uninstall:
	rm -f $(PREFIX)/p

.PHONY: install uninstall