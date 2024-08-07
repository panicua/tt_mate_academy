import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium_scraper.dto import CourseDTO, CourseType
from selenium_scraper.utils import WebDriverManager
from selenium_scraper.utils import write_to_json

from selenium_scraper.constants import (
    BASE_URL,
    OUTPUT_FILENAME,
    COURSES_ELEMENTS_XPATH,
    COURSE_DESCRIPTION_XPATH,
    COURSE_FLEX_XPATH,
    COURSE_FULL_TIME_XPATH,
    COURSE_NAME_XPATH,
)


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def courses_scraper(url: str):
    logging.info("Starting scraper")
    with WebDriverManager(headless=True) as manager:
        driver = manager.driver
        driver.get(url)

        # Get all courses
        courses_elements = driver.find_elements(
            By.XPATH, COURSES_ELEMENTS_XPATH
        )[:-1]

        courses = create_courses(courses_elements)
        write_to_json(filename=OUTPUT_FILENAME, courses=courses)
    logging.info("Scraping completed")


def create_courses(courses: list[WebElement]) -> list[CourseDTO]:
    """Creates list of CourseDTO objects from list of web elements"""
    list_of_courses = []
    for i, course in enumerate(courses):
        try:
            name = course.find_element(By.XPATH, COURSE_NAME_XPATH).text
            description = course.find_element(
                By.XPATH, COURSE_DESCRIPTION_XPATH
            ).text
            flex = course.find_elements(By.XPATH, COURSE_FLEX_XPATH)
            full_time = course.find_elements(By.XPATH, COURSE_FULL_TIME_XPATH)

            if flex:
                list_of_courses.append(
                    CourseDTO(
                        name=name,
                        description=description,
                        type=CourseType.FLEX,
                    )
                )
            if full_time:
                list_of_courses.append(
                    CourseDTO(
                        name=name,
                        description=description,
                        type=CourseType.FULL_TIME,
                    )
                )
        except Exception as e:
            logging.error(f"Error processing course {i}: {e}")
    return list_of_courses


if __name__ == "__main__":
    courses_scraper(BASE_URL)
