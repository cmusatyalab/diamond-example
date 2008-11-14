/*
 * Diamond example client
 *
 * This code is licensed under a permissive license and is meant to be
 * copied and incorporated into other projects.
 *
 * Copyright (c) 2008, Carnegie Mellon University
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 *  * Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 *
 *  * Redistributions in binary form must reproduce the above
 *    copyright notice, this list of conditions and the following
 *    disclaimer in the documentation and/or other materials provided
 *    with the distribution.
 *
 *  * Neither the name of the Carnegie Mellon University nor the names
 *    of its contributors may be used to endorse or promote products
 *    derived from this software without specific prior written
 *    permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
 * FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
 * COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
 * INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
 * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
 * STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
 * OF THE POSSIBILITY OF SUCH DAMAGE.
 */

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
