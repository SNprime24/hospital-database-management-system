import streamlit as st
from streamlit_option_menu import option_menu
import numpy as np
import pandas as pd
import os
import pyrebase


st.set_page_config(
    page_title="Global Health Hospitals",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

#configuration key
firebaseConfig = {
  'apiKey': "AIzaSyAuTIDO9PndMUDWSndYoozd6BYP_vdsQHo",
  'authDomain': "hospital-database-system.firebaseapp.com",
  'projectId': "hospital-database-system",
  'storageBucket': "hospital-database-system.appspot.com",
  'databaseURL': "https://hospital-database-system-default-rtdb.europe-west1.firebasedatabase.app/",
  'messagingSenderId': "299750398902",
  'appId': "1:299750398902:web:0aa0e43511a2640c8dff17",
  'measurementId': "G-2BDZSYZY2T"
}

#Firebase Authentication
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

#Database 
db = firebase.database()
storage = firebase.storage()

script_dir = os.path.dirname(os.path.abspath(__file__)) # Get the current script's directory
csv_path = os.path.join(script_dir, 'hospital.csv') # Construct the relative path to the CSV file
df = pd.read_csv(csv_path) # Read the CSV file into a DataFrame
st.dataframe(df)

st.title("🏥 Global Health Hospital")
st.header('', divider='rainbow')
page="Admin";

with st.sidebar:
    selected = option_menu(
        menu_title = "Main Menu",
        menu_icon = "shop",
        options = ["HOME","LOGIN","ABOUT"],
        icons  = ["hospital","box-arrow-in-left","bookmark-star-fill"],
        default_index=0,
        # orientation="horizontal"
    )

if(selected=="LOGIN"):    
    placeholder = st.empty()    
    if(page=="Home"):
        with placeholder.container():
            col1,col2,col3 = st.columns([10,1,10])
            with col1:
                st.image("hospital_image1.jpg")
            with col3:
                st.header("LOGIN 📥",divider='gray')
                selected_login = option_menu(
                    menu_title = "List",
                    menu_icon = "list",
                    options = ["Admin","Doctor"],
                    icons=["gear","clipboard2-plus"],
                    default_index=0,
                    orientation="horizontal"
                )
                if(selected_login=="Admin"):
                    with st.form('Login'):
                        emailL=st.text_input("Email Address : ")
                        passwordL = st.text_input("Password : ",type = 'password')
                        submitL = st.form_submit_button('LOGIN')
                    if(submitL):                    
                        try:
                            user = auth.sign_in_with_email_and_password(emailL,passwordL)
                            st.success("Logined Successfully")                        
                            username = db.child(user['localId']).child("Handle").get().val()
                            if(username=='Admin'):
                                page="Admin"
                        except:
                            st.warning("Wrong Username/Password")
                        
                    # emaili=st.text_input("Email Address1 : ")
                    # passwordi = st.text_input("Password1 : ",type = 'password')
                    # handle = st.text_input('Please input your Name : ',value  ='Default')
                    # submit = st.button('Create new account')
                    # if submit :
                    #     user = auth.create_user_with_email_and_password(email = emaili, password=passwordi)
                    #     st.success('Account created successfully!')
                    #     user = auth.sign_in_with_email_and_password(emaili,passwordi)
                    #     db.child(user['localId']).child("Handle").set(handle)
                    #     db.child(user['localId']).child("ID").set(user['localId'])
                    #     st.write('Welcome'+handle)
    
    if page=='Admin':
        placeholder.empty()
        with placeholder.container():
            selected_admin = option_menu(
                menu_title = "Admin Menu",
                menu_icon = "list",
                options = ["Patient Entry","Current Patient","Old Patient Report","Doctor Entry"],
                icons  = ["box-arrow-in-right","clipboard-heart","database-up","database-fill-add"],
                default_index=3,
                orientation="horizontal"
            )
            if(selected_admin=="Doctor Entry"):
                with st.form('Doctor Entry'):
                    col1,col2,col3 = st.columns([3,3,1])
                    with col1:
                        NameD = st.text_input("Name of the Doctor : ")
                    with col2:
                        SpecialisationD = st.text_input("Specialisation in : ")
                    with col3:
                        roomD = st.number_input('Room no Allocated :', value = 000,)
                    col1,col2,col3 = st.columns([1,1,1])
                    with col1:
                        ageD = st.number_input('Age of the Doctor :', value = 18,)
                    with col2:
                        genderD = st.radio('Gender :',options =['Male','Female'], help = 'Choose One',horizontal = True,index=0)
                    with col3:
                        bloodD = st.text_input("Blood Group : ")
                    col1,col2 = st.columns([1,1])
                    with col1:
                        emailL=st.text_input("Email Address of Doctor : ")
                        passwordL = st.text_input("Password : ",type = 'password')
                        cpasswordL = st.text_input("Confirm Password : ",type = 'password')
                    submitD = st.form_submit_button('Create Account')
                
                if(submitD):
                    if(passwordL != cpasswordL):
                        st.warning("Password is not matching")
                    else:
                        userD = auth.create_user_with_email_and_password(email = emailL, password=passwordL)
                        userD = auth.sign_in_with_email_and_password(emailL,passwordL)
                        db.child(userD['localId']).child("Handle").set(NameD)
                        db.child(userD['localId']).child("ID").set(userD['localId'])
                        db.child(userD['localId']).child("Specialisation").set(SpecialisationD)
                        db.child(userD['localId']).child("Age").set(ageD)
                        db.child(userD['localId']).child("Gender").set(genderD)
                        db.child(userD['localId']).child("Blood Group").set(bloodD)
                        db.child(userD['localId']).child("Room").set(roomD)
                        st.success('Account created successfully!')




                

    if(page=="Doctor"):
        placeholder.empty()
        with placeholder.container():
            st.write("Doctor")


if(selected=="HOME"):
    st.header("HOME 🏠")
    st.markdown("##### Welcome to Kharido.com - Your Trusted Marketplace for Quality Products!")
    st.markdown("###### At Kharido.com, we bring you a diverse selection of fresh produce, dairy products, gold, and more, all conveniently available in one place. Our mission is to provide you with a seamless and personalized shopping experience tailored to your preferences.")
    st.divider()
    st.subheader("**Why Choose Kharido.com?**")
    st.markdown("- ##### *Fresh and High-Quality Products :*")
    st.markdown("We source our products from trusted suppliers to ensure you receive only the freshest and highest-quality items.")
    st.markdown("")
    st.markdown("- ##### *Personalized Shopping :*")
    st.markdown("Use our easy-to-fill form to tell us your preferences, and let our machine learning models, powered by decision tree and logistic regression algorithms, create a customized order just for you and will give you exciting discounts.")
    st.markdown("")
    st.markdown("- ##### *User-Friendly Interface :*")
    st.markdown("Easily navigate the application with our intuitive and user-friendly web interface.")
    st.markdown("")
if(selected=="ABOUT"): 
    st.title("ABOUT 🙏")
    st.divider()
    selected_about = option_menu(
        menu_title = "List",
        menu_icon = "list",
        options = ["How to use","Team"],
        icons=["mouse-fill","people"],
        default_index=0,
        orientation="horizontal"
    )
    if(selected_about=="How to use"):
        st.subheader("🖱️ How to use")
        st.markdown("Data taken from Customer Personality Analysis ")
    if(selected_about=="Team"):
        st.header('🎯 Our Mission :')
        st.markdown("At Kharido.com, we envision a world where shopping is not just a transaction but an experience tailored to each customer. We strive to create a platform that not only offers top-notch products but also understands and anticipates your needs through the power of machine learning.")
        st.header("🔅 Team:")
        st.markdown("#### 🐉Dragon Developers(DD)")
        st.markdown("- 👨‍💻 Makarandh - 22CS01002")
        st.markdown("- 👨‍💻 Suprit Naik - 22CS01018")
        st.markdown("- 👨‍💻 Harsh Maurya - 22CS01046")



footer="""<style>
.footer {
position: reltive;
left: 0;
bottom: 0;
width: 100%;
background-color: #0E117;
color: black;
text-align: center;
opacity:40%;
color:white;
}
</style>
<div class="footer">
<p>Developed with 💖 by 🐉Dragon Developers(DD)</p>
</div>
"""
with st.sidebar:
    st.markdown(footer,unsafe_allow_html=True)

