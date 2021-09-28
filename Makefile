ifeq ($(PREFIX),)
	PREFIX = /usr/local
endif

BIN_PATH = $(PREFIX)/bin
MAN_PATH = $(PREFIX)/man
SHARE_PATH = $(PREFIX)/share/wordsearch

install: wordsearch
	install -m 555 wordsearch $(BIN_PATH)

	install -d $(MAN_PATH)
	install -d $(MAN_PATH)/man6
	install -m 644 man/wordsearch.6 $(MAN_PATH)

	install -d $(SHARE_PATH)
	install -m 644 puzzles/*.txt $(SHARE_PATH)
