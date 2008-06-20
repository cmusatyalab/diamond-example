all: fil_string.so

clean:
	$(RM) *.so

fil_string.so: string-filter.c
	gcc -fPIC ${LDFLAGS} ${CPPFLAGS} `pkg-config opendiamond --cflags` -O2 -g -m32 -Wall -shared -o $@ string-filter.c
	strip $@

.PHONY: all clean
