package com.example.crop_maturity;
import android.annotation.SuppressLint;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.text.Html;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;


import com.example.crop_maturity.R;
import com.example.crop_maturity.berryModel;

import org.w3c.dom.Text;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class BerryAdapter extends RecyclerView.Adapter<BerryAdapter.ViewHolder> {

    private final Context context;
    private final ArrayList<berryModel> detectionArrayList;


    // Constructor
    public BerryAdapter(Context context, ArrayList<berryModel> detectionArrayList) {
        this.context = context;
        this.detectionArrayList = detectionArrayList;

    }

    @NonNull
    @Override
    public BerryAdapter.ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        // to inflate the layout for each item of recycler view.
        View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.card_layout, parent, false);
        return new ViewHolder(view);
    }

    @SuppressLint("SetTextI18n")
    @Override
    public void onBindViewHolder(@NonNull BerryAdapter.ViewHolder holder, int position) {
        // to set data to textview and imageview of each card layout

        berryModel model = detectionArrayList.get(position);
        holder.maturity.setText(model.getStatus());
        holder.confidence.setText(model.getScore().toString()+ " "+"%");
        holder.market_price.setText(model.getPrice());
        holder.label.setText("Strawberry: "+model.getLabel());

    }

    @Override
    public int getItemCount() {
        // this method is used for showing number of card items in recycler view
        return detectionArrayList.size();
    }

    @Override
    public long getItemId(int position) {
        return position;
    }

    @Override
    public int getItemViewType(int position) {
        return position;
    }

    public class ViewHolder extends RecyclerView.ViewHolder {
        private TextView label;
        private TextView maturity;
        private TextView confidence;
        private TextView market_price;


        public ViewHolder(@NonNull View itemView) {
            super(itemView);

            label = itemView.findViewById(R.id.label);
            maturity = itemView.findViewById(R.id.maturity);
            confidence = itemView.findViewById(R.id.confidence);
            market_price = itemView.findViewById(R.id.market_price);
        }



    }



}