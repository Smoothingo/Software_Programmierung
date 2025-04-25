from pyspark.sql import SparkSession
from pyspark.sql.functions import split, explode, col, regexp_replace, lower


import os

PATH_HADOOP = r"C:\Hadoop"
PATH_JAVA = r"C:\Program Files\Java"
BINARY_DIR = "bin"
VERSION_JDK = "jdk-17"

def apply():
    os.environ["HADOOP_HOME"] = PATH_HADOOP
    os.environ["PATH"] += os.pathsep + os.path.join(PATH_HADOOP, BINARY_DIR)
    os.environ['JAVA_HOME'] = os.path.join(PATH_JAVA, VERSION_JDK)
    os.environ['PYSPARK_SUBMIT_ARGS'] = 'pyspark-shell'
apply()

spark = SparkSession.builder.master("local").appName("NussZähler").getOrCreate()

books = ["data.txt","1HP.txt", "2HP.txt", "3HP.txt", "4HP.txt"]  # Liste der Buchdateien

for book in books:
    print(f"Wir knacken all die Bücher bis aufs letzte Wort {book}...")
    df = spark.read.text(book)

    cleaned_df = df.withColumn("cleaned_value", lower(regexp_replace(col("value"), r"[^\w\s]", "")))
    split_df = cleaned_df.withColumn("word_array", split(col("cleaned_value"), " "))
    words_df = split_df.select(explode(col("word_array")).alias("word"))
    filtered_df = words_df.filter(col("word") != "")
    word_counts = filtered_df.groupBy("word").count()
    sorted_word_counts = word_counts.orderBy(col("count").desc())

    output_path = f"output/{book.split('.')[0]}"  # Speichere Ergebnisse in separaten Ordnern
    sorted_word_counts.coalesce(1).write.mode("overwrite").csv(output_path)
    print(f"Finished processing {book}. Results saved to {output_path}.")

spark.stop()
import os
os._exit(0)




