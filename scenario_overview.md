# Happy Path Scenarios:

Ideally, we would also build some functionality to seed data into the database (since this live database is being used by a lot of people)

End-to-end (UI) (would have more tests in reality):
1. Accessing the page
   * User navigates to https://computer-database.herokuapp.com/computers
     * Table should populate with results (if the results exist)
2. Filter by computer name
3. Add a computer (and then filter for it)
    * User navigates to https://computer-database.herokuapp.com/computers/new
    * User fills out form fields
    * User submits form
    * User should be taken back to the homepage
4. Test navigation buttons (next and previous page)
5. Not automated - other CRUD operations (UPDATE, DELETE)
6. Validating that all inputted data makes it to the row (difficult because the API does not return an ID for new rows)
    
Integration tests (API):
1. Add a computer
    * Query homepage for total count of computers in database
    * Add a computer
    * Total count of computers should increment by 1
2. Load a single page of the database
3. Load the whole database into memory
4. Add a computer (with only name)
5. Add a computer (with all fields filled)
6. Delete an existing computer
7. Update a computer


#Negative scenarios:

Integration:
1. A user should not be able to create a new computer without a name
    * Navigate to https://computer-database.herokuapp.com/computers/new
    * Click 'Create this computer'
    * User should remain on the 'add computer' form
2. A user should not be able to add a computer without a valid discontinued date
3. A user should not be able to add a computer without a valid introduced date
4. A user should not be able to get a computer with an invalid ID
5. Covered as part of Integration test 6 (but could be separate test) - 
   Deleting a computer by ID which does not exist in the DB
