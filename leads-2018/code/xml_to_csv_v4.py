import os
import time
from xml.etree import ElementTree
import pandas as pd

from add_wikidata import create_dict_pname, create_dict_cname, get_value_from_dict
from input_output_v3 import clean_data

	
def feature_extraction(input_file):
	tree = ElementTree.parse(input_file)
	collection = tree.getroot()
	#print (root)

	pname_dict = create_dict_pname('ISBN-publishers.csv')	
	cname_dict = create_dict_cname('ISBN-countries.csv')	
	#print(cname_dict)
	features = [] #list of features 
	
	count = 0
	for record in collection:
		print("---------------------")
		row = {}
		count = count + 1
		
		row['_id'] = count
		#for item in record:
		#	print(item)
		
		leader = record.find('{http://www.loc.gov/MARC21/slim}leader')
		leader_type = leader.text[6]
		#print(leader_type)
		row['1_leader_type'] = clean_data(leader_type)
		
		control = record.findall('{http://www.loc.gov/MARC21/slim}controlfield')
		for c in control:
			tag = c.get('tag')
			#print(tag)
			
			if tag == '001':
				oclc_controlnum = c.text
				#print(physical_desc)
				row['00_OCLCCN'] = oclc_controlnum
			
			if tag == '007':
				physical_desc = c.text
				#print(physical_desc)
				row['2_physical_desc'] = physical_desc				
			
			if tag == '008':
				value = c.text
				#print(value)
				place = clean_data(value[15:17])
				language = clean_data(value[35:37])
				catalog_source = clean_data(value[39])
				#print(place, language, catalog_source)
				row['3_place'] = place
				row['4_language'] = language
				row['5_catalogue_source'] = catalog_source	
				
				if place is None:
					row['3_place'] = "NA"
				if language is None:
					row['4_language'] = "NA"
				if len(catalog_source) == 0:
					#print(catalog_source)
					row['5_catalogue_source'] = "NA"
				
		data = record.findall('{http://www.loc.gov/MARC21/slim}datafield')
		flag = 0
		#name=""
		#country_name=""
		for d in data:
			tag = d.get('tag')
			#print(tag)
			
			if tag == '010':
				#print(d)
				subfields = d.findall('{http://www.loc.gov/MARC21/slim}subfield')
				for s in subfields:
					if s.get('code') == 'a':
						lccn = s.text
						#print(lccn)
						row['04_lccn'] = lccn										
			
			if tag == '020' and flag != 1:
				#print(d)
				subfields = d.findall('{http://www.loc.gov/MARC21/slim}subfield')
				for s in subfields:
					if s.get('code') == 'a':
						isbn = s.text
						print(isbn)
						row['01_isbn'] = isbn
						
						length = len(isbn)
						if length==10:
							isbn_name_code = int(isbn[1:3])
							#print("10D:",isbn_name_code)
							
							key = isbn[1:3]
							name = get_value_from_dict(pname_dict, key)
							
							if name is None:
								key = isbn[1:4]
								name = get_value_from_dict(pname_dict, key)
							if name is None:
								key = isbn[1:5]
								name = get_value_from_dict(pname_dict, key)	
							if name is None:
								key = isbn[1:6]
								name = get_value_from_dict(pname_dict, key)	
							if name is None:
								key = isbn[1:7]
								name = get_value_from_dict(pname_dict, key)	
							if name is None:
								key = isbn[1:8]
								name = get_value_from_dict(pname_dict, key)	
							#print(name)
							
						else:
							isbn_name_code = int(isbn[3:5])
							#print("13D:",isbn_name_code)
							
							key = isbn[3:5]
							name = get_value_from_dict(pname_dict, key)
							
							if name is None:
								key = isbn[3:6]
								name = get_value_from_dict(pname_dict, key)						
							if name is None:
								key = isbn[3:7]
								name = get_value_from_dict(pname_dict, key)							
							if name is None:
								key = isbn[3:8]
								name = get_value_from_dict(pname_dict, key)							
							if name is None:
								key = isbn[3:9]
								name = get_value_from_dict(pname_dict, key)							
							if name is None:
								key = isbn[3:10]
								name = get_value_from_dict(pname_dict, key)		
							#print(name)
						"""
						Change the stored value from publisher name to key
						"""	
						row['02_isbn_pubname'] = key 
						
						length = len(isbn)
						if length==10:
							isbn_country_code = isbn[0:1]
							#print("10D CC:", isbn_country_code)
							#print(cname_dict)
							country_name = get_value_from_dict(cname_dict, isbn_country_code)
							#print("CN", country_name)
							
							if country_name is None:
								isbn_country_code = isbn[0:2]
								country_name = get_value_from_dict(cname_dict, isbn_country_code)	
							if country_name is None:
								isbn_country_code = isbn[0:3]
								country_name = get_value_from_dict(cname_dict, isbn_country_code)	
							if country_name is None:
								isbn_country_code = isbn[0:4]
								country_name = get_value_from_dict(cname_dict, isbn_country_code)	
							if country_name is None:
								isbn_country_code = isbn[0:5]
								country_name = get_value_from_dict(cname_dict, isbn_country_code)	
							#print(isbn_country_code, country_name)
							
						else:
							isbn_country_code = isbn[3:5]
							#print("13D CC:", isbn_country_code)
							country_name = get_value_from_dict(cname_dict, isbn_country_code)
							#print("CN", country_name)
							if country_name is None:
								isbn_country_code = isbn[3:6]
								country_name = get_value_from_dict(cname_dict, isbn_country_code)	
							if country_name is None:
								isbn_country_code = isbn[3:7]
								country_name = get_value_from_dict(cname_dict, isbn_country_code)	
							if country_name is None:
								isbn_country_code = isbn[3:8]
								country_name = get_value_from_dict(cname_dict, isbn_country_code)	
							#print(isbn_country_code, country_name)
						
						#print(isbn_country_code, country_name)
						
						"""
						Change the stored value from country name to code
						"""
						
						row['03_isbn_countryname'] = country_name
												
						if name is not None:
							flag = 1
						
			
			if tag == '100':
				#print(d)
				subfields = d.findall('{http://www.loc.gov/MARC21/slim}subfield')
				for s in subfields:
					if s.get('code') == 'a':
						personal_name = clean_data(s.text)
						#print(personal_name)
						row['8_personal_name'] = personal_name
						
					if s.get('code') == '4':
						relation = clean_data(s.text)
						#print(relation)
						row['9_relation'] = relation
						
			if tag == '245':
				#print(d)
				subfields = d.findall('{http://www.loc.gov/MARC21/slim}subfield')
				for s in subfields:
					if s.get('code') == 'a':
						title = clean_data(s.text)
						#print(title)
						row['10_title'] = title
												
					if s.get('code') == 'c' :
						statement_of_responsibility = clean_data(s.text)
						#print(statement_of_responsibility)
						row['11_statement_of_responsibility'] = statement_of_responsibility
					
			if tag == '260':
				#print(d)
				subfields = d.findall('{http://www.loc.gov/MARC21/slim}subfield')
				for s in subfields:
					if s.get('code') == 'a':
						publisher_place = clean_data(s.text)
						#print(publisher_place)
						row['12_publisher_place'] = publisher_place
						
					if s.get('code') == 'b':
						publisher_name = clean_data(s.text)
						#print(publisher_name)
						row['13_publisher_name'] = publisher_name
						
					if s.get('code') == 'c':
						publication_date = clean_data(s.text)
						#print(publication_date)
						row['14_publication_date'] = publication_date
							
			if tag == '336':
				#print(d)
				subfields = d.findall('{http://www.loc.gov/MARC21/slim}subfield')
				for s in subfields:
					if s.get('code') == 'b':
						content_code = clean_data(s.text)
						#print(content_code)
						row['15_content_code'] = content_code
						
					if s.get('code') == 'a':
						content_type_term = clean_data(s.text)
						#print(content_type_term)
						row['16_content_type_term'] = content_type_term
						
					if s.get('code') == '2':
						content_source = clean_data(s.text)
						#print(source)
						row['17_content_source'] = content_source
						
			if tag == '337':
				#print(d)
				subfields = d.findall('{http://www.loc.gov/MARC21/slim}subfield')
				for s in subfields:
					if s.get('code') == 'b':
						media_code = clean_data(s.text)
						#print(media_code)
						row['18_media_code'] = media_code
						
					if s.get('code') == 'a':
						media_type_term = clean_data(s.text)
						#print(media_type_term)
						row['19_media_type_term'] = media_type_term
							
					if s.get('code') == '2':
						media_source = clean_data(s.text)
						#print(media_source)
						row['20_media_source'] = media_source
						
			if tag == '338':
				#print(d)
				subfields = d.findall('{http://www.loc.gov/MARC21/slim}subfield')
				for s in subfields:
					if s.get('code') == 'b':
						carrier_code = clean_data(s.text)
						#print(carrier_code)
						row['21_carrier_code'] = carrier_code
						
			if tag == '650':
				#print(d)
				subfields = d.findall('{http://www.loc.gov/MARC21/slim}subfield')
				for s in subfields:
					if s.get('code') == 'a':
						topical_term = clean_data(s.text)
						#print(topical_term)
						row['22_topical_term'] = topical_term
						
					if s.get('code') == 'v':
						form_subdivision = clean_data(s.text)
						#print(form_subdivision)
						row['23_form_subdivision'] = form_subdivision
						
					if s.get('code') == '2':
						heading_source = clean_data(s.text)
						#print(heading_source)
						row['24_heading_source'] = heading_source
						
					if s.get('code') == '0':
						authority_record_control_num = clean_data(s.text)
						#print(authority_record_control_num)
						row['25_authority_record_control_num'] = authority_record_control_num
						
					if s.get('code') == 'z':
						geographical_subdivision = clean_data(s.text)
						#print(geographical_subdivision)
						row['26_geographical_subdivision'] = geographical_subdivision
						
			if tag == '651':
				#print(d)
				subfields = d.findall('{http://www.loc.gov/MARC21/slim}subfield')
				for s in subfields:
					if s.get('code') == 'a':
						geo_name = clean_data(s.text)
						#print(geo_name)
						row['27_geo_name'] = geo_name
						
					if s.get('code') == '2':
						geo_source_of_headingwterm = clean_data(s.text)
						#print(source_of_headingwterm)
						row['28_geo_source_of_headingwterm'] = geo_source_of_headingwterm
						
					if s.get('code') == '0':
						geo_arn = clean_data(s.text)
						#print(geo_arn)
						row['29_geo_arn'] = geo_arn
						
			if tag == '652': #i think this is not working. the tag number is not present for any instance
				#print(d)
				subfields = d.findall('{http://www.loc.gov/MARC21/slim}subfield')
				for s in subfields:
					if s.get('code') == 'b':
						genre = clean_data(s.text)
						#print(genre)
						row['30_genre'] = genre
						
			if tag == '773':
				#print(d)
				subfields = d.findall('{http://www.loc.gov/MARC21/slim}subfield')
				for s in subfields:
					if s.get('code') == 't':
						host_item = clean_data(s.text)
						#print(host_item)
						row['31_host_item'] = host_item
						
			if tag == '830':
				#print(d)
				subfields = d.findall('{http://www.loc.gov/MARC21/slim}subfield')
				for s in subfields:
					if s.get('code') == 'a':
						series_title = clean_data(s.text)
						#print(series_title)
						row['32_series_title'] = series_title
						
					if s.get('code') == 'v':
						series_volume = clean_data(s.text)
						#print(series_volume)
						row['33_series_volume'] = series_volume
                        
			if tag == '655':
				#print(d)
				subfields = d.findall('{http://www.loc.gov/MARC21/slim}subfield')
				for s in subfields:
					if s.get('code') == 'a':
						form_data = clean_data(s.text)
						#print(form_data)
						row['34_form_data'] = form_data
						
					if s.get('code') == '2':
						source_of_term = clean_data(s.text)
						row['35_source_of_term'] = source_of_term
						
					if s.get('code') == '0':
						index_arn = clean_data(s.text)
						row['36_index_arn'] = index_arn
						
			#print(code)
			#print(value)
			
		"""
		Handling blank fields
		"""
		if '00_OCLCCN' not in row:
			row['00_OCLCCN'] = 0
		if '2_physical_desc' not in row:
			row['2_physical_desc'] = "NA"
		if '3_place' not in row:
			row['3_place'] = "NA"
		if '4_language' not in row:
			row['4_language'] = "NA"
		if '5_catalogue_source' not in row:
			row['5_catalogue_source'] = "NA"	
		if '01_isbn' not in row:
			row['01_isbn'] = "00"
		if '02_isbn_pubname' not in row:
			row['02_isbn_pubname'] = "NA"
		if '03_isbn_countryname' not in row:
			row['03_isbn_countryname'] = "NA"
		if '04_lccn' not in row:
			row['04_lccn'] = "NA"
		if '8_personal_name' not in row:
			row['8_personal_name'] = "NA"
		if '9_relation' not in row:
			row['9_relation'] = "NA"
		if '10_title' not in row:
			row['10_title'] = "NA"
		if '11_statement_of_responsibility' not in row:
			row['11_statement_of_responsibility'] = "NA"
		if '12_publisher_place' not in row:
			row['12_publisher_place'] = "NA"
		if '13_publisher_name' not in row:
			row['13_publisher_name'] = "NA"
		if '14_publication_date' not in row:
			row['14_publication_date'] = "0000"
		if '15_content_code' not in row:
			row['15_content_code'] = "NA"
		if '16_content_type_term' not in row:
			row['16_content_type_term'] = "NA"
		if '17_content_source' not in row:
			row['17_content_source'] = "NA"
		if '18_media_code' not in row:
			row['18_media_code'] = "NA"
		if '19_media_type_term' not in row:
			row['19_media_type_term'] = "NA"
		if '20_media_source' not in row:
			row['20_media_source'] = "NA"
		if '21_carrier_code' not in row:
			row['21_carrier_code'] = "NA"
		if '22_topical_term' not in row:
			row['22_topical_term'] = "NA"
		if '23_form_subdivision' not in row:
			row['23_form_subdivision'] = "NA"
		if '24_heading_source' not in row:
			row['24_heading_source'] = "NA"
		if '25_authority_record_control_num' not in row:
			row['25_authority_record_control_num'] = "NA"
		if '26_geographical_subdivision' not in row:
			row['26_geographical_subdivision'] = "NA"
		if '27_geo_name' not in row:
			row['27_geo_name'] = "NA"
		if '28_geo_source_of_headingwterm' not in row:
			row['28_geo_source_of_headingwterm'] = "NA"	
		if '29_geo_arn' is None:
			row['29_geo_arn'] = "NA"
		if '30_genre' not in row:
			row['30_genre'] = "NA"
		if '31_host_item' not in row:
			row['31_host_item'] = "NA"
		if '32_series_title' not in row:
			row['32_series_title'] = "NA"
		if '33_series_volume' not in row:
			row['33_series_volume'] = "NA"
		if '34_form_data' not in row:
			row['34_form_data'] = "NA"
		if '35_source_of_term' not in row:
			row['35_source_of_term'] = "NA"
		if '36_index_arn' not in row:
			row['36_index_arn'] = "NA"
               							
		features.append(row)
		#if count == 10:
		#	break 
	return features

def write_CSV_output(features, folder, filename):
	path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 
		(folder + '\\' + filename))
	df = pd.DataFrame(features)
	df.to_csv(path, index=False, index_label=False)
		
	
if __name__ == '__main__':
	start_time = time.time()
	input_filename = 'marc.xml'
	
	#extract features 
	features = feature_extraction(input_filename)
	write_CSV_output(features, "Output", "features-new.csv")
	
	elapsed_time = time.time() - start_time
	print("Elapsed Time: ", elapsed_time)