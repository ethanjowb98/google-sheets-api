import re
import gspread
from google.oauth2.service_account import Credentials
from time import sleep

import data.constants as constants
from ..data.constants import TestScriptExecutionStatus
import gsheets.parse_xml as parse_xml

creds = Credentials.from_service_account_file(constants.credentials_file, scopes=constants.scopes)
client = gspread.authorize(creds)

sheet = client.open_by_key(constants.test_case_portal_sheet)

worksheet = sheet.sheet1

test_case_id_col = worksheet.find("Test Case ID").col
script_command_col = worksheet.find("Script Command").col
execution_status_col = worksheet.find(re.compile(r"Execution Status 1")).col
scripted_col = script_command_col = worksheet.find("Scripted?").col

column_header = {
    "Test Case ID": test_case_id_col,
    "Script Command": script_command_col,
    "Execution Status 1": execution_status_col,
    "Scripted?": scripted_col
}

test_case = {
    "APP_UN_BLKB": "APP_UN/BLKB",
    "EXEC_UN_BLKA": "EXEC_UN/BLKA",
    "EXEC_UN_BLKB": "EXEC_UN/BLKB"
}

files = parse_xml.extract_files_to_process()

def apply_test_case_status():
    for f in files:
        tcs = parse_xml.extract_test_case_from_reports(f"reports/{f}")
        for t in tcs:
            row_cell = worksheet.find(t.name.replace("test_", ""))

            if row_cell is None:
                row_cell = worksheet.find(t.name)

            if row_cell is None:
                print(f"{t.name} is missing")
                break

            row = row_cell.row

            # If all is false then it passes
            if any([t.is_error, t.is_failed, t.is_skipped]) is False:
                worksheet.update_cell(row, column_header["Execution Status 1"], TestScriptExecutionStatus.passed)
            elif any([t.is_error, t.is_failed]):
                worksheet.update_cell(row, column_header["Execution Status 1"], TestScriptExecutionStatus.failed)
            elif t.is_skipped:
                worksheet.update_cell(row, column_header["Execution Status 1"], TestScriptExecutionStatus.not_executed)

            sleep(2)
            # print("APPLYING TEST CASE------------------")
            # print(t)

def add_test_case_script_command():
    for f in files:
        tcs = parse_xml.extract_test_case_from_reports(f"reports/{f}")
        for t in tcs:

            # Check whether the test contains the special test case name
            # Adjust the test case name to the test case ID
            # Update

            test_case_id_number = t.name.replace("test_", "")[-6:]
            marker = t.name.replace("test_", "")[:-6]

            if marker in test_case.keys():
                # Transforms test case  "test_ABC_DEF_00_00" to "ABC_DEF"
                row_cell = worksheet.find(f"{test_case[marker]}{test_case_id_number}")
            else:
                row_cell = worksheet.find(t.name.replace("test_", ""))

            if row_cell is None:
                print(f"{t.name} is missing")
                break

            row = row_cell.row

            worksheet.update_cell(row, column_header["Script Command"], t.name)
            worksheet.update_cell(row, column_header["Scripted?"], "Scripted")
            sleep(2)
            # print("APPLYING TEST CASE------------------")
            # print(t)

# add_test_case_script_command()
apply_test_case_status()
