import streamlit as st

# 아파트 동별 데이터 (예시)
apartments = {
    "101동": ["School", "House", "Room", "Desk", "Chair"],
    "102동": ["Eat", "Sleep", "Run", "Walk", "Jump"]
}

st.title("🏠 영단어 아파트 단지")

# 동 선택
selected_apt = st.selectbox("학습할 동을 선택하세요", list(apartments.keys()))

st.subheader(f"{selected_apt} 학습하기")

# 단어 체크박스 (불 켜기 효과)
for word in apartments[selected_apt]:
    # 세션 상태로 학습 여부 저장
    if st.checkbox(f"{word} 공부 완료!"):
        st.write(f"💡 **{word}** 불이 켜졌습니다!")
    else:
        st.write(f"🌑 {word}")

# 진척도 확인
st.sidebar.title("전체 단지 현황")
st.sidebar.progress(0.2) # 여기서 동별 학습률 계산
