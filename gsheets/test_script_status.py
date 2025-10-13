import gspread
from pathlib import Path
from gsheets import parse_xml
from data import constants
from data.constants import TestScriptExecutionStatus, QADashboardSheets
from google.oauth2.service_account import Credentials
from time import sleep
from typing import Literal

def add_test_script_status(
    CORE_FEATURE: Literal["HRP", "HQA 2", "Boards"],
    ENVIRONMENT: Literal["EPIC", "DEVELOP", "STAGING"],
    MILESTONE: str
):
    """ Updates the test script status sheet in the QA Automation Dashboard.

    Args:
        CORE_FEATURE (Literal["HRP", "HQA 2", "Boards"]): _Core feature being tested._
        ENVIRONMENT (Literal["EPIC", "DEVELOP", "STAGING"]): _Environment being tested._
        MILESTONE (str): _Current milestone being tested._

    Raises:
        ValueError: If the environment is not one of the accepted values.
    """
    REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports"

    creds = Credentials.from_service_account_file(constants.credentials_file, scopes=constants.scopes)
    client = gspread.authorize(creds)

    sheet = client.open_by_key(constants.qa_automation_dashboard)
    sheet = sheet.worksheet(QADashboardSheets.test_script_status)

    cf_col = sheet.find("CORE FEATURE").col
    tc_col = sheet.find("TEST CASE").col

    # Finds what column values your current milestone is in the sorts it out in ascending order
    milestone_col = sorted([n.col for n in sheet.findall(MILESTONE)])

    # Given that for each milestone there are 3 environments and its placement is in order EPIC, DEVeELOP, STAGING
    ENV_OFFSET = {
        "EPIC": 0,
        "DEVELOP": 1,
        "STAGING": 2,
    }

    # Validates that the environment is correct
    if ENVIRONMENT not in ENV_OFFSET.keys():
        raise ValueError(f"Environment {ENVIRONMENT} is not valid. Must be one of {list(ENV_OFFSET.keys())}")

    # Sets the column to the correct environment
    col = milestone_col[0] + ENV_OFFSET[ENVIRONMENT]

    files = parse_xml.extract_files_to_process()
    total_counter = 0

    print("Starting to update test script status...")
    for f in files:
        tcs = parse_xml.extract_test_case_from_reports(f"{REPORTS_DIR}/{f}")
        counter = 0
        for t in tcs:
            # Initializes the row variable if it can find an existing test case name
            row = sheet.find(t.name)

            # If it cannot find the test case name then it will find the next available row
            if row is None:
                row = len(sheet.col_values(2)) + 1
                sheet.update_cell(row, cf_col, CORE_FEATURE)
                sheet.update_cell(row, tc_col, t.name)
            else:
                row = row.row

            if any([t.is_error, t.is_failed, t.is_skipped]) is False:
                sheet.update_cell(row, col, TestScriptExecutionStatus.passed)
            elif any([t.is_error, t.is_failed]):
                sheet.update_cell(row, col, TestScriptExecutionStatus.failed)
            elif t.is_skipped:
                sheet.update_cell(row, col, TestScriptExecutionStatus.not_executed)

            counter += 1
            total_counter += 1

            print(f"Total: {total_counter} | Subtotal: {counter}/{len(tcs)} | Updated {t.name}")
            sleep(1.25)
