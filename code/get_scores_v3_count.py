import os
import time
import nltk
import string
import array
import csv

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction import text
import numpy as np
from scipy.sparse.csr import csr_matrix #need this if you want to save matrix
from nltk.stem.porter import PorterStemmer

from input_output_v3 import read_file, fetch_data, fetch_labels

MAXDOCS = 1002
sum = 1

def generate_scores(corpus, mystopwords = [], num_of_f = 5):
	flag = 0
	global sum
	if not isinstance(corpus, str):
		corpus = corpus.astype(str)
	scores_row = []
	
	stopwords = text.ENGLISH_STOP_WORDS.union(mystopwords)
	vectorizer = CountVectorizer(analyzer='word', 
						strip_accents = 'unicode',
						ngram_range=(1,3),
						max_features = num_of_f,
						stop_words = stopwords)
						
		
	# The corpus is the collection of all the rows in the input file.
	# Each row represents a document 
	# The value stored in each row is the feature string, e.g., publisher name 
	# The corpus contains all possible values for that feature string in the collection.
	
	for document in corpus:
		#print(document)
		document = [document]
		score_matrix =  vectorizer.fit_transform(corpus.astype(str))
		score = vectorizer.transform(document)
		#print(type(score))
		
		sc = score.tocsr()[0,:].A
		sc = sc.flatten().tolist()
		
		if flag==0:
			sum = sum + len(sc)
			print(sum)
			flag =1
		#print(type(sc))
		#print(sc)
		#print(score)
		#print(score.shape)
		#print(score.toarray())
		scores_row.append(sc)
	return scores_row
	
if __name__ == '__main__':
	start_time = time.time()
	input_filename = 'features-new.csv'
	
	#read the feature file and return a data frame
	df = read_file(input_filename)
	
	# the list of features in the feature file
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
	
	# Dedicated list of stop words for publisher names
	pname_stops = ["asociados", 'associate', "association", 
	"book", "books", 'classroom', 'communications', "company", "distributor", 'division', "editor", "editora",
	"editorial", "editores", 'group', 'groups', 'guild', 'organization', "print", 'press', "publishing", 
	"publications", 'pubs', "trust", "paperbacks"]
	
	i=0
	
	for f in feature_list:
		print(f)
		
		# each corpus is a specific column of the feature file 
		# with the values collected for all rows 
		
		corpus_f = fetch_data(df, f)	
		#print(corpus_pname)
		
		"""
		Publisher name specific stopwords are not removed
		"""
		
		if (f == '13_publisher_name'):
			locals()["ft_"+str(f)] = generate_scores(corpus_f, [], 30)
		
		elif (f == '00_OCLCCN' or f == '_id'):
			locals()["ft_"+str(f)] = corpus_f
		
		elif (f == '14_publication_date' or f == '04_lccn'):
			locals()["ft_"+str(f)] = generate_scores(corpus_f,[],1)	
				
		elif (f == '12_publisher_place' or f == '10_title'):
			locals()["ft_"+str(f)] = generate_scores(corpus_f, [] ,20)	
			
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
	
	with open('numeric-features-cv.csv', "w", newline = '') as f:
		writer = csv.writer(f)
		"""
		1		ft_00_OCLCCN,
		2-6		ft_01_isbn,
		7-11	ft_02_isbn_pubname,
		12-16	ft_03_isbn_countryname,
		17		ft_04_lccn,
		18-37	ft_10_title,
		38-42	ft_11_statement_of_responsibility,
		43-62	ft_12_publisher_place,
		63-92	ft_13_publisher_name,
		93		ft_14_publication_date,
		94-98	ft_15_content_code,
		99-103	ft_16_content_type_term,
		104-108	ft_17_content_source,
		109-113	ft_18_media_code,
		114-118	ft_19_media_type_term,
		119-123	ft_20_media_source,
		124-128	ft_21_carrier_code,
		129-133	ft_22_topical_term,
		134-138	ft_23_form_subdivision,
		139-143	ft_24_heading_source,
		144-148	ft_25_authority_record_control_num,
		149-153	ft_26_geographical_subdivision,
		154-158	ft_27_geo_name,
		159-163	ft_28_geo_source_of_headingwterm,
		164-168	ft_29_geo_arn,
		169-173	ft_2_physical_desc,
		174-178	ft_30_genre,
		179-183	ft_31_host_item,
		184-188	ft_32_series_title,
		189-193	ft_33_series_volume,
		194-198	ft_34_form_data,
		199-203	ft_35_source_of_term,
		204-208	ft_36_index_arn,
		209-213	ft_3_place,
		214-218	ft_4_language,
		219-223	ft_5_catalogue_source,
		224-228	ft_8_personal_name,
		229-233	ft_9_relation,
		234	ft__id
		235 cluster_number
		"""
		
		for row in rows:
			#print(row)
			expanded_row=[]
			for feature in row:
				if isinstance(feature, list):
					for element in feature:
						expanded_row.append(element)
				else:
					expanded_row.append(feature)
			writer.writerow(expanded_row)
			
		#print(expanded_row)
	elapsed_time = time.time() - start_time
	print("Elapsed Time: ", elapsed_time)