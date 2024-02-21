import streamlit as st


def configure_api_key(key_name, default_value=""):
    """
    Checks if a key is present in the session state. If not, sets a default value
    and automatically generates and displays a warning message based on the key name.

    Parameters:
    - key_name (str): The name of the key to check in the session state.
    - default_value (str, optional): The default value to set if the key is not present. Defaults to an empty string.
    """
    # Automatically generate a friendly name for the key to use in the warning message
    friendly_name = key_name.replace("_", " ").title()

    # Automatically generate the warning message
    warning_message = f"Please set your {friendly_name} in the settings page."

    if key_name not in st.session_state:
        st.session_state[key_name] = default_value
        with st.container():
            st.warning(warning_message)
