import streamlit as st

# Import your extrapolation functions from earlier
def improved_pitching_moment(turn, fade):
    Cm_base = -0.02
    Cm_turn_adjustment = 0.007 * turn
    Cm_fade_adjustment = 0.015 * (fade - 2)
    return round(Cm_base + Cm_turn_adjustment + Cm_fade_adjustment, 4)

def extrapolate_aero_coefficients(speed, glide, turn, fade):
    ref_Cl, ref_Cd = 0.15, 0.08  # Reference Wraith values
    ref_speed, ref_glide = 11, 5

    Cl = ref_Cl + 0.005 * (glide - ref_glide)
    Cd = ref_Cd - 0.002 * (speed - ref_speed)
    Cm = improved_pitching_moment(turn, fade)

    return {'Cl': round(Cl,4), 'Cd': round(Cd,4), 'Cm': Cm}

# Streamlit UI starts here
st.title('🥏 Disc Golf Flight Simulator')

st.header('Enter Disc Flight Numbers')
speed = st.slider('Speed', 1, 14, 9)
glide = st.slider('Glide', 1, 7, 5)
turn = st.slider('Turn', -5, 1, -1)
fade = st.slider('Fade', 0, 5, 3)

st.header('Player Settings')
arm_speed_option = st.selectbox('Arm Speed', ['Beginner (~40 mph)', 'Intermediate (~55 mph)', 'Expert (~70 mph)'])
wind_speed = st.slider('Wind Speed (mph)', 0, 30, 0)

# Calculate coefficients
coefficients = extrapolate_aero_coefficients(speed, glide, turn, fade)

st.header('Aerodynamic Coefficients')
st.write(f"**Lift (Cl):** {coefficients['Cl']}")
st.write(f"**Drag (Cd):** {coefficients['Cd']}")
st.write(f"**Pitching Moment (Cm):** {coefficients['Cm']}")

st.header('Conditions')
st.write(f"**Arm Speed Selected:** {arm_speed_option}")
st.write(f"**Wind Speed:** {wind_speed} mph")

st.info("Next: Here you can integrate your trajectory calculation and visualization (next step).")
