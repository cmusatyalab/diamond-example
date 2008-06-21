Diamond Example

20 Jun 2008


The filter directory contains a simple filter that can be used for
searching for text in files. This can be made with make.

The client directory contains a simple Java-based client for testing
the filter. The easiest(?) way to build is by importing into Eclipse.
Do this after importing the OpenDiamond java project into Eclipse.
OpenDiamond Java Bindings are from http://diamond.cs.cmu.edu/

To run the client, set up adiskd with some text files. Then set
your gid_map/name_map and run the java. The main class is
edu.cmu.cs.diamond.example.StringFind. You will need to give the
location of fil_string.so as well as a text string to search for.
Results will be printed.
