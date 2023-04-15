package com.example.crop_maturity;
import com.google.gson.JsonElement;

import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.GET;
import retrofit2.http.Header;
import retrofit2.http.POST;
import retrofit2.http.Path;

public interface UserService {
    @GET("/image")
    Call<urlResponse> getImage();

    @GET("/detections")
    Call<ArrayList<detectResponse>> getPrediction();

    @POST("/")
    Call<String> getwheel1Movement(@Body forwardRequest forwardrequest);

    @POST("/")
    Call<String> getwheel2Movement(@Body leftRequest leftrequest);

    @POST("/")
    Call<String> getarmMovement(@Body armRequest armrequest);





}
