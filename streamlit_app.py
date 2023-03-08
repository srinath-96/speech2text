# Libraries to be used ------------------------------------------------------------

import streamlit as st
import requests
import json
import os
import pyaudio
import base64
# title and favicon ------------------------------------------------------------

st.set_page_config(
    page_title="Speech-to-Text Transcription App", page_icon="-o-", layout="wide"
)

# App layout width -------------------------------------------------


def _max_width_():
    max_width_str = f"max-width: 2400px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>
    """,
        unsafe_allow_html=True,
    )


_max_width_()

# logo and header -------------------------------------------------

c30, c31, c32 = st.columns([2.5, 1, 3])

with c30:
    st.image(r"C:\Users\Dell\Desktop\speech-to-text-streamlit-app-main\logo.png", width=700)
    st.header("")

with c32:

    st.title("")
    st.title("")
    st.caption("")
    st.caption("")
    st.caption("")
    st.caption("")
    st.caption("")
    st.caption("")

    st.write()
       
st.text("")
st.markdown(
    f"""
                    The speech to text recognition is done via the (https://huggingface.co/theainerd/Wav2Vec2-large-xlsr-hindi)
                    """
)
st.text("")

# region Main

# multi navbar -------------------------------------------------


def main():
    pages = {
        "Wav file": API_key,
        "Real Time":demo
    }

    if "page" not in st.session_state:
        st.session_state.update(
            {
                # Default page
                "page": "Home",
                "run" : False ,
                "text" : "Listening to your Audio..."
            }
        )

    with st.sidebar:
        page = st.radio("Select your mode", tuple(pages.keys()))

    pages[page]()



# endregion main

# Free mode -------------------------------------------------
def start_listening():
	st.session_state['run'] = True

def stop_listening():
	st.session_state['run'] = False

def demo():

    c1, c2, c3 = st.columns([1, 4, 1])
    with c2:
        
        with st.form(key="my_form"):
            
            text_input = st.text_input("Enter your HuggingFace API key")
            FRAMES_PER_BUFFER = int(st.sidebar.text_input('Frames per buffer', 3200))
            FORMAT = pyaudio.paInt16
            CHANNELS = 1
            RATE = int(st.sidebar.text_input('Rate', 16000))
            p = pyaudio.PyAudio()

            # Open an audio stream with above parameter settings
            f = p.open(
               format=FORMAT,
               channels=CHANNELS,
               rate=RATE,
               input=True,
               frames_per_buffer=FRAMES_PER_BUFFER
            )


            c2.button('Start', on_click=start_listening)
            c2.button('Stop', on_click=stop_listening)
            
            st.info(
                f"""
                        👆 record audio: 
                        """
            )
    
            submit_button = st.form_submit_button(label="Transcribe")
    
    if not submit_button:
    
        st.stop()
    
    else:
    
        try:
    
            if f is not None:
                data = f.read(FRAMES_PER_BUFFER)
                bytes_data = base64.b64encode(data)
                # getsize
                getsize=20
                if getsize < 30:  # File more than 30MB

    
                    api_token = text_input
    
                    headers = {"Authorization": f"Bearer {api_token}"}
                    API_URL = "https://api-inference.huggingface.co/models/theainerd/Wav2Vec2-large-xlsr-hindi"
    
                    def query(data):
                        response = requests.request(
                            "POST", API_URL, headers=headers, data=data
                        )
                        return json.loads(response.content.decode("utf-8"))
    
                    data = query(bytes_data)
    
                    # data = query(bytes_data)
    
                    values_view = data.values()
                    value_iterator = iter(values_view)
                    text_value = next(value_iterator)
                    text_value = text_value.lower()
                    st.success(text_value)
    
                    c0, c1 = st.columns([2, 2])
    
                    with c0:
                        st.download_button(
                            "Download the transcription",
                            text_value,
                            file_name=None,
                            mime=None,
                            key=None,
                            help=None,
                            on_click=None,
                            args=None,
                            kwargs=None,
                        )
    
                else:
                    st.error(
                        "This app is still in early development so we've maxed out the file size limit. Please try again with a smaller file."
                    )
                    st.stop()
    
            else:
                path_in = None
                st.info(
                    f"""
                        👆 Upload a .wav file. Or try a sample: [Wav sample 01](https://github.com/CharlyWargnier/CSVHub/blob/main/Wave_files_demos/Welcome.wav?raw=true) | [Wav sample 02](https://github.com/CharlyWargnier/CSVHub/blob/main/Wave_files_demos/The_National_Park.wav?raw=true)
                        """
                )
    
        except ValueError:
            "ValueError"



# Custom API key mode -------------------------------------------------


def API_key():

    c1, c2, c3 = st.columns([1, 4, 1])
    with c2:

        with st.form(key="my_form"):

            text_input = st.text_input("Enter your HuggingFace API key")

            f = st.file_uploader("", type=[".wav"])

            st.info(
                f"""
                        👆 Upload a .wav file. Or record audio: 
                        """
            )

            submit_button = st.form_submit_button(label="Transcribe")

    if not submit_button:

        st.stop()

    else:

        try:

            if f is not None:
                path_in = f.name
                # Get file size from buffer
                # Source: https://stackoverflow.com/a/19079887
                old_file_position = f.tell()
                f.seek(0, os.SEEK_END)
                getsize = f.tell()  # os.path.getsize(path_in)
                f.seek(old_file_position, os.SEEK_SET)
                getsize = round((getsize / 1000000), 1)
                # st.caption("The size of this file is: " + str(getsize) + "MB")
                # getsize

                if getsize < 30:  # File more than 30MB

                    # To read file as bytes:
                    bytes_data = f.getvalue()

                    api_token = text_input

                    headers = {"Authorization": f"Bearer {api_token}"}
                    API_URL = "https://api-inference.huggingface.co/models/theainerd/Wav2Vec2-large-xlsr-hindi"

                    def query(data):
                        response = requests.request(
                            "POST", API_URL, headers=headers, data=data
                        )
                        return json.loads(response.content.decode("utf-8"))

                    data = query(bytes_data)

                    # data = query(bytes_data)

                    values_view = data.values()
                    value_iterator = iter(values_view)
                    text_value = next(value_iterator)
                    text_value = text_value.lower()

                    st.success(text_value)

                    c0, c1 = st.columns([2, 2])

                    with c0:
                        st.download_button(
                            "Download the transcription",
                            text_value,
                            file_name=None,
                            mime=None,
                            key=None,
                            help=None,
                            on_click=None,
                            args=None,
                            kwargs=None,
                        )

                else:
                    st.error(
                        "This app is still in early development so we've maxed out the file size limit. Please try again with a smaller file."
                    )
                    st.stop()

            else:
                path_in = None
                st.info(
                    f"""
                        👆 Upload a .wav file. Or try a sample: [Wav sample 01](https://github.com/CharlyWargnier/CSVHub/blob/main/Wave_files_demos/Welcome.wav?raw=true) | [Wav sample 02](https://github.com/CharlyWargnier/CSVHub/blob/main/Wave_files_demos/The_National_Park.wav?raw=true)
                        """
                )

        except ValueError:
            "ValueError"


# Notes about the app -------------------------------------------------

with st.expander("ℹ️ - About this app", expanded=False):

    st.write(
        """     

-   Speech to text for hindi language.
-   Currently works with wav files and the Live recorded audio is in progress
	    """
    )

    st.markdown("")



if __name__ == "__main__":
    main()
