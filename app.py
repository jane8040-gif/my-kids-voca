import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# 페이지 설정
st.set_page_config(page_title="우리 아이 맞춤 영단어 체크봇", layout="centered")

st.title("📝 우리 아이 맞춤 영단어 체크봇")
st.write("아이의 책이나 공책 사진을 찍어 올려주세요. 형광펜 친 단어들을 제미나이 AI가 쏙쏙 골라내어 단어장으로 만들어 드립니다!")

# 1단계에서 발급받은 API 키를 안전하게 가져오는 설정입니다.
# (스트림릿 설정창에 넣는 법은 아래 3단계에서 알려드릴게요!)
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.warning("⚠️ 구글 제미나이 API Key가 설정되지 않았습니다. 스트림릿 비밀 설정(Secrets)에 키를 입력해 주세요.")
else:
    # Gemini AI 두뇌 깨우기
    genai.configure(api_key=api_key)
    # 이미지 인식에 최신 제미나이 모델 사용
    model = genai.GenerativeModel('gemini-1.5-pro-latest')

    # 파일 업로드 창 생성
    uploaded_file = st.file_uploader("📸 영어 문장이나 형광펜 친 사진을 올려주세요", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        # 올린 이미지 화면에 보여주기
        image = Image.open(uploaded_file)
        st.image(image, caption='올린 이미지 확인', use_column_width=True)
        
        st.write("🔄 제미나이 AI가 형광펜 단어를 분석하고 분류하는 중입니다...")
        
        # Gemini AI에게 보낼 프롬프트 명령어 (아이 맞춤 교정)
        prompt = """
        이 이미지에서 하이라이트(형광펜) 처리된 영어 단어나 문장을 찾아서 분석해 주세요.
        만약 명확한 형광펜 표시가 없더라도 문맥상 중요해 보이는 초등/중등 필수 핵심 영단어들을 골라내어 분류해 주세요.
        
        결과는 아이들이 보기 쉽게 다음과 같은 깔끔한 표 형태로 출력해 주세요:
        1. 단어 (Word)
        2. 뜻 (Meaning)
        3. 예문 (Example Sentence)
        
        마지막에는 오늘 공부한 단어들을 조합하여 아이가 소리내어 읽기 좋은 '하루 한 줄 영어 한마디'를 친근한 말투로 추천해 주세요.
        """
        
        try:
            # AI에게 이미지와 명령어를 보내서 답변 받기
            response = model.generate_content([prompt, image])
            
            st.success("✨ 분석 완료!")
            st.subheader("📚 오늘의 맞춤 단어장")
            st.write(response.text)
            
        except Exception as e:
            st.error(f"오류가 발생했습니다. 다시 시도해 주세요. (상세에러: {e})")
