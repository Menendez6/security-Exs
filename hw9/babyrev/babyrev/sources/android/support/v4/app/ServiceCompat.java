package android.support.v4.app;

import android.app.Service;
import android.os.Build;
import android.support.annotation.NonNull;
import android.support.annotation.RestrictTo;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
/* loaded from: classes2.dex */
public final class ServiceCompat {
    public static final int START_STICKY = 1;
    public static final int STOP_FOREGROUND_DETACH = 2;
    public static final int STOP_FOREGROUND_REMOVE = 1;

    @Retention(RetentionPolicy.SOURCE)
    @RestrictTo({RestrictTo.Scope.LIBRARY_GROUP})
    /* loaded from: classes2.dex */
    public @interface StopForegroundFlags {
    }

    private ServiceCompat() {
    }

    public static void stopForeground(@NonNull Service service, int flags) {
        if (Build.VERSION.SDK_INT >= 24) {
            service.stopForeground(flags);
        } else {
            service.stopForeground((flags & 1) != 0);
        }
    }
}
