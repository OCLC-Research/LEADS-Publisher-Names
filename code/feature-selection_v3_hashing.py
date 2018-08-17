# Feature Extraction with Univariate Statistical Tests (Chi-squared for classification)
import pandas as pd
import numpy as np
from pandas import read_csv
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.feature_selection import RFE, f_regression
from sklearn.linear_model import LogisticRegression, LinearRegression, Ridge, Lasso, RandomizedLasso
from sklearn.decomposition import PCA
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
import csv


def evaluate_features_tree(total_features, feature_table, names_hashingfile, topk, X, Y):
	# feature extraction
	model = ExtraTreesClassifier()
	model.fit(X, Y)
	#print(model.feature_importances_)
	
	listf = model.feature_importances_
	
	for i in np.argsort(listf)[::-1][-topk:]:
		print(get_feature(feature_table, str(i+1)))


def rank_to_dict(ranks, names, order=1):
    minmax = MinMaxScaler()
    ranks = minmax.fit_transform(order * np.array([ranks]).T).T[0]
    ranks = map(lambda x: round(x, 2), ranks)
    return dict(zip(names, ranks ))
 
			
if __name__ == '__main__':
	# load data
	filename = "numeric-features-hashing.csv"
	#filename = "numeric-features-hashing-nostop.csv"
	dataframe = pd.read_csv(filename, dtype=float)
	array = dataframe.values
	
	names_hashingfile = [#"ft_00_OCLCCN",
					"ft_01_isbn",
					"ft_01_isbn",
					"ft_01_isbn",
					"ft_01_isbn",
					"ft_01_isbn",
					"ft_02_isbn_pubname",
					"ft_02_isbn_pubname",
					"ft_02_isbn_pubname",
					"ft_02_isbn_pubname",
					"ft_02_isbn_pubname",
					"ft_03_isbn_countryname",
					"ft_03_isbn_countryname",
					"ft_03_isbn_countryname",
					"ft_03_isbn_countryname",
					"ft_03_isbn_countryname",
					"ft_04_lccn",
					"ft_10_title",
					"ft_10_title",
					"ft_10_title",
					"ft_10_title",
					"ft_10_title",
					"ft_10_title",
					"ft_10_title",
					"ft_10_title",
					"ft_10_title",
					"ft_10_title",
					"ft_10_title",
					"ft_10_title",
					"ft_10_title",
					"ft_10_title",
					"ft_10_title",
					"ft_10_title",
					"ft_10_title",
					"ft_10_title",
					"ft_10_title",
					"ft_10_title",
					"ft_11_statement_of_responsibility",
					"ft_11_statement_of_responsibility",
					"ft_11_statement_of_responsibility",
					"ft_11_statement_of_responsibility",
					"ft_11_statement_of_responsibility",
					"ft_12_publisher_place",
					"ft_12_publisher_place",
					"ft_12_publisher_place",
					"ft_12_publisher_place",
					"ft_12_publisher_place",
					"ft_12_publisher_place",
					"ft_12_publisher_place",
					"ft_12_publisher_place",
					"ft_12_publisher_place",
					"ft_12_publisher_place",
					"ft_12_publisher_place",
					"ft_12_publisher_place",
					"ft_12_publisher_place",
					"ft_12_publisher_place",
					"ft_12_publisher_place",
					"ft_12_publisher_place",
					"ft_12_publisher_place",
					"ft_12_publisher_place",
					"ft_12_publisher_place",
					"ft_12_publisher_place",
					"ft_13_publisher_name",
					"ft_13_publisher_name",
					"ft_13_publisher_name",
					"ft_13_publisher_name",
					"ft_13_publisher_name",
					"ft_13_publisher_name",
					"ft_13_publisher_name",
					"ft_13_publisher_name",
					"ft_13_publisher_name",
					"ft_13_publisher_name",
					"ft_13_publisher_name",
					"ft_13_publisher_name",
					"ft_13_publisher_name",
					"ft_13_publisher_name",
					"ft_13_publisher_name",
					"ft_13_publisher_name",
					"ft_13_publisher_name",
					"ft_13_publisher_name",
					"ft_13_publisher_name",
					"ft_13_publisher_name",
					"ft_13_publisher_name",
					"ft_13_publisher_name",
					"ft_13_publisher_name",
					"ft_13_publisher_name",
					"ft_13_publisher_name",
					"ft_13_publisher_name",
					"ft_13_publisher_name",
					"ft_13_publisher_name",
					"ft_13_publisher_name",
					"ft_13_publisher_name",
					"ft_14_publication_date",
					"ft_15_content_code",
					"ft_15_content_code",
					"ft_15_content_code",
					"ft_15_content_code",
					"ft_15_content_code",
					"ft_16_content_type_term",
					"ft_16_content_type_term",
					"ft_16_content_type_term",
					"ft_16_content_type_term",
					"ft_16_content_type_term",
					"ft_17_content_source",
					"ft_17_content_source",
					"ft_17_content_source",
					"ft_17_content_source",
					"ft_17_content_source",
					"ft_18_media_code",
					"ft_18_media_code",
					"ft_18_media_code",
					"ft_18_media_code",
					"ft_18_media_code",
					"ft_19_media_type_term",
					"ft_19_media_type_term",
					"ft_19_media_type_term",
					"ft_19_media_type_term",
					"ft_19_media_type_term",
					"ft_20_media_source",
					"ft_20_media_source",
					"ft_20_media_source",
					"ft_20_media_source",
					"ft_20_media_source",
					"ft_21_carrier_code",
					"ft_21_carrier_code",
					"ft_21_carrier_code",
					"ft_21_carrier_code",
					"ft_21_carrier_code",
					"ft_22_topical_term",
					"ft_22_topical_term",
					"ft_22_topical_term",
					"ft_22_topical_term",
					"ft_22_topical_term",
					"ft_23_form_subdivision",
					"ft_23_form_subdivision",
					"ft_23_form_subdivision",
					"ft_23_form_subdivision",
					"ft_23_form_subdivision",
					"ft_24_heading_source",
					"ft_24_heading_source",
					"ft_24_heading_source",
					"ft_24_heading_source",
					"ft_24_heading_source",
					"ft_25_authority_record_control_num",
					"ft_25_authority_record_control_num",
					"ft_25_authority_record_control_num",
					"ft_25_authority_record_control_num",
					"ft_25_authority_record_control_num",
					"ft_26_geographical_subdivision",
					"ft_26_geographical_subdivision",
					"ft_26_geographical_subdivision",
					"ft_26_geographical_subdivision",
					"ft_26_geographical_subdivision",
					"ft_27_geo_name",
					"ft_27_geo_name",
					"ft_27_geo_name",
					"ft_27_geo_name",
					"ft_27_geo_name",
					"ft_28_geo_source_of_headingwterm",
					"ft_28_geo_source_of_headingwterm",
					"ft_28_geo_source_of_headingwterm",
					"ft_28_geo_source_of_headingwterm",
					"ft_28_geo_source_of_headingwterm",
					"ft_29_geo_arn",
					"ft_29_geo_arn",
					"ft_29_geo_arn",
					"ft_29_geo_arn",
					"ft_29_geo_arn",
					"ft_2_physical_desc",
					"ft_2_physical_desc",
					"ft_2_physical_desc",
					"ft_2_physical_desc",
					"ft_2_physical_desc",
					"ft_30_genre",
					"ft_30_genre",
					"ft_30_genre",
					"ft_30_genre",
					"ft_30_genre",
					"ft_31_host_item",
					"ft_31_host_item",
					"ft_31_host_item",
					"ft_31_host_item",
					"ft_31_host_item",
					"ft_32_series_title",
					"ft_32_series_title",
					"ft_32_series_title",
					"ft_32_series_title",
					"ft_32_series_title",
					"ft_33_series_volume",
					"ft_33_series_volume",
					"ft_33_series_volume",
					"ft_33_series_volume",
					"ft_33_series_volume",
					"ft_34_form_data",
					"ft_34_form_data",
					"ft_34_form_data",
					"ft_34_form_data",
					"ft_34_form_data",
					"ft_35_source_of_term",
					"ft_35_source_of_term",
					"ft_35_source_of_term",
					"ft_35_source_of_term",
					"ft_35_source_of_term",
					"ft_36_index_arn",
					"ft_36_index_arn",
					"ft_36_index_arn",
					"ft_36_index_arn",
					"ft_36_index_arn",
					"ft_3_place",
					"ft_3_place",
					"ft_3_place",
					"ft_3_place",
					"ft_3_place",
					"ft_4_language",
					"ft_4_language",
					"ft_4_language",
					"ft_4_language",
					"ft_4_language",
					"ft_5_catalogue_source",
					"ft_5_catalogue_source",
					"ft_5_catalogue_source",
					"ft_5_catalogue_source",
					"ft_5_catalogue_source",
					"ft_8_personal_name",
					"ft_8_personal_name",
					"ft_8_personal_name",
					"ft_8_personal_name",
					"ft_8_personal_name",
					"ft_9_relation",
					"ft_9_relation",
					"ft_9_relation",
					"ft_9_relation",
					"ft_9_relation"]
	
	X = array[:,1:233]
	Y = array[:,234]
	
	topk = 15
	total_features = 232

	ranks = {}
	
	"""
	Linear Regression model
	"""
	lr = LinearRegression(normalize=True)
	lr.fit(X, Y)
	ranks["Linear reg"] = rank_to_dict(np.abs(lr.coef_), names_hashingfile)
	 
	"""
	L2 regularization (called ridge regression for linear regression) adds the L2 norm penalty (α∑ni=1w2i) to the loss function.
	Since the coefficients are squared in the penalty expression, Ridge regression forces regressions coefficients to spread out 
	similarly between correlated variables. It is useful for feature interpretation: a predictive feature will get a non-zero 
	coefficient.
	"""	
	ridge = Ridge(alpha=7)
	ridge.fit(X, Y)
	ranks["Ridge"] = rank_to_dict(np.abs(ridge.coef_), names_hashingfile)
	 
	"""
	Lasso picks out the top performing features, while forcing other features to be close to zero. 
	It is useful when reducing the number of features is required.
	"""
	lasso = Lasso(alpha=.05)
	lasso.fit(X, Y)
	ranks["Lasso"] = rank_to_dict(np.abs(lasso.coef_), names_hashingfile)
	 
	"""
	Stability selection applies a feature selection algorithm on different subsets of data and with different subsets of features. 
	After repeating the process a number of times, the selection results can be aggregated, for example by checking how many times 
	a feature ended up being selected as important when it was in an inspected feature subset. We can expect strong features to have 
	scores close to 100%, since they are always selected when possible. Weaker, but still relevant features will also have non-zero 
	scores, since they would be selected when stronger features are not present in the currently selected subset, while irrelevant 
	features would have scores (close to) zero, since they would never be among selected features.
	"""
	rlasso = RandomizedLasso(alpha=0.04)
	rlasso.fit(X, Y)
	ranks["Stability"] = rank_to_dict(np.abs(rlasso.scores_), names_hashingfile)
	
	"""
	Recursive feature elimination is a greedy optimization based on the idea to repeatedly construct a model and choose either the 
	best or worst performing feature setting the feature aside and then repeating the process with the rest of the features.
	We have constructed the model using Linear Regression.
	"""
	rfe = RFE(lr, n_features_to_select=topk) #stop the search when topk features are left (they will get equal scores)
	rfe.fit(X,Y)
	ranks["RFE"] = rank_to_dict(list(map(float, rfe.ranking_)), names_hashingfile, order=-1)
	
	"""
	Random forest consists of a number of decision trees. Every node in the decision trees is a condition on a single feature, 
	designed to split the dataset into two so that similar response values end up in the same set. 	Random forest’s impurity based 
	ranking is typically aggressive in the sense that there is a sharp drop-off of scores after the first few top ones. 
	Tree based methods can model non-linear relations well and don’t require much tuning. 
	For a forest, the impurity decrease from each feature can be averaged and the features are ranked according to this measure.
	"""
	rf = RandomForestRegressor()
	rf.fit(X,Y)
	ranks["RF"] = rank_to_dict(rf.feature_importances_, names_hashingfile)
	
	"""
	Selecting the k-best features
	"""
	kbest = SelectKBest(chi2, total_features) #using all the features for analysis
	kbest.fit(X, Y)
	#print(np.abs(kbest.scores_))
	ranks["KBest"] = rank_to_dict(np.nan_to_num(np.abs(kbest.scores_)), names_hashingfile)
	
	"""
	Another tree based classifier
	"""
	treec = ExtraTreesClassifier()
	treec.fit(X, Y)
	ranks["ExtraTrees"] = rank_to_dict(treec.feature_importances_, names_hashingfile)
	
	"""
	With linear correlation (Lin. corr.), each feature is evaluated independently, and we measure the linear relationship 
	between each feature and the response variable.
	"""
	f, pval  = f_regression(X, Y, center=True)
	ranks["Corr."] = rank_to_dict(np.nan_to_num(f), names_hashingfile)
	
	r = {}
	for name in names_hashingfile:
		r[name] = round(np.mean([ranks[method][name] for method in ranks.keys()]), 2)
	methods = sorted(ranks.keys())
	ranks["Mean"] = r
	methods.append("Mean")
	
	with open('feature-analysis-hashing.csv', "w", newline = '') as f:
	#with open('feature-analysis-hashing-nostop.csv', "w", newline = '') as f:
		fileheader = "\t%s" % "\t".join(methods)
		print(fileheader)
		
		fileheader = ",%s" % ",".join(methods)
		fileheader +="\n"
		
		f.write(fileheader)
		for name in names_hashingfile:
			line = "%s\t%s" % (name, "\t".join(map(str, [ranks[method][name] for method in methods])))
			print(line)
			
			line = "%s,%s" % (name, ",".join(map(str, [ranks[method][name] for method in methods])))
			line +="\n"
			f.write(line) 
	f.close()
	
	
	
	
	