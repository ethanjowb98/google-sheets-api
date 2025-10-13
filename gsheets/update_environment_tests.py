from .test_script_duration import add_test_script_duration
from .test_script_status import add_test_script_status
from typing import Literal

CORE_FEATURE: Literal["HRP", "HQA 2", "Boards"] = "Boards"
ENVIRONMENT: Literal["EPIC", "DEVELOP", "STAGING"] = "STAGING"
MILESTONE: str = "W Sprint | 2025"

add_test_script_status(CORE_FEATURE, ENVIRONMENT, MILESTONE)
add_test_script_duration(CORE_FEATURE, ENVIRONMENT, MILESTONE)
