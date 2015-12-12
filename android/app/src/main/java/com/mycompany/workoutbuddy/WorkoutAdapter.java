package com.mycompany.workoutbuddy;

import android.widget.BaseAdapter;
import java.util.ArrayList;
import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

/**
 * Created by danielsantamaria on 12/11/15.
 */
public class WorkoutAdapter extends BaseAdapter {
    private Context mContext;
    private ArrayList<String> exList;
    private String sets;

    public WorkoutAdapter(Context c, ArrayList<String> exList, String sets) {
        mContext = c;
        this.exList = exList;
        this.sets = sets;
    }

    public int getCount() {
        return exList.size();
    }

    public Object getItem(int position) {
        return null;
    }

    public long getItemId(int position) {
        return 0;
    }

    public View getView(int position, View convertView, ViewGroup viewGroup){
        if (convertView == null) {
            LayoutInflater inflater = (LayoutInflater) mContext.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
            convertView = inflater.inflate(R.layout.workout_row, null);
        }

        TextView tvExercise = (TextView) convertView.findViewById(R.id.exercise);
        tvExercise.setText(exList.get(position));
        TextView tvSets = (TextView) convertView.findViewById(R.id.sets);
        tvSets.setText(sets);

        return convertView;
    }
}
