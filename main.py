# Import necessary libraries
import streamlit as st
import pandas as pd
from streamlit_lottie import st_lottie
import json
# Create DataFrames to store staff information and training history
staff_data = pd.DataFrame(columns=['Name', 'Age', 'Position', 'Department', 'Contact'])
training_history_data = pd.DataFrame(columns=['Name', 'Training'])

st.set_page_config(
    page_title="Staff Information Management",
    page_icon="🧊"
)


def get(path: str):
    with open(path, 'r') as f:
        return json.load(f)

path = get('./interact.json')
# Dropdown for positions and departments
positions_list = ['Manager', 'Developer', 'Designer', 'Analyst', 'Tester', 'Engineer', 'Coordinator', 'Architect', 'Administrator', 'Consultant', 'Specialist', 'Advisor', 'Supervisor', 'Coordinator', 'Team Lead', 'Director', 'Executive', 'Officer', 'Intern', 'Other']
departments_list = ['HR', 'IT', 'Finance', 'Marketing', 'Sales', 'Operations', 'Research and Development', 'Customer Service', 'Engineering', 'Legal', 'Management', 'Quality Assurance', 'Support', 'Training', 'Administration', 'Production', 'Logistics', 'Health and Safety', 'Public Relations', 'Other']

# Define the Streamlit app
def main():
    st.title('Staff Information Management')
    show_menu()
    st_lottie(path)
# Show menu
def show_menu():
    st.sidebar.header('Menu')

    options = ['View Staff Information', 'Add New Staff', 'Edit Staff Details', 'Delete Staff', 'Display Statistics', 'Training History','Add Training Details']
    selected_option = st.sidebar.selectbox('Select Option', options)

    perform_action(selected_option)

# Perform action based on selected option
def perform_action(selected_option):
    if selected_option == 'View Staff Information':
        view_staff_information()
    elif selected_option == 'Add New Staff':
        add_new_staff()
    elif selected_option == 'Edit Staff Details':
        edit_staff_details()
    elif selected_option == 'Delete Staff':
        delete_staff()
    elif selected_option == 'Display Statistics':
        display_statistics()
    elif selected_option == 'Training History':
        view_training_history()
    elif selected_option == 'Add Training Details':
        add_training_details()  # Added this option

# Function to view staff information
def view_staff_information():
    st.header('View Staff Information')
    if not staff_data.empty:
        st.table(staff_data)
    else:
        st.warning('No staff information available.')

# Function to add new staff
def add_new_staff():
    st.header('Add New Staff')

    # Create a form to collect details
    name = st.text_input('Name')
    age = st.number_input('Age', min_value=0, max_value=100, value=25)


    position = st.selectbox('Position', positions_list)
    department = st.selectbox('Department', departments_list)

    # Additional field for contact information
    contact = st.text_input('Contact Information')

    if st.button('Add Staff'):
        add_staff(name, age, position, department, contact)
def add_training_details():
    st.header('Add Training Details')

    # Display a dropdown to select a staff member
    staff_names = staff_data['Name'].tolist()
    selected_staff = st.selectbox('Select Staff Member', staff_names)

    # Create a form to collect training details
    training_description = st.text_input('Training Description')

    if st.button('Add Training'):
        add_training_record(selected_staff, training_description)
# Function to add new staff to the DataFrame and Excel file
def add_staff(name, age, position, department,contact):
    global staff_data

    new_staff = {'Name': name, 'Age': age, 'Position': position, 'Department': department, 'Contact': contact}
    staff_data.loc[len(staff_data)] = new_staff

    # Save to Excel file
    staff_data.to_excel('staff_information.xlsx', index=False)

    st.success('Staff added successfully!')

