/* Upgrade routines
 *
 * This script contains helper routines to upgrade a template spreadsheet between versions. 
 * 
 * 
 *
 */

var latestVersion = 0.5;

function setVersion() {
  var documentProperties = PropertiesService.getDocumentProperties();
  var version = documentProperties.setProperty("version",0.4);
}


function get_current_version() {
  var documentProperties = PropertiesService.getDocumentProperties();
  var version = documentProperties.getProperty("version");
  if(version == null) {
     var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Introduction & guidance (draft)")
     var version = sheet.getRange(3,3).getValue() 
  }
  Logger.log(version)  

  if(parseFloat(version) < latestVersion) {
     var ui = SpreadsheetApp.getUi();
     var response = ui.alert('Upgrade required', 'You are currently using a version ' + version + ' spreadsheet template. The current version is ' + latestVersion + '. Would you like to upgrade your template? You can revert changes using the Revision History if required', ui.ButtonSet.YES_NO);
     if (response == ui.Button.YES) {
        upgrade(version)
     } else {
         ui.alert('Upgrade required', 'No upgrade has been performed. Note, you should be careful with any further loading of data from this template until it has been upgraded.',ui.ButtonSet.OK)
     }
  }
}

function upgrade(currentVersion) {
  var documentProperties = PropertiesService.getDocumentProperties();

  if(currentVersion < 0.4) {
            SpreadsheetApp.getActiveSpreadsheet().toast("Upgrading version 0.3 to 0.4")
            // Updates to 4. Project aliases
            var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("4. Project aliases")
            var rown = getTagRow(sheet)
            sheet.getRange(rown, getTagCol("#project+skos:altLabel",sheet)).setValue("#project+skos:altLabel+1")
            sheet.getRange(rown, getTagCol("#project+skos:altLabel",sheet)).setValue("#project+skos:altLabel+2")
            
            // Updates to 5. Project location, status, commodity
            // - Rename #site+lon to #site+long
            var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("5. Project location, status, commodity")
            var rown = getTagRow(sheet)
            var startRow = rown+1
            var coln = getTagCol("#site+lon",sheet)
            sheet.getRange(rown, coln).setValue("#site+long")
          
            // - Add a country column
            coln = getTagCol("#site+address",sheet)
            sheet.insertColumnAfter(coln)
            sheet.getRange(rown, coln+1).setValue("#-")
            sheet.getRange(rown -1, coln+1).setValue("Country")
            sheet.getRange(rown -1, coln+1).setNote("This column is filled with a formula to lookup project locations automatically. If you are only providing details of a site (no project), or the site is located in a different country from the main project country, delete the formula and selection the site country from the drop-down list.")
            sheet.insertColumnAfter(coln+1)
            sheet.getRange(rown, coln+2).setValue("#country+identifier")
            sheet.getRange(rown-1, coln+2).setValue("Country Code")
          
            sheet.hideColumn(sheet.getRange(1,coln+2))
            
            SpreadsheetApp.getActiveSpreadsheet().setActiveSheet(sheet)
            setCountryValidation()
          
            var lookupRange = sheet.getRange(startRow, coln+1,sheet.getMaxRows()-startRow-1,1) 
            lookupRange.setFormula("=IF(ISBLANK(B"+startRow+"),\"\",INDEX(QUERY('1. Project List'!$A:$C,\"SELECT A WHERE C = '\"&B"+startRow+"&\"'\",false),1))")
          
            
            // Updates to 7. Contracts, concessions and companies
            // - Prefix column names with +project
            sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("7. Contracts, concessions and companies")
            rown = getTagRow(sheet)
            var startRow = rown+1
          
            sheet.getRange(rown, getTagCol("#company",sheet)).setValue("#project+company")
            sheet.getRange(rown, getTagCol("#company+share",sheet)).setValue("#project+company+share")
            sheet.getRange(rown, getTagCol("#company+isOperator",sheet)).setValue("#project+company+isOperator")  
           
            sheet.getRange(rown, getTagCol("#contract",sheet)).setValue("#project+contract")  
            sheet.getRange(rown, getTagCol("#contract+uri",sheet)).setValue("#project+contract+uri")  
            
            sheet.getRange(rown, getTagCol("#concession",sheet)).setValue("#project+concession")  
            sheet.getRange(rown, getTagCol("#concession+identifier",sheet)).setValue("#project+concession+identifier")  
          
             // - Add a country column
            coln = getTagCol("#project+concession",sheet)
            sheet.insertColumnAfter(coln)
            sheet.getRange(rown, coln+1).setValue("#-")
            sheet.getRange(rown -1, coln+1).setValue("Concession Country")
            sheet.getRange(rown -1, coln+1).setNote("This column is filled with a formula to lookup project locations automatically. If the concession is located in a different project from the country, delete this formula and select from the drop-down list.")
            sheet.insertColumnAfter(coln+1)
            sheet.getRange(rown, coln+2).setValue("#project+concession+country+identifier")
            sheet.getRange(rown-1, coln+2).setValue("Concession country code")
            sheet.hideColumn(sheet.getRange(1,coln+2))
            SpreadsheetApp.getActiveSpreadsheet().setActiveSheet(sheet)
            setCountryValidation("project+concession+")
          
            var lookupRange = sheet.getRange(startRow, coln+1,sheet.getMaxRows()-startRow-1,1) 
            lookupRange.setFormula("=IF(ISBLANK(B"+startRow+"),\"\",INDEX(QUERY('1. Project List'!$A:$C,\"SELECT A WHERE C = '\"&B"+startRow+"&\"'\",false),1))")
            
            
            // Updates to Contributors
            sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Contributor")
            rown = getTagRow(sheet)
            sheet.getRange(rown, getTagCol("#contributor+name",sheet)).setValue("#contributor+foaf:name")  
            sheet.getRange(rown, getTagCol("#contributor+mbox",sheet)).setValue("#contributor+foaf:mbox")  
            sheet.getRange(rown, getTagCol("#contributor+url",sheet)).setValue("#contributor+foaf:homepage")  
            
            // Updates to Payments sheet
            sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("10. Payments (do not use)")
            rown = getTagRow(sheet)
            sheet.deleteColumn(getTagCol("#company+identifier",sheet))
            sheet.deleteColumn(getTagCol("#project+identifier",sheet))
            sheet.getRange(1,getTagCol("#governmentReceipt+year",sheet)).setValue("Government receipt information")
            sheet.setName("10. Payments and receipts")
            
            update_name("v0.3","v0.4") 
            currentVersion = 0.4
            documentProperties.setProperty("version",currentVersion);
   }
  
  
  if(currentVersion < 0.5) { 
        SpreadsheetApp.getActiveSpreadsheet().toast("Upgrading version 0.4 to 0.5")
        var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("10. Payments and receipts")
        var rown = getTagRow(sheet)
        coln = getTagCol("#country",sheet)
        sheet.insertColumnAfter(coln)
        sheet.getRange(rown, coln+1).setValue("#country+identifier")
        sheet.getRange(rown-1, coln+1).setValue("Country Code")
        sheet.getRange(rown, coln+1,sheet.getMaxRows()-rown,1).clearDataValidations() 
        SpreadsheetApp.setActiveSheet(sheet)
        setCountryValidation()

        update_name("0.4","0.5") 
        currentVersion = 0.5
        documentProperties.setProperty("version",currentVersion);
  }
  
  
  update_codelists();
  var ui = SpreadsheetApp.getUi();
  ui.alert('Upgrade complete', 'This sheet has now been upgraded to version ' + currentVersion + '. All changes are stored in the revision history.' ,ui.ButtonSet.OK)
}



function update_name(from,to) {
  var file = DriveApp.getFileById(SpreadsheetApp.getActiveSpreadsheet().getId())
  file.setName(file.getName().replace(from,to))
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Introduction & guidance (draft)")
  sheet.getRange(3,3).setValue(to)
}

// Get codelists into authoritative state
// ToDo: Load codelists from authoriative SKOS files...
function update_codelists() {
  
  // Sources
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Codelist: source") 
  sheet.getRange(2,3,13,1).setValues([["vpd"],["mpd"],["eiti"],["govreport"],["govdb"],["otherauth"],["companyreport"],["ioreport"],["companydb"],["wikipedia"],["googlemaps"],["press"],["othernonauth"]])
  
  
}
