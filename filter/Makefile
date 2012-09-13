all: fil_string

clean:
	$(RM) fil_string

fil_string: string-filter.c
	gcc ${LDFLAGS} ${CPPFLAGS} -O2 -g -m32 -Wall -o $@ string-filter.c `pkg-config opendiamond --cflags --libs`
	strip $@

.PHONY: all clean
