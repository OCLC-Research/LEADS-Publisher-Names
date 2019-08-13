### Step 2B: Use all single publisher statement to build publisher clusters
# Add two more parameters: how many strings match foreward and backward

import pandas as pd
import re
import math

### common_remove function remove all special characters in a string
def common_remove(str):
    str = re.sub(r"[^a-zA-Z0-9' ]+", ' ', str).strip()
    str = re.sub(r" +", ' ', str).strip()
    return(str)

# If combined with any p_2 file, change the file to "publisher_10k_p1_a.csv"
data = pd.read_csv("./processed_data_10k/publisher_10k_p1.csv")
data = data.loc[data['isbn_tag'] != ""]
data = data[data['isbn_tag'].notnull()]
# Remove all records with more than one isbn tags
data = data[~ data['isbn_tag'].str.contains(";")]
data["F26x_b_cleaned_pro"] = ""
data = data.reset_index()
for i in range(len(data.index)):
    data.loc[i, "F26x_b_cleaned_pro"] = common_remove(data.loc[i, "F26x_b_cleaned"])

publisher_name = sorted(set(data.F26x_b_cleaned_pro))
# publisher_name.remove('association')
# publisher_name.remove("university microfilms")
# publisher_name.remove("association press")

df = pd.DataFrame(data={"publisher": publisher_name})
df['isbn_tag'] = ""
df['publisher_pro'] = ""
data['cluster'] = 0
for i in range(len(df.index)):
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

# ### Compare and cluster publisher names based on the raw data acquired above
# ### Create a list of abbreviations for the word_matching function
# ### List is based on: https://web.library.yale.edu/cataloging/AACR2-abbreviations
# term_list = [['corporation', "corp"],
#              ['company', "co"],
#              ['brother', "bro", "bros"],
#              ['book', "bk"],
#              ['department', "dept"],
#              ['edition', 'ed'],
#              ['editions', 'eds'],
#              ['government', "govt"],
#              ['inc', 'incorporated'],
#              ['ltd', 'limited'],
#              ['paperback', 'pbk'],
#              ['pub', 'publ', 'publishing'],
#              ['association', "assoc"],
#              ['press', "pres", "pr", "p"],
#              ['university', 'univ', "u"]]

# ### get_group retrieves the group of a text string in term_list
# ### so that to determine if two strings are supposed to be the same in AACR2 abbreviation rules
# def get_group(str):
#     if any(str in sublist for sublist in term_list) == True:
#         return([(i, term_list.index(str))
#                  for i, term_list in enumerate(term_list)
#                  if str in term_list][0][0])
#     else:
#         return("Not Available")


# ### word_matching compares how two strings are similar with each other on the word level
# ### it will return two values: whether they match and the extent to which they match
# def word_matching(str1, str2):
#     vector1 = str1.split(" ")
#     vector2 = str2.split(" ")
#     if str1 == str2:
#         match_is = True
#     elif len(vector1) == len(vector2):
#         match_freq = 0
#         for i in range(len(vector1)):
#             if vector1[i] == vector2[i]:
#                 match_freq = match_freq + 1
#             elif get_group(vector1[i]) == get_group(vector2[i]) and get_group(vector1[i]) != "Not Available":
#                 match_freq = match_freq + 1
#             elif i == 0 and (len(vector1[i]) == 1 or len(vector2[i]) == 1) and vector1[i][0] == vector2[i][0]:
#                 if len(vector1) > 2 or (any(vector1[1] in sublist for sublist in term_list) == False and vector1[1] != "books"):
#                     match_freq = match_freq + 1
#         if match_freq == len(vector1):
#             match_is = True
#         else:
#             match_is = False
#     else:
#         if ''.join(str1.split()) == ''.join(str2.split()):
#             match_is = True
#         else:
#             match_is = False
#             match_freq_1 = 0
#             for j in range(len(vector1)):
#                 for k in range(len(vector2)):
#                     if vector1[j] == vector2[k] or (get_group(vector1[j]) == get_group(vector2[k]) and get_group(
#                             vector1[j]) != "Not Available"):
#                         match_freq_1 = match_freq_1 + 1
#                         break
#     return match_is

