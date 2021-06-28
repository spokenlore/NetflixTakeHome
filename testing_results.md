Issues:
* Table sorting does not work
* Computer names sort/filter with uppercase characters after lowercase characters
    * Should sort irrespective of case
    * Current behavior:
        * ABC, DEF, a
    * Better behavior:
        * a, ABC, DEF
* Passing a sorting input that is not an int causes the application to error to a 'Bad request' page
* Passing a pagination input that is not an int causes the application to error to a 'Bad request' page
    * Not a big issue on this application (no form data), but ideally this would error on the page instead of moving
      away from the table
* Adding a computer with an invalid introduced date through a request adds the computer without an introduced date
    * The UI does not allow this, so the API should safeguard against it as well
* Adding a computer with an introduced date AFTER the discontinued date adds on the UI / API
    * This should be blocked by the form and API (most likely)

Concerns:
* No authentication for this application (realistically any user could delete the whole database)
* Computer name should likely be a unique field in the database
    * From the original data every computer name (which in this case appears to correspond to model) is unique
* Passing a pagination query parameter <1 decrements the pagination count, but doesn't affect the data
* i.e. Inputting -1 leads to -9 to 0 of 582 (which should say 1-10 because the data has not changed)
* In a 'real' application, the data should probably be returned by an API to promote separation of UI vs data
* Empty filter should not re-query DB
