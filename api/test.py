import enum
from scrapso import StackTab, ScrapStackOverflow
import pandas as pd


st = ScrapStackOverflow(tab=StackTab.BOUNTIFIED)
data = st.scrap(20)

data.to_csv("test.csv")

print(data)