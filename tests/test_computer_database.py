import requests
from src import table_functions


# Smoke test
# Given an API request for the home page
# Then the status code should be 200, and the content should not be empty
def test_database_home_page():
    response = requests.get(table_functions.app_url)
    assert response.status_code == 200
    assert response.content != "", "homepage content was empty"


# This could be slightly flaky on a production DB, and it would be best to seed data before running this
# Given an API request for the first page of the database
# Then the user should find 10 rows of data
def test_database_load_page():
    table_rows = table_functions.load_data(page=1)
    assert len(table_rows) == 10
    for row in table_rows:
        # ID is a string in the db, but it should always be a number based off of the existing data
        assert row.computer_id.isnumeric()
        assert row.computer_name != ""


# Given an initial request to the database for the number of rows in the database
# When a user sends requests for all of the pages
# Then a user should be able to get all the database rows by iterating over the pages
# Note: Slow (iterates over ~60 pages), and a live DB could have more data introduced / removed at any given time
def test_full_database_load():
    table_rows = table_functions.load_data()
    assert table_functions.get_total_count() == len(table_rows)
    for row in table_rows:
        assert row.computer_id.isnumeric()
        assert row.computer_name != ""


# Given an API request to the save endpoint with just a computer name
# Then a new row should be created in the database
# Note: Could use better validation
def test_add_computer_name_only(computer_name = "ABC"):
    total_count = table_functions.get_total_count(filter=computer_name)
    response = table_functions.add_computer
    # database count should increment by 1 after adding a new computer
    assert table_functions.get_total_count(filter=computer_name) == total_count + 1
    assert response.status_code == 200


# Given a request with all form fields filled
# When a request is sent
# Then a new row should be created in the database
# Note: Could use better validation
def test_add_computer_with_valid_data():
    computer_name = "ABCDEF"
    introduced_date = "1990-01-01"
    discontinued_date = "2020-06-27"
    # company is a field by ID not str
    company = 1

    total_count = table_functions.get_total_count(filter=computer_name)

    response = table_functions.add_computer(computer_name, introduced_date=introduced_date,
                                            discontinued_date=discontinued_date, company=company)

    assert response.status_code == 200
    assert total_count + 1 == table_functions.get_total_count(filter=computer_name)


# Given that a user is blocked from submitting a form with invalid date
# When an API request is sent with the same information
# Then the request should fail and a new row should not be created in the database
def test_add_computer_with_invalid_introduced_date():
    # this date does not conform to 'yyyy-MM-dd' UI requirement
    introduced_date = "abc"
    computer_name = "A"
    total_count = table_functions.get_total_count(filter=computer_name)

    # invalid discontinued date
    response = table_functions.add_computer(computer_name, introduced_date=introduced_date)
    assert response.status_code == 400
    assert table_functions.get_total_count(filter=computer_name) == total_count


# Given that a user is blocked from submitting a form with invalid date
# When an API request is sent with the same information
# Then the request should fail and a new row should not be created in the database
def test_add_computer_with_invalid_discontinued_date():
    # this date does not conform to 'yyyy-MM-dd' UI requirement
    discontinued_date = "def"
    computer_name = "A"
    total_count = table_functions.get_total_count(filter=computer_name)

    # invalid discontinued date
    response = table_functions.add_computer(computer_name, discontinued_date=discontinued_date)
    assert response.status_code == 400
    assert table_functions.get_total_count(filter=computer_name) == total_count


# Given that a user is blocked from submitting a form with invalid company name
# When an API request is sent with the same information
# Then the request should fail and a new row should not be created in the database
def test_add_computer_with_invalid_company():
    company = "Apple"
    computer_name = "A"
    total_count = table_functions.get_total_count(filter=computer_name)

    # invalid discontinued date
    response = table_functions.add_computer(computer_name, company=company)
    assert response.status_code == 400
    assert table_functions.get_total_count(filter=computer_name) == total_count


# Given that a user is blocked from submitting a form with no computer name
# When an API request is sent with the same information
# Then the request should fail and a new row should not be created in the database
def test_add_computer_with_invalid_name():
    computer_name = ""
    total_count = table_functions.get_total_count(filter=computer_name)

    # invalid discontinued date
    response = table_functions.add_computer(computer_name)
    assert response.status_code == 400
    assert table_functions.get_total_count(filter=computer_name) == total_count


# Given that a user cannot access a computer with ID 0
# When an API request is sent for the same computer
# Then the request should fail
def test_get_invalid_computer():
    response = requests.get(table_functions.app_url + "/0")
    assert response.status_code == 404


# Given that a user can delete a computer from the UI
# When a request is sent with the same data
# Then computer should be removed from the database
def test_delete_computer():
    total_count = table_functions.get_total_count()
    table_rows = table_functions.load_data(page=1)
    computer_id = table_rows[0].computer_id
    _url = table_functions.app_url + '/{}/delete'.format(computer_id)

    response = requests.post(_url)

    # initially sends a 303 but redirects to 200
    assert response.status_code == 200
    assert total_count - 1 == table_functions.get_total_count()

    # deleted computer should no longer exist
    assert requests.get(table_functions.app_url + "/{}".format(computer_id)).status_code == 404


# Given a user is able to update a computer's information from the UI
# When a user updates the information to a known state, and then changes the data again
# Then the data should match what the user has submitted
def test_update_computer():
    table_rows = table_functions.load_data(page=1)
    computer_id = table_rows[0].computer_id

    computer_name = "ABCDEFGHIJK"

    # Can't guarantee what the data's state, so update it to a known state
    table_functions.update_computer(computer_id, computer_name, "", "", "")
    computer = table_functions.get_computer(computer_id)

    assert computer["name"] == computer_name
    assert computer["discontinued"] == ""
    assert computer["introduced"] == ""
    assert computer["company"] is None

    introduced_date = "2000-01-01"
    discontinued_date = "2010-10-10"
    # Corresponds to "Apple Inc."
    company = 1

    table_functions.update_computer(computer_id, computer_name, introduced_date=introduced_date,
                                    discontinued_date=discontinued_date, company=company)
    computer = table_functions.get_computer(computer_id)

    assert computer["name"] == computer_name
    assert computer["discontinued"] == discontinued_date
    assert computer["introduced"] == introduced_date
    assert computer["company"] == "Apple Inc."
