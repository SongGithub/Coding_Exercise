# Monthly Pay Calculator
[![Build Status](https://travis-ci.org/SongGithub/Monthly-Pay-Calculator.svg?branch=master)](https://travis-ci.org/SongGithub/Monthly-Pay-Calculator)

Running the calculator without Docker
------------

Requirements
------------
- Linux or Mac OS X
- bash
- Python 2.7.x
- pip
- virtualenv


- Tutorial for setup environment can be found here: https://hackercodex.com/guide/python-development-environment-on-mac-osx/
- For Mac users `sudo easy_install pip`.
- `pip install virtualenv`
- start your virtualenv by following tutorial http://sourabhbajaj.com/mac-setup/Python/virtualenv.html
- Once your virtualenv is up and running. run: `pip install -r requirements.txt`
- `python main.py`

Features in this exercise
------------
- Re-usable & Extendable. TaxRate module provides JSON format outputs. Therefore it is more reusable
- Easy to maintain and debug: loose-coupled modules well orchestrated together
- Readability. Following best practices in Python: PEP-8 complied.
- Include Travis-CI for auto-testing purpose. Travis-CI is excellent choice as it is free for open-source projects and work seamlessly with Github where this project is hosted on.
- Wrap the project in Docker Container. The Docker-Container can make others get this project up and running painlessly, much easier than ask people who are not from Python world to setup Python specific environment, such as Pip, and installing dependencies for the project. Also, it reflects current trend of 'Containerization' & Devops.

Assumptions
------------
- Input csv file has correct formatted content. Format: it should contain first name, last name, salary, super rate% (0 - 50) and payment start date (for instance: 31/12/16)
- Input csv file path should be correctly listed in `settings.py`
- Either ATO website service or the Default tax rate table file is available
- ATO website HTML format is consistent as TaxRate.__get_taxrate_online__() module's codes. The code should be updated after ATO has dramatically updated its website HTML structure.


Expected Results
------------
- Output csv file with time stamp can be found in programs 'result' folder.
- Recently generated tax rate JSON file can be found in Config/tax_rate_backup folder.

Test Mannually
=====
- Simply run `nosetests` while in the root folder

TO-DO
------------
- Event logging module that takes note of unexpected events.
- Well documented. Beside inline comments and easy-to-understand names. Infrastructure has been setup on 'ReadTheDocs' site which is popular choice for open-source projects. http://coding-execrise-tax-calculator.readthedocs.io/en/latest/

Problem Description
------------

The Problem: Employee Monthly Payslip Generation

When input the employee's details: first name, last name, annual salary (positive integer) and super rate (0% - 50% inclusive), payment start date, the program should generate payslip information with the name, pay period, gross income, income tax, net income and super.

The calculation details are as follows:

pay period = per calendar month
gross income = annual salary / 12 months
income tax = based on the tax table provide below
net income = gross income - income tax
super = gross income x super rate

Note: All calculation results should be rounded to the whole dollar. If >= 50 cents round up to the next dollar increment, otherwise round down.
Tax Table

Taxable income   Tax on this income
0 - $18,200     Nil
$18,201 - $37,00019c for each $1 over $18,200
$37,001 - $80,000$3,572 plus 32.5c for each $1 over $37,000
$80,001 - $180,000$17,547 plus 37c for each $1 over $80,000
$180,001 and over$54,547 plus 45c for each $1 over $180,000

Example Data
Say for example the employee’s annual salary is $60,050 and the super rate is 9% how much will this employee be paid for the month of March?

pay period = 01/12/2016
gross income = 60,050 / 12 = 5,004.16666667 (round down) = 5,004
income tax = (3,572 + (60,050 - 37,000) x 0.325) / 12  = 921.9375 (round up) = 922
net income = 5,004 - 922 = 4,082
super = 5,004 x 9% = 450.36 (round down) = 450

Here is the csv input and output format we suggest (but feel free to use any format you want):

Input:
first name, last name, annual salary, super rate (%), payment start date
David,Rudd,60050,9%,01/03/2016
Ryan,Chen,120000,10%,01/04/2016

Output:
full name, pay period, gross income, income tax, net income, super
David Rudd,March,5004,922,4082,450
Ryan Chen,April,10000,2696,7304,1000
End of Problem.