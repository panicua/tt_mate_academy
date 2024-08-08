import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

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

    def start_driver(self):
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(options=chrome_options)

    def stop_driver(self):
        if self.driver:
            self.driver.quit()

    def get_courses(self):
        self.driver.get(self.url)

        courses_elements = self.driver.find_elements(
            By.XPATH, COURSES_ELEMENTS_XPATH
        )[:-1]
        courses = []
        for course in courses_elements:
            try:
                name = course.find_element(By.XPATH, COURSE_NAME_XPATH).text
                description = course.find_element(
                    By.XPATH, COURSE_DESCRIPTION_XPATH
                ).text
                flex_elements = course.find_elements(
                    By.XPATH, COURSE_FLEX_XPATH
                )
                full_time_elements = course.find_elements(
                    By.XPATH, COURSE_FULL_TIME_XPATH
                )

                if flex_elements:
                    flex_url = flex_elements[0].get_attribute("href")
                    courses.append(
                        {
                            "name": name,
                            "description": description,
                            "type": CourseType.FLEX,
                            "url": flex_url,
                        }
                    )

                if full_time_elements:
                    full_time_url = full_time_elements[0].get_attribute("href")
                    courses.append(
                        {
                            "name": name,
                            "description": description,
                            "type": CourseType.FULL_TIME,
                            "url": full_time_url,
                        }
                    )

            except Exception as e:
                logging.error(f"Error processing a course element: {e}")

        return courses

    def extract_course_details(self, url):
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

    def create_courses(self, courses):
        list_of_courses = []
        for course in courses:
            try:
                details = self.extract_course_details(course["url"])
                if details:
                    list_of_courses.append(
                        CourseDTO(
                            name=course["name"],
                            description=course["description"],
                            type=course["type"],
                            modules_num=details["modules_num"],
                            topics_num=details["topics_num"],
                            course_duration=details["course_duration"],
                            detailed_page_url=course["url"],
                        )
                    )
            except Exception as e:
                logging.error(f"Error processing course {course['name']}: {e}")
        return list_of_courses

    def run(self):
        logging.info("Starting scraper")
        self.start_driver()
        try:
            courses = self.get_courses()
            detailed_courses = self.create_courses(courses)
            write_courses_to_json(
                filename=OUTPUT_FILENAME, courses=detailed_courses
            )
            logging.info(
                f"Scraping completed. {len(detailed_courses)} courses found"
            )
        finally:
            self.stop_driver()


if __name__ == "__main__":
    scraper = CourseScraper(url=BASE_URL, headless=True)
    scraper.run()
