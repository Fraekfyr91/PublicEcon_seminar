# PublicEcon_seminar
The data is collected using a webscraper.
The webscraper ´scraper.py´ relies on ´selenium´, ´geopy´ , ´pandas´, ´requests´ and ´numpy´. 
I recommend VS Code to run the scraper.

The dataset contains information on houseprices, type of sale, size and much more.

The dataset is then cleaned and prepared in the jupyter notebook ´Clean_and_prepare.ipynb´. The notebook imports data from DAWA on municipal geolocations and calls on data on Grundskylds promillen (land tax promille) that is collected [https://skat.dk/SKAT.aspx?oID=2113673](here), and prepared in an excel file.

The notebook relies on ´requests´, ´geopandas´, ´pandas´, ´numpy´, ´sympy´, ´shapely´ and ´folum´.

The cleaned data is then collected as a pandas dataframe.

The data analysis is then caried out in the last notebook ´Analysis.ipynb´.



