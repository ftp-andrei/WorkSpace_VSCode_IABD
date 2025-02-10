package org.apache.hadoop.examples;

import java.io.IOException;
import java.util.Arrays;
import java.util.List;
import java.util.ArrayList;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

public class MedianCalculator extends Configured implements Tool {

    public static class MedianMapper extends Mapper<Object, Text, Text, IntWritable> {

        private final static Text constantKey = new Text("medianKey");
        private IntWritable number = new IntWritable();

        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
            try {
                // Convert the input to an integer
                int num = Integer.parseInt(value.toString());
                number.set(num);
                // Emit the number with a constant key to group all numbers in the reducer
                context.write(constantKey, number);
            } catch (NumberFormatException e) {
                // If not a valid integer, skip
            }
        }
    }

    public static class MedianReducer extends Reducer<Text, IntWritable, Text, IntWritable> {

        private IntWritable result = new IntWritable();

        public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
            List<Integer> numbers = new ArrayList<>();

            // Collect all numbers
            for (IntWritable val : values) {
                numbers.add(val.get());
            }

            // Sort the numbers
            int[] sortedNumbers = numbers.stream().mapToInt(i -> i).toArray();
            Arrays.sort(sortedNumbers);

            // Calculate the median
            int median;
            int size = sortedNumbers.length;
            if (size % 2 == 0) {
                // If even, median is the average of the two middle numbers
                median = (sortedNumbers[size / 2 - 1] + sortedNumbers[size / 2]) / 2;
            } else {
                // If odd, median is the middle number
                median = sortedNumbers[size / 2];
            }

            // Emit the result
            result.set(median);
            context.write(key, result);
        }
    }

    @Override
    public int run(String[] args) throws Exception {
        if (args.length != 2) {
            System.out.println("Usage: MedianCalculator <input> <output>");
            return 2;
        }

        Configuration conf = getConf();
        Job job = Job.getInstance(conf, "Median Calculator");

        job.setJarByClass(MedianCalculator.class);
        job.setMapperClass(MedianMapper.class);
        job.setReducerClass(MedianReducer.class);

        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        return job.waitForCompletion(true) ? 0 : 1;
    }

    public static void main(String[] args) throws Exception {
        int res = ToolRunner.run(new Configuration(), new MedianCalculator(), args);
        System.exit(res);
    }
}
