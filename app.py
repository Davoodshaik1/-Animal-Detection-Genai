### Health Management APP
from dotenv import load_dotenv

load_dotenv() 

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load Google Gemini Pro Vision API And get response

def get_gemini_repsonse(input,image,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,image[0],prompt])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        return None
    
##initialize our streamlit app

st.set_page_config(page_title="Animal Species Detection")

st.header("ANIMAL SPECIES DETECTION")
input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit=st.button("Tell me this animal ")

input_prompt="""
You are an expert in animal species identification, and you need to provide detailed information about the species depicted in the image.

Please use the following details to describe the identified species:

1. **Common Name:** [Common name of the species]
2. **Scientific Name:** [Scientific name of the species]
3. **Description:** [Brief description of the species, including its physical characteristics, habitat, behavior, and any distinctive features]
4. **Range:** [Geographical range where the species is commonly found, including continents, countries, or specific ecosystems]
5. **Conservation Status:** [Conservation status of the species, indicating whether it is endangered, vulnerable, or of least concern according to organizations like the IUCN]
6. **Ecological Role:** [Discussion of the ecological role of the species within its habitat or ecosystem, such as its position in the food chain, interactions with other species, or contributions to ecosystem services]
7. **Interesting Facts:** [Any interesting or unique facts about the species that may capture the user's attention and deepen their understanding of its significance]

Feel free to include additional images or videos of the species in its natural habitat to enhance the user's learning experience.

"""

## If submit button is clicked

if submit:
    image_data=input_image_setup(uploaded_file)
    if image_data is not None:
        response=get_gemini_repsonse(input_prompt,image_data,input)

        # Check if the response indicates a failure to detect an animal
        if "No animal detected" in response:
            st.warning("Please upload a valid image containing an animal.")
        else:
            # Add border around output
            st.markdown('<style>div.Widget.row-widget.stRadio > div{flex-direction:column;}</style>',unsafe_allow_html=True)
            st.subheader("The Response is")
            st.markdown(
              response 
            )
