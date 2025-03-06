import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(page_title="Student Innovation Hub", page_icon="🚀", layout="wide")

# Title
st.title("🎓 Student Innovation Hub")
st.subheader("A central platform to showcase student projects and assignments")

# Sidebar for navigation
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to:", ["Home", "Submit Assignment", "View Projects", "About"])

# Data Storage
if "projects" not in st.session_state:
    st.session_state.projects = pd.DataFrame(columns=["Name", "Department", "Module", "Assignment Type", "Assignment Name", "Live Link", "Image", "Group Work"])

# Home Page - Latest Projects
if page == "Home":
    st.subheader("🏆 Latest Student Projects")
    
    if not st.session_state.projects.empty:
        latest_projects = st.session_state.projects.tail(5)  # Show the latest 5 projects
        for _, row in latest_projects.iterrows():
            with st.container():
                col1, col2 = st.columns([1, 3])
                img_placeholder = "https://via.placeholder.com/100" if row["Image"] is None else row["Image"]
                col1.image(img_placeholder, width=100)
                col2.markdown(f"### {row['Name']}")
                col2.markdown(f"📚 **Department:** {row['Department']}")
                col2.markdown(f"📖 **Module:** {row['Module']}")
                col2.markdown(f"📌 **Assignment:** {row['Assignment Type']} - {row['Assignment Name']}")
                col2.markdown(f"🌍 [Explore More]({row['Live Link']})", unsafe_allow_html=True)
                st.markdown("---")
    else:
        st.info("No projects have been submitted yet. Be the first to showcase your work!")

# Form for student submission
elif page == "Submit Assignment":
    st.subheader("📩 Submit Your Project")
    
    # Input fields
    name = st.text_input("Full Name")
    department = st.text_input("Department")
    module = st.text_input("Module")
    assignment_type = st.selectbox("Assignment Type", ["Individual", "Group"])
    assignment_name = st.text_input("Assignment Name (e.g., Assignment #1, Final Project)")
    live_link = st.text_input("Live Portfolio Link")
    image = st.file_uploader("Upload Your Profile Picture or Project Screenshot", type=["jpg", "png"])
    
    if st.button("Submit Project"):
        if name and department and module and assignment_type and live_link:
            new_entry = pd.DataFrame({
                "Name": [name],
                "Department": [department],
                "Module": [module],
                "Assignment Type": [assignment_type],
                "Assignment Name": [assignment_name],
                "Live Link": [live_link],
                "Image": [image],
                "Group Work": [assignment_type == "Group"]
            })
            
            st.session_state.projects = pd.concat([st.session_state.projects, new_entry], ignore_index=True)
            st.success("✅ Your project has been submitted successfully!")
            st.experimental_rerun()  # Refresh the page to show the latest project on Home
        else:
            st.error("⚠️ Please fill out all required fields.")

# View submitted projects
elif page == "View Projects":
    st.subheader("🌍 Explore Student Projects")
    
    # Filter options
    filter_department = st.selectbox("Filter by Department", ["All"] + list(st.session_state.projects["Department"].unique()))
    filter_module = st.selectbox("Filter by Module", ["All"] + list(st.session_state.projects["Module"].unique()))
    show_group_projects = st.checkbox("Show Only Group Projects")
    
    # Apply filters
    filtered_projects = st.session_state.projects.copy()
    if filter_department != "All":
        filtered_projects = filtered_projects[filtered_projects["Department"] == filter_department]
    if filter_module != "All":
        filtered_projects = filtered_projects[filtered_projects["Module"] == filter_module]
    if show_group_projects:
        filtered_projects = filtered_projects[filtered_projects["Group Work"] == True]
    
    # Display projects
    if not filtered_projects.empty:
        for _, row in filtered_projects.iterrows():
            with st.container():
                col1, col2 = st.columns([1, 3])
                img_placeholder = "https://via.placeholder.com/100" if row["Image"] is None else row["Image"]
                col1.image(img_placeholder, width=100)
                col2.markdown(f"### {row['Name']}")
                col2.markdown(f"📚 **Department:** {row['Department']}")
                col2.markdown(f"📖 **Module:** {row['Module']}")
                col2.markdown(f"📌 **Assignment:** {row['Assignment Type']} - {row['Assignment Name']}")
                col2.markdown(f"🌍 [Explore More]({row['Live Link']})", unsafe_allow_html=True)
                st.markdown("---")
    else:
        st.info("No projects found. Please try changing the filters.")

# About Page
elif page == "About":
    st.subheader("📢 About Student Innovation Hub")
    st.write("This platform serves as a central hub for students to submit, share, and explore innovative projects and assignments. Whether individual or group work, the Innovation Hub showcases the creativity and technical skills of students in various fields.")
