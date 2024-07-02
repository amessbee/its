import raw2bank
import question
import stats
import topic
import type
import xml2tex

bank_file_path = '../data/bank/bank.xml'
inout_dir = '../data/raw/'

stats.pullStatsFromNewRawQuestions(inout_dir)

stats.count_questions_by_topic(bank_file_path)

raw2bank.add_questions_from_directory(bank_file_path,inout_dir)

question.remove_question_number_attribute(bank_file_path)

stats.count_questions_by_topic(bank_file_path)