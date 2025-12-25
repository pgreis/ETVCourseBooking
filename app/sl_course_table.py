#!/usr/bin/env python
#coding: utf-8

import streamlit as st
import os
import sys
import yaml
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env")
with open(file="app/app_config.yaml",
          mode="r",
          encoding="utf-8") as f:
    config = yaml.safe_load(f)
column_cfg = config["column_config"]

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.utils.db.db_handling import DatabaseHandler

st.title("ETV course list")

if "last_interaction_default_restore" not in st.session_state:
    st.session_state.last_interaction_default_restore = False

if "database" not in st.session_state:
    with st.spinner("Loading course table..."):
        st.session_state.database = DatabaseHandler(db_url=os.getenv("DB_URL"))

menu = st.sidebar.selectbox("Choose an action", ["Change automation", "Restore default settings"])

if menu == "Change automation":
    
    if "loaded_table" not in st.session_state or st.session_state.last_interaction_default_restore: # reload if default table was restored
        st.session_state.database.load_table(table_name=st.session_state.database.table_name)
        st.session_state.loaded_table = st.session_state.database.loaded_table
    
    st.session_state.edited_table = st.data_editor(data=st.session_state.loaded_table,
                                                   hide_index=True,
                                                   column_config={"weekday_ger_abb": st.column_config.SelectboxColumn(
                                                       column_cfg["weekday_ger_abb"]["label"],
                                                       help=column_cfg["weekday_ger_abb"]["help"],
                                                       options=column_cfg["weekday_ger_abb"]["options"],
                                                       required=True
                                                       ),
                                                         "person": st.column_config.TextColumn(
                                                             column_cfg["person"]["label"],
                                                             help=column_cfg["person"]["help"],
                                                             required=True
                                                             ),
                                                         "orig_course_name": st.column_config.TextColumn(
                                                             column_cfg["orig_course_name"]["label"],
                                                             help=column_cfg["orig_course_name"]["help"],
                                                             required=True
                                                             ),
                                                         "is_registration_active": st.column_config.SelectboxColumn(
                                                             column_cfg["is_registration_active"]["label"],
                                                             help=column_cfg["is_registration_active"]["help"],
                                                             required=True
                                                             )},
                                                            
                                                             )

    if st.button("Save changes"):
        with st.spinner("Exporting table..."):
            st.session_state.database.post_table(table=st.session_state.edited_table, table_name=st.session_state.database.table_name)
            st.session_state.loaded_table = st.session_state.edited_table
            st.success("Table successfully uploaded")

if menu == "Restore default settings":

    if st.button("Click to restore and upload default course table"):
            st.session_state.database.load_table(table_name=st.session_state.database.default_table_name)
            st.session_state.database.post_table(table=st.session_state.database.loaded_table,
                                                 table_name=st.session_state.database.table_name)
            st.session_state.last_interaction_default_restore = True
            st.success("Default table restored")