# load the set of packages
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt


# import the kNN classification model
from sklearn.neighbors import KNeighborsClassifier

# import train_test_split from sklearn.cross_validation
from sklearn.model_selection import train_test_split # using a new module in sklearn

"""
Change the input and output files as required
"""
# import the data
#feature_file = pd.read_csv('numeric-features-hashing-nostop.csv')
#feature_file = pd.read_csv('numeric-features-hashing.csv')
#feature_file = pd.read_csv('numeric-features-tfidf-nostop.csv')
#feature_file = pd.read_csv('numeric-features-tfidf.csv')
feature_file = pd.read_csv('numeric-features-cv-nostop.csv')
#feature_file = pd.read_csv('numeric-features-cv.csv')

#output_prediction_file = 'predictions-hashing-nostop.csv'
#output_prediction_file = 'predictions-hashing.csv'
#output_prediction_file = 'predictions-tfidf-nostop.csv'
#output_prediction_file = 'predictions-tfidf.csv'
output_prediction_file = 'predictions-cv-nostop.csv'
#output_prediction_file = 'predictions-cv.csv'



"""
Comment out the features you don't want to consider 
"""

# predictors for hashing approach
"""
features_to_consider =  [#"f1",
						"f2",
						"f3",
						"f4",
						"f5",
						"f6",
						"f7",
						"f8",
						"f9",
						"f10",
						"f11",
						"f12",
						"f13",
						"f14",
						"f15",
						"f16",
						"f17",
						"f18",
						"f19",
						"f20",
						"f21",
						"f22",
						"f23",
						"f24",
						"f25",
						"f26",
						"f27",
						"f28",
						"f29",
						"f30",
						"f31",
						"f32",
						"f33",
						"f34",
						"f35",
						"f36",
						"f37",
						"f38",
						"f39",
						"f40",
						"f41",
						"f42",
						"f43",
						"f44",
						"f45",
						"f46",
						"f47",
						"f48",
						"f49",
						"f50",
						"f51",
						"f52",
						"f53",
						"f54",
						"f55",
						"f56",
						"f57",
						"f58",
						"f59",
						"f60",
						"f61",
						"f62",
						"f63",
						"f64",
						"f65",
						"f66",
						"f67",
						"f68",
						"f69",
						"f70",
						"f71",
						"f72",
						"f73",
						"f74",
						"f75",
						"f76",
						"f77",
						"f78",
						"f79",
						"f80",
						"f81",
						"f82",
						"f83",
						"f84",
						"f85",
						"f86",
						"f87",
						"f88",
						"f89",
						"f90",
						"f91",
						"f92",
						"f93",
						"f94",
						"f95",
						"f96",
						"f97",
						"f98",
						"f99",
						"f100",
						"f101",
						"f102",
						"f103",
						"f104",
						"f105",
						"f106",
						"f107",
						"f108",
						"f109",
						"f110",
						"f111",
						"f112",
						"f113",
						"f114",
						"f115",
						"f116",
						"f117",
						"f118",
						"f119",
						"f120",
						"f121",
						"f122",
						"f123",
						"f124",
						"f125",
						"f126",
						"f127",
						"f128",
						"f129",
						"f130",
						"f131",
						"f132",
						"f133",
						"f134",
						"f135",
						"f136",
						"f137",
						"f138",
						"f139",
						"f140",
						"f141",
						"f142",
						"f143",
						"f144",
						"f145",
						"f146",
						"f147",
						"f148",
						"f149",
						"f150",
						"f151",
						"f152",
						"f153",
						"f154",
						"f155",
						"f156",
						"f157",
						"f158",
						"f159",
						"f160",
						"f161",
						"f162",
						"f163",
						"f164",
						"f165",
						"f166",
						"f167",
						"f168",
						"f169",
						"f170",
						"f171",
						"f172",
						"f173",
						"f174",
						"f175",
						"f176",
						"f177",
						"f178",
						"f179",
						"f180",
						"f181",
						"f182",
						"f183",
						"f184",
						"f185",
						"f186",
						"f187",
						"f188",
						"f189",
						"f190",
						"f191",
						"f192",
						"f193",
						"f194",
						"f195",
						"f196",
						"f197",
						"f198",
						"f199",
						"f200",
						"f201",
						"f202",
						"f203",
						"f204",
						"f205",
						"f206",
						"f207",
						"f208",
						"f209",
						"f210",
						"f211",
						"f212",
						"f213",
						"f214",
						"f215",
						"f216",
						"f217",
						"f218",
						"f219",
						"f220",
						"f221",
						"f222",
						"f223",
						"f224",
						"f225",
						"f226",
						"f227",
						"f228",
						"f229",
						"f230",
						"f231",
						"f232",
						"f233",
						#"f234", #id field
						#"Cluster_Number"
						]
"""
						
