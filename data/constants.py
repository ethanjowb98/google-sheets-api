test_case_portal_sheet = "10hmS39tQ2UVeuAk5ssWra3mPR_UBq2ayB8F6w79xmlw"     # Test duplicate sheet
qa_automation_dashboard = "1khv7mCsTjQnEbw2JFDt4nQGPOtk78i3dDNiKVphHmY4"

class QADashboardSheets:
    environment_testing = "Environment Testing"
    scripting_task = "Scripting Task"
    test_script_status = "Test Script Status"
    test_script_duration = "Test Script Duration"

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
credentials_file = "credentials.json"

test_case = {
    "APP_UN_BLKB": "APP_UN/BLKB",
    "EXEC_UN_BLKA": "EXEC_UN/BLKA",
    "EXEC_UN_BLKB": "EXEC_UN/BLKB"
}

class TestScriptExecutionStatus:
    passed = "Passed"
    failed = "Failed"
    suspended = "Suspended"
    not_executed = "Not Executed"

class APIStatusCode:
    success = 200
    bad_request = 400
    unauthorized = 401
    forbidden = 403
    not_found = 404
    too_many_requests = 429
    internal_server_error = 500
    bad_gateway = 502
    service_unavailable = 503
    gateway_timeout = 504
