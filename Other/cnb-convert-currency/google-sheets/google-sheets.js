function ConvertCurrency(currencyPair, conversionDate, amount) {
    var url = "https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/denni_kurz.txt?date=" + conversionDate;
    var response = UrlFetchApp.fetch(url);
    var responseText = response.getContentText();
    var lines = responseText.split('\n');
    var rate = 0;
    var found = false;
    
    for (var i = 2; i < lines.length; i++) {
      var line = lines[i];
      if (line.indexOf(currencyPair) > -1) {
        var parts = line.split('|');
        if (parts.length >= 5 && parts[3] == currencyPair.substring(0, 3)) {
          rate = parseFloat(parts[4].replace(',', '.')); // Convert comma to dot for decimal places
          found = true;
          break;
        }
      }
    }
  
    if (found) {
      return amount * rate;
    } else {
      throw 'Currency pair not found';
    }
  }