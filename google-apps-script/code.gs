//ToDo:
// - Add advanced reconcilation service
// - Add extra tools for template management

//Sheets
var codelistCountry = "Codelist: country"
var codelistSource = "Codelist: source"
var codelistCommodity = "Codelist: commodity"
var codelistStatus = "Codelist: project status"
var codelistProduction = "Codelist: production"
var sourcesheetProjects = "1. Project List"
var sourcesheetSources = "2. Source List"
var sourcesheetCompanies = "6. Companies and Groups"


function init_property(property,value) {
  if(PropertiesService.getDocumentProperties().getProperty(property) == null) {
     PropertiesService.getDocumentProperties().setProperty(property,value);
  }
}

function onInstall(e) {  
    onOpen();
}

function onOpen(e) {
    SpreadsheetApp.getUi() // Or DocumentApp or FormApp.
      .createAddonMenu()
      .addItem('Search for identifier','searchForID')
      .addItem('Reconcile column','reconcileAll')
      .addSeparator()
      .addSubMenu(SpreadsheetApp.getUi() 
          .createMenu('Tools')
          .addItem('Configure defaults', 'configure_defaults')
          .addItem('Check for upgrades', 'get_current_version')
          .addItem('Show identifiers', 'showIdentifiers')
          .addItem('Hide identifiers', 'hideIdentifiers')
          .addItem('Show tags', 'showTagRow')
          .addItem('Hide tags', 'hideTagRow')
          .addItem('Show codelist', 'showCodelists')
          .addItem('Hide codelist', 'hideCodelists'))
      .addToUi();
  
}

function configure_defaults() {
    init_property('vocab', '<http://resourceprojects.org/def/>');
    init_property('namespace', 'http://resourceprojects.org/');
    init_property('endpoint', 'http://alpha.resourceprojects.org/sparql');
    init_property('defaultLanguage', 'en');      
  
}

// Search for the first row containing # at the start of one of the first five columns
function getTagRow(sheet) {
  if(typeof sheet == 'undefined') {
    sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  }
  for(row = 1; row < 10; row++) {
    for(col = 1; col < 6; col++) {
      cellValue = sheet.getRange(row,col,1,1).getValue();
      if(cellValue[0] == "#") {
       // SpreadsheetApp.getActiveSpreadsheet().toast("Row " + row)
       return row;
       
      }
    }
  }
}

//Search for the column containing a given tag
function getTagCol(tag,sheet) {
  if(typeof sheet == 'undefined') {
    sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  }
  tagRow = getTagRow(sheet);
  for(col = 1; col <= sheet.getLastColumn(); col++) {
     cellValue = sheet.getRange(tagRow,col,1,1).getValue()
     if(cellValue == tag) {
        // SpreadsheetApp.getActiveSpreadsheet().toast("Col " + col)
        return col; 
     }
  }
}

//Search for the column containing a given class (i.e. ending with the class name)
function getClassCol(searchClass,sheet) {
  if(typeof sheet == 'undefined') {
    sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  }
  tagRow = getTagRow(sheet);
  for(col = 1; col <= sheet.getLastColumn(); col++) {
     var foundClass = getTagClass(sheet.getRange(tagRow,col,1,1).getValue())
     if(foundClass == searchClass) {
        // SpreadsheetApp.getActiveSpreadsheet().toast("Col " + col)
        return col; 
     }
  }
}


// VALIDATION CONFIGURATIONS

function setCountryValidation(prefix) {
  if(!prefix) {
      
    if(SpreadsheetApp.getActiveSheet().getSheetName()== sourcesheetProjects) {
      prefix = ""
    } else if(SpreadsheetApp.getActiveSheet().getSheetName() == "6. Companies and Groups") {
      prefix = "company+"
    } else {
      prefix = "" 
    }
 }
  
 //Hard coded codelist values 
 var countrySheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(codelistCountry);
 var countryRange = countrySheet.getRange(2,2,countrySheet.getLastRow()-1,1);
 var countryRule = SpreadsheetApp.newDataValidation().requireValueInRange(countryRange).build();
  
 //Working to setup the sheet 
 var sheet = SpreadsheetApp.getActiveSheet(); 
 var startRow = getTagRow(sheet)+1 
 var countryCol = getTagCol("#"+prefix+"country+identifier",sheet) 
 
 var selectionCol = countryCol - 1 
 var selectionRange = sheet.getRange(startRow, selectionCol,sheet.getMaxRows()-startRow-1,1) 
 selectionRange.setDataValidation(countryRule)
 
 var colId = String.fromCharCode(64 + selectionCol);
 var lookupRange = sheet.getRange(startRow, countryCol,sheet.getMaxRows()-startRow-1,1) 
 lookupRange.setFormula("=IF(LEN("+colId+ startRow+")=0,\"\",VLOOKUP("+colId+startRow+",'"+codelistCountry+"'!$B:$G,6,false))")
  
}

