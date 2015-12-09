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
import android.widget.ListView;
import android.widget.TextView;
import android.widget.ArrayAdapter;
import java.util.List;
import java.util.ArrayList;
import android.content.Context;

public class GenWorkout extends ActionBarActivity {
    private String TAG  = "GenWorkout";
    Context context = this;

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
                    ArrayAdapter<String> adapter, adapter2;
                    ListView  listview1 = (ListView) findViewById(R.id.lstLeft);
                    ListView  listview2 = (ListView) findViewById(R.id.lstRight);
                    List<String> exList = new ArrayList<String>();
                    List<String> setsList = new ArrayList<String>();
                    JSONObject jObject = new JSONObject(new String(response));
                    String category = jObject.getString("category");
                    String reps = jObject.getString("reps");
                    //TextView textView = (TextView) findViewById(R.id.category);
                    //textView.setText("Category: " + category);
                    JSONArray ExerciseList = jObject.getJSONArray("exercises");
                    for(int i=0; i < ExerciseList.length(); i++) {
                        exList.add((String) ExerciseList.get(i));
                        setsList.add(reps);
                        System.out.println(exList.get(i));
                    }
                    adapter=new ArrayAdapter<String>(context, android.R.layout.simple_list_item_1, exList);
                    listview1.setAdapter(adapter);
                    adapter2=new ArrayAdapter<String>(context, android.R.layout.simple_list_item_1, setsList);
                    listview2.setAdapter(adapter2);

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