# predictors for wordcount approach
# No isbn features
features_to_consider =  [#"f1",
						#"f2",
						#"f3",
						#"f4",
						#"f5",
						#"f6",
						#"f7",
						#"f8",
						#"f9",
						#"f10",
						#"f11",
						#"f12",
						#"f13",
						#"f14",
						#"f15",
						"f16",
						"f17",
						"f18",
						"f19",
						"f20",
						"f21",
						"f22",
						"f23",
						"f24",
						"f25",
						"f26",
						"f27",
						"f28",
						"f29",
						"f30",
						"f31",
						"f32",
						"f33",
						"f34",
						"f35",
						"f36",
						"f37",
						"f38",
						"f39",
						"f40",
						"f41",
						"f42",
						"f43",
						"f44",
						"f45",
						"f46",
						"f47",
						"f48",
						"f49",
						"f50",
						"f51",
						"f52",
						"f53",
						"f54",
						"f55",
						"f56",
						"f57",
						"f58",
						"f59",
						"f60",
						"f61",
						"f62",
						"f63",
						"f64",
						"f65",
						"f66",
						"f67",
						"f68",
						"f69",
						"f70",
						"f71",
						"f72",
						"f73",
						"f74",
						"f75",
						"f76",
						"f77",
						"f78",
						"f79",
						"f80",
						"f81",
						"f82",
						"f83",
						"f84",
						"f85",
						"f86",
						"f87",
						"f88",
						"f89",
						"f90",
						"f91",
						"f92",
						"f93",
						"f94",
						"f95",
						"f96",
						"f97",
						"f98",
						"f99",
						"f100",
						"f101",
						"f102",
						"f103",
						"f104",
						"f105",
						"f106",
						"f107",
						"f108",
						"f109",
						"f110",
						"f111",
						"f112",
						"f113",
						"f114",
						"f115",
						"f116",
						"f117",
						"f118",
						"f119",
						"f120",
						"f121",
						"f122",
						"f123",
						"f124",
						"f125",
						"f126",
						"f127",
						"f128",
						"f129",
						"f130",
						"f131",
						"f132",
						"f133",
						"f134",
						"f135",
						"f136",
						"f137",
						"f138",
						"f139",
						"f140",
						"f141",
						"f142",
						"f143",
						"f144",
						"f145",
						"f146",
						"f147",
						"f148",
						"f149",
						"f150",
						"f151",
						"f152",
						"f153",
						"f154",
						"f155",
						"f156",
						"f157",
						"f158",
						"f159",
						"f160",
						"f161",
						"f162",
						"f163",
						"f164",
						"f165",
						"f166",
						"f167",
						"f168",
						"f169",
						"f170",
						"f171",
						"f172",
						"f173",
						"f174",
						"f175",
						"f176",
						"f177",
						"f178",
						"f179",
						"f180",
						"f181",
						"f182",
						"f183",
						"f184",
						"f185",
						"f186",
						"f187",
						"f188",
						"f189",
						"f190",
						"f191",
						"f192",
						"f193",
						"f194",
						"f195",
						"f196",
						"f197",
						"f198",
						"f199",
						"f200",
						"f201",
						"f202",
						"f203",
						"f204",
						"f205",
						"f206",
						"f207",
						"f208",
						"f209",
						"f210",
						"f211",
						"f212",
						"f213"
						]