//Set validation against the commodity codelist
function setCommodityValidation() {
 var commoditySheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(codelistCommodity);
 var commodityTypeRange = commoditySheet.getRange(2,1,commoditySheet.getLastRow()-1,1);
 var commodityTypeRule = SpreadsheetApp.newDataValidation().requireValueInRange(commodityTypeRange).build();
 var commodityRange = commoditySheet.getRange(2,4,commoditySheet.getLastRow()-1,1);
 var commodityRule = SpreadsheetApp.newDataValidation().requireValueInRange(commodityRange).build(); 
  
 //Working to setup the sheet 
 var sheet = SpreadsheetApp.getActiveSheet(); 
 var startRow = getTagRow(sheet)+1 
 
 var typeCol = getTagCol("#commodity+commodityType",sheet) 
 if(typeCol) {
   var selectionRange = sheet.getRange(startRow, typeCol,sheet.getMaxRows()-startRow-1,1) 
   selectionRange.setDataValidation(commodityTypeRule)
 }

 var valueCol = getClassCol("Commodity",sheet)
 
 if(valueCol) {
   var valueRange = sheet.getRange(startRow, valueCol,sheet.getMaxRows()-startRow-1,1) 
   valueRange.setDataValidation(commodityRule)
 }
  
}

//Set status validation
function setStatusValidation () {
 var statusSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(codelistStatus);
 var statusTypeRange = statusSheet.getRange(2,1,statusSheet.getLastRow()-1,1);
 var statusTypeRule = SpreadsheetApp.newDataValidation().requireValueInRange(statusTypeRange).build();
  
 //Working to setup the sheet 
 var sheet = SpreadsheetApp.getActiveSheet(); 
 var startRow = getTagRow(sheet)+1 
 var typeCol = getTagCol("#status+statusType",sheet) 
 
 var selectionRange = sheet.getRange(startRow, typeCol,sheet.getMaxRows()-startRow-1,1) 
 selectionRange.setDataValidation(statusTypeRule)
  
}


//Set production validation
function setProductionValidation () {
 var productionSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(codelistProduction);
 var productionUnitRange = productionSheet.getRange(2,1,productionSheet.getLastRow()-1,1);
 var productionUnitRule = SpreadsheetApp.newDataValidation().requireValueInRange(productionUnitRange).build();
 var productionPriceRange = productionSheet.getRange(2,3,productionSheet.getLastRow()-1,1);
 var productionPriceRule = SpreadsheetApp.newDataValidation().requireValueInRange(productionPriceRange).build(); 
  
 var sheet = SpreadsheetApp.getActiveSheet(); 
 var startRow = getTagRow(sheet)+1 
 
 var unitCol = getTagCol("#project+production+unit",sheet) 
 if(unitCol) {
   var selectionRange = sheet.getRange(startRow, unitCol,sheet.getMaxRows()-startRow-1,1) 
   selectionRange.setDataValidation(productionUnitRule)
 }
  
 var unitCol2 = getTagCol("#reserve+unit",sheet) 
 if(unitCol2) {
   var selectionRange = sheet.getRange(startRow, unitCol2,sheet.getMaxRows()-startRow-1,1) 
   selectionRange.setDataValidation(productionUnitRule)
 }

 var priceCol = getTagCol("#project+production+priceUnit",sheet) 
 if(priceCol) {
   var selectionRange = sheet.getRange(startRow, priceCol,sheet.getMaxRows()-startRow-1,1) 
   selectionRange.setDataValidation(productionPriceRule)
 }

 var volCol = getClassCol("Volume")
 if(volCol) {
   sheet.getRange(startRow, volCol,sheet.getMaxRows()-startRow-1,1)
     .setDataValidation(SpreadsheetApp.newDataValidation()
                        .requireNumberBetween(-999999999999999,9999999999999)
                        .setHelpText("Please enter a number. Do not include commas or symbols")
                        .build())

 }
  
 var priceCol = getClassCol("Price")
 if(priceCol) {
   sheet.getRange(startRow, priceCol,sheet.getMaxRows()-startRow-1,1)
     .setDataValidation(SpreadsheetApp.newDataValidation()
                        .requireNumberBetween(-999999999999999,9999999999999)
                        .setHelpText("Please enter a number. Do not include commas or symbols")
                        .build())

 }
 
}


