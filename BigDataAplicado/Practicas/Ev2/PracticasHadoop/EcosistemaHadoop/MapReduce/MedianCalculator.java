import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;

public class MedianCalculator {

    public static class MedianMapper extends Mapper<Object, Text, IntWritable, NullWritable> {
        private IntWritable number = new IntWritable();

        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
            try {
                int num = Integer.parseInt(value.toString().trim());
                number.set(num);
                context.write(number, NullWritable.get());
            } catch (NumberFormatException e) {
                // Ignorar líneas inválidas
            }
        }
    }

    public static class MedianReducer extends Reducer<IntWritable, NullWritable, Text, NullWritable> {
        private ArrayList<Integer> numbers = new ArrayList<>();

        public void reduce(IntWritable key, Iterable<NullWritable> values, Context context) {
            numbers.add(key.get());
        }

        public void cleanup(Context context) throws IOException, InterruptedException {
            Collections.sort(numbers); // Ordenar los números

            int n = numbers.size();
            double median;
            if (n % 2 == 1) {
                median = numbers.get(n / 2);
            } else {
                median = (numbers.get(n / 2 - 1) + numbers.get(n / 2)) / 2.0;
            }

            context.write(new Text("Mediana: " + median), NullWritable.get());
        }
    }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "median calculator");

        job.setJarByClass(MedianCalculator.class);
        job.setMapperClass(MedianMapper.class);
        job.setReducerClass(MedianReducer.class);

        job.setMapOutputKeyClass(IntWritable.class);
        job.setMapOutputValueClass(NullWritable.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(NullWritable.class);

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}