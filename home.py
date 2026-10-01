import streamlit as st
import ran
import chim
import duaxe
import thugian
import apple
import pvz

st.set_page_config(
    page_title="Trang chủ",
    page_icon="🐖"
)
st.title("GAMEWIFI")
st.write("game miễn phí đầy đủ mọi thứ ")


menu = st.sidebar.selectbox(
    "Bạn cần gì cung có trừ người yêu:",
    [
        "🎮 Giải trí",
        "🎵 Thư giãn",
        
    ]
)
if menu == "🎮 Giải trí":
    chon = st.selectbox("Chọn trò chơi",
                        ["🐍Rắn săn mồi",
                         "🚗Đua xe",
                         "🦅Con chim bay",
                         "🍎 Hứng Táo",
                         "🧟Plants vs Zombies"]
    )
    if chon =="🐍Rắn săn mồi":
        ran.main()
    elif chon =="🚗Đua xe":
        duaxe.main()
    elif chon =="🦅Con chim bay":
        chim.main()
    elif chon =="🍎 Hứng Táo":
        apple.main()
    elif chon =="🧟Plants vs Zombies":
        pvz.main()
elif menu =="🎵 Thư giãn":
    thugian.main()

st.markdown("---")
st.caption("🚨 Bản quyền: Huy Phúc")