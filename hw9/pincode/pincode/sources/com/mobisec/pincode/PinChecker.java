package com.mobisec.pincode;

import android.content.Context;
import android.util.Log;
import java.security.MessageDigest;
/* loaded from: classes2.dex */
class PinChecker {
    PinChecker() {
    }

    public static boolean checkPin(Context ctx, String pin) {
        if (pin.length() != 6) {
            return false;
        }
        try {
            byte[] pinBytes = pin.getBytes();
            for (int i = 0; i < 25; i++) {
                for (int j = 0; j < 400; j++) {
                    MessageDigest md = MessageDigest.getInstance("MD5");
                    md.update(pinBytes);
                    byte[] digest = md.digest();
                    pinBytes = (byte[]) digest.clone();
                }
            }
            String hexPinBytes = toHexString(pinBytes);
            return hexPinBytes.equals("d04988522ddfed3133cc24fb6924eae9");
        } catch (Exception e) {
            Log.e("MOBISEC", "Exception while checking pin");
            return false;
        }
    }

    public static String toHexString(byte[] bytes) {
        StringBuilder hexString = new StringBuilder();
        for (byte b : bytes) {
            String hex = Integer.toHexString(b & 255);
            if (hex.length() == 1) {
                hexString.append('0');
            }
            hexString.append(hex);
        }
        return hexString.toString();
    }
}
