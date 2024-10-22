package com.ashish.thread;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.Callable;
import java.util.concurrent.StructuredTaskScope;
import java.util.function.Supplier;

import org.apache.commons.lang3.RandomUtils;

record FlightTicketPrice(String nameOfAirline){

    FlightTicketPrice(String nameOfAirline, float price){
        this(nameOfAirline);
    }
}

public class CustomStructuredPolicyExample {

    public static void main(String[] args) {

        try (var scope = new LeastPriceScope<FlightTicketPrice>()){
            var firstAirline = scope.fork(getPriceFromAirline1("Indigo"));
            var rainyWeatherSubTask = scope.fork(getPriceFromAirline2("AirIndia"));
            var coldWeatherState = scope.fork(getPriceFromAirline3("Alaska"));

            scope.join();


        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
    }

    private static Callable<FlightTicketPrice> getPriceFromAirline1(String nameOfAirline){
        //Let assume we are calling a rest API here and getting some price from it
        return () -> {
            Thread.sleep(RandomUtils.nextLong());
            return new FlightTicketPrice(nameOfAirline,RandomUtils.nextFloat());
        };
    }

    private static Callable<FlightTicketPrice> getPriceFromAirline2(String nameOfAirline){
        //Let assume we are calling a rest API here and getting some price from it
        return () -> {
            Thread.sleep(RandomUtils.nextLong());
            return new FlightTicketPrice(nameOfAirline,RandomUtils.nextFloat());
        };
    }

    private static Callable<FlightTicketPrice> getPriceFromAirline3(String nameOfAirline){
        //Let assume we are calling a rest API here and getting some price from it
        return () -> {
            Thread.sleep(RandomUtils.nextLong());
            return new FlightTicketPrice(nameOfAirline,RandomUtils.nextFloat());
        };
    }


}

class LeastPriceScope<T> extends StructuredTaskScope<T> {

    private T bestResult;
    private final List<Throwable> exceptions =
            Collections.synchronizedList(new ArrayList<>());

    public LeastPriceScope() {
    }

    @Override
    protected void handleComplete(Subtask<? extends T> subtask) {
        switch (subtask.state()) {
            case UNAVAILABLE -> {
                // Ignore
            }
            case SUCCESS -> {
                T result = subtask.get();
                synchronized (this) {
                    if (bestResult == null || comparator.compare(result, bestResult) > 0) {
                        bestResult = result;
                    }
                }
            }
            case FAILED -> exceptions.add(subtask.exception());
        }
    }

    public <X extends Throwable> T resultOrElseThrow(
            Supplier<? extends X> exceptionSupplier) throws X {
        ensureOwnerAndJoined();
        if (bestResult != null) {
            return bestResult;
        } else {
            X exception = exceptionSupplier.get();
            exceptions.forEach(exception::addSuppressed);
            throw exception;
        }
    }
}
