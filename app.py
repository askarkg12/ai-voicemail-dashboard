import streamlit as st
import datetime
from dataclasses import dataclass
import streamlit_antd_components as sac  # Added SAC import
from dotenv import dotenv_values
from supabase import create_client


@dataclass
class Ticket:
    id: int
    created_at: str
    name: str
    dob: str
    actions: list[dict[str, str]]
    patient_calling: bool
    ai_summary: str
    transcript: str
    audio_url: str
    status: str


config = dotenv_values(".env")
# from mock_data import tickets

supabase = create_client(config["SUPABASE_URL"], config["SUPABASE_KEY"])

if "tickets" not in st.session_state:
    # Get data from supabase
    response = supabase.table("tickets").select("*").execute()
    st.session_state["tickets"] = [Ticket(**ticket) for ticket in response.data]

tickets: list[Ticket] = st.session_state["tickets"]

# Define colors for action types (add more as needed)
ACTION_COLORS = {
    "cancel": "#ff6666",
    "reschedule": "#0000cc",
    "travel": "#33cc33",
    "access": "#ff33cc",
    "translator": "#cc9900",
    "accompany": "#00cc66",
    "other": "#003399",
    "no letter": "#006600",
    "more info": "#996633",
    "DEFAULT": "#616161",  # Default color
}


# Function to get color, defaulting if type not found
def get_action_color(action_type):
    action_type = action_type.lower()
    return ACTION_COLORS.get(action_type, ACTION_COLORS["DEFAULT"])


st.set_page_config(layout="wide")

st.title("Customer Service Dashboard")

# Initialize session state
if "selected_ticket_id" not in st.session_state:
    st.session_state.selected_ticket_id = tickets[0].id if tickets else None

# --- Sidebar ---
st.sidebar.title("Voicemails")

# Use streamlit-antd-components menu
with st.sidebar:
    print(
        f"--- Sidebar Start: session_state.id = {st.session_state.get('selected_ticket_id')} ---"
    )  # DEBUG
    # Prepare items for sac.menu as a list of dictionaries
    menu_items = [
        sac.MenuItem(
            label=ticket.name,
            tag=[
                sac.Tag(
                    action["action"],
                    color=get_action_color(action["action"]),
                )
                for action in ticket.actions
            ],
            description=datetime.datetime.fromisoformat(ticket.created_at).strftime(
                "%b %d, %Y, %H:%M"
            ),
        )
        for ticket in tickets
    ]

    # selected_label will be the label string returned by sac.menu
    selected_index = sac.menu(
        items=menu_items,
        key="sac_menu",
        return_index=True,  # Important: returns the label (default behavior without format_func?)
    )

    # Find the actual ID corresponding to the returned label
    selected_id = tickets[selected_index].id

    # Update session state *using the correct integer ID* if the selection changed
    # print(f"--- Before comparison: selected_id = {selected_id}, session_state.id = {st.session_state.get('selected_ticket_id')} ---") # DEBUG Removed
    if selected_id is not None and selected_id != st.session_state.selected_ticket_id:
        # print(f"--- *** Updating session state! *** ---") # DEBUG Removed
        st.session_state.selected_ticket_id = selected_id  # Store the correct ID
        st.rerun()


# --- Main Area ---
# Find the selected ticket *after* potential selection updates
with st.container(border=True):
    selected_ticket = None
    if st.session_state.selected_ticket_id:
        for t in tickets:
            if t.id == st.session_state.selected_ticket_id:
                selected_ticket = t
                break

    if selected_ticket:
        # --- Header ---
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(selected_ticket.name)
            st.markdown("**Actions:**")
            for action in selected_ticket.actions:
                with st.expander(f"**{action['action'].capitalize()}**"):
                    st.write(action["details"])
        with col2:
            st.write(f"**DOB:** {selected_ticket.dob}")
            st.write(f"**Status:** {selected_ticket.status}")

        st.divider()

        # --- AI Summary & Links ---
        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader("AI Summary")
            st.write(selected_ticket.ai_summary)
        with col2:
            with st.expander("See transcript"):
                st.write(selected_ticket.transcript)

            if selected_ticket.audio_url:
                st.audio(selected_ticket.audio_url)
            else:
                if st.button("Listen"):
                    st.warning("Audio playback not available for this item.")

        st.divider()

        # --- Action Buttons ---
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            if st.button("Mark Complete"):
                st.success(f"Ticket {selected_ticket.id} marked as complete!")
                # TODO: Update the ticket status in the database
        with col2:
            if st.button("Reassign"):
                st.info(
                    f"Reassign functionality for ticket {selected_ticket.id} not implemented yet."
                )
                # TODO: Implement reassign functionality

    else:
        st.write("Select a voicemail from the list on the left to view details.")
