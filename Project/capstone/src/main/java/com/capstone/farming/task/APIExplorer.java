package com.capstone.farming.task;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class APIExplorer {

    /**
     * GET 방식으로 JSON 형태의 응답을 받아옴
     *
     * @param requestURL 키 값을 포함한 전체 요청 URL
     * @return URL 요청에 대한 응답
     * @throws IOException
     */
    public String request(String requestURL) throws IOException {

        HttpURLConnection conn = null;
        BufferedReader rd = null;

        try {
            boolean badResponseCode = false;

//        StringBuilder urlBuilder = new StringBuilder(""); /*URL*/
//        urlBuilder.append("?" + URLEncoder.encode("ServiceKey","UTF-8") + "=서비스키"); /*Service Key*/
//        URL url = new URL(urlBuilder.toString());
            URL url = new URL(requestURL);
//            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            conn.setRequestProperty("Content-type", "application/json");
//        System.out.println("Response code: " + conn.getResponseCode());
//            BufferedReader rd;
            if (conn.getResponseCode() >= 200 && conn.getResponseCode() <= 300) {
                badResponseCode = false;
                rd = new BufferedReader(new InputStreamReader(conn.getInputStream()));
            } else {
                badResponseCode = true;
                rd = new BufferedReader(new InputStreamReader(conn.getErrorStream()));
            }
            StringBuilder sb = new StringBuilder();
            String line;
            while ((line = rd.readLine()) != null) {
                sb.append(line);
            }

//        System.out.println(sb.toString());

            if (badResponseCode) throw new IOException("badResponseCode\n" +
                                                    "Response code: " + conn.getResponseCode() + "\n" +
                                                    sb.toString());

            return sb.toString();

        } catch(IOException e) {
            throw e;
        } finally {
            if(conn != null) conn.disconnect();
            if(rd != null) rd.close();
        }
    }
}