package com.example.demo.dao;

import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

@Getter @Setter @ToString
public class Temple {
    private String name;
    private String tel;
    private double lat;
    private double lon;

    public Temple(String name, String tel, double lat, double lon) {
        this.name = name;
        this.tel = tel;
        this.lat = lat;
        this.lon = lon;
    }
}
