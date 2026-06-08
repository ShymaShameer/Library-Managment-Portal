import streamlit as st
import pandas as pd
from datetime import date
from create import *
from read import *
from update import *
from delete import *


# Title
st.title("Library Management")
st.header("Welcome to the Book Haven!", divider="gray")

# Markdown
st.markdown("""
<p style="font-style: italic; font-size: 20px;">
A cozy corner for every book lover 📚✨  <br>

Discover, organize, and manage your personal library with ease — where every book finds its place and every reader finds their next adventure.
</p>
""", unsafe_allow_html=True)
st.markdown("---")
import streamlit as st

# 1. Inject custom CSS to remove the default padding inside the sidebar element
st.markdown(
    """
    <style>
        /* Target the internal padding container of the sidebar */
        [data-testid="stSidebarUserContent"] {
            padding-top: 0rem;
            padding-left: 0rem;
            padding-right: 0rem;
        }
        
        /* Optional: Ensure the image hugs the very edges smoothly */
        [data-testid="stSidebarUserContent"] img {
            border-radius: 0px;
            width: 100% !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# 2. Build your sidebar content
with st.sidebar:
    # This image will now span completely from the left edge to the right edge!
    st.image(
        "https://images.unsplash.com/photo-1513001900722-370f803f498d?q=80&w=600", 
        use_container_width=False
    )
    
    # Add a little HTML padding below the image so your text features don't hug the edges
    st.markdown("<div style='padding: 0px 20px;'>", unsafe_allow_html=True)

    
    dropdown_value = st.selectbox("Main Navigation", ["Dashboard","Books", "Friends", "Loans"])
    st.markdown("---")
    st.caption("Version 1.0.0")
    
    st.markdown("</div>", unsafe_allow_html=True)
    


#dropdown_value = st.selectbox("Navigate To:", ["Books", "Friends", "Loans"])

if dropdown_value == "Dashboard":
    st.header("🔖  Library Dashboard 📚")
    
    try:
        summary = read_summary()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(label="📚 Total Books", value=summary["total_books"])
        with col2:
            st.metric(label="✅ Available Books", value=summary["available_books"])
        with col3:
            st.metric(label="👥 Total Friends", value=summary["total_friends"])
        with col4:
            st.metric(label="🔄 Active Loans", value=summary["active_loans"])
            

        st.divider()
        
        # --- BOOKS OUT ON LOAN ---
        st.markdown("### 📖 Books Currently Out on Loan")
        df_on_loan = read_books_on_loan()
        
        if not df_on_loan.empty:
            df_on_loan.index = df_on_loan.index + 1
            st.dataframe(df_on_loan, use_container_width=True)
        else:
            st.info("✅ No books are currently out on loan.")
            
    except Exception as e:
        st.error(f"Error loading dashboard: {e}")
# -------------------------------------------------------------------------
# SECTION 1: BOOKS
# -------------------------------------------------------------------------

 
elif dropdown_value == "Books":
    st.header("📚 Books Management")
    action = st.radio("What would you like to do?", ["Review Books", "Update Books", "Add a book", "Remove a book"])
    
    # --- ACTION 1: ADD A BOOK ---
    if action == "Add a book":
        st.subheader("Add a New Book to Inventory")
        
        st.markdown("<p style='color: red; font-size: 13px;'>* Required fields</p>", unsafe_allow_html=True)
        # Creating the form inputs
        with st.form("add_book_form", clear_on_submit=True):
            title = st.text_input("Book Title *")
            author = st.text_input("Author *")
            isbn = st.text_input("ISBN Number")
            genre = st.text_input("Genre")
            comments = st.text_area("Comments")
            
            submit_book = st.form_submit_button("Save Book")
            
            if submit_book:
                if title and author:
                    if isbn and (len(isbn) < 10 or len(isbn) > 13):
                        st.error("⚠️ ISBN must be between 10 and 13 characters.")
                    try:
                        msg = create_book(
                            title=title,
                            author=author,
                            isbn=isbn,
                            genre=genre,
                            comments=comments,
                            is_available=True  
                        )
                        st.success(f"🎉 '{title}' by {author} successfully added!")
                        
                    except Exception as e:
                        st.error(f"Database Error: Could not save book. {e}")
                        
                else:
                    st.error("Title and Author are required fields.")
    
    # --- ACTION 2: REVIEW BOOKS ---
    elif action == "Review Books":
        st.subheader("Current Book Inventory")
        try:
            df_books = read_books()
            df_books = df_books.reset_index(drop=True)
            df_books.index = df_books.index + 1
            
            # Check if the database has data
            if not df_books.empty:
                
                st.dataframe(df_books, use_container_width=True)
            else:
                st.info("The books catalog is currently empty.")
        except Exception as e:
            st.error(f"Error fetching books: {e}")
            
    # --- ACTION 3: UPDATE BOOKS ---
    
    elif action == "Update Books":
        st.subheader("Modify Book Details")
        st.markdown("<p style='color: red; font-size: 13px;'>* Required fields</p>", unsafe_allow_html=True)

    # Fetch books for dropdown
        try:
            df_books = read_books()
            book_options = {
                f"{row['title']} (ID: {row['book_id']})": row['book_id']
                for _, row in df_books.iterrows()
            }
        except Exception as e:
            st.error(f"Error loading books: {e}")
            st.stop()

    # Search box outside the form
        search_term = st.text_input("🔍 Search Book by Title *", placeholder="Start typing a book name...")

    # Filter options based on search term
        filtered_options = [
            name for name in book_options.keys()
            if search_term.lower() in name.lower()
        ] if search_term else []

        with st.form("update_book_form"):
            if not search_term:
                st.caption("🔍 Type in the search box above to find a record.")
                selected_item = None
            elif filtered_options:
                selected_book = st.selectbox("Select Book to Update *", options=filtered_options)
            else:
                st.warning("No books found matching your search.")
                selected_book = None
            

            st.caption("Fill out only the fields you wish to alter. Leave others blank.")
            title = st.text_input("New Title")
            author = st.text_input("New Author")
            isbn = st.text_input("New ISBN")
            genre = st.text_input("New Genre")
            comments = st.text_area("New Comments")
            status_action = st.radio("Update Availability?", ["No Change", "Available", "Unavailable"])

            submit_update = st.form_submit_button("Apply Changes")

        if submit_update and selected_book:
            book_id = book_options[selected_book]
            is_available = True if status_action == "Available" else False if status_action == "Unavailable" else None

            if isbn and (len(isbn) < 10 or len(isbn) > 13):
                st.error("⚠️ ISBN must be between 10 and 13 characters.")
            else:
                try:
                    msg = update_book(book_id, title, author, isbn, genre, comments, is_available)
                    st.success(msg)
                except Exception as e:
                    st.error(str(e)) 

    # --- ACTION 4: REMOVE A BOOK ---
    elif action == "Remove a book":
        st.subheader("Remove a Book from Inventory")
        st.markdown("<p style='color: red; font-size: 13px;'>* Required fields</p>", unsafe_allow_html=True)
        
        # Soft warning callout for destructive actions
        st.warning("⚠️ Warning: Deleting a book is permanent and cannot be undone!")


         # Fetch books for dropdown
        try:
            df_books = read_books()
            book_options = {
                f"{row['title']} (ID: {row['book_id']})": row['book_id']
                for _, row in df_books.iterrows()
            }
        except Exception as e:
            st.error(f"Error loading books: {e}")
            st.stop()
        # Search box outside the form
        search_term = st.text_input("🔍 Search Book by Title *", placeholder="Start typing a book name...")

        # Filter options based on search term
        filtered_options = [
            name for name in book_options.keys()
            if search_term.lower() in name.lower()
        ] if search_term else []
    
        with st.form("delete_book_form", clear_on_submit=True):
            if not search_term:
                st.caption("🔍 Type in the search box above to find a record.")
                selected_item = None
            elif filtered_options:
                selected_book = st.selectbox("Select Book to Remove *", options=filtered_options)
            else:
                st.warning("No books found matching your search.")
                selected_book = None
            
            # Double-check confirmation checkbox to prevent accidental clicks
            confirm_delete = st.checkbox("I confirm that I want to permanently delete this book entry.")
            
            submit_deletion = st.form_submit_button("Delete Book Entry")
            
            if submit_deletion and selected_book:
                book_id_to_delete = book_options[selected_book]
                if confirm_delete:
                    try:
                        # Call your backend deletion logic
                        msg = delete_book(book_id=book_id_to_delete)
                        st.success(msg)
                    except ValueError as val_err:
                        st.error(str(val_err))
                    except Exception as e:
                        st.error(f"Database Error: Could not complete deletion. {e}")
                else:
                    st.info("Deletion canceled. You must check the confirmation box to proceed.")   
                    
# -------------------------------------------------------------------------
# SECTION 2: FRIENDS 
# -------------------------------------------------------------------------

      # ACTION 1: ADD FRIENDS 
elif dropdown_value == "Friends":
    st.header("👥 Friends Directory")
    action = st.radio("What would you like to do?", ["Review Friends", "Update Friends", "Add a friend", "Remove a friend"])
    
    if action == "Add a friend":
        st.subheader("Register a New Friend")
        st.markdown("<p style='color: red; font-size: 13px;'>* Required fields</p>", unsafe_allow_html=True)
        with st.form("add_friend_form", clear_on_submit=True):
            first_name = st.text_input("First Name *")
            last_name = st.text_input("Last Name *")
            email = st.text_input("Email Address *")
            phone = st.text_input("Phone Number *")
            max_loan = st.number_input("Max Books Allowed to Borrow", min_value=1, value=2, step=1)
            notes = st.text_area(" Notes")
            
            submit_friend = st.form_submit_button("Add Friend")
            
            if submit_friend:
                if first_name and last_name and phone and email:
                    create_friend(first_name,last_name,email,phone, max_loan=2, notes=None)
                    st.success(f"🤝 {first_name} {last_name} added to your friend list!")
                else:
                    st.error("Full name and contact details are required.")
                    
    # ACTION 2 : REVIEW FRIENDS
    elif action == "Review Friends":
        st.subheader("Registered Friends List")
        try:
            # 1. Fetch data from your database logic file
            df_friends = read_friends()
            df_friends = df_friends.reset_index(drop=True)
            df_friends.index = df_friends.index + 1
            # 2. Render it inside Streamlit if it contains data
            if not df_friends.empty:
                st.dataframe(df_friends, use_container_width=True)
            else:
                st.info("No friends have been registered in the database yet.")
        except Exception as e:
            st.error(f"Error fetching friends: {e}")


     # ACTION 3 : UPDATE FRIENDS           
    elif action == "Update Friends":
        st.subheader("Modify Friend Contact Details")
        st.markdown("<p style='color: red; font-size: 13px;'>* Required fields</p>", unsafe_allow_html=True)


        # Fetch friends for dropdown
        try:
            df_friends = read_friends()
            friend_options = {
                f"{row['first_name']} {row['last_name']} (ID: {row['friend_id']})": row['friend_id']
                for _, row in df_friends.iterrows()
            }
        except Exception as e:
            st.error(f"Error loading friends: {e}")
            st.stop()
    # Search box outside the form
        search_term = st.text_input("🔍 Search Friend by Name *", placeholder="Start typing a friend's name...")

    # Filter options based on search term
        filtered_options = [
            name for name in friend_options.keys()
            if search_term.lower() in name.lower()
        ] if search_term else []


        
        with st.form("update_friend_form", clear_on_submit=True):
            if not search_term:
                st.caption("🔍 Type in the search box above to find a record.")
                selected_item = None
            elif filtered_options:
                selected_friend = st.selectbox("Select Friend to Update *", options=filtered_options)
            else:
                st.warning("No friends found matching your search.")
                selected_friend = None
            #st.markdown("---")
            st.caption("Fill out *only* the fields you wish to change. Leave everything else blank!")
            
            # Form input fields
            new_first_name = st.text_input("New First Name")
            new_last_name = st.text_input("New Last Name")
            new_email = st.text_input("New Email Address")
            new_phone = st.text_input("New Phone Number")
            new_max_loan= st.text_input ("New Max Loans")
            new_notes= st.text_input("New Notes")
            
            submit_friend_update = st.form_submit_button("Update Friend Profile")
            
            if submit_friend_update and selected_friend:
                friend_id_to_update = friend_options[selected_friend]
                # Use inline conditional checks to pass None if the text fields are empty strings
                try:
                    msg = update_friend(
                        friend_id=friend_id_to_update,
                        first_name=new_first_name if new_first_name.strip() else None,
                        last_name=new_last_name if new_last_name.strip() else None,
                        email=new_email if new_email.strip() else None,
                        phone=new_phone if new_phone.strip() else None,
                        max_loan= new_max_loan if new_max_loan.strip() else None,
                        notes= new_notes if new_notes.strip() else None,
                    )
                    
                    # If updates list was empty, our function returns None (or you can customize a string return)
                    if msg:
                        st.success(msg)
                    else:
                        st.info("No modifications were submitted.")
                        
                except Exception as e:
                    st.error(f"Database Error: Could not update friend profile. {e}")      


     # ACTION 4 : DELETE FRIENDS  
    elif action == "Remove a friend":
        st.subheader("🗑️ Remove a Friend from Directory")
        st.markdown("<p style='color: red; font-size: 13px;'>* Required fields</p>", unsafe_allow_html=True)
        st.warning("⚠️ Warning: Deleting a friend is permanent. Ensure they don't have any active loans outstanding!")
    # Fetch friends for dropdown
        try:
            df_friends = read_friends()
            friend_options = {
                f"{row['first_name']} {row['last_name']} (ID: {row['friend_id']})": row['friend_id']
                for _, row in df_friends.iterrows()
            }
        except Exception as e:
            st.error(f"Error loading friends: {e}")
            st.stop()
    # Search box outside the form
        search_term = st.text_input("🔍 Search Friend by Name *", placeholder="Start typing a friend's name...")

    # Filter options based on search term
        filtered_options = [
            name for name in friend_options.keys()
            if search_term.lower() in name.lower()
        ] if search_term else []


        with st.form("delete_friend_form", clear_on_submit=True):
            if not search_term:
                st.caption("🔍 Type in the search box above to find a record.")
                selected_item = None
            elif filtered_options:
                selected_friend = st.selectbox("Select Friend to Remove *", options=filtered_options)
            else:
                st.warning("No friends found matching your search.")
                selected_friend = None
                
            confirm_friend_delete = st.checkbox("I confirm that I want to permanently delete this friend's profile.")
            submit_deletion = st.form_submit_button("Delete Friend Profile")
            
            if submit_deletion and selected_friend:
                friend_id_to_delete = friend_options[selected_friend]
                if confirm_friend_delete:
                    try:
                        msg = delete_friend(friend_id=friend_id_to_delete)
                        st.success(msg)
                    except ValueError as val_err:
                        st.error(str(val_err))
                    except Exception as e:
                        st.error(f"Database Error: {e}")
                else:
                    st.info("Deletion canceled. You must check the confirmation box to proceed.")   

                    
# -------------------------------------------------------------------------
# SECTION 3: LOANS
# -------------------------------------------------------------------------

    # ACTION 1: ADD LOANS 
elif dropdown_value == "Loans":
    st.header("🔄 Loan Register")
    action = st.radio("What would you like to do?", ["Review Loans", "Loan a book", "Update a Loan", "Remove a Loan"])
    
    if action == "Loan a book":
        st.subheader("Log a New Book Loan")
        st.markdown("<p style='color: red; font-size: 13px;'>* Required fields</p>", unsafe_allow_html=True)

        try:
            df_books = read_books()
            df_friends = read_friends()
            # Filter only available books
            df_available_books = df_books[df_books["is_available"] == 1]
    
            if df_available_books.empty:
                st.warning("⚠️ No books are currently available for loan.")
                st.stop()

                
            book_options = {
                f"{row['title']} (ID: {row['book_id']})": row['book_id']
                for _, row in df_books.iterrows()
            }
            friend_options = {
                f"{row['first_name']} {row['last_name']} (ID: {row['friend_id']})": row['friend_id']
                for _, row in df_friends.iterrows()
            }
        
        except Exception as e:
            st.error(f"Error loading books/friends: {e}")
            st.stop()

    # Search boxes outside the form
        book_search = st.text_input("🔍 Search Book by Title *", placeholder="Start typing a book name...")
        friend_search = st.text_input("🔍 Search Friend by Name *", placeholder="Start typing a friend's name...")

    # Filter options
        filtered_books = [
            name for name in book_options.keys()
            if book_search.lower() in name.lower()
        ] if book_search else []

        filtered_friends = [
            name for name in friend_options.keys()
            if friend_search.lower() in name.lower()
        ] if friend_search else []

        with st.form("loan_form", clear_on_submit=True):
            if not book_search:
                st.caption("🔍 Type in the search box above to find a record.")
                selected_item = None
            elif filtered_books:
                selected_book = st.selectbox("Select Book *", options=filtered_books)
            else:
                st.warning("No books found matching your search.")
                selected_book = None
            
            if not friend_search:
                
                selected_item = None

            elif filtered_friends:
                selected_friend = st.selectbox("Select Friend *", options=filtered_friends)
            else:
                st.warning("No friends found matching your search.")
                selected_friend = None
                
            due_date = st.date_input("Due Date", value=date.today() + pd.Timedelta(days=14))
            remarks = st.text_input("Remarks")
            submit_loan = st.form_submit_button("Issue Book")
    
        if submit_loan and selected_book and selected_friend:
            book_id = book_options[selected_book]
            friend_id = friend_options[selected_friend]
            mock_book = {"book_id": book_id}
            mock_friend = {"friend_id": friend_id}
                
            try:
                    msg = create_loan(
                        book=mock_book,
                        friend=mock_friend,
                        loan_status="BORROWED",
                        due_date=due_date,
                        date_returned=None,
                        remarks=remarks
                    )
                    st.success(msg)
            except ValueError as e:
                    st.error(str(e))
            except Exception as ex:
                    st.error(f"An unexpected database error occurred: {ex}")
                    
    # ACTION 2: REVIEW LOANS
    if action == "Review Loans":
        st.subheader("Active and Past Book Loans")
        try:
            # 1. Fetch data from your database logic file
            df_loans = read_loans()
            df_loans = df_loans.reset_index(drop=True)
            df_loans.index = df_loans.index + 1
            
            # 2. Render it inside Streamlit if it contains data
            if not df_loans.empty:
                st.dataframe(df_loans, use_container_width=True)
            else:
                st.info("There are no loan records to display.")
        except Exception as e:
            st.error(f"Error fetching loans: {e}")
            

    # ACTION 3: UPDATE LOANS
    elif action == "Update a Loan":
        st.subheader("Process Returns or Modify Active Loans")
        st.markdown("<p style='color: red; font-size: 13px;'>* Required fields</p>", unsafe_allow_html=True)
        
        
          # Fetch active loans with book title and friend name
        try:
            df_active_loans = read_books_on_loan()
        
            if df_active_loans.empty:
                st.info("✅ No active loans to update.")
                st.stop()
        
        # Create dropdown options: "Book Title — Friend Name (Loan ID: X)"
            loan_options = {
            f"{row['title']} — {row['first_name']} {row['last_name']} (Loan ID: {row['loan_id']})": row['loan_id']
            for _, row in df_active_loans.iterrows()
            }

        except Exception as e:
            st.error(f"Error loading active loans: {e}")
            st.stop()

    # Search box outside the form
        search_term = st.text_input("🔍 Search by Book Title or Friend Name *", placeholder="Start typing to filter loans...")

    # Filter options
        filtered_options = [
            name for name in loan_options.keys()
            if search_term.lower() in name.lower()
        ] if search_term else []

            
        with st.form("update_loan_form", clear_on_submit=True):
            if not search_term:
                st.caption("🔍 Type in the search box above to find a record")
                selected_item = None
            elif filtered_options:
                selected_loan = st.selectbox("Select Loan to Update *", options=filtered_options)
            else:
                st.warning("No loans found matching your search.")
                selected_loan = None
            

        # Form fields
            new_status = st.selectbox("Change Loan Status:", ["No Change", "BORROWED", "RETURNED", "OVERDUE"])
            log_return_today = st.checkbox("Mark Book as Returned Today?")
            custom_return_date = st.date_input("Or Pick a Specific Return Date", value=None)
            new_remarks = st.text_input("Add/Update Remarks")

            submit_loan_update = st.form_submit_button("Save Loan Changes")

        if submit_loan_update and selected_loan:
            loan_id_to_update = loan_options[selected_loan]

            try:
                status_arg = None if new_status == "No Change" else new_status
                if log_return_today:
                    return_date_arg = date.today()
                elif custom_return_date is not None:
                    return_date_arg = custom_return_date
                else:
                    return_date_arg = None
                remarks_arg = new_remarks if new_remarks.strip() else None

                msg = update_loan(
                    loan_id=loan_id_to_update,
                    loan_status=status_arg,
                    date_returned=return_date_arg,
                    remarks=remarks_arg
                )
                st.success(msg)

            except ValueError as val_err:
                st.warning(str(val_err))
            except Exception as e:
                st.error(f"Database Error: {e}")


     # ACTION 4 : DELETE LOAN  
    elif action == "Remove a Loan": # Swap or extend this block condition if you name your radio action "Remove a loan" instead
        st.subheader("🗑️ Remove a Loan Record")
        st.markdown("<p style='color: red; font-size: 13px;'>* Required fields</p>", unsafe_allow_html=True)
        st.warning("⚠️ Warning: Deleting a loan record is permanent and will remove historical logging for this transaction!")

         # Fetch all loans with book title and friend name
        try:
            df_loans = read_books_on_loan()
            df_all_loans = read_loans()

        # Combine active and returned loans for full list
            loan_options = {
                f"{row['title']} — {row['first_name']} {row['last_name']} (Loan ID: {row['loan_id']})": row['loan_id']
                for _, row in df_loans.iterrows()
            }

            if not loan_options:
                st.info("No loan records found.")
                st.stop()

        except Exception as e:
            st.error(f"Error loading loans: {e}")
            st.stop()
    # Search box outside the form
        search_term = st.text_input("🔍 Search by Book Title or Friend Name *", placeholder="Start typing to filter loans...")

    # Filter options
        filtered_options = [
            name for name in loan_options.keys()
            if search_term.lower() in name.lower()
        ] if search_term else []
        
        with st.form("delete_loan_form", clear_on_submit=True):
            if not search_term:
                st.caption("🔍 Type in the search box above to find a record.")
                selected_item = None
            
            elif filtered_options:
                selected_loan = st.selectbox("Select Loan Record to Remove *", options=filtered_options)
            else:
                st.warning("No loans found matching your search.")
                selected_loan = None

            confirm_loan_delete = st.checkbox("I confirm that I want to permanently delete this loan record.")
            submit_deletion = st.form_submit_button("Delete Loan Record")
            
            if submit_deletion and selected_loan:
                loan_id_to_delete = loan_options[selected_loan]
                if confirm_loan_delete:
                    try:
                        msg = delete_loan(loan_id=loan_id_to_delete)
                        st.success(msg)
                    except ValueError as val_err:
                        st.error(str(val_err))
                    except Exception as e:
                        st.error(f"Database Error: {e}")
                else:
                    st.info("Deletion canceled. You must check the confirmation box to proceed.")
