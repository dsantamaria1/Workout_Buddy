package com.mycompany.workoutbuddy;

import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.app.Activity;
import android.os.Bundle;
import android.os.Handler;
import android.os.SystemClock;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import com.loopj.android.http.AsyncHttpClient;
import com.loopj.android.http.AsyncHttpResponseHandler;
import com.loopj.android.http.RequestParams;
import android.content.Context;
import org.apache.http.Header;

public class StopWatchTimer extends ActionBarActivity {
    private Context context = this;
    private String TAG  = "Stop Watch Timer";
    private TextView textTimer;
    private Button startButton;
    private Button pauseButton;
    private Button stopButton;
    private long startTime = 0L;
    private Handler myHandler = new Handler();
    long timeInMillies = 0L;
    long timeSwap = 0L;
    long finalTime = 0L;

    private int seconds = 0;
    private int minutes = 0;
    private int milliseconds = 0;

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
                startButton.setClickable(false);
            }
        });

        pauseButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
                timeSwap += timeInMillies;
                myHandler.removeCallbacks(updateTimerMethod);
                startButton.setClickable(true);
                if(pauseButton.getText().equals("Pause")){
                    pauseButton.setText("Reset");
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
                startButton.setClickable(true);
                System.out.println("builder?");

                AlertDialog.Builder builder = new AlertDialog.Builder(context);
                builder.setTitle("Congrats!");
                builder.setMessage("Do you wish to add this run to your history?");

                builder.setPositiveButton("Yes", new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int id) {
                        if (MainActivity.email != null) {
                            logRun(minutes, seconds, milliseconds);
                            Toast.makeText(getApplicationContext(), "Run Posted.", Toast.LENGTH_SHORT).show();
                            Intent intent = new Intent(getApplicationContext(), MainActivity.class);
                            startActivity(intent);
                            finish();
                        } else {
                            //TODO: add login capability if not currently logged in.
                            Toast.makeText(getApplicationContext(), "You are not Logged in.", Toast.LENGTH_LONG).show();
                        }
                    }
                });
                builder.setNegativeButton("No", new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int id) {
                        dialog.cancel();
                        Intent intent = new Intent(context, MainActivity.class);
                        startActivity(intent);
                        finish();
                    }
                });
                builder.show();
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

            seconds = (int) (finalTime / 1000);
            minutes = seconds / 60;
            seconds = seconds % 60;
            milliseconds = (int) (finalTime % 1000);
            textTimer.setText("" + minutes + ":" + String.format("%02d", seconds) + ":"
                    + String.format("%03d", milliseconds));
            myHandler.postDelayed(this, 0);
        }

    };

    public void logRun(int minutes, int seconds, int milliseconds){
        final String request_url = "http://Workoutbuddy-1153.appspot.com/api/logRun";
        String time = "";
        time = String.valueOf(minutes) + "." + String.valueOf(seconds);
        System.out.println("logRun");
        System.out.println(minutes);
        System.out.println(seconds);
        System.out.println(time);
        RequestParams params = new RequestParams();
        params.put("email", MainActivity.email);
        params.put("time", time);

        AsyncHttpClient httpClient = new AsyncHttpClient();
        httpClient.post(request_url, params, new AsyncHttpResponseHandler() {
            @Override
            public void onSuccess(int statusCode, Header[] headers, byte[] response) {
                Log.w("async", "log workout success!!!!");
            }

            public void onFailure(int statusCode, Header[] headers, byte[] errorResponse, Throwable e) {
                Log.e(TAG, "There was a problem in retrieving the url : " + e.toString());
            }
        });
    }
}
