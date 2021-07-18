# Scrap Stack Overflow
The project is to scrap stack overflow website. 


# Usage
This libary can be used when the key interest is to retrieve information from stackoverflow questions page. 

The package has enums for each of the available stack overflow questions tabs and scrapes 50 questions per page

## Sample codes
```python
from scrapso import StackTab, ScrapStackOverflow

 #get questions from ACTIVE TAB
 st = ScrapStackOverflow(tab=StackTab.ACTIVE)
 #pagestart option is defaulted to 1, but pagination can be supplied
 data = st.scrap(100000, pagestart=2001)

 #to return the scrapped url
 st.scrapped_url
```