"""
╔══════════════════════════════════════════════════════════════════════╗
║           American Airlines – Flight Delay Analysis                  ║
║                     PySpark Practice Problem                         ║
╚══════════════════════════════════════════════════════════════════════╝

CONTEXT
-------
You are a Data Engineer at American Airlines.
Your team receives a raw stream of flight events where each flight can
emit multiple records over its lifecycle (e.g. gate updates, pushback,
wheels-off). Your job is to clean and aggregate this data to produce a
reliable daily operations summary per departure airport.

──────────────────────────────────────────────────────────────────────
DATASET : flights_df
──────────────────────────────────────────────────────────────────────

Schema
------
  carrier             (string)     -- Airline carrier code       e.g. "AA"
  flight_num          (string)     -- Flight number              e.g. "101"
  dep_airport         (string)     -- IATA departure airport     e.g. "JFK"
  arr_airport         (string)     -- IATA arrival airport       e.g. "LAX"
  scheduled_dep_ts    (timestamp)  -- Planned departure time
  actual_dep_ts       (timestamp)  -- Real departure time
  event_ts            (timestamp)  -- When this event was recorded
                                      (multiple rows can exist per flight)

Note: The dataset may contain duplicate or stale records for the same
      flight. Always use the most recent event.

──────────────────────────────────────────────────────────────────────
TASKS
──────────────────────────────────────────────────────────────────────

A)  FLIGHT KEY
    ----------
    Create a surrogate key column called flight_key using the format:
        carrier + "-" + dep_airport + "-" + arr_airport
                + "-" + date(scheduled_dep_ts)
                + "-" + flight_num

    Example: "AA-JFK-LAX-2024-06-01-101"

B)  DE-DUPLICATION
    --------------
    There may be multiple rows for the same flight_key (duplicate /
    late-arriving events). Retain only the single most recent record
    per flight_key, determined by event_ts.

C)  DEPARTURE DELAY
    ---------------
    Compute a new column dep_delay_min:
        dep_delay_min = (actual_dep_ts − scheduled_dep_ts) in minutes

    A positive value means the flight departed late.
    A negative value means the flight departed early.

D)  AIRPORT-LEVEL DAILY AGGREGATION
    ---------------------------------
    After de-duplication, group by dep_airport and departure date
    (derived from scheduled_dep_ts) and compute the following metrics:

        • total_flights       -- total number of unique flights
        • avg_delay_min       -- average departure delay in minutes
        • pct_delayed_15plus  -- percentage of flights delayed ≥ 15 min

──────────────────────────────────────────────────────────────────────
EXPECTED OUTPUT (Task D) – shape only, values will differ
──────────────────────────────────────────────────────────────────────

  dep_airport | dep_date   | total_flights | avg_delay_min | pct_delayed_15plus
  ────────────┼────────────┼───────────────┼───────────────┼────────────────────
  JFK         | 2024-06-01 | 2             | 25.0          | 50.0
  LAX         | 2024-06-01 | 1             | 5.0           | 0.0
  ORD         | 2024-06-01 | 2             | 27.5          | 50.0

──────────────────────────────────────────────────────────────────────
"""

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

from pyspark.sql.window import Window

# ───────────────────────────────────────────────
#  Spark Session
# ───────────────────────────────────────────────
spark = (
    SparkSession.builder
    .appName("AmericanAirlines-FlightDelayAnalysis")
    .getOrCreate()
)

spark.conf.set("spark.sql.repl.eagerEval.enabled", True)

# ───────────────────────────────────────────────
#  Sample Data
# ───────────────────────────────────────────────
#
#  Scenario breakdown:
#  ┌──────┬────────────┬──────────────────────┬──────────────────────┬────────────────────────────────────────────────┐
#  │ Row  │ flight_key │ scheduled_dep_ts     │ actual_dep_ts        │ Notes                                          │
#  ├──────┼────────────┼──────────────────────┼──────────────────────┼────────────────────────────────────────────────┤
#  │ 1,2  │ AA-101-JFK │ 2024-06-01 08:00     │ 2024-06-01 08:20     │ DUPLICATE – same flight, two events; row 2     │
#  │      │            │                      │                      │ is newer (event_ts = 08:25) → keep row 2       │
#  │ 3    │ AA-202-ORD │ 2024-06-01 09:00     │ 2024-06-01 09:10     │ Small delay (10 min) – NOT ≥ 15 min            │
#  │ 4    │ AA-303-JFK │ 2024-06-01 07:30     │ 2024-06-01 08:00     │ Delayed 30 min – counts as delayed             │
#  │ 5    │ AA-404-LAX │ 2024-06-01 06:00     │ 2024-06-01 06:05     │ Minor delay (5 min) – NOT ≥ 15 min             │
#  │ 6    │ AA-505-ORD │ 2024-06-01 11:00     │ 2024-06-01 11:45     │ Delayed 45 min – counts as delayed             │
#  └──────┴────────────┴──────────────────────┴──────────────────────┴────────────────────────────────────────────────┘

