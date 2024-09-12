import streamlit as st

def check_password():
    """Returns `True` if the user entered the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password in session state
        else:
            st.session_state["password_correct"] = False

    # Check if the password has been verified
    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.write("*Please contact David Liebovitz, MD if you need an updated password for access.*")
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True

# Define quintile thresholds
def get_hsCRP_quintile(value):
    if value < 0.65:
        return 1
    elif value < 1.47:
        return 2
    elif value < 2.75:
        return 3
    elif value < 5.18:
        return 4
    else:
        return 5

def get_ldl_quintile(value):
    if value < 96.1:
        return 1
    elif value < 113.5:
        return 2
    elif value < 129.7:
        return 3
    elif value < 150.7:
        return 4
    else:
        return 5

def get_lipoprotein_a_quintile(value):
    if value < 3.6:
        return 1
    elif value < 7.6:
        return 2
    elif value < 15.5:
        return 3
    elif value < 44.1:
        return 4
    else:
        return 5

# Streamlit app
st.set_page_config(
    page_title="Women's 3 Variable 30 Year Risk Estimator",
    page_icon="❤️",)
st.title("Women's 3 Variable 30-Year :heart:     Risk Estimator " )

# Input fields
hsCRP_input = st.number_input('Enter hsCRP (mg/dL):', min_value=0.0, value=0.0)
ldl_input = st.number_input('Enter LDL cholesterol (mg/dL):', min_value=0.0, value=0.0)
lipoprotein_a_input = st.number_input('Enter lipoprotein(a) (mg/dL):', min_value=0.0, value=0.0)

if check_password():


    # Calculate quintiles
    hsCRP_quintile = get_hsCRP_quintile(hsCRP_input)
    ldl_quintile = get_ldl_quintile(ldl_input)
    lipoprotein_a_quintile = get_lipoprotein_a_quintile(lipoprotein_a_input)

    # Calculate the number of biomarkers in the top quintile
    biomarkers_in_top_quintile = sum([hsCRP_quintile == 5, ldl_quintile == 5, lipoprotein_a_quintile == 5])

    # Display quintile results
    st.info("Quintile 5 is the highest 20% of values for each biomarker.")
    st.write("Quintiles for values entered:")
    st.write(f"hsCRP Quintile: **{hsCRP_quintile}**")
    st.write(f"LDL Quintile: **{ldl_quintile}**")
    st.write(f"Lipoprotein(a) Quintile: **{lipoprotein_a_quintile}**")
    st.write(f"Number of biomarkers in the top quintile: **{biomarkers_in_top_quintile}**")

    st.info("""The following hazard ratios are based on the number of biomarkers in the top quintile from [Ridker et al., 2024](https://www.nejm.org/doi/full/10.1056/NEJMoa2405182).
            See Table S8 in the supplement; follow-up censored at time of first reported statin prescription. 
            """)
    # Hazard ratios and confidence intervals based on the number of biomarkers in the top quintile
    if biomarkers_in_top_quintile == 0:
        st.write("Referent group: No biomarkers in the top quintile.")
        st.write("First Major Cardiovascular Event: HR=1.0 (referent)")
        st.write("Coronary Heart Disease Events: HR=1.0 (referent)")
        st.write("Stroke Events: HR=1.0 (referent)")
    elif biomarkers_in_top_quintile == 1:
        st.write("First Major Cardiovascular Event: **HR=1.38 (95% CI: 1.25-1.51)**")
        st.write("Coronary Heart Disease Events: **HR=1.54 (95% CI: 1.35-1.75)**")
        st.write("Stroke Events: **HR=1.14 (95% CI: 0.96-1.34)**")
    elif biomarkers_in_top_quintile == 2:
        st.write("First Major Cardiovascular Event: **HR=1.68 (95% CI: 1.46-1.93)**")
        st.write("Coronary Heart Disease Events: **HR=1.98 (95% CI: 1.65-2.39)**")
        st.write("Stroke Events: **HR=1.63 (95% CI: 1.28-2.06)**")
    elif biomarkers_in_top_quintile == 3:
        st.write("First Major Cardiovascular Event: **HR=3.21 (95% CI: 2.41-4.27)**")
        st.write("Coronary Heart Disease Events: **HR=4.08 (95% CI: 2.88-5.77)**")
        st.write("Stroke Events: **HR=2.87 (95% CI: 1.71-4.84)**")


    # Alternative explanation: Odds (expressing risk as "times more likely")
    st.header(" Explanation")
    st.info(f"""Based on the paper by [Ridker et al., 2024](https://www.nejm.org/doi/full/10.1056/NEJMoa2405182), the following research informed considerations are provided for discussion of 30 year future cardiovascular risk for women
            for an hsCRP of :red[{hsCRP_input}], and LDL of :red[{ldl_input}], and a Lp(a) of :red[{lipoprotein_a_input}]:""")
    if biomarkers_in_top_quintile == 1:
        st.success("Over a 30-year period with 1 biomarker elevated, an individual is :red[1.38] times more likely to have a major cardiovascular event, :red[1.54] times more likely to have coronary heart disease, and :red[1.14] times more likely to have a stroke.")
    elif biomarkers_in_top_quintile == 2:
        st.success("Over a 30-year period with 2 biomarkers elevated, an individual is :red[1.68] times more likely to have a major cardiovascular event, :red[1.98] times more likely to have coronary heart disease, and :red[1.63] times more likely to have a stroke.")
    elif biomarkers_in_top_quintile == 3:
        st.success("Over a 30-year period with 3 biomarkers elevated, an individual is :red[3.21] times more likely to have a major cardiovascular event, :red[4.08] times more likely to have coronary heart disease, and :red[2.87] times more likely to have a stroke.")
    elif biomarkers_in_top_quintile == 0:
        st.success("Over a 30-year period with no biomarkers elevated, an individual has :red[no increased risk] beyond the referent group of major cardiovascular events, coronary heart disease, or stroke.")


