from collections import Counter
import copy
from viterbi import Viterbi
from forward_backward import ForwardBackward
from fractions import Fraction
from posterior_viterbi import PosteriorViterbi
from processor import Processor


normal_tags = ['START', 'O', 'B-positive', 'B-neutral', 'B-negative', 'I-positive', 'I-neutral', 'I-negative', 'STOP']
tags_only = ['START', 'O', 'B', 'I', 'STOP']
sentiment = ['START', 'positive', 'neutral', 'negative', 'STOP']

## <<< RESULTS FOR PART 2 >>>>
	
#training	
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

run_p2(r'EN/train',r'EN/dev.in',r'EN/dev.p2.out')



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

# run_forwardbackward(r'EN/train',r'EN/dev.in',r'EN/dev.p4.out')
# run_forwardbackward(r'FR/train',r'FR/dev.in',r'FR/dev.p4.out')
# run_forwardbackward(r'EN/train',r'test/EN/test.in',r'test/EN/dev.p4.out')
# run_forwardbackward(r'FR/train',r'test/FR/test.in',r'test/FR/dev.p4.out')


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

def run_separate_posteriorviterbi(fileTrain, fileIn, fileOut):
	# do normal stuff
	words_count, tag_count = Processor.parse_train(fileTrain)
	words_count = Processor.process_unknown_words(words_count,3, normal_tags)
	ep = Processor.get_emission_params(words_count, tag_count)
	tp = Processor.get_transition_params(fileTrain, normal_tags, 'normal')
	seq = Processor.parser(fileIn)
	v = PosteriorViterbi(tp,ep)
	v_out_normal = []

	for s in seq:
		out = v.assign(s)
		v_out_normal.append(out)

	# do stuff for tag
	words_count, tag_count2 = Processor.parse_tag(fileTrain)
	words_count = Processor.process_unknown_words(words_count,3, tags_only)
	ep = Processor.get_emission_params(words_count, tag_count2)
	tp = Processor.get_transition_params(fileTrain, tags_only, 'tag')
	seq = Processor.parser(fileIn)
	v_tag = PosteriorViterbi(tp,ep)
	v_out_tag = []

	for s in seq:
		out = v_tag.assign(s)
		v_out_tag.append(out)

	# do stuff for sentiment
	words_count, sentiment_count = Processor.parse_sentiment(fileTrain)
	words_count = Processor.process_unknown_words(words_count,3, sentiment)
	ep_sent = Processor.get_tag_sentiment_ratio(tag_count2, tag_count)

	v_out_swapped = Processor.swap_if_different(v_out_normal, v_out_tag, ep_sent)

	v_seq = Processor.v_result_parse(v_out_swapped,seq)
	output_to_file = Processor.convert_back(v_seq)
	Processor.output_file(output_to_file,fileOut + '_separate')
	print ("PosteriorViterbi tag done for "+ fileOut + '_separate')

run_separate_posteriorviterbi(r'FR/train',r'FR/dev.in',r'FR/dev.p5sep.out')
