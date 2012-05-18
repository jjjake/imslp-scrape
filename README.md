# Scraping the International Music Score Library Project

This repository is a collection of tools used to scrape [imslp.org](http://imslp.org/wiki/Main_Page "imslp.org").
As of May 18, 2012, IMSLP has:

+ 54,374 works
+ 193,537 scores
+ 16,140 recordings
+ 7,202 composers
+ 193 performers

## Scripts

`get_people_links.sh`: Generates a list of links to every results page under 
[http://imslp.org/wiki/Category:People](http://imslp.org/wiki/Category:People). There are 200 results per page,
and 9,162 results in total.
