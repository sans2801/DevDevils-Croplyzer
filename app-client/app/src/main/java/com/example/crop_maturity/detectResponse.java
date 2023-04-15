package com.example.crop_maturity;

import com.google.gson.annotations.SerializedName;

import java.util.ArrayList;

public class detectResponse {

    public String price;
    public Double score;
    public String status;
    public Integer img_label;

    public Integer getImg_label() {
        return img_label;
    }

    public void setImg_label(Integer img_label) {
        this.img_label = img_label;
    }

    public String getPrice() {
        return price;
    }

    public void setPrice(String price) {
        this.price = price;
    }

    public Double getScore() {
        return score;
    }

    public void setScore(Double score) {
        this.score = score;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }
}
