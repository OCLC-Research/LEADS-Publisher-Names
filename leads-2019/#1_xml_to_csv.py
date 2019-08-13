from xml.etree import ElementTree
import pandas as pd
import re
from isbnlib import mask, to_isbn10, is_isbn10, is_isbn13

# tree = ElementTree.parse("./raw_data/sample_1k_marc.xml")
tree = ElementTree.parse("./raw_data/marc_1MM.xml")
collection = tree.getroot()

code_336 = pd.read_csv("./raw_data/336_code.csv")
code_337 = pd.read_csv("./raw_data/337_code.csv")
code_338 = pd.read_csv("./raw_data/338_code.csv")

features = []  # list of features

def clean_text(x):
    x = re.sub("\\.$", "", x)
    return(x)

# range(len(collection))
for i in range(len(collection)):
    row = {}
    print("---------------------  " + str(i))
    record = collection[i]

    leader = record.find('{http://www.loc.gov/MARC21/slim}leader')
    leader_6 = leader.text[6]
    leader_17 = leader.text[17]
    leader_18 = leader.text[18]
    # print(leader_type)
    row['leader_6'] = leader_6
    row['leader_17'] = leader_17
    row['leader_18'] = leader_18

    control = record.findall('{http://www.loc.gov/MARC21/slim}controlfield')
    F006 = 0
    F007 = 0
    for c in control:
        tag = c.get('tag')
        # print(tag)

        if tag == '001':
            oclc_controlnum = c.text
            # print(physical_desc)
            row['F001_a'] = oclc_controlnum

        if tag == '006':
            F006 = F006 + 1

        if tag == '007':
            F007 = F007 + 1

        if tag == '008':
            value = c.text
            # print(value)
            pub_code = value[6]
            pub_year_1 = value[7:11]
            pub_year_2 = value[11:15]
            place = value[15:18]
            audience = value[22]
            cont_nature = value[24:28]
            government = value[28]
            literary = value[33]
            language = value[35:38]
            catalog_source = value[39]
            # print(place, language, catalog_source)
            row['F008_06'] = pub_code
            row['F008_0710'] = pub_year_1
            row['F008_1114'] = pub_year_2
            row['F008_1517'] = place
            row['F008_22'] = audience
            row['F008_2427_a'] = bool(re.search('a', cont_nature))
            row['F008_2427_b'] = bool(re.search('b', cont_nature))
            row['F008_2427_c'] = bool(re.search('c', cont_nature))
            row['F008_2427_d'] = bool(re.search('d', cont_nature))
            row['F008_2427_e'] = bool(re.search('e', cont_nature))
            row['F008_2427_f'] = bool(re.search('f', cont_nature))
            row['F008_2427_g'] = bool(re.search('g', cont_nature))
            row['F008_2427_i'] = bool(re.search('i', cont_nature))
            row['F008_2427_j'] = bool(re.search('j', cont_nature))
            row['F008_2427_k'] = bool(re.search('k', cont_nature))
            row['F008_2427_l'] = bool(re.search('l', cont_nature))
            row['F008_2427_m'] = bool(re.search('m', cont_nature))
            row['F008_2427_n'] = bool(re.search('n', cont_nature))
            row['F008_2427_o'] = bool(re.search('o', cont_nature))
            row['F008_2427_p'] = bool(re.search('p', cont_nature))
            row['F008_2427_q'] = bool(re.search('q', cont_nature))
            row['F008_2427_r'] = bool(re.search('r', cont_nature))
            row['F008_2427_s'] = bool(re.search('s', cont_nature))
            row['F008_2427_t'] = bool(re.search('t', cont_nature))
            row['F008_2427_u'] = bool(re.search('u', cont_nature))
            row['F008_2427_v'] = bool(re.search('v', cont_nature))
            row['F008_2427_w'] = bool(re.search('w', cont_nature))
            row['F008_2427_y'] = bool(re.search('y', cont_nature))
            row['F008_2427_z'] = bool(re.search('z', cont_nature))
            row['F008_2427_2'] = bool(re.search('2', cont_nature))
            row['F008_2427_5'] = bool(re.search('5', cont_nature))
            row['F008_2427_6'] = bool(re.search('6', cont_nature))
            row['F008_28'] = government
            row['F008_33'] = literary
            row['F008_3537'] = language
            row['F008_39'] = catalog_source

            if place is None:
                row['008_1517'] = "NA"
            if language is None:
                row['008_3537'] = "NA"
            if len(catalog_source) == 0:
                row['008_39'] = "NA"

    row['006_is'] = 1 if F006 > 0 else 0
    row['007_is'] = 1 if F007 > 0 else 0

    data = record.findall('{http://www.loc.gov/MARC21/slim}datafield')

    F040_e = 0
    F041_is = 0
    F050_is = 0
    F082_is = 0
    F260_is = 0
    F264_is = 0
    F26x_is = 0
    F336_is = 0
    F337_is = 0
    F338_is = 0
    F490_is = 0
    F6xxa_is = 0
    F6xxv_is = 0
    F6xxy_is = 0
    F6xxz_is = 0
    isbn_list = []
    isbn_tag_list = []
    F041_a_list = []
    F041_h_list = []
    F050_a1_list = []
    F050_a2_list = []
    F082_a1_list = []
    F082_a2_list = []
    F260_b_list = []
    F260_c_list = []
    F264_b_list = []
    F264_c_list = []
    F26x_b_list = []
    F26x_c_list = []
    F336_b_list = []
    F337_b_list = []
    F338_b_list = []
    F490_a_list = []
    F6xx_a_list = []
    F6xx_v_list = []
    F6xx_y_list = []
    F6xx_z_list = []

    for d in data:
        tag = d.get('tag')
        print("---------------------  " + str(i) + "---- " + tag)

        if tag == '020':
            # print(d)
            subfields = d.findall('{http://www.loc.gov/MARC21/slim}subfield')
            for s in subfields:
                if s.get('code') == 'a':
                    isbn = s.text

                    if len(isbn) == 10 and is_isbn10(str(isbn)) == True and mask(isbn) is not None:
                        isbn_text = str(isbn)
                        isbn_list.append(isbn_text)
                        isbn_tag = '--'.join(mask(isbn).split("-")[0:2])
                        isbn_tag_list.append(isbn_tag)
                    elif len(isbn) == 13 and is_isbn13(str(isbn)) == True and mask(isbn) is not None and isbn[0:3] == "978":
                        isbn_text = str(isbn)
                        isbn_list.append(isbn_text)
                        isbn_tag = '--'.join(mask(to_isbn10(isbn)).split("-")[0:2])
                        isbn_tag_list.append(isbn_tag)

        if tag == "040":
            subfields = d.findall('{http://www.loc.gov/MARC21/slim}subfield')
            for s in subfields:
                if s.get('code') == 'e':
                    if s.text == 'rda' or s.text == "RDA":
                        F040_e = F040_e + 1

        if tag == "041":
            F041_is = F041_is + 1
            F041_ind1 = d.get('ind1')
            subfields = d.findall('{http://www.loc.gov/MARC21/slim}subfield')
            for s in subfields:
                if s.get('code') == 'a':
                    F041_a_list.append(s.text)
                if s.get('code') == 'h':
                    F041_h_list.append(s.text)

        if tag == '050':
            F050_is = F050_is + 1
            subfields = d.findall('{http://www.loc.gov/MARC21/slim}subfield')
            for s in subfields:
                if s.get('code') == 'a':
                    match = re.search(r'^[A-Z]{1,3}', str(s.text))
                    match2 = re.search(r'^[A-Z]{1,3}[0-9]{1,}(?=\.|[A-z]|$| )', str(s.text))
                    if match and match2:
                        F050_a1_list.append(match.group())
                        F050_a2_list.append(match2.group())

        if tag == '082':
            F082_is = F082_is + 1
            subfields = d.findall('{http://www.loc.gov/MARC21/slim}subfield')
            for s in subfields:
                if s.get('code') == 'a':
                    match = re.search(r'^[0-9]{3}', str(s.text))
                    if match:
                        F082_a1_list.append(match.group()[0])
                        F082_a2_list.append(match.group())

        if tag == '260':
            F260_is = F260_is + 1
            F26x_is = F26x_is + 1
            # print(d)
            subfields = d.findall('{http://www.loc.gov/MARC21/slim}subfield')
            for s in subfields:
                if s.get('code') == 'b':
                    F260_b_list.append(s.text)
                    F26x_b_list.append(s.text)
                    if len(re.findall("printed by |distributed by |distributed in ", s.text.lower())) > 0:
                        F260_is = F260_is - 1
                        F26x_is = F26x_is - 1
                if s.get('code') == 'c':
                    F260_c_list.append(s.text)
                    text_26x = re.findall("\d{4}", s.text)
                    F26x_c_list.extend(text_26x)

        if tag == '264' and d.get('ind2') == '1':
            F264_is = F264_is + 1
            F26x_is = F26x_is + 1
            # print(d)
            subfields = d.findall('{http://www.loc.gov/MARC21/slim}subfield')
            for s in subfields:
                if s.get('code') == 'b':
                    F264_b_list.append(s.text)
                    F26x_b_list.append(s.text)
                    if len(re.findall("printed by |distributed by |distributed in ", s.text.lower())) > 0:
                        F264_is = F264_is - 1
                        F26x_is = F26x_is - 1
                if s.get('code') == 'c':
                    F264_c_list.append(s.text)
                    text_26x = re.findall("\d{4}", s.text)
                    F26x_c_list.extend(text_26x)

        if tag == '336':
            F336_is = F336_is + 1
            subfields = d.findall('{http://www.loc.gov/MARC21/slim}subfield')
            sub_code_list = []
            for t in subfields:
                sub_code_list.append(t.get("code"))
            b_is = "b" in sub_code_list
            a_is = "a" in sub_code_list
            if b_is > 0:
                for s in subfields:
                    if s.get('code') == 'b':
                        F336_b_value = s.text
                    if s.get('code') == '2':
                        F336_2_value = s.text
            elif b_is == 0 and a_is > 0:
                for s in subfields:
                    if s.get('code') == 'a' and s.text in code_336['336_a'].values:
                        text_336b = code_336.loc[code_336['336_a'] == s.text, '336_b'].values[0]
                        F336_b_value = text_336b
                    if s.get('code') == '2':
                        F336_2_value = s.text
            if "rda" in F336_2_value.lower():
                F336_b_list.append(F336_b_value)

        if tag == '337':
            F337_is = F337_is + 1
            subfields = d.findall('{http://www.loc.gov/MARC21/slim}subfield')
            sub_code_list = []
            for t in subfields:
                sub_code_list.append(t.get("code"))
            b_is = "b" in sub_code_list
            a_is = "a" in sub_code_list
            if b_is > 0:
                for s in subfields:
                    if s.get('code') == 'b':
                        F337_b_value = s.text
                    if s.get('code') == '2':
                        F337_2_value = s.text
            elif b_is == 0 and a_is > 0:
                for s in subfields:
                    if s.get('code') == 'a' and s.text in code_337['337_a'].values:
                        text_337b = code_337.loc[code_337['337_a'] == s.text, '337_b'].values[0]
                        F337_b_value = text_337b
                    if s.get('code') == '2':
                        F337_2_value = s.text
            if "rda" in F337_2_value.lower():
                F337_b_list.append(F337_b_value)

        if tag == '338':
            F338_is = F338_is + 1
            subfields = d.findall('{http://www.loc.gov/MARC21/slim}subfield')
            sub_code_list = []
            for t in subfields:
                sub_code_list.append(t.get("code"))
            b_is = "b" in sub_code_list
            a_is = "a" in sub_code_list
            if b_is > 0:
                for s in subfields:
                    if s.get('code') == 'b':
                        F338_b_value = s.text
                    if s.get('code') == '2':
                        F338_2_value = s.text
            elif b_is == 0 and a_is > 0:
                for s in subfields:
                    if s.get('code') == 'a' and s.text in code_338['338_a'].values:
                        text_338b = code_338.loc[code_338['338_a'] == s.text, '338_b'].values[0]
                        F338_b_value = text_338b
                    if s.get('code') == '2':
                        F338_2_value = s.text
            if "rda" in F338_2_value.lower():
                F338_b_list.append(F338_b_value)

        if tag == '490':
            F490_is = F490_is + 1
            # print(d)
            subfields = d.findall('{http://www.loc.gov/MARC21/slim}subfield')
            for s in subfields:
                if s.get('code') == 'a':
                    F490_a_list.append(s.text)

        if tag in ['600', '610', '611', '630', '650'] and d.get('ind2') == "0":
            # print(d)
            subfields = d.findall('{http://www.loc.gov/MARC21/slim}subfield')
            for s in subfields:
                if s.get('code') == 'a':
                    F6xxa_is = F6xxa_is + 1
                    F6xx_a_list.append(clean_text(s.text))
                if s.get('code') == 'v':
                    F6xxv_is = F6xxv_is + 1
                    F6xx_v_list.append(clean_text(s.text))
                if s.get('code') == 'y':
                    F6xxy_is = F6xxy_is + 1
                    F6xx_y_list.append(clean_text(s.text))
                if s.get('code') == 'z':
                    F6xxz_is = F6xxz_is + 1
                    F6xx_z_list.append(clean_text(s.text))

        if tag == "651" and d.get('ind2') == "0":
            # print(d)
            subfields = d.findall('{http://www.loc.gov/MARC21/slim}subfield')
            for s in subfields:
                if s.get('code') == 'a':
                    F6xxz_is = F6xxz_is + 1
                    F6xx_z_list.append(clean_text(s.text))
                if s.get('code') == 'v':
                    F6xxv_is = F6xxv_is + 1
                    F6xx_v_list.append(clean_text(s.text))
                if s.get('code') == 'y':
                    F6xxy_is = F6xxy_is + 1
                    F6xx_y_list.append(clean_text(s.text))
                if s.get('code') == 'z':
                    F6xxz_is = F6xxz_is + 1
                    F6xx_z_list.append(clean_text(s.text))

        if tag == "655" and d.get('ind2') == "0":
            # print(d)
            subfields = d.findall('{http://www.loc.gov/MARC21/slim}subfield')
            for s in subfields:
                if s.get('code') == 'a':
                    F6xxv_is = F6xxv_is + 1
                    F6xx_v_list.append(clean_text(s.text))
                if s.get('code') == 'v':
                    F6xxv_is = F6xxv_is + 1
                    F6xx_v_list.append(clean_text(s.text))
                if s.get('code') == 'y':
                    F6xxy_is = F6xxy_is + 1
                    F6xx_y_list.append(clean_text(s.text))
                if s.get('code') == 'z':
                    F6xxz_is = F6xxz_is + 1
                    F6xx_z_list.append(clean_text(s.text))

    # print(code)
    # print(value)

    isbn_list1 = set(isbn_list)
    isbn_tag_list1 = set(isbn_tag_list)
    if (len(isbn_tag_list) > 0):
        row['isbn'] = " ;; ".join(set(isbn_list1))
        row['isbn_tag'] = " ;; ".join(set(isbn_tag_list1))
        row['isbn1'] = isbn_list[0]
        row['isbn_tag1'] = isbn_tag_list[0]
    else:
        row['isbn'] = "NA"
        row['isbn_tag'] = "NA"
        row['isbn1'] = "NA"
        row['isbn_tag1'] = "NA"

    if F040_e > 0:
        row['F040_e'] = 1
    else:
        row['F040_e'] = 0

    if F041_is > 0:
        row['F041_ind1'] = F041_ind1
        row['F041_a'] = " ;; ".join(F041_a_list)
        row['F041_h'] = " ;; ".join(F041_h_list)
    else:
        row['F041_ind1'] = "NA"
        row['F041_a'] = "NA"
        row['F041_h'] = "NA"

    if len(F050_a1_list) > 0:
        row['F050_a1'] = " ;; ".join(set(F050_a1_list))
        row['F050_a2'] = " ;; ".join(set(F050_a2_list))
    else:
        row['F050_a1'] = "NA"
        row['F050_a2'] = "NA"

    if len(F082_a1_list) > 0:
        row['F082_a1'] = " ;; ".join(set(F082_a1_list))
        row['F082_a2'] = " ;; ".join(set(F082_a2_list))
    else:
        row['F082_a1'] = "NA"
        row['F082_a2'] = "NA"

    row['F260_is'] = F260_is
    if F260_is > 0:
        row['F260_b'] = " ;; ".join(F260_b_list)
        row['F260_c'] = " ;; ".join(F260_c_list)
    else:
        row['F260_b'] = "NA"
        row['F260_c'] = "NA"

    row['F264_is'] = F264_is
    if F264_is > 0:
        row['F264_b'] = " ;; ".join(F264_b_list[0:0 + F26x_is])
        row['F264_c'] = " ;; ".join(F264_c_list)
    else:
        row['F264_b'] = "NA"
        row['F264_c'] = "NA"

    row['F26x_is'] = F26x_is
    if F26x_is > 0:
        row['F26x_b'] = " ;; ".join(set(F26x_b_list[0:0 + F26x_is]))
        row['F26x_c'] = " ;; ".join(set(F26x_c_list))
    else:
        row['F26x_b'] = "NA"
        row['F26x_c'] = "NA"

    if F336_is > 0:
        F336_b_text = F336_b_list
        row['F336_b'] = " ;; ".join(F336_b_text)
        row['F336_b_txt'] = bool(re.search('txt', row['F336_b']))
        row['F336_b_sti'] = bool(re.search('sti', row['F336_b']))
        row['F336_b_cri'] = bool(re.search('cri', row['F336_b']))
        row['F336_b_spw'] = bool(re.search('spw', row['F336_b']))
        row['F336_b_tct'] = bool(re.search('tct', row['F336_b']))
    else:
        row['F336_b'] = "NA"
        row['F336_b_txt'] = ""
        row['F336_b_sti'] = ""
        row['F336_b_cri'] = ""
        row['F336_b_spw'] = ""
        row['F336_b_tct'] = ""

    if F337_is > 0:
        F337_b_text = F337_b_list
        row['F337_b'] = " ;; ".join(F337_b_text)
        row['F337_b_c'] = bool(re.search('c', row['F337_b']))
        row['F337_b_h'] = bool(re.search('h', row['F337_b']))
        row['F337_b_n'] = bool(re.search('n', row['F337_b']))
        row['F337_b_s'] = bool(re.search('s', row['F337_b']))
    else:
        row['F337_b'] = "NA"
        row['F337_b_c'] = ""
        row['F337_b_h'] = ""
        row['F337_b_n'] = ""
        row['F337_b_s'] = ""

    if F338_is > 0:
        F338_b_text = F338_b_list
        row['F338_b'] = " ;; ".join(F338_b_text)
        row['F338_b_cd'] = bool(re.search('cd', row['F338_b']))
        row['F338_b_cr'] = bool(re.search('cr', row['F338_b']))
        row['F338_b_hd'] = bool(re.search('hd', row['F338_b']))
        row['F338_b_he'] = bool(re.search('he', row['F338_b']))
        row['F338_b_nb'] = bool(re.search('nb', row['F338_b']))
        row['F338_b_sd'] = bool(re.search('sd', row['F338_b']))
    else:
        row['F338_b'] = "NA"
        row['F338_b_cd'] = ""
        row['F338_b_cr'] = ""
        row['F338_b_hd'] = ""
        row['F338_b_he'] = ""
        row['F338_b_nb'] = ""
        row['F338_b_sd'] = ""

    if F490_is > 0:
        row['F490_a'] = " ;; ".join(F490_a_list)
    else:
        row['F490_a'] = "NA"

    if F6xxa_is > 0:
        row['F6xx_a'] = " ;; ".join(set(F6xx_a_list))
    else:
        row['F6xx_a'] = "NA"

    if F6xxv_is > 0:
        row['F6xx_v'] = " ;; ".join(set(F6xx_v_list))
    else:
        row['F6xx_v'] = "NA"

    if F6xxy_is > 0:
        row['F6xx_y'] = " ;; ".join(set(F6xx_y_list))
    else:
        row['F6xx_y'] = "NA"

    if F6xxz_is > 0:
        row['F6xx_z'] = " ;; ".join(set(F6xx_z_list))
    else:
        row['F6xx_z'] = "NA"

    features.append(row)