# predictors for tf-idf file
"""				
features_to_consider =  [#"00_OCLCCN",
						"01_isbn",
						"02_isbn_pubname",
						"03_isbn_countryname",
						"04_lccn",
						"10_title",
						"11_statement_of_responsibility",
						"12_publisher_place",
						"13_publisher_name",
						"14_publication_date",
						"15_content_code",
						"16_content_type_term",
						"17_content_source",
						"18_media_code",
						"19_media_type_term",
						"20_media_source",
						"21_carrier_code",
						"22_topical_term",
						"23_form_subdivision",
						"24_heading_source",
						"25_authority_record_control_num",
						"26_geographical_subdivision",
						"27_geo_name",
						"28_geo_source_of_headingwterm",
						"29_geo_arn",
						"2_physical_desc",
						"30_genre",
						"31_host_item",
						"32_series_title",
						"33_series_volume",
						"34_form_data",
						"35_source_of_term",
						"36_index_arn",
						"3_place",
						"4_language",
						"5_catalogue_source",
						"8_personal_name",
						"9_relation",
						#"id",
						#"Cluster_Number"
						]
"""
					
# predictor
X = feature_file[features_to_consider]
# outcome
Y =	feature_file[['Cluster_Number']]				

sum3 = sum5 = sum7 = 0
avg3 = avg5 = avg7 = 0.0

for i in range(1,11):
	print("----------------------------------")
	print("Iteration:" + str(i))
	print("----------------------------------")
	# data split: 70% train, 30$ test
	# randomly assign 70% of the data to training, and 30% of the data for testing
	X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.3)
	
	# Printing the dataframes to identify the index of test instances
	X_test.to_csv("X_test.csv", sep=',', encoding='utf-8')	
	Y_test.to_csv("Y_test.csv", sep=',', encoding='utf-8')	
		
	# kNN model with n_neighbors = 3
	classifier3 = KNeighborsClassifier(n_neighbors = 3)
	classifier3.fit(X_train, Y_train.values.ravel())

	print("\nUsing n_neighbors = 3:")
	prediction3 = classifier3.predict(X_test)
	correct3 = np.sum(np.where(prediction3 == Y_test.values.ravel(),1,0))
	print("Number of correct predictions with kNN =", correct3)

	accuracy3 = correct3/len(Y_test)
	print("Accuracy of kNN model =", accuracy3)
	sum3 = sum3 + accuracy3
	
	# kNN model with n_neighbors = 5
	classifier5 = KNeighborsClassifier(n_neighbors = 5)
	classifier5.fit(X_train, Y_train.values.ravel())

	print("\nUsing n_neighbors = 5:")
	prediction5 = classifier5.predict(X_test)
	correct5 = np.sum(np.where(prediction5 == Y_test.values.ravel(),1,0))
	print("Number of correct predictions with kNN =", correct5)

	accuracy5 = correct5/len(Y_test)
	print("Accuracy of kNN model =", accuracy5)
	sum5 = sum5 + accuracy5
	
	# kNN model with n_neighbors = 7
	classifier7 = KNeighborsClassifier(n_neighbors = 7)
	classifier7.fit(X_train, Y_train.values.ravel())

	print("\nUsing n_neighbors = 7:")

	prediction7 = classifier7.predict(X_test)
	correct7 = np.sum(np.where(prediction7 == Y_test.values.ravel(),1,0))
	print("Number of correct predictions with kNN =", correct7)

	accuracy7 = correct7/len(Y_test)
	print("Accuracy of kNN model =", accuracy7)
	sum7 = sum7 + accuracy7	

avg3 = str(sum3/10)	
avg5 = str(sum5/10)
avg7 = str(sum7/10)
with open(output_prediction_file, "w", newline = '') as f:
	for p in prediction7:
		f.write(str(p)+"\n") 
	f.write(avg3+ "\n")
	f.write(avg5+ "\n")
	f.write(avg7+ "\n")			
f.close()	
