# Main constants
BASE_URL = "https://mate.academy/"
OUTPUT_FILENAME = "result.json"


# XPATH constants
COURSES_ELEMENTS_XPATH = "//*[@id='all-courses']/div/div/div/div"

COURSE_NAME_XPATH = ".//a/h3"
COURSE_DESCRIPTION_XPATH = ".//p[2]"
COURSE_FLEX_XPATH = ".//*[@data-qa='fx-course-details-button']"
COURSE_FULL_TIME_XPATH = ".//*[@data-qa='fulltime-course-more-details-button']"

COURSE_MODULES_XPATH = "//*[@id='course-program']/div[2]/div[1]/div[1]/p"
COURSE_TOPICS_XPATH = "//*[@id='course-program']/div[2]/div[1]/div[2]/p"
COURSE_DURATION_XPATH = "//*[@id='course-program']/div[2]/div[1]/div[3]/p"
