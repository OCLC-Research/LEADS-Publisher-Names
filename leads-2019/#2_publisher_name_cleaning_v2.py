decision = "b"

import pandas as pd
import numpy as np
import re
import math

### Step 2a: Evaluate if a publisher statement contains a single publisher or multiple ones.
### Separate the two situations in two files

# publisher_statement_cleaner cleans the text of publication statement
def publisher_statement_cleaner(x):
  x = x.strip()
  x = re.sub("\,$|\:$|\;$|\, $|\: $|\; $|\.{1,3}$|\.{1,3} $", "", x).strip()
  x = re.sub("^\\[|\\]$", "", x)
  x = re.sub('^[^A-Za-z0-9]+', "", x)
  x = re.sub("\\,( |)[0-9]{4}(\\,|)$", "", x)
  x = re.sub("\\&", "and", x)
  x = x.strip()
  return x

# publisher_entity_cleaner cleans the entity, such as inc., co., llc., ltd., pub.
def publisher_entity_cleaner(x):
  x = re.sub(", inc$|, inc\.$| inc$| inc\.$", " INC", x.lower()).strip()
  x = re.sub(", co$|, co\.$| co$| co\.$", " CO", x.lower()).strip()
  x = re.sub(", llc$|, llc\.$| llc$| llc\.$", " LLC", x.lower()).strip()
  x = re.sub(", ltd$|, ltd\.$| ltd$| ltd\.$", " LTD", x.lower()).strip()
  x = re.sub(", pub$|, pub\.$| pub$| pub\.$", " PUB", x.lower()).strip()
  x = re.sub("^the |^a |^an ", "", x.lower()).strip()
  return x

# decision = input("Choose the level of analysis: a = 1k, b = 10k, c = 1m?")

if decision == "a":
    data = pd.read_csv("./processed_data_1k/result_1k.csv")
else:
    data = pd.read_csv("./processed_data_1m/result_1m.csv")

data = data.replace(np.nan, '', regex=True)
data = data.loc[data.F26x_b.str.contains('publisher not identified') == False]
data = data.loc[data.F26x_b.str.contains('Printed by ') == False]
data = data.loc[data.F26x_b.str.contains('Printed for ') == False]
data = data.loc[data.F26x_b.str.contains('printed by ') == False]
data = data.loc[data.F26x_b.str.contains('printed for ') == False]
data = data.loc[data.F26x_b.str.contains('Distributed by ') == False]
data = data.loc[data.F26x_b.str.contains('distributed by ') == False]
data = data.loc[data.F26x_b.str.contains('Distributed for ') == False]
data = data.loc[data.F26x_b.str.contains('distributed for ') == False]
data = data.loc[data.F26x_b.str.contains('Issued by ') == False]
data = data.loc[data.F26x_b.str.contains('issued by ') == False]
data = data.loc[data.F26x_b.str.contains('Issued for ') == False]
data = data.loc[data.F26x_b.str.contains('issued for ') == False]
data = data.loc[data.F26x_b.str.contains('s\.n\.') == False]
data = data.loc[data.F26x_b.str.contains('s\. n\.') == False]
data = data.loc[data.F26x_b.str.contains('Publisher not identified') == False]
data = data.loc[data.F26x_b.str.contains('publisher not identified') == False]
data = data.loc[data['F26x_b'] != ""]
data = data.loc[data['F26x_is'] > 0]
target = ['published by', "published for", "in association with", "in partnership with",
          "division of", "imprint of", "part of", " ;; ", " a business", " a brand",
          " an imprint", "a division", " business$", " imprint$", " brand$", " division$",
          "co-publisher", "\[for\]", "in cooperation with", "on behalf of", " from ",
          "published with", "c\\\o"]

data["publisher_out"] = 0
data = data.reset_index()

if decision == "b":
    data = data.sample(n = 14000, random_state=1)
    data = data.reset_index()
else:
    data = data

for i in range(len(data.index)):
    data.loc[i, "F26x_b_cleaned"] = publisher_entity_cleaner(publisher_statement_cleaner(data.loc[i, "F26x_b"]))
    pub_statement = publisher_entity_cleaner(data.loc[i, "F26x_b_cleaned"])
    if pub_statement == "university press" or pub_statement == "the association":
        data.loc[i, "publisher_out"] = 1
    elif len(re.findall("|".join(target), pub_statement.lower())) > 0:
        data.loc[i, "publisher_out"] = 1
    print(str(i) + " / " + str(data.loc[i, "publisher_out"]))

print(sum(data.publisher_out == 0))

df1 = data.loc[data['publisher_out'] == 0]
df1 = df1.loc[df1['F26x_b_cleaned'] != ""]
df2 = data.loc[data['publisher_out'] == 1]
df2 = df2.loc[df2['F26x_b_cleaned'] != ""]

