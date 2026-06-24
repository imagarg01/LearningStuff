# Java Performance

## Metrices

Time-based Metrices

- Throughput [op/s or MB/s]
- Average latency (=50th percentile) [ms]
- Percentile latency [p50, p90, p95, p99, p99.9]
- Startup time [ms]
- Warmup time [ms]

Resource-based Metrices

- CPU usage [%]
- Memory usage [MB]
- Memory access pattern and cache locality
- Memory pressur [MB/s]
- Disk usage [MB]
- Network usage [MB/s]
- Thread usage [count]
- Contention
- Code size
- SIMD
- J/op <- This is important

Platform

- CPU type, stepping
- Compute/retrieve ratio
- Cache size L1, L2, L3
- NUMA
- Memory bandwidth
- Memory latency
- Number of cores
- Core intercconnect properties
- OS type

Application Specifics

- Workload distribution
- Data shape and content
- Pollution
- Avergae throughput at steady state [op/s]
- Measured after warm-up
- If it ain't compiled, its hardly used anyway
- Garbage Collector

## Measuring

- Dont use a laptop
- Run the method many times (tens of thousands of times) before measuring
  - The JVM can infer constant, fold and speculate
- Use System:nanoTime with caution
