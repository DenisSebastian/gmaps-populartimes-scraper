# gmaps-populartimes-scraper
Scrap the popular times of a Google Maps place

This repo is inspired on  https://github.com/philshem/gmaps_popular_times_scraper which i did not get it to work.
(apparently because that repo wrap a html secction that does not apper on Google Maps html anymore)

# Requirements

- Selenium
- BeautifulSoup

# Usage

```
from populartimes import PopularTimes

poptimes = PopularTimes(path = 'path/to/chromedriver') # Path to the Selenium Chromedriver
poptimes.get_populartimes(url = 'maps.google.com/....') # this must be a Place URL

# The info get saved on poptimes.days_hours attribute


# Can be saved as a JSON file
poptimes.to_json(output)
```

---
