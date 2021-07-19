# Scrapping and Classification of Stackoverflow Questions

Stackoverflow is a website to ask questions and receive answers. It has over 25million active question. 
This project is tailored towards scrapping stackoverflow website then using the scrapped data to predict number of optimal tags and classify the question


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
```
https://stackoverflow-classificiation.herokuapp.com/

```
### Endpoint `
The endpoint `/predict` accepts csv of structure from scrapping package.
``` http
POST predict/
```
|Accepted file type |  Parameter name         |  Description           |
|----------|:-------------:|-----------------------:|
| `csv` |  `file`  | Features of the questions|


## Responses
sucesss response for `POST predict/`
``` javascript
{
  "status_code": 100,
  "status_message": "Prediction Conputed",
  "data": "[3 3 3 2 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3]"
}
```

The `GET predict/` returns Top 10 requests made to the  `POST` endpoint
``` http
GET predict/
```

