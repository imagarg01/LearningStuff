package com.ashish.thread;

import java.util.concurrent.Callable;
import java.util.concurrent.StructuredTaskScope;

public class PlayingWithSC {

    record Weather(String condition) {}

    private static final int WEATHER_READ_DELAY_MS = 100;
    private static final String[] WEATHER_CONDITIONS = {"Sunny", "Rainy", "Cold"};

    public static void main(String[] args) {
        try (var scope = new StructuredTaskScope<Weather>()) {
            var sunnyWeatherTask = scope.fork(readWeather(WEATHER_CONDITIONS[0]));
            var rainyWeatherTask = scope.fork(readWeather(WEATHER_CONDITIONS[1]));
            var coldWeatherTask = scope.fork(readWeather(WEATHER_CONDITIONS[2]));

            scope.join();

            System.out.println("Sunny weather task state: " + sunnyWeatherTask.state());
            if (sunnyWeatherTask.state() == StructuredTaskScope.Subtask.State.SUCCESS) {
                System.out.println("Sunny weather result: " + sunnyWeatherTask.get());
            }

        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new WeatherReadException("Failed to read weather data", e);
        }
    }

    private static Callable<Weather> readWeather(String condition) {
        return () -> {
            Thread.sleep(WEATHER_READ_DELAY_MS);
            return new Weather(condition);
        };
    }

    static class WeatherReadException extends RuntimeException {
        public WeatherReadException(String message, Throwable cause) {
            super(message, cause);
        }
    }
}
