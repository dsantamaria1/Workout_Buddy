package com.mycompany.workoutbuddy;

import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.content.Intent;
import android.view.View;

public class ChooseWorkout extends ActionBarActivity {
    public final static String PUSH_PULL  = "push_pull";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_choose_workout);
    }

    public void GetPushWorkout(View view){
        Intent intent = new Intent(this, GenWorkout.class);
        intent.putExtra(PUSH_PULL, 0);
        startActivity(intent);
    }
    public void GetPullWorkout(View view){
        Intent intent = new Intent(this, GenWorkout.class);
        intent.putExtra(PUSH_PULL, 1);
        startActivity(intent);
    }

}
