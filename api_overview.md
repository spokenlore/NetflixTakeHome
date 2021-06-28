* GET /computers(?p=[int])
    * Page of computers
    * Query parameters:
      * ?s=(-)[int] - Sorting (DOES NOT WORK)
        * -2: Reverse alphabetical sort on name
        * -3: Date up
        * 3: Date sort down
        * 4: Discontinued date sort down
        * -4: Discontinued date sort up
        * 5: Company sort down
        * 5: Company sort up
      * ?p=[int]
        * Pagination - Gives a 10 computer slice
    * Returns HTMl page with: 
        * Table with columns Computer Name | Introduced | Discontinued | Company
        * Filter component
        * Button(s) to paginate
        * Button to reach a page to add new computer
        * Total number of computers
        * Currently viewed slice of computers (i.e. 1-10)
    * Notes:
        * Sorting on table does not work
        * Attempting to sort the table while on a page other than the homepage returns the user to the homepage
            * If the sorting *did* work, this would be annoying for a user
        * Sorting and then paginating does preserve filters
        * Sending a pagination input outside the current pages returns 'Nothing to display' (does not break UI)


* GET /computers/[int] 
    * Specific computer info by computer ID (not displayed on UI)
    * Returns HTMl page:
        * HTML page with form fields for updating Computer Name | Introduced date | Discontinued date | Company
        * Button to 'Delete computer'
        * Button to 'Save this computer' (and its changes)
        * Button to cancel (does not save state, so returns to home page)


* GET /computers?f=[str]
    * Filter for database of computers (by name)   
    * Returns HTML page with:
        * Valid filtered computers (if there are any)
        * Total count of matching computers


* GET /computers/new
    * Returns page to add a new computer, and on the UI returns the user back to the homepage
    

* POST /computers/
    * Adds new computer
    * Submits form data from form fields 
        * name 
        * introduced 
        * discontinued
        * company
    * Notes:
        * Allows duplicates by name and other form data
    
* DELETE /computers/[int]
    * Deletes computer corresponding to ID
    
