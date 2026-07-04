# 🗄️ Comprehensive SQL Syllabus for Data Engineers
### Target: Google & Microsoft — Data Engineer Interviews (L4/L5 Level)
> **Goal**: From Intermediate to FAANG-level Advanced SQL. Covers every concept, function, and edge case.
> **Google Specific Focus**: Array/Collection manipulation (BigQuery style), Event stream processing, sessionization, recursive looping, and performance at scale.

---

## 🟡 PHASE 1 — Intermediate SQL (Fundamentals)

### 1.1 Aggregations & Grouping
- **Core**: `COUNT()`, `SUM()`, `AVG()`, `MIN()`, `MAX()`
- **Distinct Aggregation**: `COUNT(DISTINCT col)`
- **Grouping**: `GROUP BY` (single & multiple columns, by expression/alias)
- **Filtering**: `WHERE` (before grouping) vs `HAVING` (after grouping)
- **NULL behavior**: `COUNT(*)` counts rows (including NULLs), `COUNT(col)` ignores NULLs.

### 1.2 JOINs & Relations
- **Inner & Outer**: `INNER JOIN`, `LEFT JOIN`, `RIGHT JOIN`, `FULL OUTER JOIN`
- **Cartesian**: `CROSS JOIN` (Generates combinations, e.g., All Dates x All Users)
- **Self & Non-Equi**: `SELF JOIN`, Joining on inequalities (`<`, `>`, `BETWEEN`)
- **Edge Cases**: Joining on NULLs (NULL ≠ NULL). Finding mismatches with `LEFT JOIN ... WHERE right.id IS NULL`.

### 1.3 Subqueries
- **Types**: Scalar, Column, Derived Tables.
- **Correlated Subqueries**: Executes row-by-row based on outer query. (Anti-pattern for performance; learn to rewrite via `JOIN` + `GROUP BY`).
- **Predicates**: `IN`, `EXISTS`, `ANY`, `ALL`.
- **Trap**: `NOT IN` fails completely if the subquery returns any NULL values. Use `NOT EXISTS`.

### 1.4 Set Operations
- `UNION` (removes duplicates) vs `UNION ALL` (keeps duplicates, much faster).
- `INTERSECT` (common) and `EXCEPT` / `MINUS` (difference).

---

## 🟢 PHASE 2 — Comprehensive SQL Functions & Data Types

### 2.1 Casting & Data Types
- **Standard Cast**: `CAST(col AS INT)`, `TRY_CAST(str AS INT)` (Returns NULL on failure).
- **Postgres Shorthand**: `'2024-01-01'::DATE`.

### 2.2 Date, Time & Unix Epochs
- **Current Dates**: `CURRENT_DATE`, `CURRENT_TIMESTAMP`, `NOW()`.
- **Date Math**: `date + INTERVAL '1 day'`, `date1 - date2`.
- **Extraction**: `EXTRACT(part FROM timestamp)` (parts: `YEAR`, `MONTH`, `DAY`, `DOW`, `HOUR`, `EPOCH`).
- **Truncation (Crucial)**: `DATE_TRUNC('month', timestamp)` - snaps to the start of the boundary.
- **Unix Timestamp**: Conversions to/from Epoch (`EXTRACT(EPOCH FROM ts)`, `TO_TIMESTAMP(16900000)`).

### 2.3 String Manipulation
- **Extraction/Position**: `SUBSTRING()`, `LEFT()`, `RIGHT()`, `POSITION()`, `LENGTH()`.
- **Regex (Google loves Regex)**: `REGEXP_REPLACE()`, `REGEXP_MATCHES()`, `~` (Posix match).
- **Concatenation**: `CONCAT(a, b)`, `CONCAT_WS(',', a, b)`.
- **Cleaning**: `TRIM()`, `LOWER()`, `UPPER()`.

