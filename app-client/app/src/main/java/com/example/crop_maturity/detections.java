package com.example.crop_maturity;

import com.google.gson.annotations.SerializedName;

public class detections {
    @SerializedName("class")
    String myclass;
    String confidence;

    public detections(String myclass, String confidence) {
        this.myclass = myclass;
        this.confidence = confidence;
    }

    public String getMyclass() {
        return myclass;
    }

    public void setMyclass(String myclass) {
        this.myclass = myclass;
    }

    public String getConfidence() {
        return confidence;
    }

    public void setConfidence(String confidence) {
        this.confidence = confidence;
    }
}
