import streamlit as st

def main():
    st.title("🎵 GÓC THƯ GIÃN")
    st.write("Chọn một nội dung để nghe nhạc:")

    st.link_button(
        "🎵 MỞ YOUTUBE",
        "https://www.youtube.com"
    )

    st.link_button(
        "🌿 Nhạc thư giãn",
        "https://www.youtube.com/results?search_query=nhac+thu+gian"
    )

    st.link_button(
        "☕ Nhạc Cafe Chill",
        "https://www.youtube.com/results?search_query=nhac+cafe+chill"
    )

    st.link_button(
        "🎹 Piano thư giãn",
        "https://www.youtube.com/results?search_query=piano+relaxing+music"
    )

if __name__ == "__main__":
    main()