# gmaps-populartimes-scraper
Scrap the popular times of a Google Maps place

This repo is inspired on  https://github.com/philshem/gmaps_popular_times_scraper which did not work for me.
(apparently because that repo wrap an html secction that does not apper on Google Maps html anymore)

# Requirements
- Selenium
- BeautifulSoup
Them can be installed with `pip install -r requirements.txt`

You also need `chromedriver` to get this to work. It can be found [here](https://chromedriver.chromium.org/downloads). Also, this [thread](https://stackoverflow.com/questions/49788257/what-is-default-location-of-chromedriver-and-for-installing-chrome-on-windows) can be helpful to get the `chromedriver` path.

# Usage
## on Python
```
from populartimes import *

poptimes = PopularTimes(path = 'path/to/chromedriver') # Path to the Selenium Chromedriver
poptimes.get_populartimes(url = 'https://www.google.com/maps/place/....') # this must be a Place URL
```
The info get saved on poptimes.days_hours attribute
```
>>> print(poptimes.days_hours)
>>> {0: {}, 1: {6: 0, 7: 0, 8: 10, 9: 18, 10: 26, 11: 34, 12: 38, 13: 36, 14: 32, 15: 33, 16: 49, 17: 76, 18: 89, 19: 0, 20: 0, 21: 0, 22: 0, 23: 0}, 2: {6: 0, 7: 0, 8: 9, 9: 17, 10: 26, 11: 34, 12: 38, 13: 39, 14: 36, 15: 38, 16: 53, 17: 79, 18: 88, 19: 0, 20: 0, 21: 0, 22: 0, 23: 0}, 3: {6: 0, 7: 0, 8: 7, 9: 15, 10: 26, 11: 36, 12: 42, 13: 41, 14: 38, 15: 40, 16: 55, 17: 78, 18: 85, 19: 0, 20: 0, 21: 0, 22: 0, 23: 0}, 4: {6: 0, 7: 0, 8: 15, 9: 22, 10: 28, 11: 34, 12: 40, 13: 43, 14: 45, 15: 49, 16: 62, 17: 85, 18: 90, 19: 0, 20: 0, 21: 0, 22: 0, 23: 0}, 5: {6: 0, 7: 0, 8: 11, 9: 16, 10: 22, 11: 28, 12: 34, 13: 38, 14: 41, 15: 46, 16: 61, 17: 90, 18: 0, 19: 0, 20: 0, 21: 0, 22: 0, 23: 0}, 6: {}}
Here the keys on the first level mean a day of the week (from 0 to 6, with 0 being Sunday and so on). Then, a second-lelvel key means an hour, and its value the precentage of concurrence of the place. 
```
Also, it can be saved as a JSON file
```
poptimes.to_json(output)
```
## From Comand Line
You can run `./poptime.py -h` to get:
```
usage: poptimes.py [-h] -u URL [-o [OUTPUT]] [--chromedriver [CHROMEDRIVER]]
                   [--wait [WAIT]]

Scrap popular times for places from Google Maps.

optional arguments:
  -h, --help                      show this help message and exit
  -u URL, --url URL               the Google Maps Place URL you want to get hourly
                                  concurrence from
  -o [OUTPUT], --output [OUTPUT]  path of the JSON output file
  --chromedriver [CHROMEDRIVER]   chromedriver path
  --wait [WAIT]                   seconds to wait for Google Maps URL to load
```
# Tested
I have tested this only on Linux. I hope it work on other systems, but i really do not know if will.

# To-do
There are somethings that i think culd be added:
[x] cli usage
[] The posibility to get the info for a plenty of URL's (may be in a csv, as the [referenced repo](https://github.com/philshem/gmaps_popular_times_scraper))

---

Scrapea la concurrencia de un Lugar desde Google Maps

Este repo está inspirado en https://github.com/philshem/gmaps_popular_times_scraper el cual no me funcionó.
(aparentemente porque en ese repo rescatan una sección del html que ya no aparece en el html de Google Maps)

# Requirimientos
- Selenium
- BeautifulSoup
Estos se pueden instalar con `pip install -r requirements.txt`

También es necesario  `chromedriver` para que esto funcione. Puede ser encontrado [aqui](https://chromedriver.chromium.org/downloads). También, este [hilo](https://stackoverflow.com/questions/49788257/what-is-default-location-of-chromedriver-and-for-installing-chrome-on-windows) puede ser util para saber la ruta de `chromedriver`.

# Uso
## en Python
```
from populartimes import *

poptimes = PopularTimes(path = 'path/to/chromedriver') # Path to the Selenium Chromedriver
poptimes.get_populartimes(url = 'https://www.google.com/maps/place/....') # this must be a Place URL
```
The info get saved on poptimes.days_hours attribute
```
>>> print(poptimes.days_hours)
>>> {0: {}, 1: {6: 0, 7: 0, 8: 10, 9: 18, 10: 26, 11: 34, 12: 38, 13: 36, 14: 32, 15: 33, 16: 49, 17: 76, 18: 89, 19: 0, 20: 0, 21: 0, 22: 0, 23: 0}, 2: {6: 0, 7: 0, 8: 9, 9: 17, 10: 26, 11: 34, 12: 38, 13: 39, 14: 36, 15: 38, 16: 53, 17: 79, 18: 88, 19: 0, 20: 0, 21: 0, 22: 0, 23: 0}, 3: {6: 0, 7: 0, 8: 7, 9: 15, 10: 26, 11: 36, 12: 42, 13: 41, 14: 38, 15: 40, 16: 55, 17: 78, 18: 85, 19: 0, 20: 0, 21: 0, 22: 0, 23: 0}, 4: {6: 0, 7: 0, 8: 15, 9: 22, 10: 28, 11: 34, 12: 40, 13: 43, 14: 45, 15: 49, 16: 62, 17: 85, 18: 90, 19: 0, 20: 0, 21: 0, 22: 0, 23: 0}, 5: {6: 0, 7: 0, 8: 11, 9: 16, 10: 22, 11: 28, 12: 34, 13: 38, 14: 41, 15: 46, 16: 61, 17: 90, 18: 0, 19: 0, 20: 0, 21: 0, 22: 0, 23: 0}, 6: {}}
Aqui las keys del primer nivel corresponden a los dias de la semana (desde 0 a 6, con 0 siendo domingo, y así sucesivamente). Luego, las key del segundo nivel conrresponden a las horas del día, y sus valores el porcentaje de concurrencia del lugar. 
```
También, se puede guardar como un archivo JSON.
```
poptimes.to_json('output')
```
## desde la linea de comandos
Puede correr `./poptime.py -h` para obtener:
```
usage: poptimes.py [-h] -u URL [-o [OUTPUT]] [--chromedriver [CHROMEDRIVER]]
                   [--wait [WAIT]]

Scrap popular times for places from Google Maps.

optional arguments:
  -h, --help                      show this help message and exit
  -u URL, --url URL               the Google Maps Place URL you want to get hourly concurrence from
  -o [OUTPUT], --output [OUTPUT]  path of the JSON output file
  --chromedriver [CHROMEDRIVER]   chromedriver path
  --wait [WAIT]                   seconds to wait for Google Maps URL to load
``` 
# Por hacer
Algunas cosas que creo que se podrian añadir:
[x] uso desde la linea de comandos
[] la posibilidad de obtener la info de muchas URL's (probablemente desde un csv, como en [el repositorio mencionado antes](https://github.com/philshem/gmaps_popular_times_scraper))

