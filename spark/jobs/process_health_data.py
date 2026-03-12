import os
import json
from datetime import datetime, timezone
from typing import List, Dict
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    split,
    when,
    count,
    avg,
    max as spark_max,
    lit,
)
import pandas as pd
from sklearn.ensemble import IsolationForest

DATA_DIR = os.environ.get("NHRIS_DATA", "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
ALERTS_PATH = os.path.join(DATA_DIR, "alerts", "latest.json")
DELTA_DIR = os.environ.get("NHRIS_DELTA", "delta")

builder = (
    SparkSession.builder.appName("NHRIS-Health-ETL")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
)

try:
    from delta import configure_spark_with_delta_pip

    spark = configure_spark_with_delta_pip(builder).getOrCreate()
except Exception:
    spark = builder.getOrCreate()

raw_df = (
    spark.read.option("header", "true")
    .option("inferSchema", "true")
    .csv(os.path.join(RAW_DIR, "*.csv"))
)

clean_df = (
    raw_df
    .withColumn("region", split(col("patient_location"), ":").getItem(0))
    .withColumn("city", split(col("patient_location"), ":").getItem(1))
    .withColumn(
        "bp_systolic",
        split(col("blood_pressure"), "/").getItem(0).cast("int"),
    )
    .withColumn(
        "bp_diastolic",
        split(col("blood_pressure"), "/").getItem(1).cast("int"),
    )
)

run_ts = datetime.now(timezone.utc).isoformat()

agg_df = (
    clean_df.groupBy("region", "city", "diagnosis")
    .agg(
        count("*").alias("case_count"),
        avg("temperature").alias("avg_temperature"),
        avg("oxygen_level").alias("avg_oxygen"),
        spark_max("heart_rate").alias("max_heart_rate"),
    )
    .withColumn("run_ts", lit(run_ts))
)

# Simple rule-based alerts for demo
def detect_anomalies(rows: List[Dict]) -> List[Dict]:
    if not rows:
        return []
    pdf = pd.DataFrame(rows)
    features = pdf[["case_count", "avg_temperature", "avg_oxygen", "max_heart_rate"]].fillna(0)
    model = IsolationForest(n_estimators=120, contamination=0.12, random_state=42)
    pdf["anomaly"] = model.fit_predict(features)
    pdf["score"] = model.decision_function(features)

    alerts = []
    for _, r in pdf.iterrows():
        if r["anomaly"] != -1:
            continue
        reason = "Anomalous spike"
        if r["diagnosis"] == "fever":
            reason = "Fever spike (anomaly)"
        elif r["diagnosis"] == "respiratory":
            reason = "Respiratory spike (anomaly)"
        if r["case_count"] >= 60:
            reason = "Hospital overload (anomaly)"
        alerts.append(
            {
                "region": r["region"],
                "city": r["city"],
                "diagnosis": r["diagnosis"],
                "case_count": int(r["case_count"]),
                "alert_reason": reason,
                "score": float(r["score"]),
            }
        )
    return alerts

# Persist Delta tables
clean_df.write.format("delta").mode("append").save(os.path.join(DELTA_DIR, "patient_events"))
agg_df.write.format("delta").mode("append").save(os.path.join(DELTA_DIR, "regional_aggregates"))

alerts = detect_anomalies([row.asDict() for row in agg_df.collect()])
alerts_df = spark.createDataFrame(alerts) if alerts else spark.createDataFrame([], schema="region string, city string, diagnosis string, case_count int, alert_reason string, score double")
alerts_df.write.format("delta").mode("append").save(os.path.join(DELTA_DIR, "alerts"))

os.makedirs(os.path.dirname(ALERTS_PATH), exist_ok=True)
with open(ALERTS_PATH, "w", encoding="utf-8") as f:
    json.dump({"generated_at": datetime.now(timezone.utc).isoformat(), "alerts": alerts}, f, indent=2)

# Save processed parquet for quick access
clean_df.write.mode("overwrite").parquet(PROCESSED_DIR)

spark.stop()
