from pyspark.sql import SparkSession
from pyspark.sql.window import Window
import pyspark.sql.functions as F
import pandas as pd
from pyspark.sql.functions import percent_rank


spark = SparkSession \
    .builder \
    .appName("readCSV") \
    .getOrCreate()
df = spark.read.csv('Building_Permits.csv',inferSchema=True, header=True)
df = df.dropna(subset=["SUBTOTAL_UNPAID"])
df= df.select("ID", "PERMIT_TYPE", "ISSUE_DATE", "SUBTOTAL_PAID", "SUBTOTAL_UNPAID", "SUBTOTAL_WAIVED", "TOTAL_FEE", "CONTACT_1_TYPE", "CONTACT_1_NAME", "CONTACT_1_CITY", "CONTACT_1_STATE", "CONTACT_1_ZIPCODE", "WARD", )
windowSpec  = Window.orderBy("SUBTOTAL_UNPAID")
df = df.withColumn("UNPAID_PERCENT_RANK",percent_rank().over(windowSpec))
pandasDF = df.toPandas()
