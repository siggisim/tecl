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
var util = require("util");

var order_pb = require("@tulipsolutions/tecl/priv/order_pb");
var orders_pb = require("@tulipsolutions/tecl/common/orders_pb");
var order_grpc = require("@tulipsolutions/tecl/priv/order_grpc_pb");

function privateOrderServiceCreateOrder(host, credentials, options) {
  // CODEINCLUDE-BEGIN-MARKER: ref-code-example-request
  var client = new order_grpc.PrivateOrderServiceClient(host, credentials);

  // CODEINCLUDE-BEGIN-MARKER: authentication-request
  // Create a request for a new order with an orderId that is the nanos since unix epoch
  var orderId = Date.now() * 1000000;
  var limitOrderRequest = new order_pb.LimitOrderRequest();
  limitOrderRequest.setSide(orders_pb.Side.BUY);
  limitOrderRequest.setBaseAmount(1.0);
  limitOrderRequest.setPrice(3000);
  var request = new order_pb.CreateOrderRequest();
  request.setMarket(orders_pb.Market.BTC_EUR);
  request.setTonce(orderId.toString());
  request.setLimitOrder(limitOrderRequest);
  // CODEINCLUDE-END-MARKER: authentication-request

  // Add a 1s deadline, and make the request asynchronously
  var deadline = new Date().setSeconds(new Date().getSeconds() + 1);
  var callOptions = Object.assign({deadline: deadline}, options);
  client.createOrder(request, callOptions, function (err, response) {
    if (err) {
      console.error("PrivateOrderService.CreateOrder error: " + err.message);
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
  var orderTypeDetail = "";
  switch (response.getOrderTypeCase()) {
    case order_pb.CreateOrderResponse.OrderTypeCase.LIMIT_ORDER:
      var order = response.getLimitOrder();
      orderTypeDetail = util.format(
        "%s %f@%f",
        Object.keys(orders_pb.Side).find(key => orders_pb.Side[key] === order.getSide()),
        order.getBaseAmount(),
        order.getPrice(),
      );
      break;
    default:
      orderTypeDetail = "Should not be empty!";
  }
  console.log(
    util.format(
      "%s: %d for market %s %s",
      "CreateOrderResponse",
      response.getOrderId(),
      Object.keys(orders_pb.Market).find(key => orders_pb.Market[key] === response.getMarket()),
      orderTypeDetail
    )
  );
  // CODEINCLUDE-END-MARKER: ref-code-example-response
}

module.exports = privateOrderServiceCreateOrder;
