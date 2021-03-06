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

import time

import grpc

from tulipsolutions.api.common import orders_pb2
from tulipsolutions.api.priv import order_pb2, order_pb2_grpc


def private_order_service_cancel_order(channel):
    # CODEINCLUDE-BEGIN-MARKER: ref-code-example-request
    stub = order_pb2_grpc.PrivateOrderServiceStub(channel)

    # Create a request for an order cancellation with a tonce that is the nanos since unix epoch
    tonce = round(time.time() * 1E9)
    request = order_pb2.CancelOrderRequest(
        order_id=1,
        market=orders_pb2.BTC_EUR,
        tonce=int(tonce),
    )

    try:
        # Make the request synchronously with a 1s deadline
        response = stub.CancelOrder(request, timeout=1)
        print(response)
    except grpc.RpcError as e:
        print("PrivateOrderService.CancelOrder error: " + str(e), file=sys.stderr)
    # CODEINCLUDE-END-MARKER: ref-code-example-request

    # CODEINCLUDE-BEGIN-MARKER: ref-code-example-response
    print(
        "{}: {} for {}".format(
            type(response).__name__,
            response.order_id,
            orders_pb2.Market.Name(response.market),
        )
    )
    # CODEINCLUDE-END-MARKER: ref-code-example-response
