import pandas as pd

url = "https://www.bseindia.com/corporates/ann.html"

df = pd.read_html(url)
print(df[4])