function setSourceTypeValidation() {
  //Setup the validation rule
  var sourceCodelistSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(codelistSource);
  var sourceTypeRange = sourceCodelistSheet.getRange(2,2,sourceCodelistSheet.getLastRow()-1,1);
  var sourceTypeRule = SpreadsheetApp.newDataValidation().requireValueInRange(sourceTypeRange).build();

  var sheet = SpreadsheetApp.getActiveSheet(); 
  var startRow = getTagRow(sheet)+1 
  var selectionCol = getTagCol("#source+sourceType",sheet)
  var lookupCol = getTagCol("#source+sourceType+identifier",sheet)
 
  if(selectionCol) {
    var selectionRange = sheet.getRange(startRow, selectionCol,sheet.getMaxRows()-startRow-1,1) 
    selectionRange.setDataValidation(sourceTypeRule)
    
  }
  
  if(lookupCol && selectionCol < 26) {
    colId = String.fromCharCode(64 + selectionCol);
    var lookupRange = sheet.getRange(startRow, lookupCol,sheet.getMaxRows()-startRow,1) 
    lookupRange.setFormula("=IF(ISBLANK("+colId+startRow+"),\"\",VLOOKUP("+colId+startRow+",'"+codelistSource+"'!$B:$C,2,false))")
  }
  
  var sourceURLTypeRange = sourceCodelistSheet.getRange(2,6,sourceCodelistSheet.getLastRow()-1,1);
  var sourceURLTypeRule = SpreadsheetApp.newDataValidation().requireValueInRange(sourceURLTypeRange).build();

  var sourceURLTypeCol = getTagCol("#source+urlType",sheet)
  var selectionRange = sheet.getRange(startRow, sourceURLTypeCol,sheet.getMaxRows()-startRow-1,1) 
  selectionRange.setDataValidation(sourceURLTypeRule)
  
  
  var dateRule = SpreadsheetApp.newDataValidation().requireDate().setHelpText("Please enter a date").build();
  var sourceDateCol = getTagCol("#source+sourceDate",sheet)
  var selectionRange = sheet.getRange(startRow, sourceDateCol,sheet.getMaxRows()-startRow-1,1) 
  selectionRange.setDataValidation(dateRule)
  var accessDateCol = getTagCol("#source+retrievedDate",sheet)
  var selectionRange = sheet.getRange(startRow, accessDateCol,sheet.getMaxRows()-startRow-1,1) 
  selectionRange.setDataValidation(dateRule)
}



//setLookupValidation - General purpose function to:
//  - ensure values in the column identified in destionationTag on the destinationSheet
//    are taken from the column identified by sourceTag on the sourceSheet

function setLookupValidation(sourceSheetName,destinationSheetName,sourceTag,destinationTag) {
 //Hard coded codelist values 
  if(sourceSheetName == destinationSheetName) {
      SpreadsheetApp.getActiveSpreadsheet().toast("Cannot add validation to this sheet. " + sourceSheetName + " is the source sheet for " + destinationTag +" validation.")

  } else { 
    
   var sourceSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sourceSheetName);
   var sourceListCol = getTagCol(sourceTag,sourceSheet)
   var sourceStartRow = getTagRow(sourceSheet)+1 
   
   var sourceRange = sourceSheet.getRange(sourceStartRow,sourceListCol,sourceSheet.getMaxRows()-sourceStartRow,1);
    var sourceRule = SpreadsheetApp.newDataValidation().requireValueInRange(sourceRange)
    .setHelpText("All values in this column must be listed on the " + sourceSheetName + " sheet before they can be referenced here. Make sure the names are written exactly the same.")
    .build()
    
   //Working to setup the sheet 
   var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(destinationSheetName);
    
   var startRow = getTagRow(sheet)+1 
   var destinationCol = getTagCol(destinationTag,sheet) 
   if(destinationCol) {
     var selectionRange = sheet.getRange(startRow, destinationCol,sheet.getMaxRows()-startRow-1,1) 
     selectionRange.setDataValidation(sourceRule)
   }
  }
}

//Set project validation

function setProjectValidation() {
 setLookupValidation(sourcesheetProjects,SpreadsheetApp.getActiveSheet().getName(),"#project","#project")
}

