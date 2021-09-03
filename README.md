# File Combiner

Given an input list of CSV files, convert the multiple files into a single CSV that matches the output schema provided below:

```
|-- provider name: string (nullable = false)
|-- campaignID: string (nullable = false)
|-- cost per ad click: float (nullable = false)
|-- redirect link: string (nullable = false)
|-- phone number: string (nullable = true)
|-- address: string (nullable = false)
|-- zipcode: string (nullable = false)
```


## How to Run

You will need the following installed:
- Python version 3.9.1 or higher
- Pytest version 6.2.5
- Pandas version 1.3.2


You can install Pandas and Pytest with the following command:

```
pip install pandas pytest
```

Place any test files in the `input` directory, then run the following command:

```
python file_combiner.py
```

To run tests use the following command:

```
pytest test.py
```



## Thoughts
- In my solution you'll see where I created a list of special case columns, such as the `null_allowed_cols` (to aid in keeping track of what needs to be done for the final schema). I simply used those to work around the special cases, but for dealing with a much larger set of files that can have a much larger array of issues, full fledged methods or helpers should probably be written around these types of inputs to more easily deal with the variety of issues someone could see with client files. Checking the rules for the formats of things such as zipcodes or phone numbers would be a good thing to do here. Since it seemed safe enough I just removed extra quotes from all columns, though technically those could be allowed for some columns while it isn't allowed for others.
- In this example the scenario is set up to be mostly ideal, but there are a lot of "real world" scenarios left out where my code could be more robust in handling, such as:
    - All the columns are assumed to be named all the same way, but it would be safer to normalize all of them in some way before checking to see if all required columns are present (by making them all lowercase in the event of miscasings, by removing spaces to account for when a client might add extra spaces in column names, etc.)
    - The header for these files are all in the proper spot, but it would be best to create a method to help locate where a header is in the event there are extra lines in a file prior to the header.
    - Though the guidance for this was to follow the schema in terms of what data is and isn't allowed, there are a few more obvious cases of bad inputs I could work around, such as checking files for duplicate values, checking that the files in use are the appropriate files to be using (ex. using the most recent files since these are daily pulls), etc.
- This code doesn't really take much larger files into account. I could do more with the code to prepare for those kinds of files with methods like utilizing read_csv's _chunksize_ parameter or _iterator_ parameter to cycle through data.
- The invalid file error could be more descriptive by listing the exact columns that are seeing issues. 
- This is a pretty simple scenario of just combining all files, but it could be expanded to flexibly aggregate data in particular ways like the following to account for all the ways sales and marketing could want to look at data:
    1. Aggregating by insurance types
    2. Aggregating by provider
    3. Aggregating by campaign ID
    4. Aggregating by zip

