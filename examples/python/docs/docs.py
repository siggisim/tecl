#!/usr/bin/env python
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


import base64
import sys
import os
from concurrent.futures import ThreadPoolExecutor

import grpc
from private_active_orders_service_get_active_orders import private_active_orders_service_get_active_orders
from private_active_orders_service_stream_active_orders import private_active_orders_service_stream_active_orders
from private_order_service_cancel_order import private_order_service_cancel_order
from private_order_service_create_order import private_order_service_create_order
from private_order_service_get_events_for_order import private_order_service_get_events_for_order
from private_order_service_get_order_events import private_order_service_get_order_events
from private_order_service_stream_order_events import private_order_service_stream_order_events
from private_trade_service_get_trades import private_trade_service_get_trades
from private_trade_service_stream_trades import private_trade_service_stream_trades
from private_wallet_service_get_balance import private_wallet_service_get_balance
from private_wallet_service_stream_balance import private_wallet_service_stream_balance
from public_market_detail_service_get_market_details import public_market_detail_service_get_market_details
from public_market_detail_service_stream_market_details import public_market_detail_service_stream_market_details
from public_ohlc_service_get_ohlc_data import public_ohlc_service_get_ohlc_data
from public_ohlc_service_stream_ohlc_data import public_ohlc_service_stream_ohlc_data
from public_orderbook_service_get_orderbook import public_orderbook_service_get_orderbook
from public_orderbook_service_stream_orderbook import public_orderbook_service_stream_orderbook
from public_ticker_service_get_tickers import public_ticker_service_get_tickers
from public_ticker_service_stream_tickers import public_ticker_service_stream_tickers
from public_trade_service_get_trades import public_trade_service_get_trades
from public_trade_service_stream_trades import public_trade_service_stream_trades
from tulipsolutions.api.auth import jwt_interceptor
from tulipsolutions.api.auth import message_authentication_interceptor


if __name__ == '__main__':
    args = sys.argv
    if len(args) == 1:
        # Use system CA trust store to connect to public MockGrpc service.
        address = 'mockgrpc.test.tulipsolutions.nl:443'
        creds = grpc.ssl_channel_credentials()
    elif len(args) == 3:
        # Use Mock CA certificates from this repository
        # The server cert is set up to accept connections to localhost
        ca_cert_path = 'mockgrpc/src/main/resources/certs/mock_ca.crt'
        if not os.path.exists(ca_cert_path):
            # If this file is run from the examples workspace, the cert file will be placed here by Bazel
            ca_cert_path = "external/nl_tulipsolutions_tecl/" + ca_cert_path
        with open(ca_cert_path, 'rb') as ca_cert_file:
            trust_cert_collection = ca_cert_file.read()
        creds = grpc.ssl_channel_credentials(trust_cert_collection)
        address = '%s:%s' % (args[1], args[2])
    elif len(args) == 4:
        # Use command line provided CA certificate bundle
        address = '%s:%s' % (args[1], args[2])
        with open(args[3], 'rb') as ca_cert_file:
            trust_cert_collection = ca_cert_file.read()
        creds = grpc.ssl_channel_credentials(trust_cert_collection)
    else:
        print("USAGE: DocsMain [host port [trustCertCollectionFilePath]]")
        sys.exit(1)

    with grpc.secure_channel(address, creds) as channel:
        # Create a SHA256 HMAC with the base64 decoded 'secret' string as its key
        dummy_secret = base64.standard_b64decode("secret==")
        dummy_jwt = "eyJraWQiOiI2YzY4OTIzMi03YTcxLTQ3NGItYjBlMi1lMmI1MzMyNDQzOWUiLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIxMjM0In0.IL9QJQl55qn3oPsT7sFa7iwd5g1GsEQVr0IO7gCe1UmQdjT7jCIc-pUfjyYUgptPR8HBQl5ncXuBnxwjdXqOMwW1WhPmi_B3BRHQh3Sfu0zNXqKhkuz2-6DffXK1ek3DmK1NpaSikXtg2ruSQ4Uk5xHcnxmXY_SwEij0yot_JRKYEs-0RbyD5Z4jOFKcsbEW46WQmiWdgG3PUKiJT5TfdFd55JM55BwzSOdPIP1S_3dQ4VTDo30mWqAs1KaVbcPqCQmjT1PL0QScTp4w8-YPDcajcafIj98ve9LUoLBLraCIAX34D-hOxu643h9DoG2kIPFfZyXbkDTiUKOl7t-Ykg"  # noqa E501

        # Create an interceptor that signs messages with the provided secret.
        # Only messages to the private API that have a 'signed' field will be signed.
        message_auth_interceptor = message_authentication_interceptor.create(dummy_secret)
        # Create an interceptor that adds a JWT token when a request to a private service is made.
        jwt_interceptor = jwt_interceptor.create(dummy_jwt)
        # Add interceptors to all requests over the channel
        channel = grpc.intercept_channel(channel, jwt_interceptor, message_auth_interceptor)
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [
                executor.submit(private_active_orders_service_get_active_orders, channel),
                executor.submit(private_active_orders_service_stream_active_orders, channel),
                executor.submit(private_order_service_cancel_order, channel),
                executor.submit(private_order_service_create_order, channel),
                executor.submit(private_order_service_get_events_for_order, channel),
                executor.submit(private_order_service_get_order_events, channel),
                executor.submit(private_order_service_stream_order_events, channel),
                executor.submit(private_trade_service_get_trades, channel),
                executor.submit(private_trade_service_stream_trades, channel),
                executor.submit(private_wallet_service_get_balance, channel),
                executor.submit(private_wallet_service_stream_balance, channel),
                executor.submit(public_market_detail_service_get_market_details, channel),
                executor.submit(public_market_detail_service_stream_market_details, channel),
                executor.submit(public_orderbook_service_get_orderbook, channel),
                executor.submit(public_orderbook_service_stream_orderbook, channel),
                executor.submit(public_ticker_service_get_tickers, channel),
                executor.submit(public_ticker_service_stream_tickers, channel),
                executor.submit(public_trade_service_get_trades, channel),
                executor.submit(public_trade_service_stream_trades, channel),
                executor.submit(public_ohlc_service_get_ohlc_data, channel),
                executor.submit(public_ohlc_service_stream_ohlc_data, channel),
            ]
