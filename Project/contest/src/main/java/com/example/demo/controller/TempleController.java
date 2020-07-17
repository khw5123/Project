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

    // 서울특별시 행정동 경계 표시
    @RequestMapping("/boundary")
    public String boundary(Model model) {
        model.addAttribute("temple", temple);
        model.addAttribute("boundary", boundary);
        return "boundary";
    }

    // 사찰 주변 점위와 사찰간 거리 표시
    @RequestMapping("/distance")
    public String distance(Model model) {
        model.addAttribute("temple", temple);
        return "distance";
    }

    // 사찰 검색
    @RequestMapping("/search")
    public String search(Model model) {
        model.addAttribute("temple", temple);
        model.addAttribute("templeObj", templeObj);
        return "search";
    }

    // 현재 위치 주변에 있는 사찰만 표시
    @RequestMapping("/range")
    public String range(Model model) {
        model.addAttribute("temple", temple);
        return "range";
    }

    // 범위 내 최소 비용 경로 표시
    @RequestMapping("/kruskal")
    public String kruskal(Model model) {
        model.addAttribute("temple", temple);
        return "kruskal";
    }

    // 출발지에서 목적지로 가는 최단 경로 표시
    @RequestMapping("/dijkstra")
    public String dijkstra(Model model) {
        model.addAttribute("temple", temple);
        return "dijkstra";
    }
}
