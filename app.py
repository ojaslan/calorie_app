from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

load_dotenv()  # Load all environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Styling
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
        padding: 20px;
    }
    .title {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        color: #4CAF50;
    }
    .subtitle {
        font-size: 20px;
        font-weight: 600;
        color: #555;
        margin-bottom: 15px;
    }
    .response-box {
        background-color: #ffffff;
        border-left: 6px solid #4CAF50;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        margin-top: 20px;
        font-size: 18px;
    }
    .upload-box {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="title">🍽️ ByteCal</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Estimate your food calories just by uploading an image</div>', unsafe_allow_html=True)

# Input
input = st.text_input("🔍 Custom Prompt (Optional):", key="input")

# Upload Image
st.markdown('<div class="upload-box">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("📷 Upload a food image (JPG/PNG):", type=["jpg", "jpeg", "png"])
st.markdown('</div>', unsafe_allow_html=True)

image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="📸 Uploaded Image", use_column_width=True)

# Submit Button
submit = st.button("✅ Tell me the total calories")

# Prompt Template
input_prompt = """
You are an expert nutritionist. Analyze the food items in the image and estimate:
1. Total calorie count
2. A detailed breakdown of each food item and its calorie content

Format:
1. Item 1 - XX calories
2. Item 2 - XX calories
...
"""

# Helper Functions
def get_gemini_repsonse(input, image, prompt):
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    response = model.generate_content([input, image[0], prompt])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{"mime_type": uploaded_file.type, "data": bytes_data}]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Generate Output
if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_repsonse(input_prompt, image_data, input)

    st.markdown('<div class="response-box">', unsafe_allow_html=True)
    st.subheader("📝 Nutritional Analysis")
    st.write(response)
    st.markdown('</div>', unsafe_allow_html=True)
