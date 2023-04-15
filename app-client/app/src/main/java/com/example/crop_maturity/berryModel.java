package com.example.crop_maturity;

public class berryModel {
    public Integer label;
public String status;
public String price;
public Double score;

    public berryModel(String status, String price, Double score, Integer label) {
        this.status = status;
        this.price = price;
        this.score = score;
        this.label = label;
    }

    public Integer getLabel() {
        return label;
    }

    public void setLabel(Integer label) {
        this.label = label;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
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
}
