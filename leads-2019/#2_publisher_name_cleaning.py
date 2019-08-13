import pandas as pd
import numpy as np
import re
import math

### Step 2a: Evaluate if a publisher statement contains a single publisher or multiple ones.
### Separate the two situations in two files.

# publisher_statement_cleaner cleans the text of publication statement
def publisher_statement_cleaner(x):
  x = x.strip()
  x = re.sub("\\,$|\\:$|\\;$|\\, $|\\: $|\\; $", "", x).strip()
  x = re.sub("^\\[|\\]$", "", x)
  x = re.sub('^[^A-Za-z0-9]+', "", x)
  x = re.sub("\\,( |)[0-9]{4}(\\,|)$", "", x)
  x = re.sub("\\&", "and", x)
  x = re.sub("g\.p\.o\.", "government printing office", x)
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

data = pd.read_csv("./processed_data_1m/result_1m.csv")
data = data.replace(np.nan, '', regex=True)

data = data.loc[data.F26x_b.str.contains('publisher not identified') == False]
data = data.loc[data.F26x_b.str.contains('Printed by') == False]
data = data.loc[data['F26x_b'] != ""]
data = data.loc[data['F26x_is'] > 0]
target = ['published by', "published for", "in association with", "in partnership with",
          "division of", "imprint of", "part of", " ;; ", " a business", " a brand",
          " an imprint", "a division", "\\/", "\\, ", " business$", " imprint$",
          " brand$", " division$", "co-publisher", "\[for\]"]
data = data.sample(n = 10000, random_state=1)
data_10k["publisher_out"] = 0
data_10k = data_10k.reset_index()

for i in range(len(data_10k.index)):
    data_10k.loc[i, "F26x_b_cleaned"] = publisher_entity_cleaner(publisher_statement_cleaner(data_10k.loc[i, "F26x_b"]))
    pub_statement = publisher_entity_cleaner(data_10k.loc[i, "F26x_b_cleaned"])
    if len(re.findall("|".join(target), pub_statement.lower())) > 0:
        data_10k.loc[i, "publisher_out"] = 1
    print(str(i) + " / " + str(data_10k.loc[i, "publisher_out"]))

print(sum(data_10k.publisher_out == 0))

df1 = data_10k.loc[data_10k['publisher_out'] == 0]
df2 = data_10k.loc[data_10k['publisher_out'] == 1]

df1.to_csv("./processed_data_10k/publisher_10k_p1.csv", index=False, index_label=False,
          columns = ["F001_a", "isbn_tag", "F26x_is", "F26x_b_cleaned"])
df2.to_csv("./processed_data_10k/publisher_10k_p2.csv", index=False, index_label=False,
          columns = ["F001_a", "isbn_tag", "F26x_is", "F26x_b_cleaned"])
data_10k.to_csv("./processed_data_10k/result_10k_cleaned.csv", index=False, index_label=False)

