# Scrapping and Classification of Stackoverflow Questions

Stackoverflow is a website to ask questions and receive answers. It hass over 25million active question. This project is tailored towards scrapping stackoverflow website then classify the data. 


# Usage
This project can be used for the following:

## Scrapping of Stackoverflow website

```python
$pip install scrap-stackoverflow
```
```python
from scrapso import StackTab, ScrapStackOverflow

 #get questions from ACTIVE TAB
 st = ScrapStackOverflow(tab=StackTab.ACTIVE)
 #pagestart option is defaulted to 1, but pagination can be supplied
 data = st.scrap(100000, pagestart=2001)

 #to return the scrapped url
 st.scrapped_url
```

## Modelling of scrapped Stackoverflow website
The data is trained using Decision Tree and KMeans

## Prediction of Question classification