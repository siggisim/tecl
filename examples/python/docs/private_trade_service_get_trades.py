# Copyright 2019 Tulip Solutions B.V.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function

import sys

import grpc

from tulipsolutions.api.common import orders_pb2
from tulipsolutions.api.priv import trade_pb2, trade_pb2_grpc


def private_trade_service_get_trades(channel):
    # CODEINCLUDE-BEGIN-MARKER: ref-code-example-request
    stub = trade_pb2_grpc.PrivateTradeServiceStub(channel)

    # Create a request for your 10 most recent trades in the BTC_EUR market
    request = trade_pb2.GetPrivateTradesRequest(
        search_direction=orders_pb2.BACKWARD,
        limit=10,
        markets=[orders_pb2.BTC_EUR]
    )

    try:
        # Make the request synchronously with a 1s deadline
        response = stub.GetTrades(request, timeout=1)
        print(response)
    except grpc.RpcError as e:
        print("PrivateTradeService.GetTrades error: " + str(e), file=sys.stderr)
    # CODEINCLUDE-END-MARKER: ref-code-example-request

    # CODEINCLUDE-BEGIN-MARKER: ref-code-example-response
    result_string = "{}\n".format(type(response).__name__)
    for trade in response.trades:
        result_string += \
            "\t{}: {} {} {}@{} quote_amount: {} fee: {} {} time: {} id {} matched_orderid: {}\n".format(
                type(trade).__name__,
                orders_pb2.Market.Name(trade.market),
                orders_pb2.Side.Name(trade.side),
                trade.base_amount,
                trade.price,
                trade.quote_amount,
                orders_pb2.Currency.Name(trade.fee_currency),
                trade.fee,
                trade.timestamp_ns,
                trade.event_id,
                trade.order_id,
            )
    print(result_string)
    # CODEINCLUDE-END-MARKER: ref-code-example-response
