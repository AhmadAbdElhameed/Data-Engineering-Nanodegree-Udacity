import configparser
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, date_format

import configparser
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col,monotonically_increasing_id, from_unixtime
from pyspark.sql.functions import year, month, dayofmonth,dayofweek, hour, weekofyear, date_format
from pyspark.sql.types import StructType as R,TimestampType as Ts ,StructField as Fld,FloatType as Flt ,DoubleType as Dbl, StringType as Str, IntegerType as Int, DateType as Date

config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID'] = config.get('AWS', 'AWS_ACCESS_KEY_ID')
os.environ['AWS_SECRET_ACCESS_KEY'] = config.get('AWS', 'AWS_SECRET_ACCESS_KEY')


def create_spark_session():

    ## Creates a new or uses the existing spark session.

    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark


def process_song_data(spark, INPUT_BUCKET, OUTPUT_DATA_PATH):
    #Description: This function loads song_data from S3 and processes it by extracting the songs and artist tables
    #and then again loaded back to S3 
    #Parameters:
    #        spark       : Spark Session
    #       INPUT_BUCKET  : location of song_data json files with the songs metadata
    #       OUTPUT_DATA_PATH : S3 bucket were dimensional tables in parquet format will be stored
    
    LOG_DATA_PATH='log-data/*/*/*.json'
    SONG_DATA_PATH ='song_data/A/A/*/*.json'
    # get filepath to song data file
    song_data = os.path.join(INPUT_BUCKET, SONG_DATA_PATH)
    
    # read song data file
    df_song = spark.read.json(song_data)

    # extract columns to create songs table
    song_columns = ["song_id","title", "artist_id", "year", "duration"]
    songs_table = df_song.select(song_columns).dropDuplicates().withColumn("song_id", monotonically_increasing_id())
    
    # write songs table to parquet files partitioned by year and artist
    songs_table.write.mode("overwrite").partitionBy("year", "artist_id").parquet(OUTPUT_DATA_PATH+'songs_table/')
    
    # extract columns to create artists table
    artists_columns = ["artist_id",
                  "artist_name as name",
                  "artist_location as location",
                  "artist_latitude as latitude",
                  "artist_longitude as longitude"]
    artists_table = df_song.selectExpr(artists_columns).dropDuplicates()
    
    # write artists table to parquet files
    artists_table.write.mode("overwrite").parquet(OUTPUT_DATA_PATH+'artists_table/')
    
    print("process song data successfully")


def process_log_data(spark, INPUT_BUCKET, OUTPUT_DATA_PATH):

    #Description: This function loads log_data from S3 and processes it by extracting the songs and artist tables
    #   and then again loaded back to S3. Also output from previous function is used in by spark.read.json command
        
    #Parameters:
    #spark       : Spark Session
    #INPUT_BUCKET  : location of log_data json files with the events data
    #OUTPUT_DATA_PATH : S3 bucket were dimensional tables in parquet format will be stored // BUT LOCAL NOW
            

    LOG_DATA_PATH='log-data/*/*/*.json'
    SONG_DATA_PATH ='song_data/A/A/*/*.json'
    
    # get filepath to log data file
    log_data = os.path.join(INPUT_BUCKET, LOG_DATA_PATH)
    # read log data file
    df_log = spark.read.json(log_data)
    
    # filter by actions for song plays
    df_log = df_log.filter(df_log.page == "NextSong")

    # extract columns for users table     
    users_columns = ["userId as user_id",
                 "firstName as first_name",
                  "lastName as last_name",
                   "level",
                  "gender",
                  "location"]
    users_table = df_log.selectExpr(users_columns).dropDuplicates()
    # write users table to parquet files
    users_table.write.mode("overwrite").parquet(OUTPUT_DATA_PATH+'users_table/')
    
    df = df_log
    # create timestamp column from original timestamp column
    get_timestamp = udf(lambda x:  datetime.fromtimestamp(x/1000).strftime('%Y-%m-%d %H:%M:%S'))
    df = df.withColumn("timestamp", get_timestamp(df.ts)) 
    
    # create datetime column from original timestamp column
    get_datetime = udf(lambda x: datetime.fromtimestamp(x/1000).strftime('%Y-%m-%d'))
    df = df.withColumn("datetime", get_datetime(df.ts))
    
    # extract columns to create time table
    time_table = df.select(
        col('timestamp').alias('start_time'),
        hour('timestamp').alias('hour'),
        dayofmonth('timestamp').alias('day'),
        weekofyear('timestamp').alias('week'),
        month('timestamp').alias('month'),
        year('timestamp').alias('year') 
   )
    
    # write time table to parquet files partitioned by year and month
    time_table.write.mode("overwrite").partitionBy("year", "month").parquet(OUTPUT_DATA_PATH + "time_table/")

    # read in song data to use for songplays table
    song_data = os.path.join(INPUT_BUCKET, SONG_DATA_PATH)
    song_df = spark.read.json(song_data) 
    
    songplays_table = song_df.select(
    col("artist_id"),
    col("artist_name"),
    col("duration"),
     col('song_id'),
    col('title')
     )
    df2 = df.select(
        col('ts').alias('ts'),
        col('userId').alias('user_id'),
        col('level').alias('level'),
        col('location').alias('location'),
        col('userAgent').alias('user_agent'),
        month('datetime').alias('month'),
        year('datetime').alias('year'),
        col("song")
                )
    total = df2.join(songplays_table, songplays_table.title == df2.song)

    # extract columns from joined song and log datasets to create songplays table 
    songplays_table = total 

    # write songplays table to parquet files partitioned by year and month
    songplays_table.write.mode("overwrite").partitionBy("year", "month").parquet(OUTPUT_DATA_PATH+'songplays/')
    
    print("process log data successfully")


def main():

    #Extract songs and events data from S3, Transform it into dimensional tables format, and Load it back to S3 in 
    #Parquet format

    spark = create_spark_session()
    INPUT_BUCKET='s3a://udacity-dend/'
    OUTPUT_DATA_PATH = "outputs/"
    process_song_data(spark, INPUT_BUCKET, OUTPUT_DATA_PATH)    
    process_log_data(spark, INPUT_BUCKET, OUTPUT_DATA_PATH)


if __name__ == "__main__":
    main()
