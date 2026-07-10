import streamlit as st

# 1. 세션 상태 초기화 (루프 밖에서 미리 선언)
if 'learned_words' not in st.session_state:
    st.session_state.learned_words = {}

words = ["School", "House", "Room", "Desk", "Chair"]

# 초기화가 안 된 단어들을 세션 상태에 추가
for word in words:
    if word not in st.session_state.learned_words:
        st.session_state.learned_words[word] = False

st.title("🏠 영단어 아파트 단지")

with st.container():
    st.subheader("🏢 101동 (사물과 장소)")
    
    # 2. 체크박스에서 바로 상태를 할당하지 않고, callback이나 딕셔너리 접근 사용
    for word in words:
        # 체크박스 상태를 세션 상태와 동기화
        is_checked = st.checkbox(f"단어: {word}", key=word, value=st.session_state.learned_words[word])
        st.session_state.learned_words[word] = is_checked
        
        # 불 켜기 시각화
        if st.session_state.learned_words[word]:
            st.markdown(f'<p style="background-color: #FFD700; padding: 5px;">💡 {word} 학습 완료!</p>', unsafe_allow_html=True)
        else:
            st.markdown(f'<p style="background-color: #eee; padding: 5px;">🌑 {word} 공부하기</p>', unsafe_allow_html=True)
