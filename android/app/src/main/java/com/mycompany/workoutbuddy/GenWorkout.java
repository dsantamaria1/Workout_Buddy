package com.mycompany.workoutbuddy;

import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import com.loopj.android.http.AsyncHttpClient;
import com.loopj.android.http.AsyncHttpResponseHandler;
import org.apache.http.Header;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import android.util.Log;

public class GenWorkout extends ActionBarActivity {
    private String TAG  = "GenWorkout";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_gen_workout);

        final String request_url = "http://Workoutbuddy-1153.appspot.com/api/genPush?category=0";

        AsyncHttpClient httpClient = new AsyncHttpClient();
        httpClient.get(request_url, new AsyncHttpResponseHandler() {
            @Override
            public void onSuccess(int statusCode, Header[] headers, byte[] response) {
                try {
                    JSONObject jObject = new JSONObject(new String(response));
                    JSONArray ExerciseList = jObject.getJSONArray("exercises");
                    for(int i=0; i < ExerciseList.length(); i++) {
                        System.out.println(ExerciseList.get(i));
                        //JSONObject exercise = ExerciseList.getJSONObject(i);
                        //System.out.println("exercise is " + exercise);
                    }
                }
                catch (JSONException j){
                    System.out.println("JSON Error");
                }
            }
            @Override
            public void onFailure(int statusCode, Header[] headers, byte[] errorResponse, Throwable e) {
                Log.e(TAG, "There was a problem in retrieving the url : " + e.toString());
            }
        });
    }
}
