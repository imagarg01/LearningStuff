
# Thoughts

As an engineer working on different role in software industry, few bits has been settled for me.

- A great design always suppose to be simple, maintainable and scalable.
- Every line of code is a liability, if you are not able to understand and make other understand and maintain it. Its a bad design.
- Tech debt has to be paid upfront before you introduce any change in the system. Otherwise it will grow exponentially and will be very difficult to manage.
- An software can be failed for many reason i.e.
    1. Connection pool got exhaust
    2. Certificate got expired.
    3. etc.

Most of time we written code in reactive manner like if this failure come do this or that.  i.e. circuit breaker, retry, timeout, backoff, fallback etc. This shows experience but does not solve the root cause of failure. Design should be done in way which prevents such failures to happen.

How you can do that ?

1. Protecting the hot paths

**The Philosophy**: The "hot path" is the critical, high-frequency user-facing request-response cycle. Don't let heavy, complex, or unreliable work run synchronously in this path.

**Failure Modes Eliminated**: HTTP/proxy timeouts (504s), thread pool exhaustion, cascading latency spikes, and user-facing outages during peak load.

**Real-World Examples:**

- **Pre-computation & Static Serving**: Instead of calculating a complex product catalog on every request (taking ~200ms per record), run a background cron job to compute the catalog, upload it as a static JSON/blob to S3 or a CDN, and have the API simply serve the blob. If the generator job fails, users receive slightly stale data rather than an outright outage.

- **Asynchronous Offloading**: Never send confirmation emails, generate invoices/PDFs, or call third-party payment analytics synchronously inside a checkout API. Write an event or job to an internal queue and immediately return 200 OK to the customer.

1. Removing Components

2. Centralizing State
3. Use Robust System
4. Try to minimize stateful compoment in a system.

The best way to eliminate a failure mode is to not do something exciting (or if you can, not do anything at all).

- Bad design is always more impressive than good design. Complex system usually a result of bad design.
