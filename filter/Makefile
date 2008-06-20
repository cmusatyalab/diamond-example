all: fil_example.so

clean:
	$(RM) *.so

fil_example.so: example-filter.c
	gcc -fPIC ${LDFLAGS} ${CPPFLAGS} `pkg-config opendiamond --cflags` -O2 -g -m32 -Wall -shared -o $@ example-filter.c
	strip $@

.PHONY: all clean
