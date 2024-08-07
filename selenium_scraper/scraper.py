import json
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from selenium_scraper.dto import CourseDTO, CourseType
from selenium_scraper.utils import WebDriverManager


def courses_scraper():
    with WebDriverManager(headless=True) as manager:
        driver = manager.driver
        driver.get('https://mate.academy/')
        courses_elements_list = driver.find_elements(
            By.XPATH, '//*[@id="all-courses"]/div/div/div/div'
        )[:-1]

        courses = create_courses(courses_elements_list)
        write_to_json(filename="result.json", courses=courses)


def create_courses(courses: list[WebElement]) -> list[CourseDTO]:
    list_of_courses = []
    for i, course in enumerate(courses):
        name = course.find_element(By.XPATH, ".//a/h3").text
        description = course.find_element(By.XPATH, ".//p[2]").text

        flex = course.find_elements(
            By.XPATH, ".//*[@data-qa='fx-course-details-button']"
        )
        full_time = course.find_elements(
            By.XPATH, ".//*[@data-qa='fulltime-course-more-details-button']"
        )

        if flex:
            list_of_courses.append(CourseDTO(
                name=name,
                description=description,
                type=CourseType.FLEX,
                # modules_num=None,
                # topics_num=None,
                # course_duration=None
            ))

        if full_time:
            list_of_courses.append(CourseDTO(
                name=name,
                description=description,
                type=CourseType.FULL_TIME,
                # modules_num=None,
                # topics_num=None,
                # course_duration=None
            ))

    return list_of_courses


def courses_to_dict(courses: List[CourseDTO]) -> List[dict]:
    return [
        {
            'course_name': course.name,
            'course_description': course.description,
            'course_type': course.type.value
        }
        for course in courses
    ]


def write_to_json(filename: str, courses: list[CourseDTO]):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(courses_to_dict(courses), file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    courses_scraper()
