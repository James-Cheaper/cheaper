# Cheaper.com
Initial Landing page![Initial Landing page](https://github.com/user-attachments/assets/7d2a1c73-0d16-4965-a2f8-4402ef267ff4)





##Technical Documentation of how to run the application 

#How to run

-To run the scraper, execute the main.py script by running the command 

python main.py

-Make sure you are in the webscraper directory when you run the command  

##Where is the entry point?

-The entry point is the main() in main.py, specifically, this block of code,  
if __name__ == "__main__":
    main()


##what file needs to be located and what variables would need to be changed if you wanted to scrape another website?

-If you wanted to scrape another website, you need to locate the file main.py and change the variables “scraper” and “pages” to whatever website you wanted and the new URl paths. As well ensure the website allows scraping.



Documentation on connecting the database to vscode with the postgres extension

1. Install the PostgreSQL Extension  in VSCode
2. Make sure PostgreSQL is Running Locally
3. click the extension on the left sidebar
4. click the plus button and create a new connection
5. fill in the needed information, server = localhost, database = cheaper_local, User = postgres, port = 5432 (default), password  = the password you made when installing PostgreSQL
7. You should be connected now and see a message and see the conencted database in the extension now.
 