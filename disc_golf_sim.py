import streamlit as st
import matplotlib.pyplot as plt
import numpy as np


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

def get_arm_speed_mph(option):
    if "Beginner" in option:
        return 40
    elif "Intermediate" in option:
        return 55
    elif "Expert" in option:
        return 70
    else:
        return 55  # default

def plot_flight_path(Cm, arm_speed_option, wind_speed_mph):
    # Set distance scaling based on arm speed
    base_speed = 55  # baseline (Intermediate)
    user_speed = get_arm_speed_mph(arm_speed_option)
    distance_scale = user_speed / base_speed

    # Simulate
    total_distance = 325 * distance_scale  # base distance ~325ft
    steps = 100
    x = np.linspace(0, total_distance, steps)

    # Curvature strength from Cm
    curvature_strength = Cm * 50
    y_curve = curvature_strength * np.sin(np.linspace(0, np.pi, steps))

    # Wind drift (assume 1 ft drift per 5 mph crosswind for now)
    wind_drift = (wind_speed_mph / 5.0)
    y_total = y_curve + wind_drift

    # Plot
    fig, ax = plt.subplots(figsize=(5, 8))
    ax.plot(y_total, x, color='orange', linewidth=3)
    ax.set_title('Top-Down Flight Path')
    ax.set_xlabel('Left ←     Lateral Position (ft)     → Right')
    ax.set_ylabel('Forward Distance (ft)')
    ax.set_xlim(-100, 100)
    ax.set_ylim(0, 450)
    ax.grid(True)
    st.pyplot(fig)
