# pylint: disable=missing-module-docstring

import ast
import duckdb
import streamlit as st

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

with st.sidebar:
    theme = st.selectbox(
        "What would you like to revise?",
        ("cross_joins", "Group By", "Windows Functions"),
        index=None,
        placeholder="Select a theme...",
    )
    st.write("You selected:", theme)

    exercise = con.execute(f"SELECT * from memory_state WHERE theme = '{theme}'").df()
    st.write(exercise)

st.header("Saisir votre code:")
query = st.text_area(label="Votre code SQL ici", key="user_input")
if query:
    result = con.execute(query).df()
    st.dataframe(result)

    # if len(result.columns) != len(
    #     solution_df.columns
    # ):  # replace with try result = result[solution_df.columns]
    #     st.write("Some columns are missing")
    #
    # try:
    #     result = result[solution_df.columns]
    #     st.dataframe(result.compare(solution_df))
    # except KeyError as e:
    #     st.write("Some columns are missing")
    #
    # n_lines_difference = result.shape[0] - solution_df.shape[0]
    # if n_lines_difference != 0:
    #     st.write(
    #         f"Result has a {n_lines_difference} lines difference with the solution_df"
    #     )


tab2, tab3 = st.tabs(["Tables", "Solution"])

with tab2:
    exercise_tables = ast.literal_eval(exercise.loc[0, 'tables'])
    for table in exercise_tables:
        st.write(f"Table : {table}")
        df_table = con.execute(f"SELECT * FROM {table}").df()
        st.dataframe(df_table)

with tab3:
    answer_file = f"answers/{exercise.loc[0, 'exercise_name']}.sql"
    with open(answer_file, "r") as f:
        ANSWER_STR = f.read()
    st.write(ANSWER_STR)
