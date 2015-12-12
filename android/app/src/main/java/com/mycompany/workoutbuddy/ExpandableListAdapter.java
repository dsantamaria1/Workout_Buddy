package com.mycompany.workoutbuddy;

import android.graphics.Typeface;
import android.view.LayoutInflater;
import android.widget.BaseExpandableListAdapter;
import android.content.Context;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

/**
 * Created by danielsantamaria on 12/12/15.
 */
public class ExpandableListAdapter extends BaseExpandableListAdapter {
    private Context mContext;
    private Map<String, ArrayList<String>> ExerciseList;
    private Map<String, String> SetsList;
    private ArrayList<String> dates;

    public ExpandableListAdapter(Context c, Map<String, ArrayList<String>> ExerciseList,
                                 Map<String, String> SetsList, ArrayList<String> dates){
        this.mContext = c;
        this.ExerciseList = ExerciseList;
        this.SetsList = SetsList;
        this.dates = dates;
    }

    public long getChildId(int groupPosition, int childPosition) {
        return childPosition;
    }

    public Object getChild(int groupPosition, int childPosition) {
        return ExerciseList.get(dates.get(groupPosition)).get(childPosition);
    }

    public Object getChild2(int groupPosition) {
        return SetsList.get(dates.get(groupPosition));
    }

    public View getChildView(int groupPosition, int childPosition, boolean isLastChild,
                             View convertView, ViewGroup parent){
        if (convertView == null) {
            LayoutInflater inflater = (LayoutInflater) mContext.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
            convertView = inflater.inflate(R.layout.child_item, null);
        }
        String exercise = (String) getChild(groupPosition, childPosition);
        String sets = (String) getChild2(groupPosition);

        TextView tvExercise = (TextView) convertView.findViewById(R.id.exercise);
        TextView tvSets = (TextView) convertView.findViewById(R.id.sets);
        tvExercise.setText(exercise);
        tvSets.setText(sets);
        return convertView;
    }

    public int getChildrenCount(int groupPosition) {
        return ExerciseList.get(dates.get(groupPosition)).size();
    }

    public Object getGroup(int groupPosition) {
        return dates.get(groupPosition);
    }

    public int getGroupCount() {
        return dates.size();
    }

    public long getGroupId(int groupPosition) {
        return groupPosition;
    }

    public View getGroupView(int groupPosition, boolean isExpanded,
                             View convertView, ViewGroup parent) {
        String date = (String) getGroup(groupPosition);

        if (convertView == null) {
            LayoutInflater inflater = (LayoutInflater) mContext.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
            convertView = inflater.inflate(R.layout.group_item, null);
        }

        TextView tvDateGroup = (TextView) convertView.findViewById(R.id.date);
        tvDateGroup.setTypeface(null, Typeface.BOLD);
        tvDateGroup.setText(date);
        return convertView;
    }

    public boolean isChildSelectable(int groupPosition, int childPosition) {
        return true;
    }

    public boolean hasStableIds() {
        return true;
    }
}
