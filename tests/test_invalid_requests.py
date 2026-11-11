import urllib.request
import urllib.error
import json

tests = [
    {
        "name": "1. GET /api/users/999999 (Non-existent User ID)",
        "method": "GET",
        "url": "http://127.0.0.1/api/users/999999",
        "body": None,
        "expected_status": 404
    },
    {
        "name": "2. POST /api/users with missing name/email",
        "method": "POST",
        "url": "http://127.0.0.1/api/users",
        "body": {"role": "student"},
        "expected_status": 400
    },
    {
        "name": "3. PUT /api/users/999999 (Update Non-existent User)",
        "method": "PUT",
        "url": "http://127.0.0.1/api/users/999999",
        "body": {"name": "Ghost", "email": "ghost@test.com"},
        "expected_status": 404
    },
    {
        "name": "4. GET /api/jobs/999999 (Non-existent Job ID)",
        "method": "GET",
        "url": "http://127.0.0.1/api/jobs/999999",
        "body": None,
        "expected_status": 404
    },
    {
        "name": "5. POST /api/jobs with missing required fields",
        "method": "POST",
        "url": "http://127.0.0.1/api/jobs",
        "body": {"location": "Remote"},
        "expected_status": 400
    },
    {
        "name": "6. GET /api/applications/999999 (Non-existent Application)",
        "method": "GET",
        "url": "http://127.0.0.1/api/applications/999999",
        "body": None,
        "expected_status": 404
    },
    {
        "name": "7. POST /api/applications with non-existent foreign keys",
        "method": "POST",
        "url": "http://127.0.0.1/api/applications",
        "body": {"job_id": 99999, "applicant_id": 99999},
        "expected_status": 400
    },
    {
        "name": "8. GET /api/users/999999/jobs (Nested Route Non-existent Parent)",
        "method": "GET",
        "url": "http://127.0.0.1/api/users/999999/jobs",
        "body": None,
        "expected_status": 404
    },
    {
        "name": "9. GET /api/jobs/999999/applications (Nested Route Non-existent Parent)",
        "method": "GET",
        "url": "http://127.0.0.1/api/jobs/999999/applications",
        "body": None,
        "expected_status": 404
    },
    {
        "name": "10. DELETE /api/applications/999999 (Delete Non-existent Application)",
        "method": "DELETE",
        "url": "http://127.0.0.1/api/applications/999999",
        "body": None,
        "expected_status": 404
    },
    {
        "name": "11. GET /api/undefined_endpoint_path (Unknown Route)",
        "method": "GET",
        "url": "http://127.0.0.1/api/undefined_endpoint_path",
        "body": None,
        "expected_status": 404
    }
]

print("=====================================================================")
print("          TESTING INVALID REQUESTS (API ERROR HANDLING)             ")
print("=====================================================================")

for t in tests:
    req = urllib.request.Request(t["url"], method=t["method"])
    if t["body"] is not None:
        data = json.dumps(t["body"]).encode("utf-8")
        req.data = data
        req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=3) as resp:
            status = resp.status
            body = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        status = e.code
        body = e.read().decode("utf-8")
    except Exception as e:
        status = 0
        body = str(e)

    pass_status = "PASS" if status == t["expected_status"] else "FAIL"
    print(f"[{pass_status}] Status: {status} (Expected: {t['expected_status']}) -> {t['name']}")
    print(f"       Response Body: {body.strip()[:180]}")
    print("---------------------------------------------------------------------")
