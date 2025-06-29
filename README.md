# FDMChallenge
Repo containing my solution for the FDM hiring challenge. 

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
3. The hourly production schedule is assumed to be the required output for ScrapChef to work, so the program will create
a production schedule for September based on the production history and order forecast. 