#Application for Data Engineer Internship (MacPaw Summer Internship 2021)

Application downloads data_list.data file from AWS S3 bucket every 5 min. It checks data_list's header for Last Modified and compare it with variable date. In case they don't match, program compares JSON file names from data_list with table catalogue. If there are new files, their names are saved to catalogue and used to download JSON files from AWS S3 bucket.
Every JSON file is checked for type `song/app/movie`. When there is a type match dict is processed by the type rule. Extracted data is saved to the corresponding table `songs/apps/movies`
 
####  **Rule by type** 
<table>
  <tr>
    <td>song </td>
    <td>Fill `ingestion_time` with a datetime indicating when this record was processed</td>
  </tr>
  <tr>
    <td>movie</td>
    <td>Fill `original_title_normalized` with value of `original_title` where any non-letter and non-number characters are removed and spaces replaced with underscore _ (e.g. Star Wars: The Force Awakens -> star_wars_the_force_awakens)</td>
  </tr>
  <tr>
    <td>app</td>
    <td>Fill `is_awesome` with a boolean value true if rafting is 5 star, all other cases fill with false</td>
  </tr>
</table>

###Technologies Used
*Python 3.8.5
*Sqlite 3
*SQLAlchemy 1.4.11 
*requests 2.25.1

###Special Gotchas
*Duplicates of info from JSON files are allowed in the database,as it is not mentioned otherwise in the task's guidelines 
*Last Modified is saved to variable date and not to database. I didn't want to create additional table just for 1 entry.


###Getting Started
####Local

You are able to start the app by typing the following command in the command line:
```
$ pip install -r requirements.txt
$ python run.py
```
####Docker

To build an image type in the cpmmand line:
```
$ docker build --rm -t app .
```
To run type next to the command line. 
```
docker run --rm -v <path to DB>:/db -e DATABASE_URL=sqlite:////db/database.db
```
Where <path to DB> is local path to sqlight db folder.