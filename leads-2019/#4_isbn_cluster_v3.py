import pandas as pd
import re

def common_remove(str):
    str = re.sub(r"[^a-zA-Z0-9' ]+", ' ', str).strip()
    str = re.sub(r" +", ' ', str).strip()
    str = re.sub(r"[0-9]{4}$|[0-9] {4}$", "", str).strip()
    return(str)

data = pd.read_csv("./processed_data_10k/cluster_result_single.csv")
raw = pd.read_csv("./processed_data_10k/publisher_10k_p1_a.csv")
raw_new = raw[pd.notnull(raw['isbn_tag'])]
raw_new = raw_new.reset_index(drop=True)
added = pd.read_csv("publisher_p2_parsed.csv")

raw_pro = []

for i in range(len(raw_new.index)):
    isbn_text = raw_new.loc[i, 'isbn_tag']
    isbn_vector = isbn_text.split(" ;; ")
    if len(isbn_vector) > 1:
        for j in range(len(isbn_vector)):
            row = {}
            row["ID"] = raw_new.loc[i, 'F001_a']
            row["ISBN"] = isbn_vector[j]
            row["Publisher"] = raw_new.loc[i, 'F26x_b_cleaned_pro']
            raw_pro.append(row)
    else:
        row = {}
        row["ID"] = raw_new.loc[i, 'F001_a']
        row["ISBN"] = isbn_vector[0]
        row["Publisher"] = raw_new.loc[i, 'F26x_b_cleaned_pro']
        raw_pro.append(row)

raw_pro_df = pd.DataFrame(raw_pro)

isbn_df = []

for i in range(len(data.index)):
    print(i)
    isbn_vector = data.loc[i, 'isbn_new']
    text_vector = data.loc[i, 'publisher_pro']
    isbn_list = isbn_vector.split(";")
    text_list = text_vector.split(";;")
    for k in range(len(isbn_list)):
        count = 0
        row = {}
        row['isbn'] = isbn_list[k]
        row['cluster_id'] = data.loc[i, 'id']

        for j in range(len(text_list)):
            df_sub = raw_pro_df[raw_pro_df['Publisher'].str.contains(common_remove(text_list[j]), case=False)]
            df_sub = df_sub[df_sub['ISBN'] == isbn_list[k]]
            count = count + len(df_sub.index)

        row["record"] = count
        row['type'] = "1"
        isbn_df.append(row)

data_1 = raw.loc[raw['F001_a'].isin(added['F001_a'])]
data_1 = data_1.reset_index()
for i in range(0, len(data_1['F001_a']), 2):
    row = {}
    publisher1 = data_1.loc[i, 'F26x_b_cleaned_pro']
    publisher2 = data_1.loc[i + 1, 'F26x_b_cleaned_pro']
    row['isbn'] = data.loc[data.publisher_pro.str.contains(publisher1), "id"].values[0]
    row['cluster_id'] = data.loc[data.publisher_pro.str.contains(publisher2), "id"].values[0]
    row["record"] = 1
    row['type'] = "2"
    isbn_df.append(row)

isbn_df = pd.DataFrame(isbn_df)
isbn_df = isbn_df.replace({'record': {0: 1}})
isbn_df.to_csv("cluster_result_single1.csv", index_label=False, index=False)
raw_pro_df.to_csv("./processed_data_10k/ID_cluster.csv", index=False, index_label=False)