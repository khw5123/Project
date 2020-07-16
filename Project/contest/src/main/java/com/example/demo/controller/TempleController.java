package com.example.demo.controller;

import com.example.demo.dao.Boundary;
import com.example.demo.dao.Temple;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.extern.slf4j.Slf4j;
import org.json.JSONArray;
import org.json.JSONObject;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;

import java.io.*;
import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.List;

@Slf4j
@Controller
public class TempleController {
    private final String templeFile =  "E:\\Git\\contest\\src\\main\\resources\\templeInfo.csv";
    private final String boundaryFile = "E:\\Git\\contest\\src\\main\\resources\\boundarySeoul.json";
    private List<Temple> templeObj = new ArrayList<Temple>();
    private List<String> temple = new ArrayList<String>();
    private List<String> boundary = new ArrayList<String>();

    // 버튼 누르면 주변 범위(원, 직선) ON/OFF
    // 검색 시 이동
    // 사찰과 범위 설정해서 검색한 범위 내 사찰들만 보여주기
    // 범위 설정해서 범위 내 최단거리 보여주기

    public TempleController() {
        try {
            BufferedReader br = new BufferedReader(new FileReader(new File(templeFile)));
            String line = "";
            int count = 0;
            while ((line = br.readLine()) != null) {
                if (count != 0) {
                    String info[] = line.split(",");
                    templeObj.add(new Temple(info[1], info[5], Double.parseDouble(info[6]), Double.parseDouble(info[7])));
                }
                count++;
            }
            br.close();
            ObjectMapper objectMapper = new ObjectMapper();
            for (int i = 0; i < templeObj.size(); i++) {
                temple.add(objectMapper.writeValueAsString(templeObj.get(i)));
            }
            setBoundary();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void setBoundary() {
        try {
            File file = new File(boundaryFile);
            char[] ch = new char[(int)file.length()];
            BufferedReader br = new BufferedReader(new FileReader(file));
            br.read(ch);
            br.close();
            String jsonString = String.valueOf(ch);
            JSONObject jObject = new JSONObject(jsonString);
            JSONArray jArray = jObject.getJSONArray("features");
            ObjectMapper objectMapper = new ObjectMapper();
            for(int i = 0; i<jArray.length();i++) {
                JSONObject obj = jArray.getJSONObject(i);
                String name = obj.getJSONObject("properties").getString("adm_nm");
                List coordinates = (List)((List)obj.getJSONObject("geometry").getJSONArray("coordinates").toList().get(0)).get(0);
                boundary.add(objectMapper.writeValueAsString(new Boundary(name, coordinates)));
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @RequestMapping("/index")
    public String index(Model model) {
        model.addAttribute("temple", temple);
        model.addAttribute("boundary", boundary);
        return "index";
    }
}
