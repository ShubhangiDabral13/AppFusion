from tarfile import PAX_NAME_FIELDS
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import base64
import streamlit as st
from PIL import Image, ImageEnhance
from io import BytesIO

def lighten_image(image_path, brightness_factor=1.0):
    img = Image.open(image_path)
    enhancer = ImageEnhance.Brightness(img)
    lightened_img = enhancer.enhance(brightness_factor)
    return lightened_img

def get_base64_from_image(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def set_background(image_path, brightness_factor= 0.99):
    lightened_img = lighten_image(image_path, brightness_factor)
    base64_img = get_base64_from_image(lightened_img)
    page_bg_img = '''
    <style>
    .stApp {
        background-image: url("data:image/png;base64,%s");
        background-size: cover;
    }
    </style>
    ''' % base64_img
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background('background2.jpeg', brightness_factor= 0.99)

st.markdown('<h1 style="color: #7C0A02;">AppFusion</h1>', unsafe_allow_html=True)
st.markdown("<h3 style='color: #A45A52'> Where Apps Align with Your Desire</h3>", unsafe_allow_html=True)       

# Function to create a new app
def create_app():

    st.markdown('<h5 style="color: #7C0A02;">Create a New App</h5>', unsafe_allow_html=True)

    # Get user input for a new app
    app_id = st.text_input("App_Id")
    app_name = st.text_input("App Name")
    developer_id = st.text_input("Developer ID")
    genre = st.text_input("Genre")
    size = st.text_input("Size (MB)")
    app_version = st.text_input("App Version")
    ios_version = st.text_input("iOS Version")
    released_date = st.text_input("Released Date (YYYY-MM-DD)")
    updated_date = st.text_input("Updated Date (YYYY-MM-DD)")
    avg_user_rating = st.text_input("Average User Rating")
    age_group = st.text_input("Age Group")

    # Get additional information for developer and pricing
    developer_name = st.text_input("Developer Name")
    price = st.text_input("Price")
    currency = st.text_input("Currency")

    # Validate and add the new app, developer, and pricing to the database
    if st.button("Create App"):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        # Insert into applications table
        insert_app_query = """
            INSERT INTO applications (App_Id, App_name, Developer_Id, Genre, Size, App_version, IOS_version, Released_date, Updated_date, Avg_user_rating, Age_group)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        app_values = (
            app_id, app_name, developer_id, genre, size, app_version,
            ios_version, released_date, updated_date, avg_user_rating, age_group
        )
        c.execute(insert_app_query, app_values)

        # Insert into developers table
        insert_dev_query = """
            INSERT INTO developers (Developer_Id, Developer)
            VALUES (?, ?);
        """
        dev_values = (developer_id, developer_name)
        c.execute(insert_dev_query, dev_values)

        # Insert into pricing table
        insert_pricing_query = """
            INSERT INTO pricing (App_id, Price, Currency)
            VALUES (?, ?, ?);
        """
        pricing_values = (app_id, price, currency)
        c.execute(insert_pricing_query, pricing_values)

        conn.commit()
        conn.close()

        st.success("App created successfully!")


# Function to update an existing app
def update_app():
    st.markdown('<h5 style="color: #7C0A02;">Update an Existing App</h5>', unsafe_allow_html=True)
    #st.subheader("Update an Existing App")

    # Get user input for updating an app
    app_id = st.text_input("App ID")

    # Fetch the existing app data based on the provided App ID and display it for editing
    existing_app_data = read_data()[read_data()['App_Id'] == app_id]
        
    if existing_app_data.empty:
        st.warning("App not found. Enter a valid App ID.")
        return
    st.dataframe(existing_app_data)

    # Fetch the existing app data based on the provided App ID and display it for editing
    existing_app_data = read_data()[read_data()['App_Id'] == app_id]

    # #fetching the developer id
    developer_id = existing_app_data.iloc[0]['Developer_Id']

    # Fetching developer data from 
    dev_data = read_developer(developer_id)

    # Fetch and display data from pricing table
    pricing_data = read_pricing(existing_app_data.iloc[0]['App_Id'])



    # Get updated values from the user
    updated_app_name = st.text_input("Updated App Name", existing_app_data.iloc[0]['App_name'])
    updated_genre = st.text_input("Updated Genre", existing_app_data.iloc[0]['Genre'])
    updated_price = st.text_input("Updated Price", pricing_data.iloc[0]['Price'])  # Added line for pricing update


    if not dev_data.empty:
        updated_dev_name = st.text_input("Updated Developer Name", dev_data.iloc[0]['Developer']) 

    # Perform validation and update logic here (replace with your implementation)
    if st.button("Update App"):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        # Update applications table
        update_app_query = """
        UPDATE applications
        SET App_name=?, Genre=?
        WHERE App_Id=?;
        """
        app_values = (
            updated_app_name, updated_genre, app_id
        )
        c.execute(update_app_query, app_values)

        # Update developers table
        if not dev_data.empty:
            update_dev_query = """
            UPDATE developers
            SET Developer=?
            WHERE Developer_Id=?;
            """
            dev_values = (updated_dev_name, existing_app_data.iloc[0]['Developer_Id'])
            c.execute(update_dev_query, dev_values)

        #Update pricing table
        update_pricing_query = """
        UPDATE pricing
        SET Price=?
        WHERE App_id=?;
        """
        pricing_values = (updated_price, app_id)
        c.execute(update_pricing_query, pricing_values)

        conn.commit()
        conn.close()

        st.success("App updated successfully!")

# Function to read an existing app
def read_app():
    #st.subheader("Read an Existing App")

    # Get user input for reading an app
    app_name_to_read = st.text_input("App name to read")

    # Fetch the existing app data based on the provided App name and display it for confirmation
    existing_app_data = read_data()[read_data()['App_name'] == app_name_to_read]

    if existing_app_data.empty:
        st.warning("App not found. Enter a valid App Name.")
        return

    # Display app data
    st.markdown('<h5 style="color: #7C0A02;">Application Information</h5>', unsafe_allow_html=True)
    st.dataframe(existing_app_data)

    # Fetch Developer ID from the existing app data
    developer_id = existing_app_data.iloc[0]['Developer_Id']

    # Fetch and display data from developers table
    dev_data = read_developer(developer_id)
    if not dev_data.empty:
        st.markdown('<h5 style="color: #7C0A02;">Developer Information</h5>', unsafe_allow_html=True)
        st.dataframe(dev_data)

    # Fetch and display data from pricing table
    pricing_data = read_pricing(existing_app_data.iloc[0]['App_Id'])
    if not pricing_data.empty:
        st.markdown('<h5 style="color: #7C0A02;">Pricing Information</h5>', unsafe_allow_html=True)
        st.dataframe(pricing_data)

    # Confirm reading
    if st.button("Read App"):
        st.success("App read successfully!")

def read_developer(developer_id):
    conn = sqlite3.connect('database.db')
    dev_query = """
    SELECT * FROM developers
    WHERE Developer_Id=?;
    """
    dev_data = pd.read_sql_query(dev_query, conn, params=(developer_id,))
    conn.close()
    return dev_data

def read_pricing(app_id):
    conn = sqlite3.connect('database.db')
    pricing_query = """
    SELECT * FROM pricing
    WHERE App_id=?;
    """
    pricing_data = pd.read_sql_query(pricing_query, conn, params=(app_id,))
    conn.close()
    return pricing_data

# Function to delete an existing app
def delete_app():
    st.markdown('<h5 style="color: #7C0A02;">Delete an Existing App</h5>', unsafe_allow_html=True)
   
    # Get user input for deleting an app
    app_id_to_delete = st.text_input("App ID to Delete")

    # Fetch the existing app data based on the provided App ID and display it for confirmation
    existing_app_data = read_data()[read_data()['App_Id'] == app_id_to_delete]

    if existing_app_data.empty:
        st.warning("App not found. Enter a valid App ID.")
        return
    
    st.dataframe(existing_app_data)

    # Confirm deletion
    if st.button("Delete App"):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        # Delete from pricing table
        delete_pricing_query = """
        DELETE FROM pricing
        WHERE App_id=?;
        """
        c.execute(delete_pricing_query, (app_id_to_delete,))

        # Fetch developer ID from the existing app data
        developer_id = existing_app_data.iloc[0]['Developer_Id']

        # Delete from developers table
        delete_dev_query = """
        DELETE FROM developers
        WHERE Developer_Id=?;
        """
        c.execute(delete_dev_query, (developer_id,))

        # Delete from applications table
        delete_app_query = """
        DELETE FROM applications
        WHERE App_Id=?;
        """
        c.execute(delete_app_query, (app_id_to_delete,))

        conn.commit()
        conn.close()

        st.success("App and related records deleted successfully!")

def read_data():
    conn = sqlite3.connect('database.db')
    df = pd.read_sql_query("SELECT * FROM applications;", conn)
    conn.close()
    return df

def top_developers():
    conn = sqlite3.connect('database.db')
    top_dev_df = pd.read_sql_query("SELECT * FROM TopDevelopers LIMIT 10;", conn)
    conn.close()

    st.markdown('<h5 style="color: #7C0A02;">Top Developers by Total Apps Developed</h5>', unsafe_allow_html=True)
    st.dataframe(top_dev_df)

    # Function to display free applications
def free_applications():
    conn = sqlite3.connect('database.db')
    free_apps_df = pd.read_sql_query("SELECT * FROM FreeApplications LIMIT 15;", conn)
    conn.close()

    st.markdown('<h5 style="color: #7C0A02;">Free Applications</h5>', unsafe_allow_html=True)
    st.dataframe(free_apps_df)

# Function to display top-rated apps by genre
def top_rated_apps_by_genre(genre):
    conn = sqlite3.connect('database.db')
    query = f"SELECT * FROM TopRatedAppsByGenre WHERE genre = '{genre}' LIMIT 10;"
    top_rated_df = pd.read_sql_query(query, conn)
    conn.close()

    st.subheader(f"Top Rated {genre} Apps")
    #st.table(top_rated_df)
    st.dataframe(top_rated_df)

    # Streamlit app
def main():
    

    # Read data from SQLite database
    app_data = read_data()

    # Display basic information about the dataset
    st.markdown('<h5 style="color: #7C0A02;">Sampled App Data</h5>', unsafe_allow_html=True)
    st.dataframe(app_data.head(10))  # Display only top 10 rows

    # Sidebar for user interactions
    st.sidebar.header("Explore Data")

    # Filter by Genre
    selected_genre = st.sidebar.selectbox("Select Genre", app_data['Genre'].unique())
    genre_filtered_df = app_data[app_data['Genre'] == selected_genre]

    # Filter by Average User Rating
    min_rating = st.sidebar.slider("Minimum Average User Rating", min_value=0, max_value=5, value=3)
    rating_filtered_df = genre_filtered_df[genre_filtered_df['Avg_user_rating'] >= min_rating]

    # Filter by Size
    min_size = st.sidebar.slider("Minimum Size (MB)", min_value=0.0, max_value=500.0, value=0.0)
    size_filtered_df = rating_filtered_df[rating_filtered_df['Size'] >= min_size]

    # Display the final filtered results
    st.markdown('<h5 style="color: #7C0A02;">Top 10 Apps based on Filters</h5>', unsafe_allow_html=True)
    st.dataframe(size_filtered_df.head(10))

    search_term = st.sidebar.text_input("Search by App Name")
    if search_term:
        search_result_df = size_filtered_df[size_filtered_df['App_name'].str.contains(search_term, case=False)]
        st.subheader('Search results')
        st.table(search_result_df.head(10))

    st.markdown('<h3 style="color: #7C0A02;">Additional Information</h3>', unsafe_allow_html=True)
    #st.title("Additional Information")

    # Additional Information Section
    st.sidebar.header("Additional Information")

   # Display top developers
    st.sidebar.subheader("Top Developers")
    top_developers()

    # Display free applications
    st.sidebar.subheader("Free Applications")
    free_applications()

    st.markdown('<h3 style="color: #7C0A02;">CRUD Operations</h3>', unsafe_allow_html=True)
    #st.header('CRUD Operations')
    selected_action = st.selectbox("Select an action", ["Create App", "Update App", "Read App", "Delete App"])

# Call the corresponding function based on the selected action
    if selected_action == "Create App":
        create_app()
    elif selected_action == "Update App":
        update_app()
    elif selected_action == "Read App":
        read_app()
    elif selected_action == "Delete App":
        delete_app()

if __name__ == "__main__":
    main()

