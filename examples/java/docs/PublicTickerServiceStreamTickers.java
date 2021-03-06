// Copyright 2019 Tulip Solutions B.V.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package docs;

import io.grpc.ManagedChannel;
import io.grpc.stub.StreamObserver;
import nl.tulipsolutions.api.pub.PublicTickerServiceGrpc;
import nl.tulipsolutions.api.pub.PublicTickerServiceGrpc.PublicTickerServiceStub;
import nl.tulipsolutions.api.pub.StreamTickersRequest;
import nl.tulipsolutions.api.pub.Tick;

public class PublicTickerServiceStreamTickers {
    public static void run(ManagedChannel channel) {
        // CODEINCLUDE-BEGIN-MARKER: ref-code-example-request
        PublicTickerServiceStub stub = PublicTickerServiceGrpc.newStub(channel);

        // Create a request for streaming the tickers for all markets
        StreamTickersRequest request = StreamTickersRequest.getDefaultInstance();

        // Make the request asynchronously and add callbacks
        stub.streamTickers(request, new StreamObserver<Tick>() {
            public void onNext(Tick response) {
                System.out.println(response);
                // CODEINCLUDE-END-MARKER: ref-code-example-request
                parseAndPrint(response);
                // CODEINCLUDE-BEGIN-MARKER: ref-code-example-request
            }

            public void onError(Throwable t) {
                System.err.println("PublicTickerService.StreamTickers error: " + t.getMessage());
            }

            public void onCompleted() {
                System.out.println("PublicTickerService.StreamTickers completed");
            }
        });
        // CODEINCLUDE-END-MARKER: ref-code-example-request
    }

    public static void parseAndPrint(Tick response) {
        // CODEINCLUDE-BEGIN-MARKER: ref-code-example-response
        System.out.printf(
            "%s %s mid_price: %f best_buy_price: %f best_buy_size: %f " +
                "best_sell_price: %f best_sell_size: %f open: %f, high: %f low: %f close: %f " +
                "volume_base: %f volume_quote: %f\n",
            response.getClass().getSimpleName(),
            response.getMarket(),
            response.getMidPrice(),
            response.getBestBuyPrice(),
            response.getBestBuySize(),
            response.getBestSellPrice(),
            response.getBestSellSize(),
            response.getDailyOpen(),
            response.getDailyHigh(),
            response.getDailyLow(),
            response.getDailyClose(),
            response.getDailyVolumeBase(),
            response.getDailyVolumeQuote()
        );
        // CODEINCLUDE-END-MARKER: ref-code-example-response
    }
}
