import streamlit as st

# CSS로 아파트 테두리와 조명 효과 정의
st.markdown("""
    <style>
    .apartment-block {
        border: 3px solid #333;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        background-color: #f9f9f9;
    }
    .window-lit {
        background-color: #FFD700; /* 불 켜진 노란색 */
        padding: 5px;
        border-radius: 5px;
        color: black;
        font-weight: bold;
    }
    .window-off {
        background-color: #eee;
        padding: 5px;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# 101동 데이터
words = ["School", "House", "Room", "Desk", "Chair"]

st.title("🏠 영단어 아파트 단지")

# 101동 건물 테두리 박스 시작
with st.container():
    st.markdown('<div class="apartment-block">', unsafe_allow_html=True)
    st.subheader("🏢 101동 (사물과 장소)")
    
    # 단어별 체크박스 및 창문 효과
    for word in words:
        # 상태 관리: 세션에 학습 여부 저장
        if word not in st.session_state:
            st.session_state[word] = False
            
        checked = st.checkbox(f"단어: {word}", key=word)
        st.session_state[word] = checked
        
        # 불 켜기 시각화
        if st.session_state[word]:
            st.markdown(f'<p class="window-lit">💡 {word} 학습 완료!</p>', unsafe_allow_html=True)
        else:
            st.markdown(f'<p class="window-off">🌑 {word} 공부하기</p>', unsafe_allow_html=True)
            
    st.markdown('</div>', unsafe_allow_html=True)
