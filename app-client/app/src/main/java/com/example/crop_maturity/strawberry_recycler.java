package com.example.crop_maturity;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.squareup.picasso.MemoryPolicy;
import com.squareup.picasso.NetworkPolicy;
import com.squareup.picasso.Picasso;

import java.util.ArrayList;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class strawberry_recycler extends AppCompatActivity {

    ArrayList<berryModel> detectionArrayList;
    RecyclerView recyler;
    TextView label;
    TextView maturity;
    TextView confidence;
    TextView market_price;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_strawberry_recycler);

        recyler = findViewById(R.id.recyler);
        label = findViewById(R.id.label);
        maturity = findViewById(R.id.maturity);
        confidence = findViewById(R.id.confidence);
        market_price = findViewById(R.id.market_price);

        getDetections();
    }

    private void getDetections() {

        Call<ArrayList<detectResponse>> appResponseCall = loginApi.getService().getPrediction();
        appResponseCall.enqueue(new Callback<ArrayList<detectResponse>>() {
            @Override
            public void onResponse(Call<ArrayList<detectResponse>> call, Response<ArrayList<detectResponse>> response) {
                ArrayList<detectResponse> eventResponse = response.body();
                System.out.println(eventResponse.size());
                detectionArrayList = new ArrayList<berryModel>();
                for(int i=0;i<eventResponse.size();i++)
                {
                    System.out.println("=============="+eventResponse.get(i).status);
                    detectResponse response2 = eventResponse.get(i);
                    detectionArrayList.add(new berryModel(response2.getStatus(),response2.getPrice(),response2.getScore(),response2.getImg_label()));
                }

                BerryAdapter berryAdapter = new BerryAdapter(strawberry_recycler.this, detectionArrayList);
                LinearLayoutManager linearLayoutManager = new LinearLayoutManager(strawberry_recycler.this, LinearLayoutManager.VERTICAL, false);

                recyler.setLayoutManager(linearLayoutManager);
                recyler.setAdapter(berryAdapter);


            }

            @Override
            public void onFailure(Call<ArrayList<detectResponse>> call, Throwable t) {
                String message = "Please Click the photo first or click it properly";
                Toast.makeText(strawberry_recycler.this, message, Toast.LENGTH_LONG).show();
            }
        });

    }
}