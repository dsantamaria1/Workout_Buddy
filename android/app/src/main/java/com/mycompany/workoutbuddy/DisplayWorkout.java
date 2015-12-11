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
import android.widget.ImageView;
import android.widget.TextView;
import com.squareup.picasso.Picasso;

public class DisplayWorkout extends ActionBarActivity {
    Context context = this;
    private String TAG  = "DisplayWorkout";
    String session_id ="0";
    int incWO=0;
    int incStep=0;

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
                    String session_id = jObject.getString("session_id");
                    String lastStep = jObject.getString("lastStep");
                    String lastWO = jObject.getString("lastWO");
                    String imageUrl = imageBaseUrl + photo_id;
                    System.out.println(imageUrl);

                    //imageView.getLayoutParams().width = 1000;
                    //Picasso.with(context).load(imageUrl).fit().into(imageView);
                    Picasso.with(context).load(imageUrl).into(imageView);
                    textView.setText(instructions);
                    textView.setTextColor(Color.BLACK);
                    textViewTitle.setTextColor(Color.BLACK);
                    textViewTitle.setText(WorkoutName);

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
}
