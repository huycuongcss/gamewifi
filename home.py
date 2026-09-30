import streamlit as st
import ran
import chim
import duaxe


st.set_page_config(
    page_title="Trang chủ",
    page_icon="🏠"
)
st.title("GAMEWIFI")
st.write("game miễn phí đầy đủ mọi thứ ")


menu = st.sidebar.selectbox(
    "Chọn chức năng",
    [
        "🎮 Giải trí",
        "🎵 Thư giãn",
        
    ]
)
if menu == "🎮 Giải trí":
    chon = st.selectbox("Chọn trò chơi",
                        ["Rắn săn mồi",
                         "Đua xe",
                         "Con chim bay"]
    )
    if chon =="Rắn săn mồi":
        ran.main()
    elif chon =="Đua xe":
        duaxe.main()
    elif chon =="Con chim bay":
        chim.main()


st.markdown("---")
st.caption("🚨 Bản quyền: Huy Phúc")