### 2.4 Mathematical & Conditional Logic
- **Math**: `ROUND()`, `CEIL()`, `FLOOR()`, `ABS()`, `MOD()`, `POWER()`.
- **Pivot Logic**: `SUM(CASE WHEN type = 'A' THEN amount ELSE 0 END) AS pivot_A`.
- **Null Handling**: `COALESCE(a, b, c)` (First non-null), `NULLIF(a, b)` (NULL if a=b, prevents divide-by-zero).
- **Comparisons**: `GREATEST(a,b,c)`, `LEAST(a,b,c)`.

---

## 🟠 PHASE 3 — Advanced SQL (Window Functions & Analytics)

### 3.1 Ranking & Row Numbering
- **`ROW_NUMBER()`**: Absolute unique integer per row. (Deduplication engine).
- **`RANK()` vs `DENSE_RANK()`**: Ties handling (1,2,2,4 vs 1,2,2,3).
- **`NTILE(n)`**: Percentiles/Deciles/Quartiles.

### 3.2 Value Offsets (Lead/Lag)
- **`LAG(col)`**: Read from previous physical rows (Crucial for time-between-events).
- **`LEAD(col)`**: Read from upcoming physical rows.

### 3.3 Framing Boundaries: ROWS vs RANGE (The Trap)
- **`ROWS BETWEEN`**: Physical bound (e.g., exactly 3 rows back). Tie values evaluated independently.
- **`RANGE BETWEEN`**: Logical bound based on values. Tie values evaluated as a single group.
- **The Trap**: Default `ORDER BY` frame is `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`. This breaks `LAST_VALUE()`. Always append `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`.

---

## 🔴 PHASE 4 — SUPER ADVANCED DE TIER (Google / Big Data Specifics)

### 4.1 🟦 ARRAYS & COLLECTIONS (Crucial for Google/BigQuery)
*Big data platforms (BigQuery, Trino, Postgres) heavily rely on nested, semi-structured arrays.*
- **Array Construction**: `ARRAY[1, 2, 3]` or `ARRAY_AGG(column_name)` (Collapsing multiple rows into a single list per group).
- **Array Expansion (Flattening)**: `UNNEST(array_col)` (Extracts list elements into individual rows). Cross joining a table against its unnested array is standard practice.
- **Array Navigation**: Finding the Nth element (`array_col[offset(0)]` in BQ, `array_col[1]` in Postgres).
- **Array Length**: `ARRAY_LENGTH()` or `CARDINALITY()`.
- **Searching Arrays**: `value = ANY(array_col)`, `value IN UNNEST(array_col)`.
- **Array Concatenation**: Combining multiple arrays (`array1 || array2`).
- **JSON Parsing**: Manipulating JSON objects/arrays (`jsonb_array_elements()`, `->>`, `#>>`).

### 4.2 🔁 LOOPING, ITERATION & RECURSION IN SQL
*SQL is declarative (set-based). Real loops represent a mindset shift to procedural or recursive execution.*
- **1. Set-Based Sequence Generation (The "SQL Loop")**:
  - `GENERATE_SERIES(start, end, step)`: Used to generate calendar dimension tables dynamically, or padding missing dates in a time-series.
- **2. RECURSIVE CTEs (The "Graph Loop")**:
  - `WITH RECURSIVE cte AS (Base Case UNION ALL Recursive Step)`
  - **Use Cases**: Employee-Manager hierarchy traversal, traversing a directed graph (Finding all mutual friends up to N degrees), parsing linked lists.
- **3. Procedural Looping (PL/pgSQL, BigQuery Scripting)**:
  - `WHILE condition DO ... END WHILE;`
  - `FOR record IN (SELECT ...) DO ... END FOR;`
  - *Note*: Procedural loops are rarely the right answer in DE interviews unless writing a database administration script or handling dynamic pipeline execution. Always prefer Set-Based/Recursive logic for data transformation.

### 4.3 Sessionization & Event Stream Parsing (Most Common Google Question)
- **Problem**: Bucket a stream of clicks. If inactive for > 30 mins, establish a new session.
- **Technique**:
  1. `LAG(timestamp)` to find time since last event.
  2. Flag it: `CASE WHEN diff > 30 THEN 1 ELSE 0 END as is_new_session`.
  3. Propagate ID: `SUM(is_new_session) OVER (PARTITION BY user_id ORDER BY timestamp)`.

