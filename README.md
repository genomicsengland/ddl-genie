# ddl-genie

`ddl-genie` was designed to read in data from delimited files and return a best-estimate of the DDL with insert statements.
It is a wrapper for the `ddlgenerator` module but I had to make my own version of the `ddlgenerator` module as it has a propensity to make a column of 1's and zeros into a boolean.

Things to bear in mind:

* You still need to check/edit the result ddl to:

	* check column types guessed correctly;

	* add in the schema where the table will go;

* table names will be made 'dialect-safe' so what you specify won't necessarily be what you get;

* Check the number of rows and columns read to check delimiters and quote characters read correctly;

* If you're doing a random sample of rows (using `-r <number_rows>` flag) pay special attention to columns marked `NOT NULL` as it may be wrong if missing data is rare;

* Similarly the lengths of `VARCHAR` may be wrong if you're only reading from a portion of the file;

* Probably the easiest way to 'force' data-types (e.g. `participant_id` will always be guessed as an integer when it is stored as string everywhere else) is to add a nonsense line to your input data with entries that will cause the guess to go your way (e.g. participant_id of `test` will cause it to come out as a varchar);

## Arguments

Usage: `python3 ddl-genie.py <inputFile>`

`inputFile`: path to input data file

`-d --delim`: default = `,`, delimiter for file (use `tsv` for tab), 

`-q --quotechar`: default = `"`, quote character used in data file

`-i --addinserts`: add insert statements for data to output

`-o --outputfile`: filename for resulting sql file (outputs to console if not specified)

`-l --dialect`: default = `postgresql`, database dialect to be used (see sqlalchemy documentation for options)

`-t --tablename`: name of table to use in output (defaults to `inputFile` basename if not specified) 

`-g --logfile`: name of log file to write to (defaults to `inputFile` basename is not specified)

`-r --maxrows`: number of rows to use for ddl generation (rows will be randomly selected from file)

## Example

```python
> python3 ddl-genie.py example-data.csv -t my_data -i
--read 7 rows from 6 columns in example-data.csv
DROP TABLE IF EXISTS my_data;

CREATE TABLE my_data (
        person_id INTEGER NOT NULL,
        age INTEGER,
        date_of_consent TIMESTAMP WITHOUT TIME ZONE NOT NULL,
        height DECIMAL(4, 1) NOT NULL,
        surname VARCHAR(14) NOT NULL,
        procedure_id INTEGER
);

INSERT INTO my_data (person_id, age, date_of_consent, height, surname, procedure_id) VALUES (1, 23, '2017-01-01 00:00:00', 156.1, 'Lennon', 3);
INSERT INTO my_data (person_id, age, date_of_consent, height, surname, procedure_id) VALUES (2, 24, '2016-11-12 00:00:00', 175.2, 'McCartney, Sir', 3);
INSERT INTO my_data (person_id, age, date_of_consent, height, surname, procedure_id) VALUES (3, 65, '2016-03-02 00:00:00', 168.4, 'Starr', 4);
INSERT INTO my_data (person_id, age, date_of_consent, height, surname, procedure_id) VALUES (4, 54, '2017-10-25 00:00:00', 156.8, 'Harrison', 7);
INSERT INTO my_data (person_id, age, date_of_consent, height, surname, procedure_id) VALUES (5, NULL, '2015-11-12 00:00:00', 165.8, 'Thompson', 1);
INSERT INTO my_data (person_id, age, date_of_consent, height, surname, procedure_id) VALUES (6, 45, '2016-08-25 00:00:00', 195.1, 'Chan', 2);
INSERT INTO my_data (person_id, age, date_of_consent, height, surname, procedure_id) VALUES (7, 46, '1960-01-01 00:00:00', 186.5, 'Walker', NULL);
```
