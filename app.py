import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. API 키 설정
api_key = st.secrets.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# 2. 이번에는 'v1' 경로를 강제로 지정합니다. 
# 구글 API에서 모델을 인식하는 정식 명칭은 아래와 같습니다.
model = genai.GenerativeModel('gemini-1.5-flash-002') 

st.title("📝 우리 아이 맞춤 영단어 체크봇")

uploaded_file = st.file_uploader("사진을 올려주세요", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='올린 이미지', use_column_width=True)
    
    if st.button("분석 시작"):
        try:
            # 3. 모델에 버전을 강제하는 대신 모델명을 최신 버전인 -002로 변경했습니다.
            response = model.generate_content(["이 이미지에서 영단어를 찾아 1.단어 2.뜻 3.예문 순서로 표를 만들어줘.", image])
            st.write(response.text)
        except Exception as e:
            st.error(f"오류 발생: {e}")
