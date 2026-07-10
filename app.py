import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. API 키 가져오기
api_key = st.secrets.get("GEMINI_API_KEY")

# 2. 인증 설정 시 API 버전을 'v1'으로 명시적으로 지정
genai.configure(api_key=api_key)

# 3. 모델 호출 (v1beta 충돌을 피하기 위해 이름을 좀 더 정확히 명시)
# gemini-1.5-flash 모델을 v1 환경에서 호출하도록 설정
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("📝 우리 아이 맞춤 영단어 체크봇")

uploaded_file = st.file_uploader("사진을 올려주세요", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='올린 이미지', use_column_width=True)
    
    if st.button("분석 시작"):
        st.write("분석 중...")
        try:
            # generate_content 호출
            response = model.generate_content(["이 이미지에서 영단어를 찾아 1.단어 2.뜻 3.예문 순서로 표를 만들어줘.", image])
            st.subheader("📚 오늘의 맞춤 단어장")
            st.write(response.text)
        except Exception as e:
            # 오류 내용을 구체적으로 확인
            st.error(f"오류 발생: {e}")
