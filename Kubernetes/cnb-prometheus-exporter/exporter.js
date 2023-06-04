const axios = require('axios');
const fs = require('fs');
const express = require('express');
const FileDownload = require('js-file-download');

const app = express();
const port = 8080;
const filePath = 'exchange_rates.txt';
const fileUrl = 'https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/denni_kurz.txt'

function parseData(){
  // Read the downloaded file
  const fileContent = fs.readFileSync(filePath, { encoding: 'utf8', flag: 'r' });

  // Split the content by new lines to get individual rows
  const rows = fileContent.split('\n');

  // Initialize an empty array to store the currency data
  const currencyData = [];

  // Extract currency and exchange rate from each row
  for (let i = 2; i < rows.length; i++) {
    const row = rows[i].split('|');
    if(row.length == 5){
      const currency = row[1];
      const exchangeRate = parseFloat(row[4].replace(',', '.'));

      // Add currency and exchange rate as an object to the array
      currencyData.push({ currency, exchangeRate });
    }
  }
  return currencyData;
}

async function downloadCurrencies(){
  await axios.get(fileUrl, { responseType: 'stream' })
    .then(response => {
      const outputStream = fs.createWriteStream(filePath);
      response.data.pipe(outputStream);

      return new Promise(resolve => outputStream.on('finish', () => {
        console.log(`File downloaded successfully: ${filePath}`);
        console.log(`Data written to ${filePath} successfully.`);
        resolve();
      }));
    })
    .catch(error => {
      console.error('Error occurred while fetching data:', error);
    });
  return parseData();
}
  


  // Create a Prometheus exporter endpoint
  app.get('/metrics', (req, res) => {
    // Generate Prometheus metrics format
    let metrics = '';
    downloadCurrencies()
      .then(result => {
        result.forEach(data => {
          metrics += `exchange_rate{currency="${data.currency}"} ${data.exchangeRate}\n`;
        });
        return metrics;
      })
      .then(metrics => {
        res.setHeader('Content-Type', 'text/plain');
        res.send(metrics);
      });
  });

  // Start the server
  app.listen(port, () => {
    console.log(`Prometheus exporter is running on port ${port}`);
  });

