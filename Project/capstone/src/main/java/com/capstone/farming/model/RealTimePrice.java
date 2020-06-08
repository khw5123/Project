package com.capstone.farming.model;

import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

@Getter @Setter @ToString
public class RealTimePrice {

    /** 경락일자 */
    private String delngDe;
    /** 경매시간 */
    private String sbidTime;
    /** 시장명 */
    private String whsalMrktNm;
    /** 부류명 */
    private String catgoryNewNm;
    /** 품목명 */
    private String stdPrdlstNewNm;
    /** 품종명 */
    private String stdSpciesNewNm;
    /** 거래단량 */
    private String delngPrut;
    /** 단위명 */
    private String stdUnitNewNm;
    /** 포장상태명 */
    private String stdFrmlcNewNm;
    /** 크기명 */
    private String stdMgNewNm;
    /** 등급명 */
    private String stdQlityNewNm;
    /** 거래가격 */
    private String sbidPric;
    /** 거래량 */
    private String delngQy;

}
