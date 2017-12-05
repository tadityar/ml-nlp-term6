from collections import Counter
import copy
from viterbi import Viterbi
from forward_backward import ForwardBackward
from fractions import Fraction
from posterior_viterbi import PosteriorViterbi
from parser import Processor


'''
Part 2
'''

#Given a certain testing data set inp and a model generated from process_unknown_words, classifies all words not found in the model as #UNK#
def process_unknown_words_testing(inp,model):
	output = copy.deepcopy(inp)
	for i in range(len(output)):
		for j in range(len(output[i])):
			for key in output[i][j]:
				present = False
				if model.get(key):
					present = key
				output[i][j] = {present : None} if present else {'#UNK#' : None}
	return output

def emission_param_preprocess(data):
	wordAndTag = {}
	for wordset in data:
		highestVal = 0
		for tag in data[wordset]:
			value = data[wordset][tag]
			if value>highestVal:
				highestVal = value
				highestTag = tag
		wordAndTag.update({wordset:highestTag})
	return wordAndTag

#parser creates [[{word:None},{word:None}],[{word:None},{word:None}]], separating sentences. 
#parser requires that you end with 2 newlines at the end of the file. (same as the dev.in)
def parser (filename):
	file = open(filename,'r', encoding = 'UTF-8')
	entiredata = []
	sentence = []

	for line in file:
		if line == "\n":
			entiredata.append(sentence)
			sentence = []
		else:
			line = line.rstrip()
			noneDict = {line:"None"}
			sentence.append(noneDict)
	file.close()
	return entiredata

#new tagging_words that works with the new parser above
#this needs to be reworked, to check if the word in  is inside wordAndTag and then 
def tagging_words(wordAndTag,entiredata):
	sentenceCounter = 0
	for sentence in entiredata:
		wordCounter = 0
		for wordDict in sentence:
			for word in wordDict:
				if word in wordAndTag:
					tag = wordAndTag.get(word)
					entiredata[sentenceCounter][wordCounter][word] = tag
				else:
					entiredata[sentenceCounter][wordCounter][word] = "None"
			wordCounter += 1
			# print ("wordCounter")
			# print (wordCounter)
		sentenceCounter += 1
		# print ("sentence")
		# print (sentenceCounter)
	return entiredata

def convert_back(p_data):
	line = ""
	output = ""
	for sentence in p_data:
		for dictionary in sentence:
			for key,value in dictionary.items():
				line = key+" "+ value + "\n"
				output = output + line
		output = output + "\n"
	return output
	
def output_file(data,fileName):
	file = open(fileName,"w", encoding = 'UTF-8')
	file.write(data)
	file.write('\n')
	file.close()
	
'''
Part 3
'''

##Writing a function to assign the viterbi output back to the seq
## that was passed in. v_out = [[tag,tag],[]] seq = [[{},{}],[{},{}]]
def v_result_parse(v_out,seq):
	sentenceCounter = 0
	for sentence in seq:
		wordCounter = 0
		for wordDict in sentence:
			for key in wordDict:
				wordDict[key] = v_out[sentenceCounter][wordCounter]
			wordCounter += 1
		sentenceCounter += 1
	return (seq)

## <<< RESULTS FOR PART 2 >>>>
	
#training	
# words_count, tag_count = Processor.parse_train(r'EN/train')
words_count, tag_count = Processor.parse_tag(r'EN/train')
print(words_count)
print(tag_count)
# words_count = Processor.process_unknown_words(words_count,3)
# ep = Processor.get_emission_params(words_count, tag_count)
# data = parser(r'EN/dev.in')
# data_p = Processor.process_unknown_words_testing(data,words_count)
# ep_p = emission_param_preprocess(ep)
# tagged_words = tagging_words(ep_p,data_p)

#testing vs actual output
# output_to_file = convert_back(tagged_words)
# output_file(output_to_file,r'EN/dev.p2.out')


## <<< RESULTS FOR PART 3 >>>

# ### RUNNING VITERBI ###

