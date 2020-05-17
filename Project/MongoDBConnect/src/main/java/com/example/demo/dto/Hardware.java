package com.example.demo.dto;

import org.springframework.data.mongodb.core.mapping.Document;

@Document(collection = "Hardware")
public class Hardware {
    private String type;
    private String name;

    public String getType() {
        return type;
    }

    public String getName() {
        return name;
    }

    public void setType(String type) {
        this.type = type;
    }

    public void setName(String name) {
        this.name = name;
    }
}
