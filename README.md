# Internal Testing Service (ITS)
Internal testing service: to formalize the making admission tests

## What does it do?

The scripts in this repo do a few things
- Insert MCQs from a bunch of files to a bank XML file
- Enable you to randomly construct a test from bank with sections
- Convert XML to TeX
- COnvert TeX to PDF (requires pdflatex)
- Various manipulations on raw and bank files
- Stats on various files

# Howto

Most of the API is references in `src/index.py`. Most importantly you can call 
- `raw2bank.add_questions_from_directory(bank_file_path,inout_dir)` 
- `makeTest.py` does everything including randomly selecting tests, separating questions and answers, converting to TeX, converting to pdf (assuming TeX is install), and perform basic cleanup. 
