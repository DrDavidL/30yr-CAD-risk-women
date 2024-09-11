import streamlit as st

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
st.title("Women's 3 Variable 30 Year Hazard Ratio Estimator")

# Input fields
hsCRP_input = st.number_input('Enter hsCRP (mg/dL):', min_value=0.0, value=0.0)
ldl_input = st.number_input('Enter LDL cholesterol (mg/dL):', min_value=0.0, value=0.0)
lipoprotein_a_input = st.number_input('Enter lipoprotein(a) (mg/dL):', min_value=0.0, value=0.0)

# Calculate quintiles
hsCRP_quintile = get_hsCRP_quintile(hsCRP_input)
ldl_quintile = get_ldl_quintile(ldl_input)
lipoprotein_a_quintile = get_lipoprotein_a_quintile(lipoprotein_a_input)

# Calculate the number of biomarkers in the top quintile
biomarkers_in_top_quintile = sum([hsCRP_quintile == 5, ldl_quintile == 5, lipoprotein_a_quintile == 5])

# Display quintile results
st.write(f"hsCRP Quintile: {hsCRP_quintile}")
st.write(f"LDL Quintile: {ldl_quintile}")
st.write(f"Lipoprotein(a) Quintile: {lipoprotein_a_quintile}")


st.divider()
st.info("The following hazard ratios are based on the number of biomarkers in the top risk quintile.")

st.write(f"Number of biomarkers in the top quintile: **{biomarkers_in_top_quintile}**")
st.info("""Covariable adjusted HRs (95%CI) of total cardiovascular events, coronary heart disease events, and
stroke events for individuals with 0, 1, 2, or 3 biomarker levels in the 5th quintile with follow-up censored at time of
first reported statin prescription.""")

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