# Function to edit staff details (restricted to administrators)
def edit_staff_details():
    st.header('Edit Staff Details')

    # Display a dropdown to select a staff member for editing
    staff_names = staff_data['Name'].tolist()
    selected_staff = st.selectbox('Select Staff Member', staff_names)

    # Get the index of the selected staff member
    selected_index = staff_data[staff_data['Name'] == selected_staff].index[0]

    # Display the current details
    st.write(f'Editing details for {selected_staff}:')
    current_age = staff_data.loc[selected_index, 'Age']
    current_position = staff_data.loc[selected_index, 'Position']
    current_department = staff_data.loc[selected_index, 'Department']
    current_contact = staff_data.loc[selected_index, 'Contact']

    # Allow editing of details
    new_age = st.number_input('Age', min_value=0, max_value=100, value=current_age)
    new_position = st.selectbox('Position', positions_list, index=positions_list.index(current_position))
    new_department = st.selectbox('Department', departments_list, index=departments_list.index(current_department))
    new_contact = st.text_input('Contact Information', value=current_contact)

    if st.button('Update Details'):
        update_staff_details(selected_index, new_age, new_position, new_department, new_contact)

# Function to update staff details
def update_staff_details(index, age, position, department, contact):
    global staff_data

    # Update the details for the selected staff member
    staff_data.at[index, 'Age'] = age
    staff_data.at[index, 'Position'] = position
    staff_data.at[index, 'Department'] = department
    staff_data.at[index, 'Contact'] = contact

    # Save to Excel file
    staff_data.to_excel('staff_information.xlsx', index=False)

    st.success('Details updated successfully!')

# Function to delete staff information
def delete_staff():
    st.header('Delete Staff Information')

    # Display a dropdown to select a staff member for deletion
    staff_names = staff_data['Name'].tolist()
    selected_staff = st.selectbox('Select Staff Member to Delete', staff_names)

    if st.button('Delete Staff'):
        delete_staff_member(selected_staff)

# Function to delete a staff member
def delete_staff_member(name):
    global staff_data

    # Delete the selected staff member
    staff_data = staff_data[staff_data['Name'] != name]

    # Save to Excel file
    staff_data.to_excel('staff_information.xlsx', index=False)

    st.success(f'{name} deleted successfully!')

# Function to display statistics
def display_statistics():
    st.header('Display Statistics')
    if not staff_data.empty:
        st.subheader('Age Statistics')
        st.write(staff_data['Age'].describe())
        st.subheader('Position Distribution')
        st.write(staff_data['Position'].value_counts())
    else:
        st.warning('No staff information available for statistics.')

# Function to view training history
def view_training_history():
    st.header('Training History')

    # Display a dropdown to select a staff member for training history
    staff_names = staff_data['Name'].tolist()

    if not staff_names:
        st.warning('No staff members available.')
        return

    selected_staff = st.selectbox('Select Staff Member', staff_names)

    # Get the training history for the selected staff member
    staff_training_history = training_history_data[training_history_data['Name'] == selected_staff]

    if not staff_training_history.empty:
        st.table(staff_training_history)
    else:
        st.warning(f'No training history available for {selected_staff}.')

# Function to add training record for a staff member
def add_training_record(name, training):
    global training_history_data

    new_training_record = {'Name': name, 'Training': training}
    new_training_df = pd.DataFrame([new_training_record])  # Create a new DataFrame with the new record
    training_history_data = pd.concat([training_history_data, new_training_df], ignore_index=True)

    # Save to Excel file
    training_history_data.to_excel('training_history.xlsx', index=False)

    st.success('Training record added successfully!')
 
# Function to view training history
def view_training_history():
    st.header('Training History')

    # Display a dropdown to select a staff member for training history
    staff_names = staff_data['Name'].tolist()
    selected_staff = st.selectbox('Select Staff Member', staff_names)

    # Get the training history for the selected staff member
    staff_training_history = training_history_data[training_history_data['Name'] == selected_staff]

    if not staff_training_history.empty:
        st.table(staff_training_history)
    else:
        st.warning(f'No training history available for {selected_staff}.')


# Run the app
if __name__ == '__main__':
    # Load existing data from Excel files on app startup
    try:
        staff_data = pd.read_excel('staff_information.xlsx')
        training_history_data = pd.read_excel('training_history.xlsx')
    except FileNotFoundError:
        pass  # Files don't exist yet

    main()
