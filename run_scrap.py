import enum
from scrapso import StackTab, ScrapStackOverflow
import pandas as pd


st = ScrapStackOverflow(tab=StackTab.ACTIVE)
data = st.scrap(10, pagestart=2)

print(data)