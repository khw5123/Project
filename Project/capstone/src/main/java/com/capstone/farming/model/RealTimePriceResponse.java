package com.capstone.farming.model;

import com.capstone.farming.model.RealTimePrice;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

import java.util.List;

@Getter @Setter @ToString
public class RealTimePriceResponse {

    /** 실시간 가격 정보 인스턴스 리스트 */
    private List<RealTimePrice> realTimePriceList;

    /** 한 페이지 결과 수 */
    private int numOfRows;

    /** 페이지 번호 */
    private int pageNo;

    /** 전체 결과 수 */
    private int totalCount;

}
