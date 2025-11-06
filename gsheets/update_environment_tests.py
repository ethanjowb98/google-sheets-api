from .test_script_duration import add_test_script_duration
from .test_script_status import add_test_script_status
from typing import Literal
from pathlib import Path
import subprocess

CORE_FEATURE: Literal["HRP", "HQA 1", "HQA 2", "Boards"] = "Boards"
ENVIRONMENT: Literal["EPIC", "DEVELOP", "STAGING"] = "DEVELOP"
MILESTONE: str = "X Sprint | 2025 | 01"

print(f"Confirming {CORE_FEATURE} | {ENVIRONMENT} | {MILESTONE} ...")
breakpoint()


REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports"

# Removes existing reports directory and creates a new one
if Path(REPORTS_DIR).exists():
    subprocess.run("rm -rf reports", shell=True, check=True)
subprocess.run("mkdir reports", shell=True, check=True)

add_test_script_status(CORE_FEATURE, ENVIRONMENT, MILESTONE)
add_test_script_duration(CORE_FEATURE, ENVIRONMENT, MILESTONE)
