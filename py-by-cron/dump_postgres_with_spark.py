#/usr/bin/env python
print('It works')

import os
os.environ['PYSPARK_SUBMIT_ARGS'] = '--driver-class-path /home/jovyan/postgresql-42.2.5.jar --jars /home/jovyan/postgresql-42.2.5.jar pyspark-shell'

import sys
sys.path.append('/opt/conda/lib/python3.7/site-packages')

import findspark
findspark.init()

import pyspark

spark = pyspark.sql.SparkSession.builder \
        .master("local[1]") \
        .appName("snapshot") \
        .getOrCreate()

print("Application started")

spark.sparkContext.range(1000).sum()
print("Spark application is ready for work")

customers = spark.read.format('jdbc').options(
        url = "jdbc:postgresql://postgres:5432/postgres?user=postgres&password=postgres&currentSchema=inventory",
        database='postgres',
        dbtable='customers'
    ).load()

products = spark.read.format('jdbc').options(
        url = "jdbc:postgresql://postgres:5432/postgres?user=postgres&password=postgres&currentSchema=inventory",
        database='postgres',
        dbtable='products'
    ).load()

orders = spark.read.format('jdbc').options(
        url = "jdbc:postgresql://postgres:5432/postgres?user=postgres&password=postgres&currentSchema=inventory",
        database='postgres',
        dbtable='orders'
    ).load()

customers.registerTempTable("customers")
products.registerTempTable("products")
orders.registerTempTable("orders")

#print("Customers table")
#customers.show(5)
#print("Orders table")
#orders.show(5)
#print("Products table")
#products.show(5)

query = "\
SELECT \
  customers.id, \
  first(customers.first_name) AS first_name, \
  first(customers.last_name) AS last_name, \
  SUM(products.weight) AS total_weight, \
  current_timestamp() AS load_dttm \
FROM \
  customers \
  LEFT JOIN orders ON (orders.purchaser = customers.id) \
  LEFT JOIN products ON (products.id = orders.product_id) \
WHERE \
  customers.id <= 1005 \
GROUP BY \
  customers.id \
"
result = spark.sql(query)
result.write.format("parquet").save("/home/jovyan/weight_report", mode="overwrite")

spark.read \
    .format("parquet").load("/home/jovyan/weight_report").show()
