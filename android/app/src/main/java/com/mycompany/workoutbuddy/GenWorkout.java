package com.mycompany.workoutbuddy;

import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import com.loopj.android.http.AsyncHttpClient;
import com.loopj.android.http.AsyncHttpResponseHandler;
import com.loopj.android.http.RequestParams;

import org.apache.http.Header;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import android.util.Log;
import android.view.View;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.ArrayAdapter;
import java.util.List;
import java.util.ArrayList;
import android.content.Context;
import android.content.Intent;
import android.widget.Toast;

public class GenWorkout extends ActionBarActivity {
    private String TAG  = "GenWorkout";
    Context context = this;
    public final static String IncWO = "incWO";
    public final static String IncStep = "incStep";
    public final static String SESSION_ID = "session_id";
    String session_id = "0";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_gen_workout);
        Intent intent = getIntent();
        int workout = intent.getIntExtra(ChooseWorkout.PUSH_PULL, -1);
        final String base_url = "http://Workoutbuddy-1153.appspot.com/api/genPush?category=";
        String request_url = base_url + workout;
        System.out.println(request_url);
        AsyncHttpClient httpClient = new AsyncHttpClient();
        httpClient.get(request_url, new AsyncHttpResponseHandler() {
            @Override
            public void onSuccess(int statusCode, Header[] headers, byte[] response) {
                try {
                    ListView  listview2 = (ListView) findViewById(R.id.lstRight);
                    ArrayList<String> exList = new ArrayList<String>();
                    List<String> setsList = new ArrayList<String>();
                    JSONObject jObject = new JSONObject(new String(response));
                    String reps = jObject.getString("reps");
                    session_id = jObject.getString("session_id");
                    JSONArray ExerciseList = jObject.getJSONArray("exercises");
                    for(int i=0; i < ExerciseList.length(); i++) {
                        exList.add((String) ExerciseList.get(i));
                        setsList.add(reps);
                        System.out.println(exList.get(i));
                    }


                    WorkoutAdapter adapter=new WorkoutAdapter(context, exList, reps);
                    listview2.setAdapter(adapter);

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

    public void ShowSteps(View view){
        Intent intent = new Intent(this, DisplayWorkout.class);
        intent.putExtra(SESSION_ID, session_id);

        final String request_url = "http://Workoutbuddy-1153.appspot.com/api/activateSession";
        RequestParams params = new RequestParams();
        params.put("session_id", session_id);
        params.put("incStep", 0);
        params.put("incWO", -1);
        AsyncHttpClient httpClient = new AsyncHttpClient();
        httpClient.post(request_url, params, new AsyncHttpResponseHandler() {
            @Override
            public void onSuccess(int statusCode, Header[] headers, byte[] response) {
                Log.w("async", "success!!!!");
            }

            public void onFailure(int statusCode, Header[] headers, byte[] errorResponse, Throwable e) {
                Log.e(TAG, "There was a problem in retrieving the url : " + e.toString());
            }
        });


        Toast.makeText(context, "Swipe left to see the following steps. Swipe right to see previous step.", Toast.LENGTH_LONG).show();
        startActivity(intent);
    }
}