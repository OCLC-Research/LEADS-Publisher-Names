import os
import time
import nltk
import string
import array
import csv

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import text
import numpy as np
from scipy.sparse.csr import csr_matrix #need this if you want to save tfidf_matrix
from nltk.stem.porter import PorterStemmer

from input_output_v3 import read_file, fetch_data, fetch_labels

MAXDOCS = 1002

def generate_scores(corpus, mystopwords = []):
	scores = []
	
	stopwords = text.ENGLISH_STOP_WORDS.union(mystopwords)
	tf = TfidfVectorizer(analyzer='word', 
						strip_accents = 'unicode',
						ngram_range=(1,3),
						min_df = 0, 
						stop_words = stopwords, 
						sublinear_tf=True)
						
	tfidf_matrix =  tf.fit_transform(corpus.astype(str))
	
	feature_names = tf.get_feature_names()
	#print(feature_names)
	#print(len(feature_names))
	
	for doc in range(0, MAXDOCS):
		#print(doc)
		#doc = 4
		feature_index = tfidf_matrix[doc,:].nonzero()[1]
		tfidf_scores = zip(feature_index, [tfidf_matrix[doc, x] for x in feature_index])
		score = 0
		for w, s in [(feature_names[i], s) for (i, s) in tfidf_scores]:
			score = s 
			word = w
		#print (w, s)
		scores.append(score)
	return scores

if __name__ == '__main__':
	start_time = time.time()
	input_filename = 'features-new.csv'
	
	#read feature file
	df = read_file(input_filename)
	
	feature_list = ['00_OCLCCN',
					'01_isbn',
					'02_isbn_pubname',
					'03_isbn_countryname',
					'04_lccn',
					'10_title',
					'11_statement_of_responsibility',
					'12_publisher_place',
					'13_publisher_name',
					'14_publication_date',
					'15_content_code',
					'16_content_type_term',
					'17_content_source',
					'18_media_code',
					'19_media_type_term',
					'20_media_source',
					'21_carrier_code',
					'22_topical_term',
					'23_form_subdivision',
					'24_heading_source',
					'25_authority_record_control_num',
					'26_geographical_subdivision',
					'27_geo_name',
					'28_geo_source_of_headingwterm',
					'29_geo_arn',
					'2_physical_desc',
					'30_genre',
					'31_host_item',
					'32_series_title',
					'33_series_volume',
					'34_form_data',
					'35_source_of_term',
					'36_index_arn',
					'3_place',
					'4_language',
					'5_catalogue_source',
					'8_personal_name',
					'9_relation',
					'_id'
					]
	
	pname_stops = ["asociados", 'associate', "association", 
	"book", "books", 'classroom', 'communications', "company", "distributor", 'division', "editor", "editora",
	"editorial", "editores", 'group', 'groups', 'guild', 'organization', "print", 'press', "publishing", 
	"publications", 'pubs', "trust", "paperbacks"]
	
	i=0
	
	for f in feature_list:
		print(f)
		corpus_f = fetch_data(df, f)	
		#print(corpus_pname)
		"""
		Publisher name specific stopwords are not removed
		"""
		if (f == '13_publisher_name'):
			locals()["ft_"+str(f)] = generate_scores(corpus_f, [])
			#print("here:", f)
		elif (f == '00_OCLCCN'):
			locals()["ft_"+str(f)] = corpus_f
		elif (f == '_id'):
			locals()["ft_"+str(f)] = corpus_f
		#elif (f == '01_isbn' or f == '02_isbn_pubname' or f =='03_isbn_countryname' or f == '04_lccn'):
		#	locals()["ft_"+str(f)] = corpus_f
		else: 
			locals()["ft_"+str(f)] = generate_scores(corpus_f)	
		i=i+1
	
	rows = zip(	ft_00_OCLCCN,
				ft_01_isbn,
				ft_02_isbn_pubname,
				ft_03_isbn_countryname,
				ft_04_lccn,
				ft_10_title,
				ft_11_statement_of_responsibility,
				ft_12_publisher_place,
				ft_13_publisher_name,
				ft_14_publication_date,
				ft_15_content_code,
				ft_16_content_type_term,
				ft_17_content_source,
				ft_18_media_code,
				ft_19_media_type_term,
				ft_20_media_source,
				ft_21_carrier_code,
				ft_22_topical_term,
				ft_23_form_subdivision,
				ft_24_heading_source,
				ft_25_authority_record_control_num,
				ft_26_geographical_subdivision,
				ft_27_geo_name,
				ft_28_geo_source_of_headingwterm,
				ft_29_geo_arn,
				ft_2_physical_desc,
				ft_30_genre,
				ft_31_host_item,
				ft_32_series_title,
				ft_33_series_volume,
				ft_34_form_data,
				ft_35_source_of_term,
				ft_36_index_arn,
				ft_3_place,
				ft_4_language,
				ft_5_catalogue_source,
				ft_8_personal_name,
				ft_9_relation,
				ft__id) 
	
	with open('numeric-features-tfidf-nostop.csv', "w", newline = '') as f:
		writer = csv.writer(f)
		fnames = [				
				'00_OCLCCN',
				'01_isbn',
				'02_isbn_pubname',
				'03_isbn_countryname',
				'04_lccn',
				'10_title',
				'11_statement_of_responsibility',
				'12_publisher_place',
				'13_publisher_name',
				'14_publication_date',
				'15_content_code',
				'16_content_type_term',
				'17_content_source',
				'18_media_code',
				'19_media_type_term',
				'20_media_source',
				'21_carrier_code',
				'22_topical_term',
				'23_form_subdivision',
				'24_heading_source',
				'25_authority_record_control_num',
				'26_geographical_subdivision',
				'27_geo_name',
				'28_geo_source_of_headingwterm',
				'29_geo_arn',
				'2_physical_desc',
				'30_genre',
				'31_host_item',
				'32_series_title',
				'33_series_volume',
				'34_form_data',
				'35_source_of_term',
				'36_index_arn',
				'3_place',
				'4_language',
				'5_catalogue_source',
				'8_personal_name',
				'9_relation',
				'id']
		writer.writerow(fnames)
		for row in rows:
			#print(row)
			writer.writerow(row)
	elapsed_time = time.time() - start_time
	print("Elapsed Time: ", elapsed_time)