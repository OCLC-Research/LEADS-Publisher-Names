import pandas as pd
import string 
import re 

def read_file(filename):
	df = pd.read_csv(filename, encoding = "ISO-8859-1", header=0)
	return df
	

def write_CSV_output(features, folder="", filename="default_output.csv"):
	path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 
		(folder + '\\' + filename))
	df = pd.DataFrame(features)
	df.to_csv(path, index=False, index_label=False)

def fetch_data(df, feature_name):
	feature_corpus = df[feature_name].values
	return feature_corpus
	
def fetch_labels(df):
	cluster_names = df['Cluster Name'].values
	return cluster_names
	
def clean_data(text):
	list = ['fst', 'ocolc']
	text = text.strip().lower()
	for i in list:
		text = text.replace(i,'')
	#text = ''.join(e + '' for e in text if e.isalnum())
	text = text.translate(str.maketrans('','',string.punctuation))
	text = re.sub(r"[^a-zA-Z0-9]+", ' ', text)
	return text.strip()
	
if __name__ == '__main__':
	print(clean_data('1971, ©1968.'))
	