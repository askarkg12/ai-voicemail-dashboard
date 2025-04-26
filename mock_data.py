
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