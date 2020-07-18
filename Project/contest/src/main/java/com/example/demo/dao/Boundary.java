package com.example.demo.dao;

import lombok.Getter;
import lombok.Setter;
import lombok.ToString;
import java.util.List;

@Getter @Setter @ToString
public class Boundary {
    private String name;
    private List coordinates;

    public Boundary(String name, List coordinates) {
        this.name = name;
        this.coordinates = coordinates;
    }
}
