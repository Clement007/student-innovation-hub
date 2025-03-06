import streamlit as st
import pandas as pd
import os
import time
from PIL import Image
from io import BytesIO
from datetime import datetime

# Set page configuration
st.set_page_config(page_title="Student Innovation Hub", page_icon="🚀", layout="wide")

# Title
st.title("🎓 Student Innovation Hub")
st.subheader("A central platform to showcase student projects and assignments")

# Sidebar for navigation
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to:", ["Home", "Submit Assignment", "View Projects", "About"])

# Data Storage
projects_file = "projects.csv"
if "projects" not in st.session_state:
    if os.path.exists(projects_file):
        st.session_state.projects = pd.read_csv(projects_file)

        # Ensure Timestamp column exists
        if "Timestamp" not in st.session_state.projects.columns:
            st.session_state.projects["Timestamp"] = None
    else:
        st.session_state.projects = pd.DataFrame(columns=[
            "Name", "Department", "Module", "Assignment Type",
            "Assignment Name", "Live Link", "Image", "Group Work", "Timestamp"
        ])

# Home Page - Latest Projects
if page == "Home":
    st.subheader("🏆 Latest Student Projects")
    
    if not st.session_state.projects.empty:
        if "Timestamp" in st.session_state.projects.columns:
            latest_projects = st.session_state.projects.sort_values(by="Timestamp", ascending=False).head(5)
        else:
            latest_projects = st.session_state.projects.head(5)

        for _, row in latest_projects.iterrows():
            with st.container():
                col1, col2 = st.columns([1, 3])

                # Handle image loading
                if row["Image"] is None or pd.isna(row["Image"]):
                    img_placeholder = "https://via.placeholder.com/100"
                else:
                    try:
                        if os.path.exists(row["Image"]):
                            img = Image.open(row["Image"])
                        else:
                            img = Image.open(BytesIO(row["Image"]))
                        img_placeholder = img
                    except Exception as e:
                        st.warning(f"Error loading image: {e}")
                        img_placeholder = "https://via.placeholder.com/100"
                
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
            # Check for duplicates (same name, module, and assignment name)
            duplicate = st.session_state.projects[
                (st.session_state.projects["Name"] == name) &
                (st.session_state.projects["Module"] == module) &
                (st.session_state.projects["Assignment Name"] == assignment_name)
            ]

            if not duplicate.empty:
                st.warning("⚠️ You have already submitted this assignment!")
            else:
                # Handle timestamp
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Save the uploaded image
                image_path = None
                if image is not None:
                    try:
                        if not os.path.exists("temp_images"):
                            os.makedirs("temp_images")
                        image_path = os.path.join("temp_images", image.name)
                        img = Image.open(image)
                        img.save(image_path)
                    except Exception as e:
                        st.error(f"⚠️ Error processing the image: {e}")

                # Add new project entry
                new_entry = pd.DataFrame({
                    "Name": [name],
                    "Department": [department],
                    "Module": [module],
                    "Assignment Type": [assignment_type],
                    "Assignment Name": [assignment_name],
                    "Live Link": [live_link],
                    "Image": [image_path if image_path else None],
                    "Group Work": [assignment_type == "Group"],
                    "Timestamp": [timestamp]
                })

                # Update session state and save to CSV
                st.session_state.projects = pd.concat([st.session_state.projects, new_entry], ignore_index=True)
                st.session_state.projects.to_csv(projects_file, index=False)
                st.success("✅ Your project has been submitted successfully!")
                time.sleep(2)
                st.rerun()
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

    # Sort by timestamp
    if "Timestamp" in filtered_projects.columns:
        filtered_projects = filtered_projects.sort_values(by="Timestamp", ascending=False)

    # Display projects
    if not filtered_projects.empty:
        for _, row in filtered_projects.iterrows():
            with st.container():
                col1, col2 = st.columns([1, 3])
                
                # Handle images
                if row["Image"] is None or pd.isna(row["Image"]):
                    img_placeholder = "https://via.placeholder.com/100"
                else:
                    try:
                        if isinstance(row["Image"], bytes):
                            img = Image.open(BytesIO(row["Image"]))
                        else:
                            img = Image.open(row["Image"])
                        img_placeholder = img
                    except Exception as e:
                        st.warning(f"Error loading image: {e}")
                        img_placeholder = "https://via.placeholder.com/100"
                
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
    st.write("This platform serves as a hub for students to submit, share, and explore innovative projects.")

# Footer
# st.markdown("---")
#st.markdown("© 2025 Student Innovation Hub | Powered by Streamlit 🚀")


# Footer
st.markdown("---")
st.markdown("👨‍💻 © 2025 **Student Innovation Hub** | Built with ❤️ by CS Department at INES - Ruhengeri| Contact: [Email](mailto:mclement@ines.ac.rw) | 🚀")

