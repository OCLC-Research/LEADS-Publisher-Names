### Step 2B: Use all single publisher statement to build publisher clusters
# Add two more parameters: how many strings match foreward and backward

import pandas as pd
import re
import math

def string_split(text):
    text = " ".join(re.split("[^a-zA-Z0-9]+ ", text))
    text = "".join(re.split("[^a-zA-Z0-9]+", text))
    return text
def get_contain(str1, str2):
    finder1 = "^"+str1+" |^"+str1+"$| "+str1+" | "+str1+"$|^"+str1+"\,|^"+str1+"\-| "+str1+"\,| "+str1+"\-|\-"+str1+" |\-"+str1 +"$"
    finder2 = "^" + str2 + " |^" + str2 + "$| " + str2 + " | " + str2 + "$|^" + str2 + "\,|^" + str2 + "\-| " + str2 + "\,| " + str2 + "\-|\-" + str2 + " |\-" + str2 + "$"
    if len(re.findall(finder1, str2)) > 0 or len(re.findall(finder2, str1)) > 0:
        x = 1
    else:
        x = 0
    return x
def forward_sim(str1, str2):
    str1a = ''.join(e for e in str1 if e.isalnum())
    str2a = ''.join(e for e in str2 if e.isalnum())
    str_len = min(len(str1a), len(str2a))
    sim = 0
    sim1 = 0
    for i in range(str_len):
        if (str1a[i] == str2a[i]):
            sim = sim + 1
        else:
            break
    for i in range(str_len):
        if (str1a[- (i + 1)] == str2a[- (i + 1)]):
            sim1 = sim1 + 1
        else:
            break
    x = math.sqrt((sim / len(str1a)) * (sim / len(str2a)))
    x1 = math.sqrt((sim1 / len(str1a)) * (sim1 / len(str2a)))
    return [x, x1]
def common_remove(str):
    # Removes full stop and question mark by the end of the string
    # Also remove parenthesis
    str = re.sub("\.$|\?$|\(|\)", "", str)
    # Automatically restore space after a full stop
    str = re.sub(r"(?<=[a-z]\.)([a-z])", r" \1", str)
    # Remove all other special characters
    str = re.sub(r"[^a-zA-Z0-9 ]+", '', str)
    str = re.sub("\-|\*", " ", str)
    str = re.sub(" +", " ", str)
    list = ["publishing group", "publishing platform",
            'pub', 'publisher', "publications",
            'publishers', 'publishing', 'co', "company",
            "press", "inc", "books", "llc", "ltd", "publ", "book",
            "and", "verlag", "group", "gmbh", "limited", "corp",
            "ptr"]
    mark = " " + "$| ".join(list) + "$"
    while len(re.findall(mark, str)) > 0:
        str = re.sub(mark, "", str)
    return(str)

data = pd.read_csv("./processed_data_10k/publisher_10k_p1.csv")
data = data.loc[data['isbn_tag'] != ""]
data = data[data['isbn_tag'].notnull()]

publisher_name = sorted(set(data.F26x_b_cleaned))
# publisher_name.remove('association')
# publisher_name.remove("university microfilms")
# publisher_name.remove("association press")

df = pd.DataFrame(data={"publisher": publisher_name})
df['isbn_tag'] = ""
for i in range(len(df.index)):
    pub = df.loc[i, 'publisher']
    isbn_list = []
    isbn_vector = data.loc[data['F26x_b_cleaned'] == pub, 'isbn_tag'].tolist()
    for item in isbn_vector:
        if len(re.findall(";;", item)) > 0:
            items = item.split(" ;; ")
            isbn_list.extend(items)
        else:
            isbn_list.append(item)
    isbn_list_final = ";".join(set(isbn_list))
    df.loc[i, "isbn_tag"] = isbn_list_final

df['cluster'] = -1
df_stat = []

