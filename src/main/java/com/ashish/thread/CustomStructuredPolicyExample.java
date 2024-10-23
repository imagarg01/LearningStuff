package com.ashish.thread;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.Callable;
import java.util.concurrent.StructuredTaskScope;
import java.util.function.Supplier;

import org.apache.commons.lang3.RandomUtils;

class FlightTicketPrice{

    int mPrice;
    String mNameOfAirline;
    FlightTicketPrice(String nameOfAirline, int price){
        this.mNameOfAirline = nameOfAirline;
        this.mPrice = price;
    }
}

public class CustomStructuredPolicyExample {

    public static void main(String[] args) {

        try (var scope = new LeastPriceScope<FlightTicketPrice>()){
            var firstAirline = scope.fork(getPriceFromAirline1("Indigo"));
            var rainyWeatherSubTask = scope.fork(getPriceFromAirline2("AirIndia"));
            var coldWeatherState = scope.fork(getPriceFromAirline3("Alaska"));

            scope.join();

            float bestPrice = scope.result();
            System.out.println("My best price is "+bestPrice);
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
    }

    private static Callable<FlightTicketPrice> getPriceFromAirline1(String nameOfAirline){
        //Let assume we are calling a rest API here and getting some price from it
        return () -> {
            Thread.sleep(100);
            return new FlightTicketPrice(nameOfAirline,RandomUtils.nextInt());
        };
    }

    private static Callable<FlightTicketPrice> getPriceFromAirline2(String nameOfAirline){
        //Let assume we are calling a rest API here and getting some price from it
        return () -> {
            Thread.sleep(100);
            return new FlightTicketPrice(nameOfAirline,RandomUtils.nextInt());
        };
    }

    private static Callable<FlightTicketPrice> getPriceFromAirline3(String nameOfAirline){
        //Let assume we are calling a rest API here and getting some price from it
        return () -> {
            Thread.sleep(100);
            return new FlightTicketPrice(nameOfAirline,RandomUtils.nextInt());
        };
    }


}

class LeastPriceScope<T> extends StructuredTaskScope<T> {

    ArrayList<Integer> arrayOfPrices = new ArrayList<Integer>();
    private int bestPrice;
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
                FlightTicketPrice result = (FlightTicketPrice) subtask.get();
                 arrayOfPrices.add(result.mPrice);
                synchronized (this) {
                    bestPrice = Collections.min(arrayOfPrices);
                }
            }
            case FAILED -> exceptions.add(subtask.exception());
        }
    }

    public int result(){
        return bestPrice;
    }

    public <X extends Throwable> float resultOrElseThrow(
            Supplier<? extends X> exceptionSupplier) throws X {
        ensureOwnerAndJoined();
        if (bestPrice != 0) {
            return bestPrice;
        } else {
            X exception = exceptionSupplier.get();
            exceptions.forEach(exception::addSuppressed);
            throw exception;
        }
    }
}
