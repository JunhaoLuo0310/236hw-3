#!/usr/bin/env Rscript

# Install duckdb if not available
if (!require("duckdb", quietly = TRUE)) {
  install.packages("duckdb", repos = "https://cloud.r-project.org")
  library(duckdb)
}

# Create DuckDB connection
db <- duckdb::duckdb()
con <- DBI::dbConnect(db)

# Use DuckDB SQL to efficiently process 1B rows without loading entire file into memory
# DuckDB uses a streaming CSV parser and on-disk aggregation to keep memory usage low
result <- DBI::dbGetQuery(con, "
  SELECT 
    station,
    MIN(temperature)::FLOAT as min_temp,
    AVG(temperature)::FLOAT as mean_temp,
    MAX(temperature)::FLOAT as max_temp
  FROM read_csv_auto('measurements.txt', sep=';', header=false, 
                      columns={'station': 'VARCHAR', 'temperature': 'FLOAT'})
  GROUP BY station
  ORDER BY station
")

# Format output as required: {Station=min/mean/max, Station=min/mean/max, ...}
output_str <- paste0(
  "{",
  paste0(
    result$station,
    "=",
    sprintf("%.1f", result$min_temp),
    "/",
    sprintf("%.1f", result$mean_temp),
    "/",
    sprintf("%.1f", result$max_temp),
    collapse = ", "
  ),
  "}"
)

# Write to file
writeLines(output_str, "result_R.txt")

# Also print to console
cat(output_str, "\n")

# Close connection
DBI::dbDisconnect(con)
duckdb::duckdb_shutdown(db)
