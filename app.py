# pylint: disable=missing-module-docstring
# pylint: disable=unspecified-encoding
# pylint: disable=exec-used

import logging
import os
import duckdb
import streamlit as st

if "data" not in os.listdir():
    print("creating folder data - print")
    logging.error(os.listdir())
    logging.error("creating folder data - logging")
    os.mkdir("data")

if "exercises_sql_tables.duckdb" not in os.listdir("data"):
    with open("init_db.py", "r") as idb:
        exec(idb.read())

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

with st.sidebar:
    theme = st.selectbox(
        "What would you like to revise?",
        ("cross_joins", "Group By", "Windows Functions"),
        index=None,
        placeholder="Select a theme...",
    )
    st.write("You selected:", theme)

    exercise = (
        con.execute(f"SELECT * from memory_state WHERE theme = '{theme}'")
        .df()
        .sort_values("last_reviewed")
        .reset_index()
    )
    st.write(exercise)
    ANSWER_FILE = f"answers/{exercise.loc[0, 'exercise_name']}.sql"
    with open(
        ANSWER_FILE,
        "r",
    ) as f:
        answer_str = f.read()
    solution_df = con.execute(answer_str).df()

st.header("Enter your code:")
query = st.text_area(label="Your code here", key="user_input")
if query:
    result = con.execute(query).df()
    st.dataframe(result)

    if len(result.columns) != len(
        solution_df.columns
    ):  # replace with try result = result[solution_df.columns]
        st.write("Some columns are missing")

    try:
        result = result[solution_df.columns]
        st.dataframe(result.compare(solution_df))
    except KeyError as e:
        st.write("Some columns are missing")

    n_lines_difference = result.shape[0] - solution_df.shape[0]
    if n_lines_difference != 0:
        st.write(
            f"Result has a {n_lines_difference} lines difference with the solution_df"
        )

tab2, tab3 = st.tabs(["Tables", "Solution"])

with tab2:
    exercise_tables = exercise.loc[0, "tables"]
    for table in exercise_tables:
        st.write(f"Table : {table}")
        df_table = con.execute(f"SELECT * FROM {table}").df()
        st.dataframe(df_table)

with tab3:
    st.write(answer_str)
