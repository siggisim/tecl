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
from tulipsolutions.api.priv import wallet_pb2, wallet_pb2_grpc


def private_wallet_service_stream_balance(channel):
    # CODEINCLUDE-BEGIN-MARKER: ref-code-example-request
    stub = wallet_pb2_grpc.PrivateWalletServiceStub(channel)

    # Create a request for streaming your balances for all currencies
    request = wallet_pb2.StreamBalanceRequest()

    try:
        # Make the request synchronously and iterate over the received orderbook entries
        for response in stub.StreamBalance(request):
            print(response)
            # CODEINCLUDE-END-MARKER: ref-code-example-request
            parse_and_print(response)
    # CODEINCLUDE-BEGIN-MARKER: ref-code-example-request
    except grpc.RpcError as e:
        print("PrivateWalletService.StreamBalance error: " + str(e), file=sys.stderr)
    # CODEINCLUDE-END-MARKER: ref-code-example-request


def parse_and_print(response):
    # CODEINCLUDE-BEGIN-MARKER: ref-code-example-response
    print(
        "{} {} total: {} locked: {}".format(
            type(response).__name__,
            orders_pb2.Currency.Name(response.currency),
            response.total_amount,
            response.locked_amount,
        )
    )
    # CODEINCLUDE-END-MARKER: ref-code-example-response
