package com.example.sakshyam.lrr;

import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.View;
import android.view.animation.Animation;
import android.view.animation.AnimationSet;
import android.view.animation.AnimationUtils;
import android.view.animation.Animation.AnimationListener;
import android.widget.ImageButton;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

public class MainActivity extends AppCompatActivity implements AnimationListener{


    Animation startAnim;
    Animation enterClothes;
    View clothes;
    ImageButton startButton;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.mainscreen);

        startAnim = AnimationUtils.loadAnimation(this, R.anim.dryerstartenter);
        enterClothes = AnimationUtils.loadAnimation(this, R.anim.clothesenter);

        startAnim.setAnimationListener(this);

        startButton = (ImageButton)findViewById(R.id.startButton);
        clothes = (View)findViewById(R.id.clothesSpin);
        clothes.setAlpha(0.0f);

        startButton.setOnClickListener(new View.OnClickListener(){

            @Override
            public void onClick(View v) {
                AnimationSet s = new AnimationSet(false);
                s.addAnimation(startAnim);
                clothes.startAnimation(s);
                clothes.animate().alpha(1.0f);
                clothes.startAnimation(startAnim);
                WMStatus(1);
            }});

    }


    public void WMStatus(Integer Status){
        FirebaseDatabase database = FirebaseDatabase.getInstance();
        DatabaseReference Wmstatus = database.getReference("washingMachine");
        Wmstatus.setValue(Status);
    }

    @Override
    public void onAnimationEnd(Animation animation) {
        // TODO Auto-generated method stub

    }

    @Override
    public void onAnimationRepeat(Animation animation) {
        // TODO Auto-generated method stub

    }

    @Override
    public void onAnimationStart(Animation animation) {
        clothes.setVisibility(View.VISIBLE);


    }

}
