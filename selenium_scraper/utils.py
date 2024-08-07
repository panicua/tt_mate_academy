import json
import logging
from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium_scraper.dto import CourseDTO


class WebDriverManager:
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.driver = None

    def __enter__(self):
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(options=chrome_options)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.driver:
            self.driver.quit()


def courses_to_dict(courses: List[CourseDTO]) -> List[dict]:
    return [
        {
            "course_name": course.name,
            "course_description": course.description,
            "course_type": course.type.value,
        }
        for course in courses
    ]


def write_to_json(filename: str, courses: list[CourseDTO]):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(courses_to_dict(courses), file, indent=4, ensure_ascii=False)
    logging.info(f"Data written to {filename}")
