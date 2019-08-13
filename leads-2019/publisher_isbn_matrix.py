import pandas as pd
import re

data = pd.read_csv("result_1k_cleaned.csv",
                   dtype={'isbn_tag':str}, encoding="utf-8")
isbn = pd.read_csv("isbn_list_wikipedia.csv", encoding="utf-8")

isbn['isbn_tag'] = isbn['Country_code'].map(str) + "--" + isbn['Publisher_code'].map(str)
isbn = isbn[['isbn_tag', "Publisher"]]

data = data.loc[data['isbn_tag'] != ""]
data = data.loc[data.isbn_tag.str.contains(";;") == False]
data = data.loc[data['publisher_out'] == 0]
data = data[['isbn_tag', 'F26x_b_cleaned']]
data = pd.DataFrame(data)
tag_list = set(data['isbn_tag'])

data1 = []
for e in tag_list:
    row = {}
    publishers = ";".join(set(data.loc[data['isbn_tag'] == e, 'F26x_b_cleaned']))
    row["isbn_tag"] = e
    row['publishers'] = publishers
    data1.append(row)

data1 = pd.DataFrame(data1)
isbn_publisher = pd.merge(data1, isbn, on='isbn_tag', how='left')
df = pd.DataFrame(isbn_publisher)
df.to_csv("isbn_publisher.csv", index_label= False, index=False,
          encoding="utf-8")