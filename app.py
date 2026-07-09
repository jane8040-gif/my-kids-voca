Python
import streamlit as st
import time
import json
import os

# 페이지 기본 설정
st.set_page_config(
    page_title="한입 영단어 암기 봇",
    page_icon="✏️",
    layout="centered"
)

# 스타일 커스텀 (아이들이 보기 편한 큰 글씨와 깔끔한 디자인)
st.markdown("""
    <style>
    .big-title { font-size: 30px !important; font-weight: bold; color: #1E3A8A; text-align: center; margin-bottom: 20px; }
    .word-box { font-size: 45px !important; font-weight: bold; color: #2563EB; text-align: center; padding: 20px; background-color: #F0F4FF; border-radius: 15px; margin: 20px 0; border: 2px solid #BFDBFE; }
    .meaning-box { font-size: 24px !important; text-align: center; color: #4B5563; margin-bottom: 30px; }
    .score-text { font-size: 22px !important; font-weight: bold; color: #059669; text-align: center; }
    div.stButton > button { font-size: 20px !important; padding: 10px 24px !important; border-radius: 12px !important; width: 100%; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">✏️ 우리 아이 맞춤 영단어 체크봇</div>', unsafe_allow_html=True)

# 세션 상태(State) 초기화 (페이지 이동 시 데이터 유지)
if 'step' not in st.session_state:
    st.session_state.step = 'upload'  # upload -> study -> test -> result
if 'words' not in st.session_state:
    st.session_state.words = []
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = {}
if 'test_start_time' not in st.session_state:
    st.session_state.test_start_time = None

# --- 1단계: 사진 업로드 및 단어 추출 ---
if st.session_state.step == 'upload':
    st.subheader("📸 1단계: 형광펜 친 책 사진을 올려주세요!")
    uploaded_file = st.file_uploader("사진을 찍어 올리면 AI가 단어를 뽑아줍니다.", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="우리 아이 공부 흔적", use_container_width=True)
        
        if st.button("✨ 단어장 만들기 (AI 분석 시작)"):
            with st.spinner("AI가 형광펜 단어를 읽는 중..."):
                time.sleep(2) # 데모용 부드러운 딜레이
                
                # 테스트용 샘플 데이터 (Gemini API를 연결하면 이 자리에 자동 추출된 단어가 들어갑니다)
                st.session_state.words = [
                    {"word": "APPLE", "meaning": "사과"},
                    {"word": "BANANA", "meaning": "바나나"},
                    {"word": "CHAIR", "meaning": "의자"},
                    {"word": "DESK", "meaning": "책상"}
                ]
                st.session_state.step = 'study'
                st.rerun()

# --- 2단계: 깜빡이 암기 (공부하기) ---
elif st.session_state.step == 'study':
    st.subheader("🔊 2단계: 시험 보기 전에 먼저 읽어봐요!")
    
    words = st.session_state.words
    idx = st.session_state.current_index
    
    st.progress((idx + 1) / len(words))
    st.write(f"단어 {idx + 1} / {len(words)}")
    
    st.markdown(f'<div class="word-box">{words[idx]["word"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="meaning-box">뜻: {words[idx]["meaning"]}</div>', unsafe_allow_html=True)
    
    st.info("💡 발음을 귀로 들으면서 입으로 크게 3번 따라 읽어보세요!")
    
    col1, col2 = st.columns(2)
    with col1:
        if idx > 0:
            if st.button("⬅️ 이전 단어"):
                st.session_state.current_index -= 1
                st.rerun()
    with col2:
        if idx < len(words) - 1:
            if st.button("다음 단어 ➡️"):
                st.session_state.current_index += 1
                st.rerun()
        else:
            if st.button("🔥 공부 끝! 시험 보러 가기"):
                st.session_state.step = 'test'
                st.session_state.current_index = 0
                st.session_state.test_start_time = time.time()
                st.rerun()

# --- 3단계: 시간 제한 철자 시험 ---
elif st.session_state.step == 'test':
    st.subheader("⏱️ 3단계: 단어 맞추기 게임!")
    
    # 타이머 (60초 제한)
    elapsed_time = int(time.time() - st.session_state.test_start_time)
    time_left = max(0, 60 - elapsed_time)
    
    st.metric(label="⏱️ 남은 시간", value=f"{time_left}초")
    if time_left == 0:
        st.error("🚨 시간이 끝났어요! 결과 창으로 이동합니다.")
        if st.button("결과 보러 가기"):
            st.session_state.step = 'result'
            st.rerun()
            
    words = st.session_state.words
    idx = st.session_state.current_index
    
    st.write(f"문제 {idx + 1} / {len(words)}")
    st.markdown(f'<div class="word-box">뜻: {words[idx]["meaning"]}</div>', unsafe_allow_html=True)
    
    user_input = st.text_input("여기에 올바른 영어 철자를 입력하세요:", key=f"q_{idx}").strip().upper()
    
    # 철자 하나하나 실시간 체크 (초록색 ✅ / 빨간색 ❌ 피드백)
    target_word = words[idx]["word"]
    if user_input:
        match_str = ""
        for i, char in enumerate(user_input):
            if i < len(target_word):
                if char == target_word[i]:
                    match_str += f" ✅ {char} "
                else:
                    match_str += f" ❌ {char} "
        st.markdown(f"**실시간 글자 확인:** {match_str}")

    if st.button("제출 후 다음 문제"):
        st.session_state.user_answers[idx] = user_input
        if idx < len(words) - 1:
            st.session_state.current_index += 1
        else:
            st.session_state.step = 'result'
        st.rerun()

# --- 4단계: 채점 결과창 ---
elif st.session_state.step == 'result':
    st.markdown('<div class="big-title">🎉 대단해요! 시험을 마쳤어요!</div>', unsafe_allow_html=True)
    
    words = st.session_state.words
    answers = st.session_state.user_answers
    
    correct_count = 0
    wrong_words = []
    
    for i, item in enumerate(words):
        user_ans = answers.get(i, "").strip().upper()
        if user_ans == item["word"]:
            correct_count += 1
        else:
            wrong_words.append({"word": item["word"], "meaning": item["meaning"], "user": user_ans})
            
    score = int((correct_count / len(words)) * 100)
    st.markdown(f'<div class="score-text">🎯 점수: {score}점! ({correct_count}개 맞춤)</div>', unsafe_allow_html=True)
    
    if score == 100:
        st.balloons() # 100점 축하 폭죽 팝업!
        st.success("🏅 우와! 완벽해요! 아주 멋진 실력이에요!")
    else:
        st.warning("👍 정말 열심히 잘했어요! 틀린 단어는 복습해 봐요.")
        st.write("📚 **오답 노트**")
        for w in wrong_words:
            st.markdown(f"- **{w['meaning']}**: 정답은 **{w['word']}** (내가 쓴 답: `{w['user'] if w['user'] else '공란'}`)")
            
    if st.button("🔄 새로운 사진으로 또 하기"):
        st.session_state.step = 'upload'
        st.session_state.words = []
        st.session_state.current_index = 0
        st.session_state.user_answers = {}
        st.session_state.test_start_time = None
        st.rerun()
