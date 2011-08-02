all: fil_orientation.search

clean:
	$(RM) *.search

fil_orientation.search: fil_orientation.xml fil_orientation.py
	diamond-bundle-search $^

.PHONY: all clean