print("Writing data to the file.")
print(str(i), "lines.")
df = pd.DataFrame(features)
df.to_csv("./processed_data_1m/result_1m.csv", index=False, index_label=False,
          columns = ["leader_6", "leader_17", "leader_18", "F001_a",
                     "F008_06", "F008_0710", "F008_1114", "F008_1517",
                     "F008_22", 'F008_2427_a', 'F008_2427_b', 'F008_2427_c',
                     'F008_2427_d', 'F008_2427_e', 'F008_2427_f',
                     'F008_2427_g', 'F008_2427_i', 'F008_2427_j',
                     'F008_2427_k', 'F008_2427_l', 'F008_2427_m',
                     'F008_2427_n', 'F008_2427_o', 'F008_2427_p',
                     'F008_2427_q', 'F008_2427_r', 'F008_2427_s',
                     'F008_2427_t', 'F008_2427_u', 'F008_2427_v',
                     'F008_2427_w', 'F008_2427_y', 'F008_2427_z',
                     'F008_2427_2', 'F008_2427_5', 'F008_2427_6',
                     "F008_28", "F008_33", "F008_3537", "F008_39",
                     "006_is", "007_is", "isbn", "isbn_tag", "isbn1", "isbn_tag1", "F040_e",
                     "F041_ind1", "F041_a", "F041_h", "F050_a1", "F050_a2",
                     "F082_a1", "F082_a2", "F260_is", "F260_b", "F260_c",
                     "F264_is", "F264_b", "F264_c", "F26x_is", "F26x_b",
                     "F26x_c", "F336_b", 'F336_b_txt', 'F336_b_sti',
                     'F336_b_cri', 'F336_b_spw', 'F336_b_tct', "F337_b",
                     'F337_b_c', 'F337_b_h', 'F337_b_n', 'F337_b_s',
                     "F338_b", 'F338_b_cd', 'F338_b_cr', 'F338_b_hd',
                     'F338_b_he', 'F338_b_nb', 'F338_b_sd',
                     "F490_a", "F6xx_a", "F6xx_v", "F6xx_y", "F6xx_z"])
