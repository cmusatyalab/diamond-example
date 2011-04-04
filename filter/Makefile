all: fil_string

clean:
	$(RM) fil_string

fil_string: string-filter.c
	@# glib for base64 decoding
	gcc ${LDFLAGS} ${CPPFLAGS} `pkg-config opendiamond --cflags --libs` `pkg-config glib-2.0 --cflags --libs` -O2 -g -m32 -Wall -o $@ string-filter.c
	strip $@

.PHONY: all clean
