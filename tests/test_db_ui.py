from selenium import webdriver
from selenium.webdriver.common.by import By

app_url = "https://computer-database.herokuapp.com/computers"


# Given a user using chrome
# When navigating to the database's home page
# Then the counts of computers should match at the top and bottom
def test_homepage_counts_match():
    try:
        driver = webdriver.Chrome("../chromedriver.exe")
        driver.get(app_url)

        # Sanity check to make sure the correct page was reached
        assert driver.title == "Computers database"

        header_computer_count = int(driver.find_element(By.XPATH, "//section/h1").text.split(" ")[0])
        lower_computer_count = int(driver.find_element(By.XPATH, "//li[@class='current']").text.split(" ")[5])

        assert header_computer_count == lower_computer_count
    finally:
        driver.quit()


# Given a user using chrome and going to a specific page
# When clicking the banner element
# Then they should end up back on the home page
def test_homepage_button():
    try:
        driver = webdriver.Chrome("../chromedriver.exe")
        # empty filter (so that the url will change)
        driver.get(app_url + "?f=")

        homepage_button = driver.find_element(By.XPATH, "//h1[@class='fill']/a")
        homepage_button.click()
        assert driver.current_url == app_url

    finally:
        driver.quit()


# Given a user on the database's home page
# When they add a filter and activate it
# Then all results should have the filtered text
def test_filter():
    try:
        from test_computer_database import test_add_computer_name_only
        test_add_computer_name_only()
        driver = webdriver.Chrome("../chromedriver.exe")
        driver.get(app_url)
        filter_input = driver.find_element(By.XPATH, "//input[@type='search']")
        filter_input.click()
        # This should exist because add_computer adds a computer with name "ABC"
        filter_input.send_keys("ABC")
        filter_button = driver.find_element(By.XPATH, "//input[@type='submit']")
        filter_button.click()
        table_rows = driver.find_elements(By.XPATH, "//tbody/tr")

        for row in table_rows:
            assert "ABC" in row.text
    finally:
        driver.quit()


# Given a user on the database's home page
# When they navigate to the next page
# And then the previous page
# Then they should end up back on the home page
def test_navigation_buttons():
    try:
        driver = webdriver.Chrome("../chromedriver.exe")
        driver.get(app_url)

        # navigate to next page
        next_button = driver.find_element(By.XPATH, "//li[@class='next']/a")
        next_button.click()
        # confirm url changed
        assert driver.current_url == app_url + "?p=1"

        # navigate back (to homepage)
        previous_button = driver.find_element(By.XPATH, "//li[@class='prev']/a")
        previous_button.click()
        # assert url changed back to homepage
        assert driver.current_url == app_url
    finally:
        driver.quit()
