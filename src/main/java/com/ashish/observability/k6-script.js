import http from 'k6/http';
import { check, sleep } from 'k6';

// 1. Setup the stages of the load test
export const options = {
    stages: [
        { duration: '10s', target: 5 },  // Ramp up to 5 virtual users
        { duration: '30s', target: 5 },  // Stay at 5 users for 30s
        { duration: '10s', target: 0 },  // Ramp down to 0
    ],
    thresholds: {
        http_req_duration: ['p(95)<500'], // 95% of requests must complete within 500ms
    },
};

// 2. The main test execution
export default function () {
    const BASE_URL = 'http://localhost:8080/api/orders';

    // A. Hit the Zero-Code endpoint
    const resAuto = http.post(`${BASE_URL}/auto?item=Book`);
    check(resAuto, {
        'auto status is 200': (r) => r.status === 200,
    });

    // small pause
    sleep(0.5);

    // B. Hit the Manual Code endpoint
    const qty = Math.floor(Math.random() * 5) + 1; // 1 to 5
    const resManual = http.post(`${BASE_URL}/manual?item=Monitor&qty=${qty}`);
    check(resManual, {
        'manual status is 200': (r) => r.status === 200,
    });

    // C. Chaos Engineering: Inject a deliberately bad payload ~10% of the time
    if (Math.random() < 0.1) {
        // We know from the code that item="error" triggers our Chaos exception
        const resChaos = http.post(`${BASE_URL}/manual?item=error&qty=1`);
        check(resChaos, {
            'chaos status is 400 (Expected Error)': (r) => r.status === 400,
        });
    }

    sleep(1);
}
