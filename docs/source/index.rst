# Coding_Exercise
coding for fun! it uses Python, data-harvesting against HTML, and more

Features in this exercise
=======================
- More realistic! TaxRate module harvests targeted tax data from Australian Taxation Office website.
- Re-usable. TaxRate module provide JSON format outputs. Therefore it is more reusable
- Easy to maintain and debug loose-coupled modules well orchestrated together
- Well documented. Beside inline comments and easy-to-understand names. Infrastructure has been setup on 'ReadTheDocs' site which is popular choice for open-source projects. http://coding-execrise-tax-calculator.readthedocs.io/en/latest/
- Readability. Following best practices in Python. PEP-8 complied.

Assumptions
===========
- Input csv file has correct formatted content. Format: it should contain first name, last name, salary, super rate% (0 - 50) and payment start date (for instance: 31/12/16)
- Input csv file path should be correctly listed in `settings.py`
- Either ATO website service or the Default tax rate table file is available
- ATO website HTML format is consistent as TaxRate.__get_taxrate_online__() module's codes. The code should be updated after ATO has dramatically updated its website HTML structure.

How To Run?
======
Tutorial for setup environment can be found here: https://hackercodex.com/guide/python-development-environment-on-mac-osx/
- For Mac users `sudo easy_install pip`.
- `pip install virtualenv`
- start your virtualenv by following tutorial http://sourabhbajaj.com/mac-setup/Python/virtualenv.html
- Once your virtualenv is up and running. run: `pip install -r requirements.txt`
- `python main.py`

Expected Results
==============
- Output csv file with time stamp can be found in programs 'result' folder.
- Recently generated tax rate JSON file can be found in Config/tax_rate_backup folder.

Test
=====
- Simply run `nosetests`

TO-DO
=====
- Convert the project to a web application using Flask (Micro web framework in Python) and Docker-Containers hosting at Heroku
- Event logging module that takes note of unexpected events.