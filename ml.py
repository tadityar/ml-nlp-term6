from collections import Counter
import copy
from viterbi import Viterbi
from forward_backward import ForwardBackward
from fractions import Fraction
from posterior_viterbi import PosteriorViterbi
from processor import Processor
import sys


normal_tags = ['START', 'O', 'B-positive', 'B-neutral', 'B-negative', 'I-positive', 'I-neutral', 'I-negative', 'STOP']
tags_only = ['START', 'O', 'B', 'I', 'STOP']
sentiment = ['START', 'positive', 'neutral', 'negative', 'STOP']

## <<< RESULTS FOR PART 2 >>>>

def run_p2(fileTrain,fileIn,fileOut):
	words_count, tag_count = Processor.parse_train(fileTrain)
	words_count = Processor.process_unknown_words(words_count,3, normal_tags)
	ep = Processor.get_emission_params(words_count, tag_count)
	data = Processor.parser(fileIn)
	data_p = Processor.process_unknown_words_testing(data,words_count)
	ep_p = Processor.emission_param_preprocess(ep)
	tagged_words = Processor.tagging_words(ep_p,data_p)

	output_to_file = Processor.convert_back(tagged_words)
	Processor.output_file(output_to_file,fileOut)
	print ("Part 2 done for "+fileOut)

## <<< RESULTS FOR PART 3 >>>

# ### RUNNING VITERBI ###

def run_viterbi(fileTrain, fileIn, fileOut):
	words_count, tag_count = Processor.parse_train(fileTrain)
	words_count = Processor.process_unknown_words(words_count,3, normal_tags)
	ep = Processor.get_emission_params(words_count, tag_count)
	tp = Processor.get_transition_params(fileTrain, normal_tags, 'normal')
	seq = Processor.parser(fileIn)
	v = Viterbi(tp,ep)
	v_out = []

	for s in seq:
		out = v.assign(s)
		v_out.append(out)

	v_seq = Processor.v_result_parse(v_out,seq)
	output_to_file = Processor.convert_back(v_seq)
	Processor.output_file(output_to_file,fileOut)
	print ("Viterbi done for "+ fileOut)

## <<< RESULTS FOR PART 4 >>>

# ### RUNNING FORWARDBACKWARD ###
def run_forwardbackward(fileTrain,fileIn,fileOut):
	words_count, tag_count = Processor.parse_train(fileTrain)
	words_count = Processor.process_unknown_words(words_count,3, normal_tags)
	ep = Processor.get_emission_params(words_count, tag_count)
	tp = Processor.get_transition_params(fileTrain, normal_tags, 'normal')
	seq = Processor.parser(fileIn)

	v = ForwardBackward(tp,ep)
	v_out = []

	for s in seq:
		out = v.assign(s)
		v_out.append(out)

	v_seq = Processor.v_result_parse(v_out,seq)
	output_to_file = Processor.convert_back(v_seq)
	Processor.output_file(output_to_file,fileOut)
	print ("ForwardBackward done for "+ fileOut)

def run_posteriorviterbi(fileTrain, fileIn, fileOut):
	words_count, tag_count = Processor.parse_train(fileTrain)
	words_count = Processor.process_unknown_words(words_count,3, normal_tags)
	ep = Processor.get_emission_params(words_count, tag_count)
	tp = Processor.get_transition_params(fileTrain, normal_tags, 'normal')
	seq = Processor.parser(fileIn)
	v = PosteriorViterbi(tp,ep)
	v_out = []

	for s in seq:
		out = v.assign(s)
		v_out.append(out)

	v_seq = Processor.v_result_parse(v_out,seq)
	output_to_file = Processor.convert_back(v_seq)
	Processor.output_file(output_to_file,fileOut)
	print ("PosteriorViterbi done for "+ fileOut)

def run_separate_posteriorviterbi(fileTrain, fileIn, fileOut, n=3):
	# HMM for Entity + Sentiment
	words_count, tag_count = Processor.parse_train(fileTrain)
	words_count = Processor.process_unknown_words(words_count,n, normal_tags)
	ep = Processor.get_emission_params(words_count, tag_count)
	tp = Processor.get_transition_params(fileTrain, normal_tags, 'normal')
	seq = Processor.parser(fileIn)
	v = PosteriorViterbi(tp,ep)
	v_out_normal = []

	for s in seq:
		out = v.assign(s)
		v_out_normal.append(out)

	# HMM for Entity only
	words_count, tag_count2 = Processor.parse_tag(fileTrain)
	words_count = Processor.process_unknown_words(words_count,n, tags_only)
	ep = Processor.get_emission_params(words_count, tag_count2)
	tp = Processor.get_transition_params(fileTrain, tags_only, 'tag')
	seq = Processor.parser(fileIn)
	v_tag = PosteriorViterbi(tp,ep)
	v_out_tag = []

	for s in seq:
		out = v_tag.assign(s)
		v_out_tag.append(out)

	# Get sentiment ratio
	words_count, sentiment_count = Processor.parse_sentiment(fileTrain)
	words_count = Processor.process_unknown_words(words_count,n, sentiment)
	ep_sent = Processor.get_tag_sentiment_ratio(tag_count2, tag_count)

	v_out_swapped = Processor.swap_if_different(v_out_normal, v_out_tag, ep_sent)

	v_seq = Processor.v_result_parse(v_out_swapped,seq)
	output_to_file = Processor.convert_back(v_seq)
	Processor.output_file(output_to_file,fileOut)
	print ("PosteriorViterbi tag done for "+ fileOut)

if __name__ == "__main__":
	part = sys.argv[1]
	trainFile = sys.argv[2]
	inputFile = sys.argv[3]
	outputFile = sys.argv[4]

	if (part == '2'):
		run_p2(trainFile, inputFile, outputFile)
	elif (part == '3'):
		run_viterbi(trainFile, inputFile, outputFile)
	elif (part == '4'):
		run_forwardbackward(trainFile, inputFile, outputFile)
	elif (part == '5'):
		run_separate_posteriorviterbi(trainFile, inputFile, outputFile)

