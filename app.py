import streamlit as st
import google.generativeai as genai
from PIL import Image

st.title("📝 우리 아이 맞춤 영단어 체크봇")

# Secrets에서 API 키를 가져옵니다.
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("API Key가 설정되지 않았습니다. 스트림릿 Secrets 설정을 확인하세요.")
else:
    genai.configure(api_key=api_key)
    
    # [최종] 모델 이름을 이렇게 지정하세요. 
    # 이게 구글에서 가장 공식적으로 권장하는 방식입니다.
    model = genai.GenerativeModel('gemini-1.5-flash')

    uploaded_file = st.file_uploader("사진을 올려주세요", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='올린 이미지', use_column_width=True)
        
        if st.button("분석 시작"):
            st.write("분석 중...")
            try:
                prompt = "이 이미지에서 형광펜으로 표시된 영단어를 찾아 1.단어 2.뜻 3.예문 순서로 표를 만들어줘."
                response = model.generate_content([prompt, image])
                st.subheader("📚 오늘의 맞춤 단어장")
                st.write(response.text)
            except Exception as e:
                st.error(f"분석 중 오류 발생: {e}")
