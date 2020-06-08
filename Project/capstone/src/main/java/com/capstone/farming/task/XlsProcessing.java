package com.capstone.farming.task;

import com.capstone.farming.dao.AreaFarmInfoDAO;
import com.capstone.farming.model.ShippingArea;
import org.apache.poi.openxml4j.exceptions.InvalidFormatException;
import org.apache.poi.EncryptedDocumentException;
import org.apache.poi.ss.usermodel.*;
import org.apache.poi.xssf.usermodel.XSSFCell;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.Iterator;

@Component //
public class XlsProcessing {

    @Autowired
    AreaFarmInfoDAO areaFarmInfoDAO;

    public void insertMongo() throws EncryptedDocumentException, IOException, InvalidFormatException {

        String filePath = "C:\\Users\\JAVIS\\Downloads\\returnFarmAreaFarmingInfo_20200518.xls";
        InputStream inputStream = new FileInputStream(filePath);

        Workbook workbook = WorkbookFactory.create(inputStream);
        Sheet sheet = workbook.getSheetAt(0);
        Iterator<Row> rowItr = sheet.iterator();

        while(rowItr.hasNext()) {
            ShippingArea shippingArea = new ShippingArea();
            Row row = rowItr.next();

            //첫번째 행이 헤더인 경우 스킵
            if (row.getRowNum() == 0) {
                continue;
            }
            Iterator<Cell> cellItr = row.cellIterator();
            while (cellItr.hasNext()) {
                Cell cell = cellItr.next();
                int index = cell.getColumnIndex();

                switch (index) {
                    case 0: //번호
                        break;
                    case 1: //
                        shippingArea.setProvince((String) getValueFromCell(cell));
                        break;
                    case 2:
                        shippingArea.setCity((String) getValueFromCell(cell));
                        break;
                    case 3:
                        String itemes = (String) getValueFromCell(cell);
                        String[] item = itemes.split(">");
                        shippingArea.setItem(item[2].trim());
                        break;
                    case 4:
                        shippingArea.setFamily_management_scale((String) getValueFromCell(cell));
                        break;
                    case 5:
                        shippingArea.setAverage_investment_cost((String) getValueFromCell(cell));
                        break;
                    case 6:
                        shippingArea.setAnnual_operating_cost((String) getValueFromCell(cell));
                    case 7:
                        shippingArea.setAverage_income((String) getValueFromCell(cell));
                        break;
                    case 8:
                        shippingArea.setAverage_farmland_price((String) getValueFromCell(cell));
                        break;
                }
            }
            System.out.println(shippingArea.toString());// 확인용 출력문
            areaFarmInfoDAO.insertShippingArea(shippingArea);

        }

    }

    private static Object getValueFromCell(Cell cell){
        switch (cell.getCellType()){
            case XSSFCell.CELL_TYPE_STRING:
                return cell.getStringCellValue();
            case XSSFCell.CELL_TYPE_BOOLEAN:
                return cell.getBooleanCellValue();
            case XSSFCell.CELL_TYPE_NUMERIC:
                if(DateUtil.isCellDateFormatted(cell)){
                    return cell.getDateCellValue();
                }
                return cell.getNumericCellValue();
            case XSSFCell.CELL_TYPE_FORMULA:
                return cell.getCellFormula();
            case XSSFCell.CELL_TYPE_BLANK:
                return "";
            default:
                return "";

        }
    }
}
