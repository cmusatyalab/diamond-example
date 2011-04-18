all: fil_orientation.zip

clean:
	$(RM) *.zip

fil_orientation.zip: fil_orientation.py
	diamond-bundle-python $^

.PHONY: all clean
