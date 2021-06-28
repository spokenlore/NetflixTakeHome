import requests
from src import table_functions


# A user should be able to access the homepage
def test_database_home_page():
    response = requests.get(table_functions.app_url)
    assert response.status_code == 200
    assert response.content != "", "homepage content was empty"


# A user should be able to see a full list of rows on the home page
def test_database_load_page():
    table_rows = table_functions.load_data(page=1)
    assert len(table_rows) == 10
    for row in table_rows:
        # ID is a string in the db, but it should always be a number based off of the existing data
        assert row.computer_id.isnumeric()
        assert row.computer_name != ""


# A user should be able to get all the database rows by iterating over the pages
# Note: Slow (iterates over ~60 pages), and a live DB could have more data introduced / removed at any given time
def test_full_database_load():
    table_rows = table_functions.load_data()
    assert table_functions.get_total_count() == len(table_rows)
    for row in table_rows:
        assert row.computer_id.isnumeric()
        assert row.computer_name != ""


# A user should be able to add a computer with just a name
def test_add_computer_name_only():
    computer_name = "A"
    total_count = table_functions.get_total_count(filter=computer_name)
    response = table_functions.add_computer("A")
    # database count should increment by 1 after adding a new computer
    assert table_functions.get_total_count(filter=computer_name) == total_count + 1
    assert response.status_code == 200


# A user should be able to add a computer with all form fields filled
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


# A user is blocked from adding a computer with invalid introduced date in the UI, so the API should block it too
# This inexplicably does not fail (the computer is added with no date)
def test_add_computer_with_invalid_introduced_date():
    # this date does not conform to 'yyyy-MM-dd' UI requirement
    introduced_date = "abc"
    computer_name = "A"
    total_count = table_functions.get_total_count(filter=computer_name)

    # invalid discontinued date
    response = table_functions.add_computer(computer_name, introduced_date=introduced_date)
    assert response.status_code == 400
    assert table_functions.get_total_count(filter=computer_name) == total_count


# A user is blocked from adding a computer with invalid discontinued date in the UI, so the API should block it too
def test_add_computer_with_invalid_discontinued_date():
    # this date does not conform to 'yyyy-MM-dd' UI requirement
    discontinued_date = "def"
    computer_name = "A"
    total_count = table_functions.get_total_count(filter=computer_name)

    # invalid discontinued date
    response = table_functions.add_computer(computer_name, discontinued_date=discontinued_date)
    assert response.status_code == 400
    assert table_functions.get_total_count(filter=computer_name) == total_count


# A user is blocked from adding a computer with a company that is not in the UI dropdown, so the API should block it too
def test_add_computer_with_invalid_company():
    company = "Apple"
    computer_name = "A"
    total_count = table_functions.get_total_count(filter=computer_name)

    # invalid discontinued date
    response = table_functions.add_computer(computer_name, company=company)
    assert response.status_code == 400
    assert table_functions.get_total_count(filter=computer_name) == total_count


# A user should not be able to reach a page for a computer which does not exist
def test_get_invalid_computer():
    response = requests.get(table_functions.app_url + "/0")
    assert response.status_code == 404


# A user should be able to go to the homepage, choose a computer to delete, delete it, and confirm that it is gone
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


# A user should be able to go to the homepage, choose a computer, and update its data
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
