import streamlit as st
import google.generativeai as genai
from PIL import Image

st.title("📝 우리 아이 맞춤 영단어 체크봇")

# 1. API 키 가져오기
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("API Key가 설정되지 않았습니다. Secrets 설정을 확인하세요.")
else:
    genai.configure(api_key=api_key)
    
    # 2. 모델 선택 (오류를 방지하기 위해 가장 안정적인 모델 사용)
    # 1.5-flash가 안 된다면 gemini-pro를 사용하도록 설정
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
    except:
        model = genai.GenerativeModel('gemini-pro')

    uploaded_file = st.file_uploader("사진을 올려주세요", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='올린 이미지', use_column_width=True)
        
        if st.button("분석 시작"):
            st.write("분석 중...")
            try:
                prompt = "이 이미지에서 형광펜으로 표시된 영어 단어를 찾아 표(단어, 뜻, 예문)로 정리해줘."
                response = model.generate_content([prompt, image])
                st.subheader("결과")
                st.write(response.text)
            except Exception as e:
                st.error(f"분석 중 오류 발생: {e}")
                st.write("팁: 만약 404 오류가 계속되면, Google AI Studio에서 모델 접근 권한이 최신인지 확인해주세요.")
