package com.mobisec.babyrev;

import android.os.Bundle;
import android.support.v4.internal.view.SupportMenu;
import android.support.v7.app.AppCompatActivity;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
/* loaded from: classes.dex */
public class MainActivity extends AppCompatActivity {
    TextView mResultWidget = null;

    /* JADX INFO: Access modifiers changed from: protected */
    @Override // android.support.v7.app.AppCompatActivity, android.support.v4.app.FragmentActivity, android.support.v4.app.SupportActivity, android.app.Activity
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        final EditText flagWidget = (EditText) findViewById(R.id.flag);
        Button checkFlag = (Button) findViewById(R.id.checkflag);
        final TextView resultWidget = (TextView) findViewById(R.id.result);
        this.mResultWidget = resultWidget;
        flagWidget.addTextChangedListener(new TextWatcher() { // from class: com.mobisec.babyrev.MainActivity.1
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
        checkFlag.setOnClickListener(new View.OnClickListener() { // from class: com.mobisec.babyrev.MainActivity.2
            @Override // android.view.View.OnClickListener
            public void onClick(View v) {
                String msg;
                int color;
                String flag = flagWidget.getText().toString();
                boolean result = FlagChecker.checkFlag(MainActivity.this, flag);
                if (result) {
                    msg = "Valid flag!";
                    color = -16737536;
                } else {
                    msg = "Invalid flag";
                    color = SupportMenu.CATEGORY_MASK;
                }
                resultWidget.setText(msg);
                resultWidget.setTextColor(color);
            }
        });
    }
}
