import io
import pandas as pd
import duckdb

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

# ------------------------------------------------------------
# CROSS JOIN EXERCISES
# ------------------------------------------------------------
csv = """
beverage,price
orange juice,2.5
Expresso,2
Tea,3
"""
beverages = pd.read_csv(io.StringIO(csv))
con.execute("CREATE TABLE IF NOT EXISTS beverages AS SELECT * FROM beverages")

csv2 = """
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
"""
food_items = pd.read_csv(io.StringIO(csv2))
con.execute("CREATE TABLE IF NOT EXISTS food_items AS SELECT * FROM food_items")


# sizes = """
# size
# XS
# M
# L
# XL
# """
# sizes = pd.read_csv(io.StringIO(sizes))
# con.execute("CREATE TABLE IF NOT EXISTS sizes AS SELECT * FROM sizes")
#
# trademarks = """
# trademark
# Nike
# Asphalte
# Abercrombie
# Lewis
# """
# trademarks = pd.read_csv(io.StringIO(trademarks))
# con.execute("CREATE TABLE IF NOT EXISTS trademarks AS SELECT * FROM trademarks")

# ------------------------------------------------------------
# EXERCISES LIST
# ------------------------------------------------------------

data = {
   "theme": ["cross_joins", "window_functions"],
   "exercise_name": ["beverages_and_food", "simple_window"],
   "tables": [["beverages", "food_items"], "simple_window"],
   "last_reviewed": ["1980-01-01", "1980-01-01"],
}
memory_state_df = pd.DataFrame(data)
con.execute("CREATE OR REPLACE TABLE memory_state AS SELECT * FROM memory_state_df")

con.close()