### 4.4 Gaps, Islands & Overlapping Intervals
- **Gaps & Islands (Streaks)**: Group rows by subtracting `ROW_NUMBER()` from the `date`. Consecutive dates yield the same difference anchor.
- **Overlapping Intervals**: Calculate total *unique* days subscribed without double-counting overlaps using a running `MAX(end_date)` to define isolated intervals.

### 4.5 Advanced Aggregations (OLAP)
- **`ROLLUP(region, country, city)`**: Hierarchical subtotals + grand totals in one pass.
- **`CUBE(region, category)`**: All combinatorial groupings.
- **Ordered-Set Aggregates**: Medians using `PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY num)`.

---

## ⚫ PHASE 5 — Data Pipeline & Architecture Patterns

### 5.1 Slowly Changing Dimensions (SCD Type 2)
- Managing state history using `valid_from_ts`, `valid_to_ts`, and `is_active=Boolean`. 
- Point-in-time joins: `event_ts BETWEEN valid_from AND valid_to`.

### 5.2 Performance, Skew, & Execution
- **Data Skew**: Handling the 1-billion-row "bot" user crashing a join. (Salting / Re-partitioning / Broadcasting).
- **`EXPLAIN ANALYZE`**: Diagnosing Hash Joins vs Merge Joins vs Nested Loops.
- **Partition Pruning**: Why you partition log tables by `DATE`.
- **Idempotency**: Using `INSERT ... ON CONFLICT (id) DO UPDATE` to ensure pipelines can safely fail and retry without duplicating data.

---

## 🟣 PHASE 6 — Advanced PostgreSQL & Architecture Concepts

### 6.1 Table Partitioning & Storage
- **Declarative Partitioning**: Range (by date), List (by region), Hash (modulo).
- **Partition Pruning**: Query planner skipping irrelevant partitions.
- **Clustering**: `CLUSTER table_name USING index_name` (Physically reordering table data on disk based on an index).
- **Vacuuming**: `VACUUM`, `VACUUM FULL`, `VACUUM ANALYZE`, Auto-vacuum daemon (preventing transaction ID wraparound and clearing dead tuples).
- **Materialized Views**: `CREATE MATERIALIZED VIEW`, `REFRESH MATERIALIZED VIEW CONCURRENTLY`.

### 6.2 DML Operations & Concurrency
- **MERGE Statement**: Formally inserting/updating/deleting in one pass (`MERGE INTO target USING source ON ... WHEN MATCHED THEN UPDATE ... WHEN NOT MATCHED THEN INSERT`).
- **Upserts**: `INSERT INTO ... ON CONFLICT (key) DO UPDATE SET ...` or `DO NOTHING`.
- **Writeable CTEs**: Using `INSERT/UPDATE/DELETE RETURNING` inside a `WITH` clause to chain DML operations.
- **Transactions**: `BEGIN`, `COMMIT`, `ROLLBACK`, Isolation Levels (Read Uncommitted, Read Committed, Repeatable Read, Serializable).

### 6.3 Indexing Strategies
- **B-Tree**: Default, equality and range queries.
- **GIN (Generalized Inverted Index)**: Crucial for JSONB, Arrays, and Full-Text Search.
- **GiST / SP-GiST**: Geometric types, range types, nearest-neighbor.
- **BRIN (Block Range Index)**: Massive append-only tables (time-series).
- **Advanced Types**: Partial Indexes (`WHERE col IS NOT NULL`), Covering Indexes (`INCLUDE (col)`), Expression Indexes (`ON (LOWER(email))`).

---

## 🗓️ PHASE 7 — Deep Dive: Date, Time & Timestamps

### 7.1 Data Types
- `DATE`, `TIME`, `TIMESTAMP` (Without Time Zone), `TIMESTAMPTZ` (With Time Zone), `INTERVAL`.

