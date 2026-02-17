PREFIX ?= /usr/local
DESTDIR ?=

APPDIR := $(DESTDIR)$(PREFIX)/Lumivio
BINDIR := $(DESTDIR)$(PREFIX)/bin
DESKTOPDIR := $(DESTDIR)/usr/share/applications

install:
	install -d "$(APPDIR)" "$(BINDIR)" "$(DESKTOPDIR)"
	cp -a usr/local/Lumivio/. "$(APPDIR)/"
	install -m 755 usr/local/bin/lumivio "$(BINDIR)/lumivio"
	install -m 644 usr/share/applications/lumivio.desktop "$(DESKTOPDIR)/lumivio.desktop"
	@echo "Installed Lumivio."

uninstall:
	rm -f "$(BINDIR)/lumivio"
	rm -f "$(DESKTOPDIR)/lumivio.desktop"
	rm -rf "$(APPDIR)"
	@echo "Removed Lumivio."
