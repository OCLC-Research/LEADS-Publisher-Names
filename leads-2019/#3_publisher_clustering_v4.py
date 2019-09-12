import pandas as pd
import re

### common_remove function remove all special characters in a string
def common_remove(str):
    str = re.sub(r"[^a-zA-Z0-9' ]+", ' ', str).strip()
    str = re.sub(r" +", ' ', str).strip()
    return(str)

x = "2015"
### x being the text string of years
def publisher_cluster(x):

    raw = pd.read_csv("./processed_data_1m/publisher_1m_p1.csv")
    raw = raw.loc[raw['F008_0710'] == x]
    raw_new = raw[pd.notnull(raw['isbn_tag'])]
    raw_new = raw_new.reset_index(drop=True)

    raw_pro = []

    for i in range(len(raw_new.index)):
        isbn_text = raw_new.loc[i, 'isbn_tag']
        isbn_vector = isbn_text.split(" ;; ")
        if len(isbn_vector) > 1:
            for j in range(len(isbn_vector)):
                row = {}
                row["ID"] = raw_new.loc[i, 'F001_a']
                row["ISBN"] = isbn_vector[j]
                row["Publisher"] = raw_new.loc[i, 'F26x_b_cleaned']
                raw_pro.append(row)
        else:
            row = {}
            row["ID"] = raw_new.loc[i, 'F001_a']
            row["ISBN"] = isbn_vector[0]
            row["Publisher"] = raw_new.loc[i, 'F26x_b_cleaned']
            raw_pro.append(row)

    raw_pro_df = pd.DataFrame(raw_pro)
    return(raw_pro_df)

# x is the year as the text string
# potentially, this should be changed to a loop structure?
def summary_year(x):

    raw_pro_df = publisher_cluster(x)
    ### Load the dataset containing only single-publisher records
    data = pd.read_csv("./processed_data_1m/publisher_1m_p1.csv")
    ### Remove records without any ISBN
    data = data.loc[data['isbn_tag'] != ""]
    data = data[data['isbn_tag'].notnull()]
    ### Remove records without any publisher statement
    data = data[data['F26x_b_cleaned'].notnull()]
    # Remove all records with more than one isbn tags
    data = data[~ data['isbn_tag'].str.contains(";")]
    # Create a new field called "F26x_b_cleaned_pro" including a cleaned version of the statement
    data["F26x_b_cleaned_pro"] = ""
    data = data.reset_index()
    print(len(data.index))
    for i in range(len(data.index)):
        data.loc[i, "F26x_b_cleaned_pro"] = common_remove(data.loc[i, "F26x_b_cleaned"])
        print(i)

    data = data.loc[data['F008_0710'] == x]

    publisher_name = sorted(set(data.F26x_b_cleaned_pro))

    df = pd.DataFrame(data={"publisher": publisher_name})
    df['isbn_tag'] = ""
    df['publisher_pro'] = ""
    data['cluster'] = 0
    for i in range(len(df.index)):
        print(i)
        pub = df.loc[i, 'publisher']
        isbn_list = []
        year_list = []
        isbn_vector = data.loc[data['F26x_b_cleaned_pro'] == pub, 'isbn_tag'].tolist()
        year_vector = data.loc[data['F26x_b_cleaned_pro'] == pub, 'F008_0710'].tolist()
        record_no = len(data.loc[data['F26x_b_cleaned_pro'] == pub])
        data_sub = data.loc
        for item in isbn_vector:
            if len(re.findall(";;", item)) > 0:
                items = item.split(" ;; ")
                isbn_list.extend(items)
            else:
                isbn_list.append(item)
        for item in year_vector:
            year_list.append(item)
        isbn_list_final = ";".join(set(isbn_list))
        year_list_final = ";".join(set(year_list))
        df.loc[i, "isbn_tag"] = isbn_list_final
        df.loc[i, "year"] = year_list_final
        df.loc[i, "record"] = record_no
        df.loc[i, "publisher_pro"] = common_remove(df.loc[i, "publisher"])
        list = data.loc[data['F26x_b_cleaned_pro'] == pub, 'source'].tolist()

        if (2 in list):
            df.loc[i, "source"] = 2
        else:
            df.loc[i, "source"] = 1

        data.loc[data['F26x_b_cleaned_pro'] == pub, 'cluster'] = i
        df.loc[i, "cluster_original"] = int(i)

    cluster_result = []
    for i in range(max(df['cluster_original'].astype(int))):
        row = {}
        row['id'] = i
        row['text'] = ";;".join(df.loc[df['cluster_original'] == i, "publisher"])
        row['publisher_pro'] = ";;".join(df.loc[df['cluster_original'] == i, "publisher_pro"])
        row['isbn'] = ";".join(df.loc[df['cluster_original'] == i, "isbn_tag"])
        row['year'] = ";".join(df.loc[df['cluster_original'] == i, "year"])
        row['record'] = sum(df.loc[df['cluster_original'] == i, "record"])
        isbn_vector = row['isbn'].split(";")
        year_vector = row['year'].split(";")
        row['isbn_new'] = ";".join(set(isbn_vector))
        row['year_min'] = min(year_vector)
        row['year_max'] = max(year_vector)
        row['length'] = row['text'].count(';;') + 1
        row['group'] = i
        cluster_result.append(row)
        print(i)

    df1 = pd.DataFrame(cluster_result)
    data = data[data['publisher_pro'].notnull()]
    data = data.reset_index()

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

    isbn_df = pd.DataFrame(isbn_df)
    isbn_df = isbn_df.replace({'record': {0: 1}})
    isbn_df.to_csv("./processed_data_1m/isbn_df_simple.csv", index_label=False, index=False)

df = summary_year(x)
df.to_csv("./processed_data_1m/cluster_result_single.csv", index=False, index_label=False,
               columns=["id", "length", "text", "publisher_pro",
                        "isbn_new", "year_min", "year_max", "record"])
raw_pro_df = publisher_cluster(x)
raw_pro_df.to_csv("./processed_data_1m/ID_cluster.csv", index=False, index_label=False)