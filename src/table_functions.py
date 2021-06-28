import requests
from bs4 import BeautifulSoup

app_url = "https://computer-database.herokuapp.com/computers"
HEADER = "ID | Name | Introduced | Discontinued | Company"


class TableRow:
    computer_id = ""
    computer_name = ""
    introduced_date = ""
    discontinued_date = ""
    company = ""

    def __init__(self, columns):
        self.computer_id = columns[0].find_all('a', href=True)[0]['href'].split("/")[2]
        self.computer_name = columns[0].text
        self.introduced_date = columns[1].text.strip()
        self.discontinued_date = columns[2].text.strip()
        self.company = columns[3].text.strip()

    def __str__(self):
        return "{self.computer_id} | {self.computer_name} | {self.introduced_date} | {self.discontinued_date} | {self.company}" \
            .format(self=self)


def get_homepage_content(page):
    content = requests.get(page).content
    soup = BeautifulSoup(content, 'html.parser')
    return soup


def get_total_count(filter=None):
    url = app_url + "?f={}".format(filter) if filter else app_url
    soup = get_homepage_content(url)

    # handle case where nothing exists for the current filter
    if soup.find_all('li', class_='current'):
        return int(soup.find_all('li', class_='current')[0].text.strip().split(" ")[5])
    else:
        return 0


def load_data(page=0):
    soup = get_homepage_content(app_url)
    pagination_counts = soup.find_all('li', class_='current')[0].text.strip().split(" ")
    # slice_start = pagination_counts[1]
    # slice_end = pagination_counts[3]
    total_count = int(pagination_counts[5])
    table_rows = []

    start_page = page if page else 1
    # +2 is to include the last page
    end_page = page + 1 if page else int(int(total_count) / 10) + 2
    for x in range(start_page, end_page):
        table = soup.findAll('table')[0]

        for row in table.find_all('tr'):
            columns = row.find_all('td')
            if columns:
                row = TableRow(columns)
                table_rows.append(row)
        next_page = app_url + "?p={}".format(x)
        soup = get_homepage_content(next_page)

    return table_rows


def create_form_data_dict(name, introduced="", discontinued="", company=""):
    return {
        "name": name,
        "introduced": introduced,
        "discontinued": discontinued,
        "company": company
    }


def get_computer(computer_id):
    response = requests.get(app_url + "/{}".format(computer_id))
    soup = BeautifulSoup(response.content, 'html.parser')
    field_values = soup.find_all("input")
    dropdown_value = soup.find('option', {'selected': True})

    if dropdown_value:
        dropdown_value = dropdown_value.text

    return create_form_data_dict(field_values[0]["value"], field_values[1]["value"],
                                 field_values[2]["value"], dropdown_value)


def add_computer(computer_name, introduced_date="", discontinued_date="", company=""):
    form_data = create_form_data_dict(computer_name, introduced=introduced_date, discontinued=discontinued_date,
                                      company=company)

    response = requests.post(app_url, data=form_data)
    return response


def update_computer(id, computer_name, introduced_date="", discontinued_date="", company=""):
    form_data = create_form_data_dict(computer_name, introduced=introduced_date, discontinued=discontinued_date,
                                      company=company)

    response = requests.post(app_url + "/{}".format(id), data=form_data)

    return response


# load_data()
# add_computer("ABC")
# add_computer("A", company="Apple")

get_computer(501)
