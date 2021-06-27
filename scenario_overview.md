Happy Path Scenarios:
    End-to-end:
        1. Accessing the page
            * User navigates to https://computer-database.herokuapp.com/computers
            * Table should populate with results (if the results exist)
        2. Filter
        3. Add a computer (and then filter for it)
            * User navigates to https://computer-database.herokuapp.com/computers/new
            * User fills out form fields
            * User submits form
            * User should be taken back to the homepage
    Integration tests:
        1. Add a computer
            * Query homepage for total count of computers in database
            * Add a computer
            * Total count of computers should increment by 1
        2. 
        

4. Access subsequent pages

Negative scenarios:
1. A user should not be able to create a new computer without a name
    * Navigate to https://computer-database.herokuapp.com/computers/new
    * Click 'Create this computer'
    * User should remain on the 'add computer' form
2. A user should not be able to add a computer without a name to the database