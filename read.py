import pandas as pd
from sqlalchemy import create_engine, text
import streamlit as st
connection_string = st.secrets["connection_string"]


def read_friends():
    query = """
        SELECT *
        FROM friends
    """
    return pd.read_sql(query,con=connection_string)


def read_books():
    query = """
        SELECT *
        FROM books
    """
    return pd.read_sql(query,con=connection_string)


def read_loans():
    query = """
        SELECT *
        FROM loans
    """
    return pd.read_sql(query,con=connection_string)



def read_summary():
    available_books = pd.read_sql("SELECT COUNT(*) as count FROM books WHERE is_available = 1", con=connection_string)
    total_books = pd.read_sql("SELECT COUNT(*) as count FROM books", con=connection_string)
    total_friends = pd.read_sql("SELECT COUNT(*) as count FROM friends", con=connection_string)
    active_loans = pd.read_sql("SELECT COUNT(*) as count FROM loans WHERE date_returned IS NULL", con=connection_string)
    
    return {
        "available_books": available_books["count"][0],
        "total_books": total_books["count"][0],
        "total_friends": total_friends["count"][0],
        "active_loans": active_loans["count"][0]
    }

def read_books_on_loan():
    query = """
        SELECT 
            l.loan_id,
            b.title,
            b.author,
            f.first_name,
            f.last_name,
            l.date_borrowed,
            l.due_date,
            l.remarks
        FROM loans l
        JOIN books b ON l.book_id = b.book_id
        JOIN friends f ON l.friend_id = f.friend_id
        WHERE l.date_returned IS NULL
    """
    return pd.read_sql(query, con=connection_string)
