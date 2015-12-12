package com.mycompany.workoutbuddy;

import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.util.Log;

import com.loopj.android.http.AsyncHttpClient;
import com.loopj.android.http.AsyncHttpResponseHandler;

import org.apache.http.Header;
import org.json.JSONException;
import org.json.JSONObject;

public class WorkoutHistory extends ActionBarActivity {
    private String TAG  = "Workout History";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_workout_history);
        String request_url = "http://Workoutbuddy-1153.appspot.com/api/logWorkout?email="
                                + MainActivity.email;
        System.out.println(request_url);
        AsyncHttpClient httpClient = new AsyncHttpClient();
        httpClient.get(request_url, new AsyncHttpResponseHandler() {
            @Override
            public void onSuccess(int statusCode, Header[] headers, byte[] response) {
                try {
                    JSONObject jObject = new JSONObject(new String(response));
                    JSONObject date = jObject.getJSONObject("date");
                    JSONObject exercises = jObject.getJSONObject("exercises");
                    JSONObject reps = jObject.getJSONObject("reps");
                    //JSONObject category = jObject.getJSONObject("category");
                    for(int i = 0; i < date.names().length(); i++){
                        System.out.println(date.getString( date.names().getString(i) ));
                        System.out.println(exercises.getString( date.names().getString(i) ));
                        System.out.println(reps.getString(date.names().getString(i)));

                    }
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
