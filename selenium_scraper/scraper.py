import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from selenium_scraper.constants import (
    BASE_URL,
    OUTPUT_FILENAME,
    COURSES_ELEMENTS_XPATH,
    COURSE_DESCRIPTION_XPATH,
    COURSE_FLEX_XPATH,
    COURSE_FULL_TIME_XPATH,
    COURSE_NAME_XPATH,
    COURSE_MODULES_XPATH,
    COURSE_TOPICS_XPATH,
    COURSE_DURATION_XPATH,
)
from selenium_scraper.dto import CourseDTO, CourseType
from selenium_scraper.utils import write_courses_to_json

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class CourseScraper:
    def __init__(self, url: str, headless: bool = True):
        self.url = url
        self.headless = headless
        self.driver = None

    def start_driver(self) -> None:
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=chrome_options)

    def stop_driver(self) -> None:
        if self.driver:
            self.driver.quit()

    def get_course_elements(self) -> list[WebElement]:
        self.driver.get(self.url)
        return self.driver.find_elements(By.XPATH, COURSES_ELEMENTS_XPATH)[:-1]

    @staticmethod
    def extract_course_info(course_element: WebElement) -> tuple:
        try:
            name = course_element.find_element(
                By.XPATH, COURSE_NAME_XPATH
            ).text
            description = course_element.find_element(
                By.XPATH, COURSE_DESCRIPTION_XPATH
            ).text
            flex_elements = course_element.find_elements(
                By.XPATH, COURSE_FLEX_XPATH
            )
            full_time_elements = course_element.find_elements(
                By.XPATH, COURSE_FULL_TIME_XPATH
            )

            return name, description, flex_elements, full_time_elements
        except Exception as e:
            logging.error(f"Error extracting course info: {e}")
            return None, None, None, None

    def build_course_list(
            self, course_elements: list[WebElement]
    ) -> list[dict]:
        """Form list of course info (name, description, course_type, url)."""
        courses = []
        for course_element in course_elements:
            name, description, flex_elements, full_time_elements = (
                self.extract_course_info(course_element)
            )
            if name and description:
                if flex_elements:
                    flex_url = flex_elements[0].get_attribute("href")
                    courses.append(
                        {
                            "name": name,
                            "description": description,
                            "course_type": CourseType.FLEX,
                            "url": flex_url,
                        }
                    )
                if full_time_elements:
                    full_time_url = full_time_elements[0].get_attribute("href")
                    courses.append(
                        {
                            "name": name,
                            "description": description,
                            "course_type": CourseType.FULL_TIME,
                            "url": full_time_url,
                        }
                    )
        return courses

    def get_courses(self) -> list[dict]:
        """
        Get complete list of dictionaries with course info
        (name, description, course_type, url).
        """
        course_elements = self.get_course_elements()
        return self.build_course_list(course_elements)

    def extract_course_details(self, url: str) -> dict | None:
        """Get course detail (number of modules, topics, and duration)."""
        try:
            self.driver.get(url)
            modules_num = self.driver.find_element(
                By.XPATH, COURSE_MODULES_XPATH
            ).text
            topics_num = self.driver.find_element(
                By.XPATH, COURSE_TOPICS_XPATH
            ).text
            course_duration = self.driver.find_element(
                By.XPATH, COURSE_DURATION_XPATH
            ).text

            return {
                "modules_num": modules_num,
                "topics_num": topics_num,
                "course_duration": course_duration,
            }
        except Exception as e:
            logging.error(f"Error extracting details from {url}: {e}")
            return None

    def create_courses(self, courses: list[dict]) -> list[CourseDTO]:
        """Create CourseDTO objects from a list of dictionaries."""
        list_of_courses = []
        for course in courses:
            try:
                details = self.extract_course_details(course["url"])
                if details:
                    list_of_courses.append(
                        CourseDTO(
                            name=course["name"],
                            description=course["description"],
                            course_type=course["course_type"],
                            modules_num=details["modules_num"],
                            topics_num=details["topics_num"],
                            course_duration=details["course_duration"],
                            detailed_page_url=course["url"],
                        )
                    )
            except Exception as e:
                logging.error(f"Error processing course {course['name']}: {e}")
        return list_of_courses

    def run(self) -> None:
        logging.info("Starting scraper")

        self.start_driver()
        courses = self.get_courses()
        detailed_courses = self.create_courses(courses)
        write_courses_to_json(
            filename=OUTPUT_FILENAME, courses=detailed_courses
        )

        logging.info(
            f"Scraping completed. {len(detailed_courses)} courses found"
        )
        self.stop_driver()


if __name__ == "__main__":
    scraper = CourseScraper(url=BASE_URL, headless=True)
    scraper.run()
