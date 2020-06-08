package com.capstone.farming.dao;

import com.capstone.farming.model.RealTimePrice;
import com.capstone.farming.model.RealTimePriceResponse;
import com.capstone.farming.task.APIExplorer;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Repository;

import java.io.IOException;
import java.util.List;

@Repository
public class RealTimePriceDAO {

    @Value("${custom.api.real-time-price-u-r-l}")
    private String realTimePriceURL;

    @Value("${custom.api.real-time-price-a-p-i-key}")
    private String realTimePriceAPIKey;

    /**
     * @param numOfRows 한 페이지 결과 수 (greater than 0)
     * @param pageNo 페이지 번호 (greater than 0)
     * @param delngDe 경락일자 (not {@code null})
     * @param prdlstCd 품목코드 (not {@code null})
     * @param spciesCd 품종코드
     * @param whsalCd 도매시장코드
     *
     * @throws IOException if an I/O error occurs
     * @throws IllegalArgumentException if {@code numOfRows} or {@code PageNo} is less than {@code 1} or
     *                                      {@code delngDe} or {@code prdlstCd} is {@code null}
     */
    public RealTimePriceResponse getRealTimePriceList(int numOfRows, int pageNo,
                                                      String delngDe, String prdlstCd,
                                                      String spciesCd, String whsalCd)
                                                                throws IOException, IllegalArgumentException {

        if(numOfRows < 1) throw new IllegalArgumentException("numOfRows should be greater than 0 but is assigned " + numOfRows);
        if(pageNo < 1) throw new IllegalArgumentException("pageNo should be greater than 0 but is assigned " + pageNo);
        if(delngDe == null) throw new IllegalArgumentException("delngDe should not be null but is null");
        if(prdlstCd == null) throw new IllegalArgumentException("prdlstCd should not be null but is null");

        String request = this.realTimePriceURL + "?ServiceKey=" + this.realTimePriceAPIKey + "&_type=json"
                            + "&numOfRows=" + numOfRows + "&pageNo=" + pageNo
                            + "&delngDe=" + delngDe + "&prdlstCd=" + prdlstCd
                            + (spciesCd==null ? "" : ("&spciesCd=" + spciesCd))
                            + (whsalCd==null ? "" : ( "&whsalCd=" + whsalCd ));

        APIExplorer apiExplorer = new APIExplorer();
        String respones = apiExplorer.request(request);

        ObjectMapper objectMapper = new ObjectMapper();
        objectMapper.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
        JsonNode root = objectMapper.readTree(respones);

        RealTimePriceResponse realTimePriceResponse = objectMapper.readValue(
                                                            String.valueOf(root.at("/response/body")),
                                                            RealTimePriceResponse.class);

        if(realTimePriceResponse.getTotalCount() != 0) {
            realTimePriceResponse.setRealTimePriceList(objectMapper.readValue(
                                                                String.valueOf(root.at("/response/body/items/item")),
                                                                new TypeReference<List<RealTimePrice>>(){}));
        }

        return realTimePriceResponse;
    }

}
