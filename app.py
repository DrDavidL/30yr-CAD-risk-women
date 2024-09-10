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
st.title("Women's 3 Variable 30 Year Risk Estimator")

# Input fields
hsCRP_input = st.number_input('Enter hsCRP (mg/dL):', min_value=0.0, value=0.0)
ldl_input = st.number_input('Enter LDL cholesterol (mg/dL):', min_value=0.0, value=0.0)
lipoprotein_a_input = st.number_input('Enter lipoprotein(a) (mg/dL):', min_value=0.0, value=0.0)

# Calculate quintiles
hsCRP_quintile = get_hsCRP_quintile(hsCRP_input)
ldl_quintile = get_ldl_quintile(ldl_input)
lipoprotein_a_quintile = get_lipoprotein_a_quintile(lipoprotein_a_input)

# Display results
st.write(f"hsCRP Quintile: {hsCRP_quintile}")
st.write(f"LDL Quintile: {ldl_quintile}")
st.write(f"Lipoprotein(a) Quintile: {lipoprotein_a_quintile}")

# Placeholder for future risk calculation
st.write("Future step: CAD risk calculation based on these quintiles.")
