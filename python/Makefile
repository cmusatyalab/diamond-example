all: orientation.pred

clean:
	$(RM) *.pred

orientation.pred: orientation.xml fil_orientation.py
	diamond-bundle-predicate $^

.PHONY: all clean
