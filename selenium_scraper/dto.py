from dataclasses import dataclass
from enum import Enum


class CourseType(Enum):
    FULL_TIME = "full-time"
    FLEX = "flex"


@dataclass
class CourseDTO:
    name: str
    description: str
    type: CourseType
    # modules_num: int
    # topics_num: int
    # course_duration: str