//Set project validation

function setCompanyValidation() {
 setLookupValidation(sourcesheetCompanies,SpreadsheetApp.getActiveSheet().getName(),"#company","#project+company")
 setLookupValidation(sourcesheetCompanies,SpreadsheetApp.getActiveSheet().getName(),"#company","#company")
}


//Set source validation

function setSourceValidation() {
 setLookupValidation(sourcesheetSources,SpreadsheetApp.getActiveSheet().getName(),"#source","#project+source")
 setLookupValidation(sourcesheetSources,SpreadsheetApp.getActiveSheet().getName(),"#source","#source")
}


//LOOKUP TOOLS

function getTagClass(tag) {
  tag = stripTagLang(tag)
  tag = tag.replace("#","")
  class = tag.split("+").pop()
  return class.charAt(0).toUpperCase() + class.slice(1);
}

function getTagLang(tag) {
  var defaultLanguage = PropertiesService.getDocumentProperties().getProperty("defaultLanguage")

  if(tag.substring(tag.length-3,tag.length-2) == "+") {
    return tag.substring(tag.length-2,tag.length)
  } else {
    return defaultLanguage
  }
}

function stripTagLang(tag) {
  if(tag.substring(tag.length-3,tag.length-2) == "+") {
    return tag.substring(tag.length-3,0)
  } else {
    return tag
  }
}


function showSidebar(resultSet) {
  var template = HtmlService.createTemplateFromFile('Page');
  template.data = resultSet;
  SpreadsheetApp.getUi() // Or DocumentApp or FormApp.
      .showSidebar(template.evaluate().setSandboxMode(HtmlService.SandboxMode.IFRAME).setTitle('Select results').setWidth(450));
}



