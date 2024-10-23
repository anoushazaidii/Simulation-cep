import streamlit as st
import numpy as np
import pandas as pd

# Set the layout to wide
st.set_page_config(layout="wide")

# Streamlit app title
st.title("Single Server Queuing System Simulation")

# User inputs
N = st.number_input('Number of Customers (N)', min_value=1, value=50, step=1, help="Total number of customers to simulate.")
lambda_arrival = st.number_input('Arrival Rate (λ)', min_value=0.1, value=1.0, step=0.1, help="Rate at which customers arrive.")
mu_service = st.number_input('Service Rate (μ)', min_value=0.1, value=2.5, step=0.1, help="Rate at which customers are served.")

# Initialize or reset session state
if "customer_numbers" not in st.session_state:
    st.session_state.customer_numbers = []
    st.session_state.interarrival_times = []
    st.session_state.service_times = []
    st.session_state.queue_wait_times = []
    st.session_state.service_start_times = []
    st.session_state.service_end_times = []
    st.session_state.clock_times = []
    st.session_state.next_arrival_times = []
    st.session_state.next_departure_times = []
    st.session_state.current_customer = 0
    st.session_state.arrival_time = 0.0
    st.session_state.service_end_time = 0.0
    st.session_state.na = 0  # Number of arrivals
    st.session_state.nd = 0  # Number of departures
    st.session_state.totλ = 0.0  # Total interarrival time
    st.session_state.totμ = 0.0  # Total service time

# Function to simulate one customer
def simulate_customer(current_customer):
    if current_customer == 1:
        interarrival_time = 0.0
    else:
        interarrival_time = np.random.exponential(1 / lambda_arrival)

    # Update the clock time for the current customer
    st.session_state.arrival_time += interarrival_time
    st.session_state.na += 1  # Increment arrival count
    st.session_state.totλ += interarrival_time  # Update total interarrival time

    # Generate the service time
    service_time = np.random.exponential(1 / mu_service)
    st.session_state.totμ += service_time  # Update total service time

    # Check when the service starts
    service_start_time = max(st.session_state.arrival_time, st.session_state.service_end_time)
    service_end_time = service_start_time + service_time

    # Calculate the waiting time in queue (if any)
    queue_wait_time = service_start_time - st.session_state.arrival_time
    clock_time = st.session_state.arrival_time

    # Store the data for this customer
    st.session_state.customer_numbers.append(current_customer)
    st.session_state.interarrival_times.append(interarrival_time)
    st.session_state.service_times.append(service_time)
    st.session_state.queue_wait_times.append(queue_wait_time)
    st.session_state.service_start_times.append(service_start_time)
    st.session_state.service_end_times.append(service_end_time)
    st.session_state.clock_times.append(clock_time)

    # Store Next Arrival Time (ta) for the next customer
    next_arrival_time = st.session_state.arrival_time + np.random.exponential(1 / lambda_arrival)
    st.session_state.next_arrival_times.append(next_arrival_time)

    # Update service end time for the next customer
    st.session_state.service_end_time = service_end_time
    st.session_state.next_departure_times.append(service_end_time)
    st.session_state.nd += 1  # Increment departure count

# "Next Customer" button
if st.button("Next Customer") and st.session_state.current_customer < N:
    st.session_state.current_customer += 1
    simulate_customer(st.session_state.current_customer)

# "Complete Simulation" button
if st.button("Complete Simulation") and st.session_state.current_customer < N:
    while st.session_state.current_customer < N:
        st.session_state.current_customer += 1
        simulate_customer(st.session_state.current_customer)

# Create a DataFrame to store and display the results
if st.session_state.customer_numbers:
    # Prepare individual customer data
    data = {
        "Customer": st.session_state.customer_numbers,
        "Interarrival Time": st.session_state.interarrival_times,
        "Clock Time": st.session_state.clock_times,
        "Service Time": st.session_state.service_times,
        "Service Start Time": st.session_state.service_start_times,
        "Service End Time": st.session_state.service_end_times,
        "Queue Wait Time": st.session_state.queue_wait_times,
    }
    df = pd.DataFrame(data)
# Display the resulting table using Streamlit
st.subheader("Simulation Results")
if st.session_state.customer_numbers:
    # Prepare individual customer data
    data = {
        "Customer": st.session_state.customer_numbers,
        "Interarrival Time": st.session_state.interarrival_times,
        "Clock Time": st.session_state.clock_times,
        "Service Time": st.session_state.service_times,
        "Service Start Time": st.session_state.service_start_times,
        "Service End Time": st.session_state.service_end_times,
        "Queue Wait Time": st.session_state.queue_wait_times,
    }
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)

    # Compute and display the averages dynamically
    mean_interarrival_time = np.mean(st.session_state.interarrival_times)
    mean_service_time = np.mean(st.session_state.service_times)
    mean_queue_wait_time = np.mean(st.session_state.queue_wait_times)

    st.subheader("Averages")
    st.write(f"**Mean Interarrival Time:** {mean_interarrival_time:.4f}")
    st.write(f"**Mean Service Time:** {mean_service_time:.4f}")
    st.write(f"**Mean Queue Wait Time:** {mean_queue_wait_time:.4f}")

    # Display total interarrival time, total service time, and total number of arrivals and departures
    st.subheader("Totals and Counts")
    st.write(f"**Total Interarrival Time (λ):** {st.session_state.totλ:.4f}")
    st.write(f"**Total Service Time (μ):** {st.session_state.totμ:.4f}")
    st.write(f"**Total Number of Arrivals (na):** {st.session_state.na}")
    st.write(f"**Total Number of Departures (nd):** {st.session_state.nd}")

# Reset button to clear session state and start over
if st.button("Reset Simulation"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
