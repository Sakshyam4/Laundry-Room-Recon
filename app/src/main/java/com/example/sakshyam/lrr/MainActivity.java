package com.example.sakshyam.lrr;

import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.view.animation.Animation;
import android.view.animation.AnimationSet;
import android.view.animation.AnimationUtils;
import android.view.animation.Animation.AnimationListener;
import android.widget.ImageButton;

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import java.util.ArrayList;
import java.util.List;

public class MainActivity extends AppCompatActivity implements AnimationListener{


    Animation startAnim;
    Animation enterClothes;
    View clothes;
    View slidein;
    View startview;
    ImageButton startButton;
    Integer checkWMStatus=0;
    Integer checkDoorStatus=0;
    //FirebaseDatabase database = FirebaseDatabase.getInstance();
    //DatabaseReference Wmstatus = database.getReference("washingMachine/runningStatus");
    //@Override
    FirebaseDatabase firebaseDatabase;
    DatabaseReference databaseReference;
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.mainscreen);


        firebaseDatabase=FirebaseDatabase.getInstance();
        databaseReference=firebaseDatabase.getReferenceFromUrl("https://laundry-room-recon.firebaseio.com/");



        startAnim = AnimationUtils.loadAnimation(this, R.anim.dryerstartenter);
        enterClothes = AnimationUtils.loadAnimation(this, R.anim.clothesenter);

        startAnim.setAnimationListener(this);

        startButton = (ImageButton)findViewById(R.id.startButton);
        clothes = (View)findViewById(R.id.clothesSpin);
        clothes.setAlpha(0.0f);

        slidein = (View)findViewById(R.id.rightSlider);
        slidein.setAlpha(0.0f);
        slidein.setX(-1000);
        startview = (View)findViewById(R.id.readystate);



        startButton.setOnClickListener(new View.OnClickListener(){

            @Override
            public void onClick(View v) {
                //System.out.println("Blam");
                //Log.i("as","bamn");
                AnimationSet s = new AnimationSet(false);
                s.addAnimation(startAnim);
                clothes.startAnimation(s);
                clothes.animate().alpha(1.0f);
                clothes.startAnimation(startAnim);
                WMStatus(1);
                slidein.animate().alpha(1.0f);
                slidein.animate().x(0);
                startview.animate().x(-1000);
            }});



        DatabaseReference mReadRunningStatus=databaseReference.child("washingMachine").child("runningStatus");
        mReadRunningStatus.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                checkWMStatus=dataSnapshot.getValue(Integer.class);
                Log.i("check:",""+checkWMStatus);

                if(checkWMStatus==1){
                    //System.out.println("Blam");
                    //Log.i("as","bamn");

                    AnimationSet s = new AnimationSet(false);
                    s.addAnimation(startAnim);
                    clothes.startAnimation(s);
                    clothes.animate().alpha(1.0f);
                    clothes.startAnimation(startAnim);

                    slidein.animate().alpha(1.0f);
                    slidein.animate().x(0);
                    startview.animate().x(-1000);
                }
                if(checkWMStatus==0){

                    startButton = (ImageButton)findViewById(R.id.startButton);
                    clothes = (View)findViewById(R.id.clothesSpin);
                    clothes.setAlpha(0.0f);

                    slidein = (View)findViewById(R.id.rightSlider);
                    slidein.setAlpha(0.0f);
                    slidein.animate().x(-1000);
                    startview.animate().x(0);


                    startButton.setOnClickListener(new View.OnClickListener(){

                        @Override
                        public void onClick(View v) {
                            //System.out.println("Blam");
                            //Log.i("as","bamn");
                            AnimationSet s = new AnimationSet(false);
                            s.addAnimation(startAnim);
                            clothes.startAnimation(s);
                            clothes.animate().alpha(1.0f);
                            clothes.startAnimation(startAnim);
                            WMStatus(1);
                            slidein.animate().alpha(1.0f);
                            slidein.animate().x(0);
                            startview.animate().x(-1000);
                        }});

                }

            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {

            }
        });

        //ValueSetListener for Door
        DatabaseReference mReadDoor=databaseReference.child("washingMachine").child("doorSensor");
        mReadDoor.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                checkDoorStatus=dataSnapshot.getValue(Integer.class);
                Log.i("checkDoor:",""+checkDoorStatus);

                if(checkDoorStatus==1){
                    Log.i("DoorStatus: ", "Door is Open");
                }
                if(checkDoorStatus==0){
                    Log.i("DoorStatus: ", "Door is Closed");
                }
            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {

            }
        });







    }




    public void WMStatus(Integer Status){

        DatabaseReference mchild=databaseReference;
        mchild.child("washingMachine").child("runningStatus").setValue(Status);
        //Wmstatus.setValue(Status);
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
