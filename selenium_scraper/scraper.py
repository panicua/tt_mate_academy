import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium_scraper.dto import CourseDTO, CourseType
from selenium_scraper.utils import WebDriverManager
from selenium_scraper.utils import write_to_json


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

BASE_URL = "https://mate.academy/"
OUTPUT_FILE = "result.json"


def courses_scraper(url: str):
    logging.info("Starting scraper")
    with WebDriverManager(headless=True) as manager:
        driver = manager.driver
        driver.get(url)
        courses_elements = driver.find_elements(
            By.XPATH, "//*[@id='all-courses']/div/div/div/div"
        )[:-1]
        courses = create_courses(courses_elements)
        write_to_json(filename=OUTPUT_FILE, courses=courses)
    logging.info("Scraping completed")


def create_courses(courses: list[WebElement]) -> list[CourseDTO]:
    list_of_courses = []
    for i, course in enumerate(courses):
        try:
            name = course.find_element(By.XPATH, ".//a/h3").text
            description = course.find_element(By.XPATH, ".//p[2]").text
            flex = course.find_elements(
                By.XPATH, ".//*[@data-qa='fx-course-details-button']"
            )
            full_time = course.find_elements(
                By.XPATH,
                ".//*[@data-qa='fulltime-course-more-details-button']",
            )

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
