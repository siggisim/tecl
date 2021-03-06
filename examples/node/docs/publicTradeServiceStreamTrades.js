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

const trade_pb = require('@tulipsolutions/tecl/pub/trade_pb');
const orders_pb = require('@tulipsolutions/tecl/common/orders_pb');
const public_trade_grpc = require('@tulipsolutions/tecl/pub/trade_grpc_pb');

function publicTradeServiceStreamTrades(host, credentials, options) {
  // CODEINCLUDE-BEGIN-MARKER: ref-code-example-request
  const client = new public_trade_grpc.PublicTradeServiceClient(host, credentials);

  // Create a request for streaming all trades in the BTC_EUR market that occur after initiation of the request
  const request = new trade_pb.StreamPublicTradesRequest();
  request.setMarket(orders_pb.Market.BTC_EUR);

  // Make the request asynchronously
  const call = client.streamTrades(request, options);
  call.on('data', response => {
    console.log(response.toObject());
    // CODEINCLUDE-END-MARKER: ref-code-example-request
    parseAndPrint(response);
    // CODEINCLUDE-BEGIN-MARKER: ref-code-example-request
  });
  call.on('error', err => {
    console.error('PublicTradeService.StreamTrades error: ' + err.message);
  });
  call.on('end', () => {
    console.log('PublicTradeService.StreamTrades completed');
  });
  // CODEINCLUDE-END-MARKER: ref-code-example-request
}

function parseAndPrint(response) {
  // CODEINCLUDE-BEGIN-MARKER: ref-code-example-response
  console.log(
    util.format(
      '%s: %s %s %f@%f quote_amount: %f time: %s id: %s',
      'PublicTrade',
      Object.keys(orders_pb.Market).find(key => orders_pb.Market[key] === response.getMarket()),
      Object.keys(orders_pb.Side).find(key => orders_pb.Side[key] === response.getSide()),
      response.getBaseAmount(),
      response.getPrice(),
      response.getQuoteAmount(),
      response.getTimestampNs(),
      response.getEventId()
    )
  );
  // CODEINCLUDE-END-MARKER: ref-code-example-response
}

module.exports = publicTradeServiceStreamTrades;