function regExpEscape(literal_string) {
    return literal_string.replace(/[-[\]{}()*+!<=:?.\/\\^$|#\s,]/g, '\\\\$&');
}

// Fetch all the details we need for an active search
function defineActiveSearch() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var cell = sheet.getActiveCell(); 
  var tagRow = getTagRow(sheet);
  var tag = sheet.getRange(tagRow,cell.getColumn(),1,1).getValue();
    
  var lang = getTagLang(tag)
  var class = getTagClass(tag)
  
  var identifierCol = getTagCol(stripTagLang(tag)+"+identifier",sheet)
  
  if(getTagCol(stripTagLang(tag)+"+country+identifier",sheet)) {
    var country = sheet.getRange(cell.getRow(),getTagCol(stripTagLang(tag)+"+country+identifier",sheet)).getValue();
  } else if(getTagCol("#country+identifier",sheet)) {
    var country = sheet.getRange(cell.getRow(),getTagCol("#country+identifier",sheet)).getValue();
  } else {
    var country = ""
    SpreadsheetApp.getActiveSpreadsheet().toast("Note: no country restriction found - check results carefully")
  }
  
  if (identifierCol) {
     // SpreadsheetApp.getActiveSpreadsheet().toast("Identifier in col" + identifierCol)
  } else {
     SpreadsheetApp.getActiveSpreadsheet().toast("No identifier column found for " + tag + ". We must have a column named '" 
                                                 + stripTagLang(tag)+"+identifier' in order to be able to write out lookup results."  )
  }
  
  return {
    cell: cell,
    tag: tag,
    countryRestriction: country,
    lang: lang,
    class: class,
    identifierCol: identifierCol
  }
  
}

function reconcileAll() {
  searchForID(true)
}


function searchForID(multiRow) {
  if(PropertiesService.getDocumentProperties().getProperty("vocab") == null) {
    configure_defaults();
  }
  var vocab = PropertiesService.getDocumentProperties().getProperty("vocab")
  var namespace = PropertiesService.getDocumentProperties().getProperty("namespace")
  var endpoint = PropertiesService.getDocumentProperties().getProperty("endpoint")
  var defaultLanguage = PropertiesService.getDocumentProperties().getProperty("defaultLanguage")

    
  var search = defineActiveSearch()
  
  var query = "prefix def: "+vocab
  + "\nSELECT DISTINCT * WHERE {\n"
  +"?s a def:" + search.class + ".\n";
  
  if(search.countryRestriction) {
    query += "?s def:hasLocation <"+ namespace + "country/"+search.countryRestriction+">.\n"
  }
  
  query += "?s skos:prefLabel ?label.\n";
  query += "OPTIONAL { ?s def:hasLocation ?country. ?country a def:Country. ?country skos:prefLabel ?countryName. }\n";
  
  query += "FILTER regex(?label, \""+regExpEscape(search.cell.getValue())+"\",\"i\")"
  +"}";

  Logger.log(query)
  var url = endpoint + "?format="+encodeURIComponent("application/sparql-results+json")+"&query="+encodeURIComponent(query)
  var response = UrlFetchApp.fetch(url);
  json = JSON.parse(response)
  
  Logger.log(response);
  
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  
  if(json.results.bindings.length < 1) {

    SpreadsheetApp.getActiveSpreadsheet().toast("No values found. Perform a manual search.")    

  } else if(json.results.bindings.length == 1) {

    updateCell(search.cell.getRow(),search.identifierCol,json.results.bindings[0].s.value)
    
  } else {
    // Check for an exact match of name in the results. If we find one and only one directly matching name we can use this.
    var foundValue = 0
    for(i = 0; i <= json.results.bindings.length; i++) {
      if(json.results.bindings[i].label.value == search.cell.getValue()) {
        foundID = json.results.bindings[i].s.value;
        var foundValue = foundValue+1
        break;
      }   
    } 
    
    if(foundValue == 1) {
      updateCell(search.cell.getRow(),search.identifierCol,foundID)
    } else {
    
          if(multiRow) {
            sheet.getRange(search.cell.getRow(),search.cell.getColumn()).setNote("Multiple possible responses found during bulk reconciliation. Run single reconciliation.")
          } else {
           SpreadsheetApp.getActiveSpreadsheet().toast("We found multiple possible IDs. Please select from the detailed interface.")
           showSidebar({
             results: json.results.bindings,
             row: search.cell.getRow(),
             col: search.identifierCol,
             search: search.cell.getValue()
           })
         } 
    }
  }
  
  if(multiRow) {
    sheet.setActiveRange(sheet.getRange(search.cell.getRow()+1,search.cell.getColumn()))
    if(sheet.getActiveRange().getValue()) {
      searchForID(true) 
    }
  }
   
  
}
  
function updateCell(row,col,value) {
 uri = value.split("/").splice(4).join("/")
 var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
 sheet.getRange(row,col).setFormula("=Hyperlink(\""+value.replace("http://","http://alpha.")+"\",\""+uri+"\")") 
 sheet.getRange(row,col-1).setNote("")
}





// Show and hide columns and rows
// To avoid problems with wrapped text in merged cells that span hidden columns, we set the width to 1 pixel before hiding
// and restore to 200 pixels when showing
function hideIdentifiers(sheet) {
  if(typeof sheet == 'undefined') {
    sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  }
  tagRow = getTagRow(sheet)
  for(col = 1; col < sheet.getLastColumn(); col++) {
    cellValue = sheet.getRange(tagRow,col,1,1).getValue()
    if(cellValue.indexOf("identifier") > -1) {
        sheet.setColumnWidth(col, 1);
        sheet.hideColumn(sheet.getRange(1,col)) 
    }
  }
}

function showIdentifiers(sheet) {
  if(typeof sheet == 'undefined') {
    sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  }
  tagRow = getTagRow(sheet)
  for(col = 1; col < sheet.getLastColumn(); col++) {
    cellValue = sheet.getRange(tagRow,col,1,1).getValue()
    if(cellValue.indexOf("identifier") > -1) {
        sheet.setColumnWidth(col, 200);
        sheet.unhideColumn(sheet.getRange(1,col)) 
    }
  }
}

function hideTagRow(sheet) {
  if(typeof sheet == 'undefined') {
    sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  }
  tagRow = getTagRow(sheet)
  sheet.hideRow(sheet.getRange(tagRow,1))
}

function showTagRow(sheet) {
  if(typeof sheet == 'undefined') {
    sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  }
  tagRow = getTagRow(sheet)
  sheet.unhideRow(sheet.getRange(tagRow,1))
}


function hideCodelists() {
   showHideCodelists("hide") 
}

function showCodelists() {
   showHideCodelists("show") 
}

function showHideCodelists(action) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheets = ss.getSheets();

  for (var sheetNum = 1; sheetNum < sheets.length; sheetNum++){
     var ws = ss.getSheets()[sheetNum]
     if(ws.getName().indexOf("Codelist") > -1) {
       if(action == "hide") { ws.hideSheet() }
       if(action == "show") { ws.showSheet() }
     }

  }
  
}