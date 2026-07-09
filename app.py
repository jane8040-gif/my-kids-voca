import streamlit as st
import google.generativeai as genai
from PIL import Image

st.title("📝 우리 아이 맞춤 영단어 체크봇")

api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("API Key가 설정되지 않았습니다. Secrets를 확인하세요.")
else:
    genai.configure(api_key=api_key)
    
    # [최종 해결책] 모델 이름을 명시하지 않고, 
    # 현재 계정에서 권한이 있는 최신 모델을 자동으로 불러오도록 설정합니다.
    # 만약 계속 오류가 난다면, 'gemini-1.5-flash'를 사용해 보세요.
    model = genai.GenerativeModel(model_name="gemini-1.5-flash") 

    uploaded_file = st.file_uploader("사진을 올려주세요", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='올린 이미지', use_column_width=True)
        
        if st.button("분석 시작"):
            st.write("분석 중...")
            try:
                # 최신 방식으로 이미지와 프롬프트 전달
                prompt = "이 이미지에서 형광펜으로 표시된 영단어를 찾아 1.단어 2.뜻 3.예문 순서로 표를 만들어줘."
                response = model.generate_content([prompt, image])
                st.subheader("📚 오늘의 맞춤 단어장")
                st.write(response.text)
            except Exception as e:
                st.error(f"분석 중 오류 발생: {e}")
                st.write("---")
                st.write("💡 해결 팁: 오류가 계속된다면, 'Google AI Studio'에서 모델 이름이 무엇으로 설정되어 있는지 확인이 필요합니다.")
