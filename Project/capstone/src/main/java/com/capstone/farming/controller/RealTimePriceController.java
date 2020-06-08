package com.capstone.farming.controller;

import com.capstone.farming.model.RealTimePriceResponse;
import com.capstone.farming.service.RealTimePriceService;
import lombok.extern.log4j.Log4j;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.io.IOException;

@Slf4j
@Controller
@RequestMapping("/Price")
public class RealTimePriceController {

    private RealTimePriceService realTimePriceService;

    @Autowired
    public RealTimePriceController(RealTimePriceService realTimePriceService) {
        this.realTimePriceService = realTimePriceService;
    }

    @RequestMapping(value = "RealTimePrice", method = RequestMethod.GET)
    public String realTimePrice(Model model) {

        return "Price/RealTimePrice";
    }

    @RequestMapping(value = "RealTimePrice", method = RequestMethod.POST)
    public String realTimePrice(Model model,
                                @RequestParam(value = "numOfRows", required = false, defaultValue = "10") int numOfRows,
                                @RequestParam(value = "pageNo", required = false, defaultValue = "1") int pageNo,
                                @RequestParam(value = "delngDe", required = false) String delngDe,
                                @RequestParam(value = "prdlstNm", required = false) String prdlstNm,
                                @RequestParam(value = "spciesNm", required = false) String spciesNm,
                                @RequestParam(value = "whsalNm", required = false) String whsalNm)
                                                                        throws IOException, IllegalArgumentException {

        RealTimePriceResponse realTimePriceResponse = realTimePriceService.getRealTimePriceList(numOfRows, pageNo,
                                                                                                delngDe, prdlstNm,
                                                                                                spciesNm, whsalNm);

        int totalPage = (realTimePriceResponse.getTotalCount() - 1) / numOfRows + 1;

        String message = null;
        if(realTimePriceResponse.getTotalCount() == 0) message = "해당 거래 내역이 없습니다.";

        model.addAttribute("realTimePriceList", realTimePriceResponse.getRealTimePriceList());
        model.addAttribute("pageNo", pageNo);
        model.addAttribute("totalPage", totalPage);
        model.addAttribute("message", message);

        return "Price/RealTimePrice";
    }

    @ResponseStatus(value = HttpStatus.BAD_REQUEST, reason = "입력 변수가 잘못되었습니다.")
    @ExceptionHandler(IllegalArgumentException.class)
    public void handleIllegalArgumentException(IllegalArgumentException e) {
        log.error("==================================================================================");
        log.error("handle IllegalArgumentException\n", e);
    }

    @ResponseStatus(value = HttpStatus.INTERNAL_SERVER_ERROR, reason = "I/O 에러 발생")
    @ExceptionHandler(IOException.class)
    public void handleIOException(IOException e) {
        log.error("==================================================================================");
        log.error("handle IOException\n", e);
    }

    @ResponseStatus(value = HttpStatus.INTERNAL_SERVER_ERROR, reason = "오류 발생")
    @ExceptionHandler(Exception.class)
    public void handleException(Exception e) {
        log.error("==================================================================================");
        log.error("handle Exception\n", e);
    }
}
