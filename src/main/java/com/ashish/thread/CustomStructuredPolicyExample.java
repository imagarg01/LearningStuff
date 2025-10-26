package com.ashish.thread;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;
import java.util.concurrent.Callable;
import java.util.concurrent.StructuredTaskScope;
import java.util.function.Supplier;

record FlightTicketPrice(String airlineName, int price) {}

public class CustomStructuredPolicyExample {

    private static final String[] AIRLINE_NAMES = {"Indigo", "AirIndia", "Alaska"};
    private static final int API_CALL_DELAY_MS = 100;
    private static final Random random = new Random();

    public static void main(String[] args) {
        try (var scope = new LeastPriceScope<FlightTicketPrice>()) {
            var indigoTask = scope.fork(getPriceFromAirline(AIRLINE_NAMES[0]));
            var airIndiaTask = scope.fork(getPriceFromAirline(AIRLINE_NAMES[1]));
            var alaskaTask = scope.fork(getPriceFromAirline(AIRLINE_NAMES[2]));

            scope.join();

            var bestPrice = scope.result();
            System.out.println("My best price is " + bestPrice);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new FlightPriceException("Failed to get flight prices", e);
        }
    }

    private static Callable<FlightTicketPrice> getPriceFromAirline(String nameOfAirline) {
        // Simulates calling a REST API to get price from airline
        return () -> {
            Thread.sleep(API_CALL_DELAY_MS);
            // Generate a positive random price between 100 and 1000
            var price = 100 + random.nextInt(900);
            return new FlightTicketPrice(nameOfAirline, price);
        };
    }

    static class FlightPriceException extends RuntimeException {
        public FlightPriceException(String message, Throwable cause) {
            super(message, cause);
        }
    }
}

class LeastPriceScope<T extends FlightTicketPrice> extends StructuredTaskScope<T> {

    private final List<Integer> prices = Collections.synchronizedList(new ArrayList<>());
    private volatile int bestPrice = Integer.MAX_VALUE;
    private final List<Throwable> exceptions = Collections.synchronizedList(new ArrayList<>());

    @Override
    protected void handleComplete(Subtask<? extends T> subtask) {
        switch (subtask.state()) {
            case UNAVAILABLE -> {
                // Task not available, ignore
            }
            case SUCCESS -> {
                var result = subtask.get();
                if (result != null) {
                    var price = result.price();
                    prices.add(price);
                    synchronized (this) {
                        if (price < bestPrice) {
                            bestPrice = price;
                        }
                    }
                }
            }
            case FAILED -> {
                var exception = subtask.exception();
                if (exception != null) {
                    exceptions.add(exception);
                }
            }
        }
    }

    public int result() {
        ensureOwnerAndJoined();
        if (bestPrice == Integer.MAX_VALUE) {
            throw new IllegalStateException("No successful price results available");
        }
        return bestPrice;
    }

    public <X extends Throwable> int resultOrElseThrow(Supplier<? extends X> exceptionSupplier) throws X {
        ensureOwnerAndJoined();
        if (bestPrice != Integer.MAX_VALUE) {
            return bestPrice;
        } else {
            var exception = exceptionSupplier.get();
            exceptions.forEach(exception::addSuppressed);
            throw exception;
        }
    }

    public List<Throwable> getExceptions() {
        return new ArrayList<>(exceptions);
    }
}
