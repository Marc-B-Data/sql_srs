# pylint: disable=missing-module-docstring

import io
import pandas as pd
import duckdb

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

# ------------------------------------------------------------
# CROSS JOIN EXERCISES
# ------------------------------------------------------------
CSV = """
beverage,price
orange juice,2.5
Expresso,2
Tea,3
"""
beverages = pd.read_csv(io.StringIO(CSV))
con.execute("CREATE TABLE IF NOT EXISTS beverages AS SELECT * FROM beverages")

CSV2 = """
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
"""
food_items = pd.read_csv(io.StringIO(CSV2))
con.execute("CREATE TABLE IF NOT EXISTS food_items AS SELECT * FROM food_items")

SIZES = """
size
XS
M
L
XL
"""
sizes = pd.read_csv(io.StringIO(SIZES))
con.execute("CREATE TABLE IF NOT EXISTS sizes AS SELECT * FROM sizes")

TRADEMARKS = """
trademark
Nike
Asphalte
Abercrombie
Lewis
"""
trademarks = pd.read_csv(io.StringIO(TRADEMARKS))
con.execute("CREATE TABLE IF NOT EXISTS trademarks AS SELECT * FROM trademarks")

# ------------------------------------------------------------
# EXERCISES LIST
# ------------------------------------------------------------

DATA = {
    "theme": ["cross_joins", "cross_joins"],
    "exercise_name": ["beverages_and_food", "sizes_and_trademarks"],
    "tables": [["beverages", "food_items"], ["sizes", "trademarks"]],
    "last_reviewed": ["1970-01-01", "1970-01-01"],
}
memory_state_df = pd.DataFrame(DATA)
con.execute("CREATE OR REPLACE TABLE memory_state AS SELECT * FROM memory_state_df")

con.close()
