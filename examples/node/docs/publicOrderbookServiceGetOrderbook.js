/**
 * Copyright 2019 Tulip Solutions B.V.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
const util = require('util');

const orders_pb = require('@tulipsolutions/tecl/common/orders_pb');
const orderbook_pb = require('@tulipsolutions/tecl/pub/orderbook_pb');
const orderbook_grpc = require('@tulipsolutions/tecl/pub/orderbook_grpc_pb');

function publicOrderbookServiceGetOrderbook(host, credentials, options) {
  // CODEINCLUDE-BEGIN-MARKER: ref-code-example-request
  const client = new orderbook_grpc.PublicOrderbookServiceClient(host, credentials);

  // Create a request for the BTC_EUR orderbook, with the greatest precision and largest length
  // See TBD for semantics of Precision and Length
  const request = new orderbook_pb.GetOrderbookRequest();
  request.setMarket(orders_pb.Market.BTC_EUR);
  request.setPrecision(orderbook_pb.Precision.P3);
  request.setLength(orderbook_pb.Length.NUM_ENTRIES_100);

  // Add a 1s deadline, and make the request asynchronously
  const deadline = new Date().setSeconds(new Date().getSeconds() + 1);
  const callOptions = Object.assign({ deadline: deadline }, options);
  client.getOrderbook(request, callOptions, (err, response) => {
    if (err) {
      console.error('PublicOrderbookService.GetOrderbook error: ' + err.message);
    }
    if (response) {
      console.log(response.toObject());
      // CODEINCLUDE-END-MARKER: ref-code-example-request
      parseAndPrint(response);
      // CODEINCLUDE-BEGIN-MARKER: ref-code-example-request
    }
  });
  // CODEINCLUDE-END-MARKER: ref-code-example-request
}

function parseAndPrint(response) {
  // CODEINCLUDE-BEGIN-MARKER: ref-code-example-response
  let resultString = util.format('%s\n', 'OrderbookEntries');
  response.getEntriesList().forEach(entry => {
    resultString += util.format(
      '\t%s %s %d orders @ %f total %f\n',
      'OrderbookEntry',
      Object.keys(orders_pb.Side).find(key => orders_pb.Side[key] === entry.getSide()),
      entry.getOrdersAtPriceLevel(),
      entry.getPriceLevel(),
      entry.getAmount()
    );
  });
  console.log(resultString);
  // CODEINCLUDE-END-MARKER: ref-code-example-response
}

module.exports = publicOrderbookServiceGetOrderbook;
