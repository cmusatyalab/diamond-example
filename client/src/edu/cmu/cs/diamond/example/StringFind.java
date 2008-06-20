package edu.cmu.cs.diamond.example;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;

import edu.cmu.cs.diamond.opendiamond.*;

public class StringFind {

    public static void main(String[] args) {
        if (args.length != 2) {
            System.out.println("usage: fil_string.so string_query");
            System.exit(1);
        }

        // check file
        File codeFile = new File(args[0]);
        if (!codeFile.canRead()) {
            System.out.println("Cannot read \"" + codeFile.toString() + "\"");
            System.exit(1);
        }

        // get search target
        final String target = args[1];

        // Diamond
        try {
            // code
            FilterCode code = new FilterCode(new FileInputStream(codeFile));

            // filter
            Filter stringFilter = new Filter("string", code, "f_eval_string",
                    "f_init_string", "f_fini_string", 1, new String[0],
                    new String[] { target }, 100);

            // searchlet
            Searchlet searchlet = new Searchlet();
            searchlet.addFilter(stringFilter);
            searchlet.setApplicationDependencies(new String[] { "string" });

            // search
            Search s = Search.getSharedInstance();
            s.setScope(ScopeSource.getPredefinedScopeList().get(0));
            s.setSearchlet(searchlet);
            s.start();
            
            // results
            Result r;
            while ((r = s.getNextResult()) != null) {
                processResult(r);
            }
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    public static void processResult(Result r) {
        // some metadata
        String objName = r.getObjectName();
        String serverName = r.getServerName();

        // the object itself
        byte[] data = r.getData();
        int dataLength = data.length;

        // attribute (created by filter)
        int index = Integer.parseInt(Util.extractString(r
                .getValue("string-index")));

        // print
        System.out.println("\"" + objName + "\" on server \"" + serverName
                + "\"");
        System.out.println("data length: " + dataLength);
        System.out.println("found string at index: " + index);
        System.out.println();
    }
}