# ### Below are the character-level evaluations
# def get_contain(str1, str2):
#     finder1 = "^"+str1+" |^"+str1+"$| "+str1+" | "+str1+"$|^"+str1+"\,|^"+str1+"\-| "+str1+"\,| "+str1+"\-|\-"+str1+" |\-"+str1 +"$"
#     finder2 = "^" + str2 + " |^" + str2 + "$| " + str2 + " | " + str2 + "$|^" + str2 + "\,|^" + str2 + "\-| " + str2 + "\,| " + str2 + "\-|\-" + str2 + " |\-" + str2 + "$"
#     if len(re.findall(finder1, str2)) > 0 or len(re.findall(finder2, str1)) > 0:
#         x = 1
#     else:
#         x = 0
#     return x
# def forward_sim(str1, str2):
#     str1a = ''.join(e for e in str1 if e.isalnum())
#     str2a = ''.join(e for e in str2 if e.isalnum())
#     str_len = min(len(str1a), len(str2a))
#     sim = 0
#     sim1 = 0
#     for i in range(str_len):
#         if (str1a[i] == str2a[i]):
#             sim = sim + 1
#         else:
#             break
#     for i in range(str_len):
#         if (str1a[- (i + 1)] == str2a[- (i + 1)]):
#             sim1 = sim1 + 1
#         else:
#             break
#     x = math.sqrt((sim / len(str1a)) * (sim / len(str2a)))
#     x1 = math.sqrt((sim1 / len(str1a)) * (sim1 / len(str2a)))
#     return [x, x1]
# def common_remove_1(str):
#     # Removes full stop and question mark by the end of the string
#     # Also remove parenthesis
#     str = re.sub("\.$|\?$|\(|\)", "", str)
#     # Automatically restore space after a full stop
#     str = re.sub(r"(?<=[a-z]\.)([a-z])", r" \1", str)
#     # Remove all other special characters
#     str = re.sub(r"[^a-zA-Z0-9 ]+", '', str)
#     str = re.sub("\-|\*", " ", str)
#     str = re.sub(" +", " ", str)
#     list = ["publishing group", "publishing platform",
#             'pub', 'publisher', "publications",
#             'publishers', 'publishing', 'co', "company",
#             "press", "inc", "books", "llc", "ltd", "publ", "book",
#             "and", "verlag", "group", "gmbh", "limited", "corp",
#             "ptr"]
#     mark = " " + "$| ".join(list) + "$"
#     while len(re.findall(mark, str)) > 0:
#         str = re.sub(mark, "", str)
#     return(str)
#
# ### common_remove function remove all special characters in a string
# def common_remove(str):
#     str = re.sub(r"[^a-zA-Z0-9' ]+", ' ', str).strip()
#     str = re.sub(r" +", ' ', str).strip()
#     str = re.sub(r"[0-9]{4}$|[0-9] {4}$", "", str).strip()
#     return(str)
#
# # Outputs include the cluster ID, text strings of all combined publishers
# cluster_iter = 0
# combined = 0
# for i in range(len(df.index)):
#
#     for j in range(i + 1, len(publisher_name)):
#         row = {}
#
#         string_1 = common_remove(publisher_name[i])
#         string_2 = common_remove(publisher_name[j])
#
#         sameness = word_matching(string_1, string_2)
#         isbn_vector_1 = df.loc[i, 'isbn_tag'].split(";")
#         isbn_vector_2 = df.loc[j, 'isbn_tag'].split(";")
#         vector_overlap = bool(set(isbn_vector_1) & set(isbn_vector_2))
#
#         string_3 = common_remove_1(publisher_name[i])
#         string_4 = common_remove_1(publisher_name[j])
#         containment_1 = get_contain(string_3, string_4)
#         forward_1 = forward_sim(string_3, string_4)[0]
#         backward_1 = forward_sim(string_3, string_4)[1]
#
#         row['pub1_id'] = i
#         row['pub2_id'] = j
#         row['pub1'] = publisher_name[i]
#         row['pub2'] = publisher_name[j]
#         row['sameness'] = sameness
#         row["isbn_overlap"] = vector_overlap
#         row['select'] = sameness == True
#         row["contain_1"] = containment_1
#         row['forward_1'] = forward_1
#         row['backward_1'] = backward_1
#
#         df_stat.append(row)
#
#         cluster_no_current = cluster_iter
#
#         # If two strings are similar enough
#         if row['select'] == True:
#             # if both strings are not connected to any cluster
#             if df.loc[i, 'cluster_pre'] == -1 and df.loc[j, 'cluster_pre'] == -1:
#                 df.loc[j, 'cluster_pre'] = cluster_iter
#             elif df.loc[i, 'cluster_pre'] != -1 and df.loc[j, 'cluster_pre'] == -1:
#                 df.loc[j, 'cluster_pre'] = df.loc[i, 'cluster_pre']
#                 cluster_no_current = df.loc[i, 'cluster_pre']
#             elif df.loc[i, 'cluster_pre'] == -1 and df.loc[j, 'cluster_pre'] != -1:
#                 cluster_no_current = df.loc[j, 'cluster_pre']
#             elif df.loc[i, 'cluster_pre'] != -1 and df.loc[j, 'cluster_pre'] != -1 and df.loc[i, 'cluster_pre']!= df.loc[j, 'cluster_pre']:
#                 cluster_no_current = min(s for s in [[df.loc[i, 'cluster_pre'], df.loc[j, 'cluster_pre']]])
#                 number_tr = max(s for s in [[df.loc[i, 'cluster_pre'], df.loc[j, 'cluster_pre']]])
#                 df['cluster_pre'].replace(number_tr, cluster_no_current)
#             combined = combined + 1
#         elif df.loc[i, 'cluster_pre'] == -1:
#             cluster_no_current = cluster_iter
#         else:
#             cluster_no_current = df.loc[i, 'cluster_pre']
#
#     if cluster_no_current == cluster_iter:
#         cluster_iter = cluster_iter + 1
#     df.loc[i, 'cluster_pre'] = cluster_no_current
#     print(i)
#
# df_stat = pd.DataFrame(df_stat)
# df_stat.to_csv("./processed_data_10k/publisher_similarity.csv", index=False, index_label=False,
#                columns=['pub1_id', "pub2_id", "pub1", "pub2", "sameness",
#                         "select", "isbn_overlap", "contain_1",
#                         "forward_1", "backward_1"])

# If using pair-wise comparisons, delete the following line of code
# think about this

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
df1.to_csv("./processed_data_10k/cluster_result_single.csv", index=False, index_label=False,
           columns=["id", "length", "text", "publisher_pro",
                    "isbn_new", "year_min", "year_max", "record"])