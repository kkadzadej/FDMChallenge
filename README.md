# FDMChallenge

Repo containing my solution for the FDM hiring challenge. 

____________________________________________________________________________________________________________________________________

Some key assumptions made are:

1. There will be a continuous stream of large data, so the files from the API will immediately be sent to the database. 
2. Some changes were made to the data received, so this implies the assumption that in reality before they are sent to 
the API they go through a data pipe that transforms them OR they are transformed programmatically before being cast to a database. 
For simplicity these changes were done manually in this example. The data transformations and their reasons are explained below:
   1. The order forecasts were transposed so that the dates become indexes and the different product types become columns.
   This is a bit clearer to handle in SQL than having dates as column names. This also helps in the long run if the
   time resolution of the data becomes finer (i.e. we get daily forecasts) and we add rows instead of columns. 
   2. The monthly steel grade production was also transposed for similar reasons to the one given above. Another change 
   made here is that the first column was deleted before transposing so that the different grades were the column 
   headers. The mapping between the products and the grades was moved within the code in a dict in constants.py. 
   This again is done for simplicity - a more robust way would be to create another db table. 
   3. The daily production schedule was transformed to a single column where the datetime for each batch was changed
   to also include the right day. This format again better befits a database and makes the data easier to work with.
   4. The files were uploaded as .csv instead of .xslx for simplicity.
3. The logic and assumptions made to get the grade heat breakdown is explained in docstrings in the
get_grade_batch_breakdown_for_september method in /main/main.py.
4. The database is created automatically from run.py. The schemas used are defined in constants.py
5. For simplicity the files are read directly from disk rather than from the database after they are written into the database.

____________________________________________________________________________________________________________________________________

Info on the repo:

- run.py contains a run method to get the data, create the database and write the data to the database, as well asget the batch
breakdown that ScrapChef needs. **Before running run.py copy and run "uvicorn main.api:api --reload" on bash or terminal to setup
the local server that allows interaction with the API**
- The API can be visited at http://127.0.0.1:8000 after the server is set, and all the endpoints can be seen at http://127.0.0.1:8000/docs