raw_data = [
    # carrier  flt   dep    arr    scheduled_dep_ts  actual_dep_ts  event_ts      [note]
    ("AA", "101", "JFK", "LAX", 1717228800,       1717230000,    1717229100),  # stale duplicate
    ("AA", "101", "JFK", "LAX", 1717228800,       1717230000,    1717230300),  # latest – keep this
    ("AA", "202", "ORD", "DFW", 1717232400,       1717233000,    1717232700),  # 10 min delay
    ("AA", "303", "JFK", "MIA", 1717227000,       1717228800,    1717227900),  # 30 min delay
    ("AA", "404", "LAX", "SEA", 1717221600,       1717221900,    1717222200),  # 5 min delay
    ("AA", "505", "ORD", "JFK", 1717239600,       1717242300,    1717240800),  # 45 min delay
    
    # June 2nd data
    ("AA", "101", "JFK", "LAX", 1717315200,       1717315200,    1717315500),  # On time
    ("AA", "606", "DFW", "ORD", 1717322400,       1717323300,    1717323600),  # 15 min delay
    ("AA", "707", "MIA", "JFK", 1717329600,       1717329300,    1717330200),  # 5 min early
]

schema = [
    "carrier", "flight_num", "dep_airport", "arr_airport",
    "scheduled_dep_ts", "actual_dep_ts", "event_ts",
]

# When data is Unix integers, we convert them to Timestamps for Task A/D
flights_df = (
    spark.createDataFrame(raw_data, schema)
    .withColumn("scheduled_dep_ts", F.timestamp_seconds(F.col("scheduled_dep_ts")))
    .withColumn("actual_dep_ts",    F.timestamp_seconds(F.col("actual_dep_ts")))
    .withColumn("event_ts",         F.timestamp_seconds(F.col("event_ts")))
)

# flights_df.show(truncate=False)

# ── YOUR SOLUTION GOES BELOW ──────────────────

flights_df = flights_df.withColumn(
    "flight_key",
    F.concat_ws(
        "-",
        F.col("carrier"),
        F.col("dep_airport"),
        F.col("arr_airport"),
        F.date_format(F.col("scheduled_dep_ts"), "yyyy-MM-dd"),
        F.col("flight_num")
    )
)

# creating window_spec 

window_spec = Window.partitionBy(F.col("flight_key"))\
    .orderBy(F.col("event_ts").desc())

flights_df = (
    flights_df.withColumn(
    "row_num",
    F.row_number().over(window_spec))\
        .filter(F.col("row_num")==1)\
        .drop(F.col("row_num"))
)

# lets calculate departure delay 

from pyspark.sql.types import LongType

flights_df = flights_df.withColumn(
    "dep_delay_min",
    (F.unix_timestamp("actual_dep_ts")-F.unix_timestamp("scheduled_dep_ts"))/60
)

# finally the report layer , 

report_df = (
    flights_df.withColumn("dep_date",
        F.to_date("scheduled_dep_ts"))
    .groupBy("dep_airport","dep_date")
    .agg(
        F.count("flight_key").alias("total_flights"),
        F.round(F.avg("dep_delay_min"),2).alias("avg_delay_min"),
        # calculate % of delay where delay is more than 15 min 
        F.round(
            (
                F.count(
                    F.when(
                        F.col("dep_delay_min")>=15,1
                    )
                ) / F.count("*")
            )*100,2
        ).alias("pct_of_delay_15plus")
    )
    .orderBy(F.col("dep_date"),F.col("dep_airport"))
)

report_df.show(truncate=False)

# the de-duplication 


