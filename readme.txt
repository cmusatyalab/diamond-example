Diamond Example

19 Jun 2012


The filter directory contains a simple filter that can be used for
searching for text in files. This can be made with make.


The client directory contains a simple Java-based client for testing
the filter. This can be built with Ant. You must have the OpenDiamond Java
library, which is available at <http://diamond.cs.cmu.edu/>.

To run the client, set up diamondd with some text files. Then set
your gid_map/name_map and run the java. The main class is
edu.cmu.cs.diamond.example.StringFind. You will need to give the
location of fil_string as well as a text string to search for.
Results will be printed.


The python directory contains a Python implementation of the text search
filter.  This can be used with the example client as a drop-in replacement
for the C filter.

The python directory also contains a predicate for use with HyperFind which
filters images based on their orientation (horizontal or vertical).  This
can be packaged into a predicate bundle with make.  The bundle can then be
installed in a directory in the HyperFind bundle path or dragged into the
HyperFind window for one-off searches.


The webapp directory contains a sample web application using the JSON
Blaster.  Run webappfind.py with the --help option to get the supported
parameters.
