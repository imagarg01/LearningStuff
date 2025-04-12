package com.ashish.thread;

import java.util.concurrent.Callable;
import java.util.concurrent.StructuredTaskScope;

public class PlayingWithSC {

  record Weather(String weather) {
  }

  public static void main(String[] args) {

    try (var scope = new StructuredTaskScope<Weather>()) {
      var weatherSubTask = scope.fork(readSunnyWeather());
      var rainyWeatherSubTask = scope.fork(readRainyWeather());
      var coldWeatherState = scope.fork(readColdWeather());

      scope.join();

      System.out.println("State is " + weatherSubTask.state());

    } catch (InterruptedException e) {
      throw new RuntimeException(e);
    }
  }

  private static Callable<Weather> readSunnyWeather() {
    return () -> {
      Thread.sleep(100);
      return new Weather("Sunny");
    };
  }

  private static Callable<Weather> readRainyWeather() {
    return () -> {
      Thread.sleep(100);
      return new Weather("Rainy");
    };
  }

  private static Callable<Weather> readColdWeather() {
    return () -> {
      Thread.sleep(100);
      return new Weather("Cold");
    };
  }

   
}
