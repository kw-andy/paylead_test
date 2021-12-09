Goal

----

Write a command-line based Python program which fetches an Open dataset and provides some insights pertaining to that data. The program should be accompanied by some form of automated testing.

This code will be used as a basis for your upcoming technical interview: you will be asked to explain its design, what your coding process was, etc. Your interviewers will need the code at least one working day in advance, with whichever setup instructions you feel relevant.

Expectations

The code must be compatible with a UNIX shell (e.g bash), running under Python 3.8 or 39; if external libraries are used, the list should be provided in the setup instructions— assume the user is running a ubuntu-like operating system. For the SQL part, it mustbe compatible with either SQLite or PostgreSQL.
We expect you to spend at most a couple hours on the project; it's more important tohave a minimal working implementation than a huge, bug-ridden program — run your testsoften!

Instructions
The program should display some statistics about french theaters, based on the datasetat https://www.data.gouv.fr/fr/datasets/cinemas-issus-dopenstreetmap/.
For instance:
    10 smallest theaters;
    Biggest networks;
    The city or department with the most theaters (through the INSEE area code).
A fictive output could be:

Fetch the data from the remote source

$ ./cinema-facts.py --download
Fetched 5768 theaters, loaded into ./db/theaters.sqlite3

Expose the data, filtering on a specific theater network

$ ./cinema-facts.py --network=Vue

- Smallest theater: My room (seats 3, Paris)
- Most screens: Vue Paddington (12 rooms), London
- Widest openings:
  - Vue Paddington (112 hours/week)
  - Vue St James (102 hours/week)

The program should store the data in a local SQLite database, and use that database toperform the requests.
Hints & advice

The following parts of the Python Standard Library could be useful:
    json to parse the dataset
    zipfile to handle Zip files
    argparse if needed, for command line arguments parsing
    sqlite3 to access a SQLite database
    unittest for automated testing
    http.server to simulate a local HTTP server from a directory
The following third party libraries may prove interesting:
    requests to fetch data over HTTP
    responses to bypass requests for testing
    colorama if you wish to add some colour
    pytest as an alternative to unittest for automated testing
    psycopg2 if you've opted for a PostgreSQL database instead of SQLite
The SQL database structure can be chosen freely; for inspiration, the following SQLcould be used:

CREATE TABLE networks (
    id INTEGER PRIMARY KEY AUTOINCREMENT, pip
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    zipcode TEXT UNIQUE NOT NULL
);

CREATE TABLE theaters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    osm_id TEXT UNIQUE NOT NULL,
    rooms INTEGER,
    seats INTEGER,
    department INTEGER NOT NULL REFERENCES departments (id),
    network INTEGER REFERENCES networks (id)
);