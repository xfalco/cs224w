
import pandas as pd
import numpy as np
import time

def load_data():

	df = pd.read_csv("network_python.csv")
	df['Net'] = df["EdgeAttrUpVotes"] - df["EdgeAttrDownVotes"]
	df['Rank'] = np.zeros(len(df))
	df['Weight'] = np.zeros(len(df))
	return df
	
def save_data():

	df.to_csv("network_python_processed.csv")
	return 
	
def rank_answers_to_question(question_id, df):

	answers = df.ix[df.ix[:,'EdgeAttrQuestionId'] == question_id, :]
	answers = answers.sort('Net', ascending = False)
	rank = range(len(answers)) + np.ones(len(answers))
	answers['Rank'] = rank
	answers['Weight'] = np.power (2, 1 - rank)
	df.ix[answers.index, 'Rank'] = answers['Rank']
	df.ix[answers.index, 'Weight'] = answers['Weight']

	return
	
df = load_data()

question_list = df["EdgeAttrQuestionId"].unique()

print "Total edges = ", len(df)
print "Total questions = ", len(question_list)
print "sample record ", df.ix[1]
t = time.time()
r = rm = rm_old = 0
for i in question_list:
	r += 1
# 	print "processing question ", i
 	a = rank_answers_to_question(i, df)
# 	print a.ix[:,['Net','Rank', 'Weight']]
	rm = r//1000
	if rm != rm_old:
		print rm * 1000
		rm_old = rm

	
		
print "\n Time : ", t - time.time()

save_data()