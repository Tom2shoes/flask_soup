The following Flask application uses Python's BeautifulSoup and requests libraries to scrape images and text about the planet Mars from the following sources:

* [nasa.gov](https://mars.nasa.gov/news/)
* [jpl.nasa.gov](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars)
* [twitter @MarsWxReport](https://twitter.com/marswxreport?lang=en)
* [space-facts.com](http://space-facts.com/mars/)
* [astrogeology.usgs.gov](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars)

The data is stored in a local Mongo database and displayed with a Bootstrap 3 web Framework.

to run the app, clone the repository and run app.py with the required dependencies installed and have Mongo running. Alternatively you can run just the scraping code with the jupyter notebook file.
