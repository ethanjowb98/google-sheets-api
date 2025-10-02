import gspread
from pathlib import Path
from gsheets import parse_xml
from data import constants
from data.constants import QADashboardSheets
from google.oauth2.service_account import Credentials
from time import sleep

# Run this python command to run this python script:
# python -m gsheets.test_script_duration
CORE_FEATURE = "HRP"
ENVIRONMENT = "DEVELOP"
MILESTONE = "W Sprint | 2025"
REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports"

creds = Credentials.from_service_account_file(constants.credentials_file, scopes=constants.scopes)
client = gspread.authorize(creds)

sheet = client.open_by_key(constants.qa_automation_dashboard)
sheet = sheet.worksheet(QADashboardSheets.test_script_duration)

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

        sheet.update_cell(row, col, t.duration)

        counter += 1
        total_counter += 1
        print(f"Total: {total_counter} | Subtotal: {counter}/{len(tcs)} | Updated {t.name} with duration {t.duration}s")
        sleep(1)