### 7.2 Current Time & Generation
- `NOW()`, `CURRENT_DATE`, `CURRENT_TIME`, `CURRENT_TIMESTAMP`, `LOCALTIMESTAMP`
- Transaction vs Statement: `transaction_timestamp()` vs `statement_timestamp()` vs `clock_timestamp()` (wall-clock time).
- `GENERATE_SERIES(start_date, end_date, step_interval)`: Create continuous date/time ranges.

### 7.3 Extraction & Truncation
- `EXTRACT(field FROM source)` / `DATE_PART(field, source)`: Extract `CENTURY`, `DECADE`, `YEAR`, `QUARTER`, `MONTH`, `WEEK`, `DAY`, `DOW`, `DOY`, `HOUR`, `MINUTE`, `SECOND`, `EPOCH`.
- `DATE_TRUNC(field, source)`: Snap to start of boundary (e.g., `DATE_TRUNC('month', ts)`).

### 7.4 Unix Epoch / Timestamp Conversions
- **To Unix Timestamp (Seconds)**: `EXTRACT(EPOCH FROM timestamp)`
- **From Unix Timestamp (Seconds)**: `TO_TIMESTAMP(unix_numeric)` / `FROM_UNIXTIME()`
- **From Milliseconds**: `TO_TIMESTAMP(unix_ms / 1000.0)`

### 7.5 Formatting & Parsing
- `TO_CHAR(ts, format_string)` (e.g., `'YYYY-MM-DD HH24:MI:SS'`)
- `TO_DATE(string, format_string)`
- `TO_TIMESTAMP(string, format_string)`

### 7.6 Arithmetic & Time Zones
- `timestamp + interval '2 days'`
- `timestamp - timestamp` -> Returns `INTERVAL`
- `date - date` -> Returns integer (days)
- `AGE(timestamp, timestamp)`: Returns human-readable interval (e.g., '1 year 2 mons').
- Overlaps: `(start1, end1) OVERLAPS (start2, end2)`
- `AT TIME ZONE 'UTC'`, `SET TIME ZONE 'America/New_York'`

---

## 📚 APPENDIX A — Exhaustive SQL Function Reference
*(Complete list of functions grouped by category for rapid recall)*

### 1. Aggregate Functions
`COUNT` | `SUM` | `AVG` | `MIN` | `MAX` | `BOOL_AND` | `BOOL_OR` | `CORR` | `COVAR_POP` | `COVAR_SAMP` | `STDDEV` | `STDDEV_POP` | `STDDEV_SAMP` | `VARIANCE` | `VAR_POP` | `VAR_SAMP` | `STRING_AGG` | `ARRAY_AGG` | `JSON_AGG` | `JSONB_AGG` | `XMLAGG`

### 2. Window Functions
`ROW_NUMBER` | `RANK` | `DENSE_RANK` | `PERCENT_RANK` | `CUME_DIST` | `NTILE` | `LAG` | `LEAD` | `FIRST_VALUE` | `LAST_VALUE` | `NTH_VALUE`

### 3. Date / Time Functions
`AGE` | `CLOCK_TIMESTAMP` | `CURRENT_DATE` | `CURRENT_TIME` | `CURRENT_TIMESTAMP` | `DATE_PART` | `DATE_TRUNC` | `EXTRACT` | `ISFINITE` | `JUSTIFY_DAYS` | `JUSTIFY_HOURS` | `JUSTIFY_INTERVAL` | `LOCALTIME` | `LOCALTIMESTAMP` | `MAKE_DATE` | `MAKE_INTERVAL` | `MAKE_TIME` | `MAKE_TIMESTAMP` | `MAKE_TIMESTAMPTZ` | `NOW` | `STATEMENT_TIMESTAMP` | `TIMEOFDAY` | `TRANSACTION_TIMESTAMP`

