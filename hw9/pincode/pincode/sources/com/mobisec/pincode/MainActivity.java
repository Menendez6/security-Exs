package com.mobisec.pincode;

import android.os.Bundle;
import android.os.StrictMode;
import android.support.v4.internal.view.SupportMenu;
import android.support.v4.view.ViewCompat;
import android.support.v7.app.AppCompatActivity;
import android.text.Editable;
import android.text.TextWatcher;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
/* loaded from: classes2.dex */
public class MainActivity extends AppCompatActivity {
    TextView mResultWidget = null;

    /* JADX INFO: Access modifiers changed from: protected */
    @Override // android.support.v7.app.AppCompatActivity, android.support.v4.app.FragmentActivity, android.support.v4.app.SupportActivity, android.app.Activity
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);
        final EditText pinWidget = (EditText) findViewById(R.id.pincode);
        Button checkPin = (Button) findViewById(R.id.checkpin);
        final TextView resultWidget = (TextView) findViewById(R.id.result);
        this.mResultWidget = resultWidget;
        pinWidget.addTextChangedListener(new TextWatcher() { // from class: com.mobisec.pincode.MainActivity.1
            @Override // android.text.TextWatcher
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {
            }

            @Override // android.text.TextWatcher
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                MainActivity.this.mResultWidget.setText(BuildConfig.FLAVOR);
            }

            @Override // android.text.TextWatcher
            public void afterTextChanged(Editable s) {
            }
        });
        checkPin.setOnClickListener(new View.OnClickListener() { // from class: com.mobisec.pincode.MainActivity.2
            @Override // android.view.View.OnClickListener
            public void onClick(View v) {
                String pin = pinWidget.getText().toString();
                resultWidget.setText("Checking PIN....");
                resultWidget.setTextColor(ViewCompat.MEASURED_STATE_MASK);
                boolean pinValid = PinChecker.checkPin(MainActivity.this, pin);
                String flag = null;
                String exception = null;
                if (!pinValid) {
                    resultWidget.setText("PIN is not valid.");
                    resultWidget.setTextColor(SupportMenu.CATEGORY_MASK);
                    return;
                }
                try {
                    flag = MainActivity.this.getFlag(pin);
                } catch (Exception e) {
                    exception = e.getMessage();
                }
                if (exception != null) {
                    resultWidget.setText("PIN was valid, but there was an exception getting the flag...");
                    resultWidget.setTextColor(SupportMenu.CATEGORY_MASK);
                } else if (flag != null) {
                    TextView textView = resultWidget;
                    textView.setText("PIN was valid! Here is the message from the server: " + flag);
                    if (!flag.startsWith("FLAG")) {
                        resultWidget.setTextColor(SupportMenu.CATEGORY_MASK);
                    } else {
                        resultWidget.setTextColor(-16737536);
                    }
                } else {
                    TextView textView2 = resultWidget;
                    textView2.setText("PIN was valid, but something went wrong. Exception: " + exception);
                    resultWidget.setTextColor(SupportMenu.CATEGORY_MASK);
                }
            }
        });
    }

    public String getFlag(String pin) {
        String url = "https://challs.reyammer.io/pincode/" + pin;
        try {
            String ans = getUrlContent(url);
            return ans;
        } catch (FileNotFoundException e) {
            return "Too many requests, slow down. You can do at most 10 requests per minute.";
        } catch (Exception e2) {
            String ans2 = "Exception: " + Log.getStackTraceString(e2);
            Log.e("MOBISEC", "Exception: " + Log.getStackTraceString(e2));
            return ans2;
        }
    }

    public static String getUrlContent(String sUrl) throws Exception {
        URL url = new URL(sUrl);
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        connection.setRequestMethod("GET");
        connection.connect();
        BufferedReader rd = new BufferedReader(new InputStreamReader(connection.getInputStream()));
        String content = BuildConfig.FLAVOR;
        while (true) {
            String line = rd.readLine();
            if (line != null) {
                content = content + line + "\n";
            } else {
                return content;
            }
        }
    }
}
