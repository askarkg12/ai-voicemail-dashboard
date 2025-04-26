import streamlit as st
import streamlit_antd_components as sac # Added SAC import


# Sample ticket data (replace with your actual data source)
tickets = [
    {
        "id": 1, 
        "name": "Alice Smith", 
        "dob": "1990-05-15", 
        "summary": "Cannot log in, tried password reset.", # Added summary
        "actions": [ # Changed from tags to actions
            {"type": "Urgent", "details": "Needs immediate assistance."},
            {"type": "Login Issue", "details": "Standard login troubleshooting required."}
        ], 
        "ai_summary": "User cannot log in to their account. Tried resetting password, but still facing issues. Needs immediate assistance.", 
        "status": "Open", 
        "audio_url": None, 
        "transcript": "Full transcript text here..."
    },
    {
        "id": 2, 
        "name": "Bob Johnson", 
        "dob": "1985-11-22", 
        "summary": "Question about invoice double charge.", # Added summary
        "actions": [ # Changed from tags to actions
             {"type": "Billing", "details": "Potential double charge inquiry."}
        ], 
        "ai_summary": "User has a question about their recent invoice. Believes there might be a double charge for a service.", 
        "status": "Open", 
        "audio_url": None, 
        "transcript": "Another transcript..."
    },
    {
        "id": 3, 
        "name": "Charlie Brown", 
        "dob": "1998-01-30", 
        "summary": "Requests custom date range filter.", # Added summary
        "actions": [ # Changed from tags to actions
             {"type": "Feature Request", "details": "Reporting dashboard - custom date range."}
        ], 
        "ai_summary": "User requests a new feature for the reporting dashboard to allow custom date range filtering.", 
        "status": "Pending", 
        "audio_url": None, 
        "transcript": "More transcript text..."
    },
     {
        "id": 4, 
        "name": "Eve Davis", # Added a new entry for accessibility example
        "dob": "1965-07-12",
        "summary": "Needs wheelchair access for appointment.", # Added summary
        "actions": [ # Changed from tags to actions
             {"type": "Appointment", "details": "Reschedule or confirm existing."},
             {"type": "Accessibility", "details": "Requires wheelchair access for the clinic visit."}
        ],
        "ai_summary": "Patient called to confirm appointment details and ensure wheelchair accessibility is available at the facility.",
        "status": "Open",
        "audio_url": None,
        "transcript": "Patient transcript regarding accessibility..."
    },
    {
        "id": 5, # Renumbered old ID 4
        "name": "Diana Prince", 
        "dob": "1977-03-08", 
        "summary": "Password reset successful.", # Added summary
        "actions": [ # Changed from tags to actions
            {"type": "Password", "details": "Password reset completed via email."},
             {"type": "Resolved", "details": "Issue resolved during the call/interaction."}
        ], 
        "ai_summary": "User needed help resetting their password. Successfully reset via email link.", 
        "status": "Closed", 
        "audio_url": None, 
        "transcript": "Final transcript example..."
    },
]

# Define colors for action types (add more as needed)
ACTION_COLORS = {
    "Urgent": "#F_RED_500",
    "Login Issue": "#F_ORANGE_500",
    "Billing": "#F_AMBER_500",
    "Feature Request": "#F_LIME_500",
    "Accessibility": "#F_BLUE_500",
    "Password": "#F_CYAN_500",
    "Appointment": "#F_PURPLE_500",
    "Resolved": "#F_GREEN_500",
    "DEFAULT": "#F_GRAY_500" # Default color
}

# Function to get color, defaulting if type not found
def get_action_color(action_type):
    return ACTION_COLORS.get(action_type, ACTION_COLORS["DEFAULT"])

st.set_page_config(layout="wide")

st.title("Customer Service Dashboard")

# Initialize session state
if 'selected_ticket_id' not in st.session_state:
    st.session_state.selected_ticket_id = tickets[0]['id'] if tickets else None

# --- Sidebar ---
st.sidebar.title("Voicemails")

# Use streamlit-antd-components menu
with st.sidebar:
    print(f"--- Sidebar Start: session_state.id = {st.session_state.get('selected_ticket_id')} ---") # DEBUG
    # Prepare items for sac.menu as a list of dictionaries
    menu_items = [
        {
            "label": ticket['name'], 
            "id": ticket['id'], # Use 'id' key for identification
        } for ticket in tickets
    ]

    # Determine the default selected id
    current_selected_id = st.session_state.selected_ticket_id
    all_ids = [item['id'] for item in menu_items]
    if current_selected_id not in all_ids:
        current_selected_id = all_ids[0] if all_ids else None
    
    # Calculate the index based on the current ID for initial selection
    current_index = all_ids.index(current_selected_id) if current_selected_id in all_ids else 0

    # selected_label will be the label string returned by sac.menu
    selected_label = sac.menu(
        items=menu_items, 
        key='sac_menu', 
        index=current_index, 
        return_index=False # Important: returns the label (default behavior without format_func?)
    )

    # Find the actual ID corresponding to the returned label
    selected_id = None
    for item in menu_items:
        if item['label'] == selected_label:
            selected_id = item['id']
            break

    # Update session state *using the correct integer ID* if the selection changed
    # print(f"--- Before comparison: selected_id = {selected_id}, session_state.id = {st.session_state.get('selected_ticket_id')} ---") # DEBUG Removed
    if selected_id is not None and selected_id != st.session_state.selected_ticket_id:
        # print(f"--- *** Updating session state! *** ---") # DEBUG Removed
        st.session_state.selected_ticket_id = selected_id # Store the correct ID
        st.rerun() 


# --- Main Area ---
# Find the selected ticket *after* potential selection updates
selected_ticket = None
if st.session_state.selected_ticket_id:
    for t in tickets:
        if t['id'] == st.session_state.selected_ticket_id:
            selected_ticket = t
            break

if selected_ticket:
    # --- Header ---
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader(selected_ticket['name'])
        st.markdown("**Actions:**")
        for action in selected_ticket['actions']:
            with st.expander(f"{action['type']}", expanded=True):
                st.write(action['details'])
    with col2:
        st.write(f"**DOB:** {selected_ticket['dob']}")
        st.write(f"**Status:** {selected_ticket['status']}")

    st.divider()

    # --- AI Summary & Links ---
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("AI Summary")
        st.write(selected_ticket['ai_summary'])
    with col2:
        with st.expander("See transcript >"):
            st.write(selected_ticket.get('transcript', 'No transcript available.'))

        if selected_ticket.get('audio_url'):
             st.audio(selected_ticket['audio_url'])
        else:
            if st.button("Listen >"):
                 st.warning("Audio playback not available for this item.")

    st.divider()

    # --- Action Buttons ---
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        if st.button("Mark Complete"):
            st.success(f"Ticket {selected_ticket['id']} marked as complete!")
    with col2:
        if st.button("Reassign"):
            st.info(f"Reassign functionality for ticket {selected_ticket['id']} not implemented yet.")

else:
    st.write("Select a voicemail from the list on the left to view details.") 