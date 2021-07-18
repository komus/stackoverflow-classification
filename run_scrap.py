import enum
from scrapso import StackTab, ScrapStackOverflow
import pandas as pd


st = ScrapStackOverflow(tab=StackTab.BOUNTIFIED)
data = st.scrap(300)


data.to_csv('model/stackoverflow_main4')