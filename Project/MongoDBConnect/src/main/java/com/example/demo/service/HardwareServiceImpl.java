package com.example.demo.service;

import com.example.demo.dto.Hardware;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.data.mongodb.core.query.Update;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public class HardwareServiceImpl implements HardwareService {
    private final MongoTemplate mongoTemplate;

    @Autowired
    public HardwareServiceImpl(MongoTemplate mongoTemplate) {
        this.mongoTemplate = mongoTemplate;
    }

    @Override
    public List<Hardware> selectAll() {
        return mongoTemplate.findAll(Hardware.class);
    }

    @Override
    public List<Hardware> selectByType(String type) {
        Query query = new Query();
        query.addCriteria(Criteria.where("type").is(type));
        return mongoTemplate.find(query, Hardware.class);
    }

    @Override
    public void insertByTypeName(String type, String name) {
        Hardware hardware = new Hardware();
        hardware.setType(type);
        hardware.setName(name);
        mongoTemplate.insert(hardware);
    }

    @Override
    public void updateByName(String name, String newName) {
        Query query = new Query();
        query.addCriteria(Criteria.where("name").is(name));
        Update update = new Update();
        update.set("name", newName);
        mongoTemplate.updateFirst(query, update, "Hardware");
    }

    @Override
    public void deleteByTypeName(String type, String name) {
        Query query = new Query();
        query.addCriteria(Criteria.where("type").is(type));
        query.addCriteria(Criteria.where("name").is(name));
        mongoTemplate.remove(query, Hardware.class);
    }
}
