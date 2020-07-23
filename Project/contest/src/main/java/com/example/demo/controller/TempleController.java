package com.example.demo.controller;

import com.example.demo.dao.Boundary;
import com.example.demo.dao.Temple;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.extern.slf4j.Slf4j;
import org.apache.poi.xssf.usermodel.XSSFCell;
import org.apache.poi.xssf.usermodel.XSSFRow;
import org.apache.poi.xssf.usermodel.XSSFSheet;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
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
    private final String dataFile =  "E:\\Git\\contest\\src\\main\\resources\\data.xlsx"; // 전체 데이터 파일
    private final String templeFile =  "E:\\Git\\contest\\src\\main\\resources\\templeInfo.csv"; // 사찰 데이터 파일
    private final String boundaryFile = "E:\\Git\\contest\\src\\main\\resources\\boundarySeoul.json";
    private List<Temple> templeObj = new ArrayList<Temple>();
    private List<String> temple = new ArrayList<String>();
    private List<String> boundary = new ArrayList<String>();

    public TempleController() {
        try {
            /*
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
            */
            FileInputStream fis = new FileInputStream(dataFile);
            XSSFWorkbook workbook = new XSSFWorkbook(fis);
            XSSFSheet sheet=workbook.getSheetAt(0); // 시트 인덱스
            int rowLength = sheet.getPhysicalNumberOfRows(); // 행 수
            for (int rowIndex = 1; rowIndex < rowLength; rowIndex++) { // 첫 번째 행은 컬럼이므로 제외
                XSSFRow row = sheet.getRow(rowIndex); // 행 읽음
                ArrayList<String> rowData = new ArrayList();
                if (row != null) {
                    int colLength = 12; // row.getPhysicalNumberOfCells(); // 열 수 (뒤에 콤마가 이상하게 들어가 있으면 컬럼 수가 크게 나올 수 있으므로 컬럼 수 지정)
                    for (int colIndex = 0; colIndex <= colLength; colIndex++) {
                        XSSFCell col = row.getCell(colIndex); // 열 읽음
                        String value = "";
                        if (col == null) { // 비어 있을 경우
                            continue;
                        } else {
                            value = col.toString();
                            /*
                            switch (col.getCellType()) {
                                case XSSFCell.CELL_TYPE_FORMULA:
                                    value = col.getCellFormula();
                                    break;
                                case XSSFCell.CELL_TYPE_NUMERIC:
                                    value = col.getNumericCellValue() + "";
                                    break;
                                case XSSFCell.CELL_TYPE_STRING:
                                    value = col.getStringCellValue() + "";
                                    break;
                                case XSSFCell.CELL_TYPE_BLANK:
                                    value = col.getBooleanCellValue() + "";
                                    break;
                                case XSSFCell.CELL_TYPE_ERROR:
                                    value = col.getErrorCellValue() + "";
                                    break;
                            }
                        }
                        */
                            // 일단 테스트를 위해 기존에 구현된 컬럼들만 추가 (영문 이름, 경도, 위도, 전화번호)
                            if (colIndex == 2 || colIndex == 9) {
                                rowData.add(value);
                            } else if (colIndex == 3 || colIndex == 4) {
                                // 위경도는 실수 데이터인데 그놈의 콤마가 들어가 있는 경우가 있어서 콤마 제거
                                // 이거 설명 같은 경우에는 콤마가 있을 수 있는데 숫자 데이터의 경우 무조건 다음과 같이 처리해야 할 듯
                                rowData.add(value.replaceAll(",", ""));
                            }
                        }
                    }
                    // System.out.println(rowData.get(0) + " " + rowData.get(3) + " " + rowData.get(2) + " " + rowData.get(1));
                    templeObj.add(new Temple(rowData.get(0), rowData.get(3), Double.parseDouble(rowData.get(2)), Double.parseDouble(rowData.get(1))));
                }
            }
            /*
            for (int i = 0; i < templeObj.size(); i++) {
                System.out.println(templeObj.get(i).getName() + " " + templeObj.get(i).getTel() + " " + templeObj.get(i).getLat() + " " + templeObj.get(i).getLon());
            }
            */
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
