package com.mobisec.babyrev;

import android.content.Context;
/* loaded from: classes.dex */
public class FlagChecker {
    public static boolean checkFlag(Context ctx, String flag) {
        if (flag.startsWith("MOBISEC{") && new StringBuilder(flag).reverse().toString().charAt(0) == '}' && flag.length() == 35 && flag.toLowerCase().substring(8).startsWith("this_is_") && new StringBuilder(flag).reverse().toString().toLowerCase().substring(1).startsWith(ctx.getString(R.string.last_part)) && flag.charAt(17) == '_' && flag.charAt((int) (getY() * Math.pow(getX(), getY()))) == flag.charAt(((int) Math.pow(Math.pow(2.0d, 2.0d), 2.0d)) + 1) && bam(flag.toUpperCase().substring(getY() * getX() * getY(), (int) (Math.pow(getZ(), getX()) - 1.0d))).equals("ERNYYL") && flag.toLowerCase().charAt(16) == 'a' && flag.charAt(16) == flag.charAt(26) && flag.toUpperCase().charAt(25) == flag.toUpperCase().charAt(26) + 1) {
            String r = getR();
            return flag.substring(8, flag.length() - 1).matches(r);
        }
        return false;
    }

    private static int getX() {
        return 2;
    }

    private static int getY() {
        return 3;
    }

    private static int getZ() {
        return 5;
    }

    //bam(flag.toUpperCase().substring(getY() * getX() * getY(), (int) (Math.pow(getZ(), getX()) - 1.0d))).equals("ERNYYL")
    
    private static String bam(String s) {
        String out = BuildConfig.FLAVOR;
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c >= 'a' && c <= 'm') {
                c = (char) (c + '\r');
            } else if (c >= 'A' && c <= 'M') {
                c = (char) (c + '\r');
            } else if (c >= 'n' && c <= 'z') {
                c = (char) (c - '\r');
            } else if (c >= 'N' && c <= 'Z') {
                c = (char) (c - '\r');
            }
            out = out + c;
        }
        return out;
    }

    public static String getR() {
        String r = BuildConfig.FLAVOR;
        boolean upper = true;
        for (int i = 0; i < 26; i++) {
            r = upper ? r + "[A-Z_]" : r + "[a-z_]";
            upper = !upper;
        }
        return r;
    }
}
