from .test_script_duration import add_test_script_duration
from .test_script_status import add_test_script_status
from typing import Literal

CORE_FEATURE: Literal["HRP", "HQA 1", "HQA 2", "Boards"] = "HRP"
ENVIRONMENT: Literal["EPIC", "DEVELOP", "STAGING"] = "DEVELOP"
MILESTONE: str = "W Sprint | 2025 | 02"

add_test_script_status(CORE_FEATURE, ENVIRONMENT, MILESTONE)
add_test_script_duration(CORE_FEATURE, ENVIRONMENT, MILESTONE)
