raw_data = LOAD 'hdfs:///data/claims.csv' USING TextLoader() AS (line: chararray);
words = FOREACH raw_data GENERATE FLATTEN(TOKENIZE(line)) AS word;
grouped_words = GROUP words BY word;
word_count = FOREACH grouped_words GENERATE group AS word, COUNT(words) AS count;
STORE word_count INTO 'hdfs:///data/output_directory' USING PigStorage(',');