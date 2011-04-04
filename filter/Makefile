all: fil_string

clean:
	$(RM) fil_string

fil_string: string-filter.c
	gcc ${LDFLAGS} ${CPPFLAGS} `pkg-config opendiamond --cflags --libs` -O2 -g -m32 -Wall -o $@ string-filter.c
	strip $@

.PHONY: all clean