# Outputs include the cluster ID, text strings of all combined publishers
cluster_iter = 0
combined = 0
for i in range(len(df.index)):

    for j in range(i + 1, len(publisher_name)):
        row = {}
        # string_1 = re.sub(r"[^a-zA-Z0-9 ]+", '', publisher_name[i])
        # string_2 = re.sub(r"[^a-zA-Z0-9 ]+", '', publisher_name[j])
        # forward = forward_sim(string_1, string_2)[0]
        # backward = forward_sim(string_1, string_2)[1]
        string_3 = common_remove()
        string_4 = common_remove(re.sub(r"[^a-zA-Z0-9 ]+", '', publisher_name[j]))
        containment_1 = get_contain(common_remove(publisher_name[i]), common_remove(publisher_name[j]))
        forward_1 = forward_sim(string_3, string_4)[0]
        backward_1 = forward_sim(string_3, string_4)[1]

        isbn_vector_1 = df.loc[i, 'isbn_tag'].split(";")
        isbn_vector_2 = df.loc[j, 'isbn_tag'].split(";")
        vector_overlap = bool(set(isbn_vector_1) & set(isbn_vector_2))

        row['pub1_id'] = i
        row['pub2_id'] = j
        row['pub1'] = publisher_name[i]
        row['pub2'] = publisher_name[j]
        row["contain_1"] = containment_1
        row['forward_1'] = forward_1
        row['backward_1'] = backward_1
        row["isbn_overlap"] = vector_overlap
        row['select_1'] = (((forward_1 == 1 or backward_1 == 1) or \
                forward_1 + backward_1 > 0.9 or \
                (containment_1 == 1 and forward_1 + backward_1 > 0.75)) and \
                (forward_1 + backward_1) * containment_1 != 0) or \
                          (vector_overlap == True and forward_1 + backward_1 > 0.75 and
                           forward_1 > 0 and backward_1 > 0)
        row['select_2'] = ((forward_1 == 1 or backward_1 == 1) or \
                           forward_1 + backward_1 > 0.9 or \
                           (containment_1 == 1 and forward_1 + backward_1 > 0.75)) and \
                          forward_1 * backward_1 * containment_1 != 0
        if row['select_1'] == True and row['select_2'] == True:
            row['select'] = True
        elif row['select_1'] == False and row['select_2'] == False:
            row['select'] = False
        else:
            row['select'] = row["isbn_overlap"]

        df_stat.append(row)

        cluster_no_current = cluster_iter

        # If two strings are similar enough
        if row['select'] == True:
            # if both strings are not connected to any cluster
            if df.loc[i, 'cluster'] == -1 and df.loc[j, 'cluster'] == -1:
                df.loc[j, 'cluster'] = cluster_iter
            elif df.loc[i, 'cluster'] != -1 and df.loc[j, 'cluster'] == -1:
                df.loc[j, 'cluster'] = df.loc[i, 'cluster']
                cluster_no_current = df.loc[i, 'cluster']
            elif df.loc[i, 'cluster'] == -1 and df.loc[j, 'cluster'] != -1:
                cluster_no_current = df.loc[j, 'cluster']
            elif df.loc[i, 'cluster'] != -1 and df.loc[j, 'cluster'] != -1 and df.loc[i, 'cluster']!= df.loc[j, 'cluster']:
                cluster_no_current = min(s for s in [[df.loc[i, 'cluster'], df.loc[j, 'cluster']]])
                number_tr = max(s for s in [[df.loc[i, 'cluster'], df.loc[j, 'cluster']]])
                df['cluster'].replace(number_tr, cluster_no_current)
            combined = combined + 1
        elif df.loc[i, 'cluster'] == -1:
            cluster_no_current = cluster_iter
        else:
            cluster_no_current = df.loc[i, 'cluster']

    if cluster_no_current == cluster_iter:
        cluster_iter = cluster_iter + 1
    df.loc[i, 'cluster'] = cluster_no_current
    print(i)

df_stat = pd.DataFrame(df_stat)
df_stat.to_csv("./processed_data_10k/publisher_similarity.csv", index=False, index_label=False,
               columns=['pub1_id', "pub2_id", "pub1", "pub2",
                        "contain_1", "forward_1", "backward_1", "select", "isbn_overlap"])

cluster_result = []
for i in range(max(df['cluster'])):
    row = {}
    row['id'] = i
    row['text'] = ";;".join(df.loc[df['cluster'] == i, "publisher"])
    row['isbn'] = ";".join(df.loc[df['cluster'] == i, "isbn_tag"])
    isbn_vector = row['isbn'].split(";")
    row['isbn_new'] = ";".join(set(isbn_vector))
    row['length'] = row['text'].count(';') + 1
    cluster_result.append(row)
    print(i)

df1 = pd.DataFrame(cluster_result)
df1.to_csv("./processed_data_10k/cluster_result.csv", index=False, index_label=False,
          columns=["id", "length", "text", "isbn_new"])