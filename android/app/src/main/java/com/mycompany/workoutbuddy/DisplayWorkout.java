package com.mycompany.workoutbuddy;

import android.graphics.Color;
import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import com.loopj.android.http.AsyncHttpClient;
import com.loopj.android.http.AsyncHttpResponseHandler;
import android.content.Context;
import android.content.Intent;
import org.apache.http.Header;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import android.util.Log;
import android.view.View;
import android.app.AlertDialog;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;
import android.content.DialogInterface;

import com.loopj.android.http.RequestParams;
import com.squareup.picasso.Picasso;

public class DisplayWorkout extends ActionBarActivity {
    Context context = this;
    private String TAG  = "DisplayWorkout";
    private String session_id ="0";
    int incWO=0;
    int incStep=0;
    private Boolean lastWO;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_display_workout);
        final String base_url = "http://Workoutbuddy-1153.appspot.com/api/activateSession?session_id=";
        final String imageBaseUrl = "http://Workoutbuddy-1153.appspot.com/img?photo_id=";
        final TextView textView = (TextView) findViewById(R.id.instructions);
        final TextView textViewTitle = (TextView) findViewById(R.id.title);
        final ImageView imageView = (ImageView) findViewById(R.id.imageDisplay);
        Intent intent = getIntent();
        session_id = intent.getStringExtra(GenWorkout.SESSION_ID);
        incStep = intent.getIntExtra(GenWorkout.IncStep,0);
        incWO = intent.getIntExtra(GenWorkout.IncWO,0);
        String request_url = base_url + session_id +"&incStep="+incStep+"&incWO="+incWO;
        System.out.println(request_url);
        AsyncHttpClient httpClient = new AsyncHttpClient();
        httpClient.get(request_url, new AsyncHttpResponseHandler() {
            @Override
            public void onSuccess(int statusCode, Header[] headers, byte[] response) {
                try {
                    JSONObject jObject = new JSONObject(new String(response));
                    String photo_id = jObject.getString("photo");
                    String instructions = jObject.getString("instructions");
                    String WorkoutName = jObject.getString("name");
                    final String session_id = jObject.getString("session_id");
                    final Boolean lastStep = jObject.getBoolean("lastStep");
                    lastWO = jObject.getBoolean("lastWO");
                    String imageUrl = imageBaseUrl + photo_id;
                    System.out.println(imageUrl);

                    Picasso.with(context).load(imageUrl).into(imageView);
                    textView.setText(instructions);
                    textView.setTextColor(Color.BLACK);
                    textViewTitle.setTextColor(Color.BLACK);
                    textViewTitle.setText(WorkoutName);
                    System.out.println("before");

                    imageView.setOnTouchListener(new OnSwipeTouchListener(context){
                        //TODO: swipe Right
                        @Override
                        public void onSwipeLeft(){ //go to next step or workout
                            if((lastWO == Boolean.TRUE) && (lastStep == Boolean.TRUE)){ //end workout
                                System.out.println("last workout");

                                AlertDialog.Builder builder = new AlertDialog.Builder(context);
                                builder.setTitle("Congratulations!");
                                builder.setMessage("You have finished the workout. " +
                                        "Do you wish to add this workout to your workout history?");

                                builder.setPositiveButton("Yes", new DialogInterface.OnClickListener() {
                                    public void onClick(DialogInterface dialog, int id) {
                                        Toast.makeText(context, "Workout Logged.", Toast.LENGTH_SHORT).show();
                                    }
                                });
                                builder.setNegativeButton("No", new DialogInterface.OnClickListener() {
                                    public void onClick(DialogInterface dialog, int id) {
                                        dialog.cancel();
                                    }
                                });
                                builder.show();
                            }
                            else if(lastStep == Boolean.TRUE){ //go to next workout
                                int step = 0; int WO = 1;
                                getNextStep(step, WO);
                                Toast.makeText(context, "Next Workout", Toast.LENGTH_SHORT).show();
                                Intent intent = new Intent(context, DisplayWorkout.class);
                                intent.putExtra(GenWorkout.SESSION_ID, session_id);
                                intent.putExtra(GenWorkout.IncStep, step);
                                intent.putExtra(GenWorkout.IncWO, WO);
                                startActivity(intent);
                            }
                            else{ // go to next step
                                int step = 1; int WO = 0;
                                getNextStep(step, WO);
                                Toast.makeText(context, "Next Step", Toast.LENGTH_SHORT).show();
                                Intent intent = new Intent(context, DisplayWorkout.class);
                                intent.putExtra(GenWorkout.SESSION_ID, session_id);
                                intent.putExtra(GenWorkout.IncStep, step);
                                intent.putExtra(GenWorkout.IncWO, WO);
                                startActivity(intent);
                            }
                        }
                    });

                } catch (JSONException j) {
                    System.out.println("JSON Error");
                    System.out.println(j.getMessage());
                }
            }

            @Override
            public void onFailure(int statusCode, Header[] headers, byte[] errorResponse, Throwable e) {
                Log.e(TAG, "There was a problem in retrieving the url : " + e.toString());
            }
        });
    }

    public void getNextStep(int step, int WO){
        final String request_url = "http://Workoutbuddy-1153.appspot.com/api/activateSession";
        RequestParams params = new RequestParams();
        params.put("session_id", session_id);
        params.put("incStep",step);
        params.put("incWO", WO);
        AsyncHttpClient httpClient = new AsyncHttpClient();
        httpClient.post(request_url, params, new AsyncHttpResponseHandler() {
            @Override
            public void onSuccess ( int statusCode, Header[] headers,byte[] response){
                Log.w("async", "success!!!!");
            }

            public void onFailure ( int statusCode, Header[] headers,byte[] errorResponse, Throwable e){
                Log.e(TAG, "There was a problem in retrieving the url : " + e.toString());
            }
        });
    }

}
