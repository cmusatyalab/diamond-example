package edu.cmu.cs.diamond.example;

public class StringFind {

    public static void main(String[] args) {
        if (args.length != 1) {
            System.out
                    .println("Please specify exactly 1 search string. (May need to be quoted.)");
            System.exit(1);
        }
    }
}