def run_viterbi(fileTrain, fileIn, fileOut):
	words_count, tag_count = Processor.parse_train(fileTrain)
	words_count = Processor.process_unknown_words(words_count,3)
	ep = Processor.get_emission_params(words_count, tag_count)
	tp = Processor.get_transition_params(fileTrain)
	seq = parser(fileIn)
	v = Viterbi(tp,ep)
	v_out = []

	for s in seq:
		out = v.assign(s)
		v_out.append(out)

	v_seq = v_result_parse(v_out,seq)
	output_to_file = convert_back(v_seq)
	output_file(output_to_file,fileOut)
	print ("Viterbi done for "+ fileOut)

# run_viterbi(r'EN/train',r'EN/dev.in',r'EN/dev.p3.out')
# run_viterbi(r'FR/train',r'FR/dev.in',r'FR/dev.p3.out')
# run_viterbi(r'CN/train',r'CN/dev.in',r'CN/dev.p3.out')
# run_viterbi(r'SG/train',r'SG/dev.in',r'SG/dev.p3.out')
# run_viterbi(r'EN/train',r'test/EN/test.in',r'test/EN/dev.p3.out')
# run_viterbi(r'FR/train',r'test/FR/test.in',r'test/FR/dev.p3.out')
## <<< RESULTS FOR PART 4 >>>

# ### RUNNING FORWARDBACKWARD ###
def run_forwardbackward(fileTrain,fileIn,fileOut):
	words_count, tag_count = Processor.parse_train(fileTrain)
	words_count = Processor.process_unknown_words(words_count,3)
	ep = Processor.get_emission_params(words_count, tag_count)
	tp = Processor.get_transition_params(fileTrain)
	seq = parser(fileIn)

	v = ForwardBackward(tp,ep)
	v_out = []

	for s in seq:
		out = v.assign(s)
		v_out.append(out)

	v_seq = v_result_parse(v_out,seq)
	output_to_file = convert_back(v_seq)
	output_file(output_to_file,fileOut)
	print ("ForwardBackward done for "+ fileOut)

# run_forwardbackward(r'EN/train',r'EN/dev.in',r'EN/dev.p4.out')
# run_forwardbackward(r'FR/train',r'FR/dev.in',r'FR/dev.p4.out')
# run_forwardbackward(r'EN/train',r'test/EN/test.in',r'test/EN/dev.p4.out')
# run_forwardbackward(r'FR/train',r'test/FR/test.in',r'test/FR/dev.p4.out')


def run_posteriorviterbi(fileTrain, fileIn, fileOut):
	words_count, tag_count = Processor.parse_train(fileTrain)
	words_count = Processor.process_unknown_words(words_count,3)
	ep = Processor.get_emission_params(words_count, tag_count)
	tp = Processor.get_transition_params(fileTrain)
	seq = parser(fileIn)
	v = PosteriorViterbi(tp,ep)
	v_out = []

	for s in seq:
		out = v.assign(s)
		v_out.append(out)

	v_seq = v_result_parse(v_out,seq)
	output_to_file = convert_back(v_seq)
	output_file(output_to_file,fileOut)
	print ("PosteriorViterbi done for "+ fileOut)

# run_posteriorviterbi(r'EN/train',r'EN/dev.in',r'EN/dev.p5p.out')
# run_posteriorviterbi(r'FR/train',r'FR/dev.in',r'FR/dev.p5p.out')
# run_posteriorviterbi(r'test/EN/dev.p5.out',r'EN/dev.in',r'test/EN/dev.ptest1')
# run_posteriorviterbi(r'test/FR/dev.p5.out',r'FR/dev.in',r'test/FR/dev.ptest1')
# run_posteriorviterbi(r'test/EN/dev.p4.out',r'EN/dev.in',r'test/EN/dev.ptest2')
# run_posteriorviterbi(r'test/FR/dev.p4.out',r'FR/dev.in',r'test/FR/dev.ptest2')
# run_posteriorviterbi(r'test/EN/dev.p3.out',r'EN/dev.in',r'test/EN/dev.ptest3')
# run_posteriorviterbi(r'test/FR/dev.p3.out',r'FR/dev.in',r'test/FR/dev.ptest3')
# p = viterbi(seq,-1,tp,ep)
# print (p)

# o = viterbi_backtrack(tp,p,'STOP')
# print (o)
