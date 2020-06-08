package com.capstone.farming;

import lombok.Getter;
import lombok.Setter;
import org.springframework.boot.context.properties.ConfigurationProperties;

/**
 * API와 관련된 property 정의를 위한 클래스
 */

@Getter @Setter
@ConfigurationProperties(prefix = "custom.api")
public class APIProperties {

    /** 실시간 가격 정보 서비스 요청 URL */
    private String realTimePriceURL;

    /** 실시간 가격 정보 서비스 요청에 사용할 API key */
    private String realTimePriceAPIKey;
}
