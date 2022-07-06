function doGet(e) {
  var tracks = getTracks()
  var result = {"result":tracks}
  return ContentService.createTextOutput(JSON.stringify(result))
    .setMimeType(ContentService.MimeType.JSON);
}


function getTracks() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Tracks");
  var lastRow = sheet.getLastRow();
  var lastCol = sheet.getLastColumn();
  var rng = sheet.getRange(1,1,lastRow,lastCol);
  var tracks = rng.getValues();
  //Logger.log(tracks);
  return tracks;
}