if decision == "a":
    filename_1 = "./processed_data_1k/publisher_1k_p1.csv"
    filename_2 = "./processed_data_1k/publisher_1k_p2.csv"
    filename_3 = "./processed_data_1k/result_1k_cleaned.csv"
elif decision == "b":
    filename_1 = "./processed_data_10k/publisher_10k_p1.csv"
    filename_2 = "./processed_data_10k/publisher_10k_p2.csv"
    filename_3 = "./processed_data_10k/result_10k_cleaned.csv"

df1.to_csv(filename_1, index=False, index_label=False,
          columns = ["F001_a", "leader_18", "isbn_tag", "isbn_tag1", "F008_0710",
                     "F040_e", "F260_is", "F264_is", "F26x_b_cleaned"])
df2.to_csv(filename_2, index=False, index_label=False,
           columns=["F001_a", "leader_18", "isbn_tag", "isbn_tag1", "F008_0710",
                    "F040_e", "F260_is", "F264_is", "F26x_b_cleaned"])
data.to_csv(filename_3, index=False, index_label=False)

df1 = pd.read_csv(filename_1)
df2 = pd.read_csv(filename_2)

def publisher_statement_cleaner(x):
  x = x.strip()
  x = re.sub("\,$|\:$|\;$|\, $|\: $|\; $|\.{1,3}$|\.{1,3} $", "", x).strip()
  x = re.sub("^\\[|\\]$", "", x)
  x = re.sub('^[^A-Za-z0-9]+', "", x)
  x = re.sub("\\,( |)[0-9]{4}(\\,|)$", "", x)
  x = re.sub("\\&", "and", x)
  x = re.sub("^the |^The |^a |^A |^an |^ An", "", x)
  x = x.strip()
  return x

df2['class'] = ""
imprint_no = 0

for i in range(len(df2.index)):
    print(i)
    publisher = df2.loc[i, "F26x_b_cleaned"]
    if len(re.findall(r"imprint", publisher)) > 0 and len(re.findall(r";;", publisher)) == 0:
        df2.loc[i, "class"] = "imprint"
        imprint_no = imprint_no + 1
    if len(re.findall(r";;", publisher)) > 0:
        df2.loc[i, "class"] = "double"
        imprint_no = imprint_no + 1

print("The first section is finished.")

data1 = df2.loc[df2['class'].isin(['imprint'])]
data1 = data1.reset_index()
data1['publisher1'] = ""
data1['publisher2'] = ""
a = 0
print(len(df1.index))
df1['source'] = "1"

for i in range(len(data1.index)):
    publisher = data1.loc[i, "F26x_b_cleaned"]
    if len(re.findall(r"is an imprint of", publisher)) > 0:
        publisher_vector = publisher.split("is an imprint of")
        data1.loc[i, 'publisher1'] = publisher_vector[0]
        data1.loc[i, 'publisher2'] = publisher_vector[1]
        a = a + 1
    elif len(re.findall(r"the imprint of", publisher)) > 0:
        publisher_vector = publisher.split("the imprint of")
        data1.loc[i, 'publisher1'] = publisher_vector[0]
        data1.loc[i, 'publisher2'] = publisher_vector[1]
        a = a + 1
    elif len(re.findall(r"an imprint of", publisher)) > 0:
        publisher_vector = publisher.split("an imprint of")
        data1.loc[i, 'publisher1'] = publisher_vector[0]
        data1.loc[i, 'publisher2'] = publisher_vector[1]
        a = a + 1
    if len(publisher_vector) > 0:
        for j in range(2):
            if len(re.findall(r"distributed|issued|printed", publisher_vector[j])) == 0:
                row = {}
                row['F001_a'] = data1.loc[i, "F001_a"]
                row['leader_18'] = data1.loc[i, "leader_18"]
                row['isbn_tag'] = data1.loc[i, "isbn_tag"]
                row['isbn_tag1'] = data1.loc[i, "isbn_tag1"]
                row['F008_0710'] = data1.loc[i, "F008_0710"]
                row['F040_e'] = data1.loc[i, "F040_e"]
                row['F260_is'] = data1.loc[i, "F260_is"]
                row['F264_is'] = data1.loc[i, "F264_is"]
                row['F26x_b_cleaned'] = publisher_statement_cleaner(publisher_vector[j])
                row['source'] = 2
                df1 = df1.append(row, ignore_index=True)

df1.to_csv(filename_1, index=False, index_label=False,
          columns = ["F001_a", "leader_18", "isbn_tag", "isbn_tag1", "F008_0710",
                     "F040_e", "F260_is", "F264_is", "F26x_b_cleaned", "source"])

