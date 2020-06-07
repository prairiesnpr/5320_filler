# 5320.20 Filler

##### Purpose
The script is designed to allow for automatically filling ATF form 5320.20.

##### Requirements

1. [pdftk-server](https://www.pdflabs.com/tools/pdftk-server/) (Must add to your path enviroment varible).
2. Python version 3.6 or greater.

##### Install
1. ```pip install fill5320```
2. Copy static_data.csv, destinations_data.csv, signature.png, fields.json, atf_form_5320.pdf to directory of choice.

##### Setup
1. Modify owner and firearm information in static_data.csv
2. Modify destinations in destinations_data.csv
3. Edit signature.png

##### Running
1. From the desired working direcotry ```python -m fill5320```
2. Filled files will be placed in a directory titled filled and signed will be placed in signed


[Example Output](example_output/atf_form_5320_KY.pdf)