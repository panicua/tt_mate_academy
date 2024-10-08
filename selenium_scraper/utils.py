import json
import logging
from typing import List

from selenium_scraper.dto import CourseDTO


def courses_to_dict(courses: List[CourseDTO]) -> List[dict]:
    return [
        {
            "course_name": course.name,
            "course_description": course.description,
            "course_type": course.course_type.value,
            "modules_num": course.modules_num,
            "topics_num": course.topics_num,
            "course_duration": course.course_duration,
        }
        for course in courses
    ]


def write_courses_to_json(filename: str, courses: list[CourseDTO]) -> None:
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(courses_to_dict(courses), file, indent=4, ensure_ascii=False)
    logging.info(f"Data written to {filename}")
