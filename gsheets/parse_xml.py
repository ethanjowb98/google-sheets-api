from xml.etree import ElementTree
from pathlib import Path

import subprocess
import textwrap

REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports"

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

def does_file_name_contains(file: Path, text: str) -> bool:
    """Checks if the given text is present in the file name.

    Args:
        file (Path): The file path object.
        text (str): The text to search for in the file name.

    Returns:
        bool: True if the text is found in the file name, False otherwise.
    """
    return file.name.find(text) != -1

def extract_files_to_process() -> list[str]:
    """Filters out the xml files that contain "filtered" in their name. Also removes
    any excess html and log files from previous test runs.

    Returns:
        list[str]: List of xml files with "filtered" in their name.
    """
    # Using glob so *.zip works or any * conditions

    # Moves any downloaded zip files to reports directory
    if list(Path.home().glob("Downloads/*.zip")):
        print("Moving downloaded report files...")
        subprocess.run(f"mv ~/Downloads/*.zip {REPORTS_DIR}/", shell=True, check=True)

    # Makes sure to extract any zip files in the reports directory
    if list(Path(REPORTS_DIR).glob("*.zip")):
        print("Extracting report files...")
        subprocess.run(f"unzip -o {REPORTS_DIR}/*.zip -d {REPORTS_DIR}/", shell=True, check=True)
        print("Organizing extracted files...")

    # Moves any extracted files from nested tests/reports directory to reports directory
    if list(Path(REPORTS_DIR / "tests" / "reports").glob("*")):
        subprocess.run(f"mv {REPORTS_DIR}/tests/reports/* {REPORTS_DIR}/", shell=True, check=True)
        print("Cleaning up extracted files...")
        subprocess.run(f"rm -rf {REPORTS_DIR}/tests {REPORTS_DIR}/*.zip", shell=True, check=True)

    # Moves any downloaded xml files to reports directory
    if list(Path.home().glob("Downloads/*.xml")):
        print("Moving downloaded xml report files...")
        subprocess.run(f"mv ~/Downloads/*.xml {REPORTS_DIR}/", shell=True, check=True)

    # Removes excess files
    subprocess.run(f"rm -rf {REPORTS_DIR}/*.html {REPORTS_DIR}/*.log", shell=True, check=True)
    # Returns a list of xml files with filtered in the name
    if list(Path(REPORTS_DIR).glob("*filtered*.xml")):
        print("Using filtered report files...")
        files = [f.name for f in Path(REPORTS_DIR).iterdir() if does_file_name_contains(f, "filtered")]
    else:
        print("Using all report files...")
        files = [f.name for f in Path(REPORTS_DIR).iterdir()]
    print(files)
    return files

def extract_test_case_from_reports(filename: str) -> list[TestCase]:
    """Extracts test cases from the given xml report file.

    Args:
        filename (str): The name of the xml report file.

    Returns:
        list[TestCase]: A list of TestCase objects extracted from the report.
    """
    return [TestCase(tc) for tc in ElementTree.parse(filename).getroot().findall("testsuite/testcase")]
