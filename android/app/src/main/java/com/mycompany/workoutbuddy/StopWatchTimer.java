package com.mycompany.workoutbuddy;

import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.app.Activity;
import android.os.Bundle;
import android.os.Handler;
import android.os.SystemClock;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

public class StopWatchTimer extends ActionBarActivity {
    private TextView textTimer;
    private Button startButton;
    private Button pauseButton;
    private Button stopButton;
    private long startTime = 0L;
    private Handler myHandler = new Handler();
    long timeInMillies = 0L;
    long timeSwap = 0L;
    long finalTime = 0L;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_stop_watch_timer);

        textTimer = (TextView) findViewById(R.id.textTimer);

        startButton = (Button) findViewById(R.id.btnStart);
        pauseButton = (Button) findViewById(R.id.btnPause);
        stopButton = (Button) findViewById(R.id.btnStop);

        startButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
                startTime = SystemClock.uptimeMillis();
                myHandler.postDelayed(updateTimerMethod, 0);
                pauseButton.setText("Pause");
            }
        });

        pauseButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
                timeSwap += timeInMillies;
                myHandler.removeCallbacks(updateTimerMethod);
                if(pauseButton.getText().equals("Pause")){
                    pauseButton.setText("Reset");
                    Toast.makeText(getApplicationContext(), "Paused", Toast.LENGTH_SHORT).show();
                }
                else if(pauseButton.getText().equals("Reset")){
                    pauseButton.setText("Pause");
                    textTimer.setText("00:00:00");
                    finalTime = 0L;
                    timeInMillies = 0L;
                    timeSwap = 0L;
                }
            }
        });

        stopButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
                timeSwap += timeInMillies;
                myHandler.removeCallbacks(updateTimerMethod);
                Toast.makeText(getApplicationContext(), "Finished Run!", Toast.LENGTH_SHORT).show();
                pauseButton.setText("Pause");
                textTimer.setText("00:00:00");
                finalTime = 0L;
                timeInMillies = 0L;
                timeSwap = 0L;
            }
        });
    }
    private Runnable updateTimerMethod = new Runnable() {

        public void run() {
            timeInMillies = SystemClock.uptimeMillis() - startTime;
            finalTime = timeSwap + timeInMillies;
            int seconds = (int) (finalTime / 1000);
            int minutes = seconds / 60;
            seconds = seconds % 60;
            int milliseconds = (int) (finalTime % 1000);
            textTimer.setText("" + minutes + ":" + String.format("%02d", seconds) + ":"
                                + String.format("%03d", milliseconds));
            myHandler.postDelayed(this, 0);
        }

    };

}
