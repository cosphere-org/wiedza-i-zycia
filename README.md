
# Wiedza i Życie - Scraper
___________________________

### Prerequisites

* pip
* python3
* virtualenv
* (for use of mallet install default-jdk)
___________________________

### Installation

in bash run following command

```bash
make install
```
___________________________

### Building Command

in order to build the command for scraper run:

```bash
python setup.py develop
```
___________________________

### To see all available CLI commands


```bash
scraper --help
```
___________________________

### To scrape all available editions

```bash
source env.sh && \
scraper scrape-all-and-save
```
___________________________

### To scrape all particular edition (for debugging)

```bash
source env.sh && \
scraper scrape-edition https://www.wiz.pl/10,274.html
```
___________________________

### To scrape all particular article (for debugging)

```bash
source env.sh && \
scraper scrape-article https://www.wiz.pl/8,2116.html
```
