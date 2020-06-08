package com.capstone.farming.service;

import com.capstone.farming.dao.RealTimePriceDAO;
import com.capstone.farming.model.RealTimePriceResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.IOException;

@Service
//@Scope(value = "prototype", proxyMode= ScopedProxyMode.TARGET_CLASS)
public class RealTimePriceService {

    private RealTimePriceDAO realTimePriceDAO;

    @Autowired
    public RealTimePriceService(RealTimePriceDAO realTimePriceDAO) {
        this.realTimePriceDAO = realTimePriceDAO;
    }

    public RealTimePriceResponse getRealTimePriceList(int numOfRows, int pageNo,
                                                      String delngDe, String prdlstNm,
                                                      String spciesNm, String whsalNm)
                                                                throws IOException, IllegalArgumentException {

        String prdlstCd = null;
        if(prdlstNm != null) {
            switch(prdlstNm) {
                case "고구마" : prdlstCd = "0502"; break;
                case "포도" : prdlstCd = "0603"; break;
            }
        }

        String spciesCd = null;
        if(spciesNm != null) {
            switch(spciesNm) {
                case "호박고구마" : spciesCd = "050204"; break;
                case "밤고구마" : spciesCd = "050201"; break;
                case "델라웨어" : spciesCd = "060303"; break;
                case "샤인마스캇" : spciesCd = "060336"; break;
            }
        }

        String whsalCd = null;
        if(whsalNm != null) {
            switch(whsalNm) {
                case "서울가락도매시장" : whsalCd = "110001"; break;
                case "인천삼산도매시장" : whsalCd = "230003"; break;
            }
        }

        return realTimePriceDAO.getRealTimePriceList(numOfRows, pageNo,
                                                            delngDe, prdlstCd,
                                                            spciesCd, whsalCd);
    }
}
