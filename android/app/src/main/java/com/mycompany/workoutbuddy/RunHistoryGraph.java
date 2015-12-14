package com.mycompany.workoutbuddy;

import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import com.jjoe64.graphview.GraphView;
import com.jjoe64.graphview.series.BarGraphSeries;
import com.jjoe64.graphview.series.DataPoint;
import com.jjoe64.graphview.GridLabelRenderer.GridStyle;
import com.jjoe64.graphview.series.LineGraphSeries;
import com.jjoe64.graphview.helper.DateAsXAxisLabelFormatter;
import com.jjoe64.graphview.helper.StaticLabelsFormatter;
import com.jjoe64.graphview.series.PointsGraphSeries;
import com.loopj.android.http.AsyncHttpClient;
import com.loopj.android.http.AsyncHttpResponseHandler;

import java.util.Calendar;
import java.util.Date;
import android.content.Context;
import android.util.Log;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import org.apache.http.Header;

public class RunHistoryGraph extends ActionBarActivity {
    private Context context = this;
    private String TAG  = "Run History";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_run_history_graph);

        String request_url = "http://Workoutbuddy-1153.appspot.com/api/logRun?email="
                + MainActivity.email;
        System.out.println(request_url);
        AsyncHttpClient httpClient = new AsyncHttpClient();
        httpClient.get(request_url, new AsyncHttpResponseHandler() {
            @Override
            public void onSuccess(int statusCode, Header[] headers, byte[] response) {
                try {
                    JSONObject jObject = new JSONObject(new String(response));
                    JSONArray keyList = jObject.getJSONArray("testList");
                    JSONArray dateList = jObject.getJSONArray("dateList");
                    JSONObject timeDict = jObject.getJSONObject("timeDict");

                    for(int i = 0; i < keyList.length(); i++) {
                        System.out.println("starting prints");
                        System.out.println(keyList.getString(i));
                        System.out.println(timeDict.getDouble(keyList.getString(i)));
                        System.out.println(dateList.getString(i));
                    }






                    GraphView graph = (GraphView) findViewById(R.id.graph);
// you can directly pass Date objects to DataPoint-Constructor
// this will convert the Date to double via Date#getTime()
                    BarGraphSeries<DataPoint> series = new BarGraphSeries<DataPoint>(new DataPoint[] {
                            new DataPoint(1, 30.3),
                            new DataPoint(2, 29.5),
                            new DataPoint(3, 12.3),
                            new DataPoint(4, 18.6),
                            new DataPoint(5, 25.7)
                    });
                    graph.addSeries(series);

// set date label formatter
                    //graph.getGridLabelRenderer().setLabelFormatter(new DateAsXAxisLabelFormatter(context));
                    //graph.getGridLabelRenderer().setNumHorizontalLabels(3); // only 4 because of the space
                    String[] WEEK_DAYS = {"12/12", "12/13", "12/14", "12/15", "12/10"};
                    StaticLabelsFormatter staticLabelsFormatter = new StaticLabelsFormatter(graph);
                    staticLabelsFormatter.setHorizontalLabels(WEEK_DAYS);
                    graph.getGridLabelRenderer().setLabelFormatter(staticLabelsFormatter);
                    graph.getGridLabelRenderer().setGridStyle(GridStyle.NONE);

                    graph.getViewport().setYAxisBoundsManual(true);
                    graph.getViewport().setMinY(0);
                    series.setSpacing(10);
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
