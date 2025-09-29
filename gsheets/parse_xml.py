from xml.etree import ElementTree
from pathlib import Path

import subprocess
import textwrap

class TestCase:

    def __init__(self, tc_element: ElementTree.Element) -> None:
        self.tc_object: ElementTree.Element = tc_element
        self.name: str = tc_element.get('name')
        self.is_failed: bool = tc_element.find('failure') is not None
        self.is_error: bool = tc_element.find('error') is not None
        self.is_skipped: bool = tc_element.find('skippped') is not None
        self.duration: float = tc_element.get('time')

    def __str__(self):
        return textwrap.dedent(f"""
            Test Case: {self.name}
            Duration: {self.duration}
            Is failed: {self.is_failed}
            Is error: {self.is_error}
            Is skipped: {self.is_skipped}
        """)

def extract_files_to_process() -> list[str]:
    # Removes excess files
    subprocess.run("rm -rf reports/*.html reports/*.log", shell=True, check=True)

    return [f.name for f in Path("reports/").iterdir() if f.name.find("filtered") != -1]

def extract_test_case_from_reports(filename: str) -> list[TestCase]:
    return [TestCase(tc) for tc in ElementTree.parse(filename).getroot().findall("testsuite/testcase")]