### 4. String / Text Functions
`ASCII` | `BIT_LENGTH` | `BTRIM` | `CHAR_LENGTH` / `CHARACTER_LENGTH` | `CHR` | `CONCAT` | `CONCAT_WS` | `FORMAT` | `INITCAP` | `LEFT` | `LENGTH` | `LOWER` | `LPAD` | `LTRIM` | `MD5` | `OCTET_LENGTH` | `OVERLAY` | `PARSE_IDENT` | `PG_CLIENT_ENCODING` | `POSITION` | `QUOTE_IDENT` | `QUOTE_LITERAL` | `QUOTE_NULLABLE` | `REGEXP_MATCH` | `REGEXP_MATCHES` | `REGEXP_REPLACE` | `REGEXP_SPLIT_TO_ARRAY` | `REGEXP_SPLIT_TO_TABLE` | `REPEAT` | `REPLACE` | `REVERSE` | `RIGHT` | `RPAD` | `RTRIM` | `SPLIT_PART` | `STRPOS` | `SUBSTRING` `SUBSTR` | `STARTS_WITH` | `TRANSLATE` | `TRIM` | `UPPER`

### 5. Mathematical Functions
`ABS` | `ACOS` | `ASIN` | `ATAN` | `ATAN2` | `CBRT` | `CEIL` / `CEILING` | `COS` | `COTD` | `DEGREES` | `DIV` | `EXP` | `FLOOR` | `LN` | `LOG` | `MOD` | `PI` | `POWER` | `RADIANS` | `DIV` | `RANDOM` | `ROUND` | `SETSEED` | `SIGN` | `SIN` | `SQRT` | `TAN` | `TRUNC` | `WIDTH_BUCKET`

### 6. Conditional & Null/Comparison Functions
`CASE` | `COALESCE` | `NULLIF` | `GREATEST` | `LEAST` | `IS NULL` | `IS NOT NULL` | `IS DISTINCT FROM` | `IS NOT DISTINCT FROM` 

### 7. Array Functions
`ARRAY_APPEND` | `ARRAY_CAT` | `ARRAY_DIMS` | `ARRAY_FILL` | `ARRAY_LENGTH` | `ARRAY_LOWER` | `ARRAY_NDIMS` | `ARRAY_POSITION` | `ARRAY_POSITIONS` | `ARRAY_PREPEND` | `ARRAY_REMOVE` | `ARRAY_REPLACE` | `ARRAY_TO_JSON` | `ARRAY_TO_STRING` | `ARRAY_UPPER` | `CARDINALITY` | `UNNEST`

### 8. JSON / JSONB Functions
`TO_JSON` | `TO_JSONB` | `JSON_ARRAY_ELEMENTS` | `JSONB_ARRAY_ELEMENTS` | `JSON_ARRAY_ELEMENTS_TEXT` | `JSON_ARRAY_LENGTH` | `JSON_BUILD_ARRAY` | `JSON_BUILD_OBJECT` | `JSON_EACH` | `JSONB_EACH` | `JSON_EACH_TEXT` | `JSON_EXTRACT_PATH` | `JSON_OBJECT_KEYS` | `JSON_POPULATE_RECORD` | `JSON_STRIP_NULLS` | `JSONB_SET` | `JSONB_INSERT` | `JSONB_PRETTY`

### 9. Type Casting & Formatting
`CAST` | `::` (Postgres operator) | `TRY_CAST` (Standard/Other DBs) | `TO_CHAR` | `TO_DATE` | `TO_NUMBER` | `TO_TIMESTAMP`

### 10. Range Functions
`ISEMPTY` | `LOWER` | `UPPER` | `LOWER_INC` | `UPPER_INC` | `LOWER_INF` | `UPPER_INF` | `RANGE_MERGE`

### 11. System, Information & Meta Functions
`CURRENT_DATABASE` | `CURRENT_QUERY` | `CURRENT_SCHEMA` | `CURRENT_USER` | `SESSION_USER` | `PG_BACKEND_PID` | `PG_SLEEP` | `PG_SIZE_PRETTY` | `PG_RELATION_SIZE` | `PG_TOTAL_RELATION_SIZE` | `VERSION` | `HAS_TABLE_PRIVILEGE` | `FORMAT_TYPE` | `COL_DESCRIPTION` | `OBJ_DESCRIPTION`
