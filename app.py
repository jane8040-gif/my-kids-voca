import streamlit as st
import google.generativeai as genai
from PIL import Image

st.title("📝 우리 아이 맞춤 영단어 체크봇")

api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("API Key가 설정되지 않았습니다. Secrets 설정을 확인하세요.")
else:
    genai.configure(api_key=api_key)
    
    # 모델 이름을 명시하지 않거나, 가장 범용적인 방식으로 호출합니다.
    # 만약 아래 코드도 오류가 나면 'gemini-1.5-flash'를 사용하되, 
    # 구글 AI 스튜디오 설정에서 권한을 다시 확인해야 합니다.
    model = genai.GenerativeModel('gemini-1.5-flash')

    uploaded_file = st.file_uploader("사진을 올려주세요", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='올린 이미지', use_column_width=True)
        
        if st.button("분석 시작"):
            st.write("분석 중...")
            try:
                # 명령어를 조금 더 간결하게 수정
                prompt = "이 이미지에서 형광펜으로 칠해진 영어 단어들을 찾아서 1. 단어, 2. 뜻, 3. 예문 순서로 표를 만들어줘."
                response = model.generate_content([prompt, image])
                st.subheader("📚 분석 결과")
                st.write(response.text)
            except Exception as e:
                st.error(f"분석 중 오류 발생: {e}")
                st.write("팁: 404 오류가 반복되면, API 키를 생성한 프로젝트가 Gemini API를 정상적으로 지원하는지 확인해주세요.")
