package com.mycompany.workoutbuddy;

import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.util.Log;
import android.widget.ExpandableListView;

import com.loopj.android.http.AsyncHttpClient;
import com.loopj.android.http.AsyncHttpResponseHandler;

import org.apache.http.Header;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import android.widget.ExpandableListView;

import java.util.LinkedHashMap;
import java.util.Map;
import android.content.Context;

public class WorkoutHistory extends ActionBarActivity {
    private String TAG  = "Workout History";
    private Context context = this;
    private Map<String, ArrayList<String>> ExerciseList;
    private Map<String, String> SetsList;

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
                    ArrayList<String> dates = new ArrayList<String>();
                    ArrayList<String> sets = new ArrayList<String>();
                    ArrayList<JSONArray> tempList = new ArrayList<JSONArray>();
                    ArrayList<String> tempList2 = new ArrayList<String>();
                    ArrayList<JSONArray> exerciseList = new ArrayList<JSONArray>();
                    ArrayList<ArrayList<String>> qexerciseList = new ArrayList<ArrayList<String>>();

                    for(int i = 0; i < date.names().length(); i++){
                        dates.add(date.getString(date.names().getString(i)));
                        exerciseList.add(exercises.getJSONArray(date.names().getString(i)));
                        //displayStreams = exercises.getJSONArray(date.names().getString(i));
                        sets.add(reps.getString(date.names().getString(i)));

                    }
                    for (int i = 0; i < exerciseList.size(); i++){
                        JSONArray tmpList = exerciseList.get(i);
                        for (int j = 0; j < tmpList.length(); j++){
                            tempList2.add(tmpList.getString(j));
                        }
                        System.out.println("santa 0");
                        System.out.println(tempList2);
                        qexerciseList.add( new ArrayList<String>(tempList2));
                        System.out.println(qexerciseList);
                        tempList2.clear();
                    }
                    System.out.println("santa 1");
                    System.out.println(qexerciseList);
                    System.out.println("santa 2");
                    System.out.println(exerciseList);
                    System.out.println(dates);
                    System.out.println(sets);
                    System.out.println("hahahahaha");
                    populateMap(dates,qexerciseList,sets);
                    ExpandableListView expListView = (ExpandableListView) findViewById(R.id.ExListView);
                    ExpandableListAdapter expListAdapter = new ExpandableListAdapter(
                            context, ExerciseList, SetsList, dates);
                    expListView.setAdapter(expListAdapter);

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

    public void populateMap(ArrayList<String> dates, ArrayList<ArrayList<String>> exerciseList,
                             ArrayList<String> setsList){
        ArrayList<String> newLIst = new ArrayList<String>();
        ExerciseList = new LinkedHashMap<String, ArrayList<String>>();
        SetsList = new LinkedHashMap<String, String>();
        for (int i = 0; i < dates.size(); i++){
            //System.out.println(dates.get(i));
            //System.out.println(exerciseList.get(i));

            ExerciseList.put(dates.get(i), exerciseList.get(i));
            SetsList.put(dates.get(i), setsList.get(i));
        }
        System.out.println(ExerciseList);
        System.out.println(SetsList);
    }
}
