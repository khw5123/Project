package com.example.demo.controller;

import com.example.demo.service.HardwareService;
import com.example.demo.dto.Hardware;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;

import java.util.List;

@Controller
public class HardwareController {
    private final HardwareService hardwareService;

    @Autowired
    public HardwareController(HardwareService hardwareService) {
        this.hardwareService = hardwareService;
    }

    @RequestMapping("/index")
    public String main_page(Model model) {
        return "thymeleaf/index";
    }

    @RequestMapping("/select")
    public String select_page(Model model, String type) {
        List<Hardware> list;
        if(type == null || type == "") {
            type = "전체";
            list = hardwareService.selectAll();
        } else {
            list = hardwareService.selectByType(type);
        }
        model.addAttribute("type", type);
        model.addAttribute("hardwareList", list);
        return "thymeleaf/select";
    }

    @RequestMapping("/insert")
    public String insert_page(Model model, String type, String name) {
        if(type == null && name == null) {

        } else if(type == "" || name == "") {
            model.addAttribute("result", "부품 추가 실패");
        } else {
            hardwareService.insertByTypeName(type, name);
            model.addAttribute("result", "부품 추가 성공");
        }
        return "thymeleaf/insert";
    }

    @RequestMapping("/update")
    public String update_page(Model model, String name, String newName) {
        if (name != null) {
            boolean exist = false;
            List<Hardware> list = hardwareService.selectAll();
            for (int i = 0; i < list.size(); i++) {
                if (list.get(i).getName().equals(name)) {
                    exist = true;
                    break;
                }
            }
            if (exist) {
                hardwareService.updateByName(name, newName);
                model.addAttribute("result", "부품 교체 성공");
            } else {
                model.addAttribute("result", "부품 교체 실패");
            }
        }
        return "thymeleaf/update";
    }

    @RequestMapping("/delete")
    public String delete_page(Model model, String type, String name) {
        if (type != null && name != null) {
            boolean exist = false;
            List<Hardware> list = hardwareService.selectAll();
            for (int i = 0; i < list.size(); i++) {
                if (list.get(i).getType().equals(type) && list.get(i).getName().equals(name)) {
                    exist = true;
                    break;
                }
            }
            if (exist) {
                hardwareService.deleteByTypeName(type, name);
                model.addAttribute("result", "부품 제거 성공");
            } else {
                model.addAttribute("result", "부품 제거 실패");
            }
        }
        return "thymeleaf/delete";
    }
}
