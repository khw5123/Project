package com.capstone.farming.model;

import org.springframework.data.mongodb.core.mapping.Document;

@Document(collection = "shippingArea")
public class ShippingArea {

    //@Id
    //private String _id;

    private String province;
    private String city;
    private String item;
    private String family_management_scale;
    private String average_investment_cost;
    private String annual_operating_cost;
    private String average_income;
    private String average_farmland_price;

    public void setProvince(String province) {
        this.province = province;
    }

    public void setCity(String city) {
        this.city = city;
    }

    public void setItem(String item) {
        this.item = item;
    }

    public void setFamily_management_scale(String family_management_scale) {
        this.family_management_scale = family_management_scale;
    }

    public void setAverage_investment_cost(String average_investment_cost) {
        this.average_investment_cost = average_investment_cost;
    }

    public void setAnnual_operating_cost(String annual_operating_cost) {
        this.annual_operating_cost = annual_operating_cost;
    }

    public void setAverage_income(String average_income) {
        this.average_income = average_income;
    }

    public void setAverage_farmland_price(String average_farmland_price) {
        this.average_farmland_price = average_farmland_price;
    }

    public String getProvince() {
        return province;
    }

    public String getCity() {
        return city;
    }

    public String getItem() {
        return item;
    }

    public String getFamily_management_scale() {
        return family_management_scale;
    }

    public String getAverage_investment_cost() {
        return average_investment_cost;
    }

    public String getAnnual_operating_cost() {
        return annual_operating_cost;
    }

    public String getAverage_income() {
        return average_income;
    }

    public String getAverage_farmland_price() {
        return average_farmland_price;
    }

    @Override
    public String toString() {
        return "province: " + province +", city: "+ city + ", item: "+ item + ", family_management_scale: "+ family_management_scale +
                ", average_investment_cost: " + average_investment_cost + ", annual_operating_cost: " + annual_operating_cost
                + ", average_income: " + average_income + ", average_farmland_price: " + average_farmland_price;
    }
}
