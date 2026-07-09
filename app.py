import streamlit as st
import google.generativeai as genai
from PIL import Image

st.title("📝 우리 아이 맞춤 영단어 체크봇")

# API 키 가져오기
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("API Key가 설정되지 않았습니다. 스트림릿 Secrets 설정을 확인하세요.")
else:
    genai.configure(api_key=api_key)
    
    # [수정된 부분] 모델 이름을 특정하지 않고, 
    # 현재 계정에서 지원하는 가장 안정적인 모델인 'gemini-1.5-flash'를 기본값으로 사용합니다.
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"모델 연결 실패: {e}")

    uploaded_file = st.file_uploader("사진을 올려주세요", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='올린 이미지', use_column_width=True)
        
        if st.button("분석 시작"):
            st.write("분석 중...")
            try:
                prompt = "이 이미지에서 형광펜으로 표시된 영어 단어를 찾아서 1. 단어, 2. 뜻, 3. 예문 순서로 표(Table)로 정리해줘."
                response = model.generate_content([prompt, image])
                st.subheader("📚 오늘의 맞춤 단어장")
                st.write(response.text)
            except Exception as e:
                st.error(f"분석 중 오류 발생: {e}")
                st.info("팁: 404 오류가 계속된다면, Google AI Studio에서 생성한 API 키가 활성화된 프로젝트인지 확인해주세요.")
