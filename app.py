# pylint: disable=missing-module-docstring
# pylint: disable=unspecified-encoding
# pylint: disable=exec-used

import logging
import os
from datetime import date, timedelta

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


def check_users_solution(user_query: str) -> bool:
    """
    Checks that user SQL query is correct by:
    1: checking the columns
    2: checking the values
    :param user_query: a string containing the query inserted by the user
    Returns True if solution is right, returns False in any others cases
    """
    result = con.execute(user_query).df()
    st.dataframe(result)
    if len(result.columns) != len(
        solution_df.columns
    ):  # replace with try result = result[solution_df.columns]
        st.write("Some columns are missing")
        return False
    try:
        result = result[solution_df.columns]
        # st.dataframe(result.compare(solution_df))
        result.compare(solution_df)
    except KeyError:
        st.write("Some columns are missing or with bad values")
        return False
    n_lines_difference = result.shape[0] - solution_df.shape[0]
    if n_lines_difference != 0:
        st.write(
            f"Result has a {n_lines_difference} lines difference with the solution_df"
        )
        return False
    return True


def manage_update_button(recall_nb_days: int, local_exercise_name) -> None:
    """
    Depending on the button used indicating the revision time, new revision date is updated
    in the memory_state table.
    :recall_nb_days: Nb days to add at the current revision date
    :local_exercise_name: Exercise name in the memory_state table
    """
    if recall_nb_days == 0:
        if st.button("Reset"):
            con.execute(
                """
                UPDATE memory_state 
                SET last_reviewed = '1970-01-01'
                """
            )
            st.rerun()
    else:
        if st.button(f"Review in {recall_nb_days} days"):
            next_review = date.today() + timedelta(days=recall_nb_days)
            con.execute(
                f"""
                UPDATE memory_state 
                SET last_reviewed = '{next_review}'
                WHERE exercise_name = '{local_exercise_name}'
                """
            )
            st.rerun()


with st.sidebar:
    list_theme_df = con.execute("SELECT DISTINCT theme FROM memory_state").df()
    theme = st.selectbox(
        "What would you like to revise?",
        #         ("cross_joins", "Group By", "Windows Functions"),
        list_theme_df["theme"].unique(),
        index=None,
        placeholder="Select a theme...",
    )
    if theme:
        st.write("You selected:", theme)
        SELECT_EXCERCISE_QUERY = f"SELECT * from memory_state WHERE theme = '{theme}'"
    else:
        SELECT_EXCERCISE_QUERY = "SELECT * from memory_state"
    exercise = (
        con.execute(SELECT_EXCERCISE_QUERY)
        .df()
        .sort_values("last_reviewed")
        .reset_index()
    )
    st.write(exercise)
    exercise_name = exercise.loc[0, "exercise_name"]

    # Get and display answer file
    ANSWER_FILE = f"answers/{exercise_name}.sql"
    with open(
        ANSWER_FILE,
        "r",
    ) as f:
        answer_str = f.read()
    solution_df = con.execute(answer_str).df()

    # Get and display question file
    QUESTION_FILE = f"questions/{exercise_name}.txt"
    with open(
        QUESTION_FILE,
        "r",
    ) as f:
        question_str = f.read()

st.header("Train your SQL code :point_down:")
st.text(f"Instructions : \n {question_str}")
form = st.form("my_form")
query = form.text_area(label="Your SQL code here", key="user_input")
form.form_submit_button("Submit")

if query:
    if check_users_solution(query):
        st.write("Good job ! You're the boss :wave:")

col0, col2, col7, col21 = st.columns(4)

with col0:
    manage_update_button(0, exercise_name)
with col2:
    manage_update_button(2, exercise_name)
with col7:
    manage_update_button(7, exercise_name)
with col21:
    manage_update_button(21, exercise_name)

tab2, tab3 = st.tabs(["Tables", "Solution"])

with tab2:
    exercise_tables = exercise.loc[0, "tables"]
    for table in exercise_tables:
        st.write(f"Table : {table}")
        df_table = con.execute(f"SELECT * FROM {table}").df()
        st.dataframe(df_table)

with tab3:
    st.text(answer_str)
