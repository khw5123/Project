package com.example.demo.service;

import com.example.demo.dto.Hardware;

import java.util.List;

public interface HardwareService {
    List<Hardware> selectAll();
    List<Hardware> selectByType(String type);
    void insertByTypeName(String type, String name);
    void deleteByTypeName(String type, String name);
    void updateByName(String name, String newName);
}
