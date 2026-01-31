package com.ashish.thread;

import java.util.List;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CopyOnWriteArrayList;

/**
 * Demonstrates thread-safe collections.
 */
public class ConcurrentCollectionsDemo {

    public static void main(String[] args) {

        // 1. Thread-Safe Map
        var map = new ConcurrentHashMap<String, Integer>();

        // Atomic operations
        map.put("A", 1);
        map.compute("A", (k, v) -> v + 1); // Atomic update
        map.putIfAbsent("A", 10); // Won't overwrite

        System.out.println("Map: " + map);

        // 2. Thread-Safe List (Read Heavy)
        List<String> list = new CopyOnWriteArrayList<>();
        list.add("Item 1");

        // Iterator is safe from ConcurrentModificationException
        // It iterates over a snapshot
        for (String item : list) {
            System.out.println("Reading: " + item);
            list.add("Item 2"); // Safe to modify during iteration (change not visible in this loop)
        }

        System.out.println("List: " + list);
    }
}
