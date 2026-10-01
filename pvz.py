```python
import streamlit as st
import random
import time

st.set_page_config(
    page_title="PVZ Mini",
    page_icon="🌱",
    layout="wide"
)

# =========================
# KHỞI TẠO GAME
# =========================

def khoi_tao():
    if "sun" not in st.session_state:
        st.session_state.sun = 150

    if "plants" not in st.session_state:
        st.session_state.plants = {}

    if "zombies" not in st.session_state:
        st.session_state.zombies = []

    if "bullets" not in st.session_state:
        st.session_state.bullets = []

    if "score" not in st.session_state:
        st.session_state.score = 0

    if "game_over" not in st.session_state:
        st.session_state.game_over = False

    if "running" not in st.session_state:
        st.session_state.running = False

    if "last_time" not in st.session_state:
        st.session_state.last_time = time.time()

    if "sun_time" not in st.session_state:
        st.session_state.sun_time = time.time()

    if "zombie_time" not in st.session_state:
        st.session_state.zombie_time = time.time()


# =========================
# TRỒNG CÂY
# =========================

def trong_cay(row, col, loai):

    key = (row, col)

    if key in st.session_state.plants:
        return

    gia = {
        "pea": 50,
        "wall": 50,
        "cherry": 100
    }

    if st.session_state.sun < gia[loai]:
        return

    st.session_state.sun -= gia[loai]

    if loai == "pea":
        st.session_state.plants[key] = {
            "type": "pea",
            "hp": 100
        }

    elif loai == "wall":
        st.session_state.plants[key] = {
            "type": "wall",
            "hp": 300
        }

    elif loai == "cherry":
        st.session_state.plants[key] = {
            "type": "cherry",
            "hp": 1
        }


# =========================
# TẠO ZOMBIE
# =========================

def tao_zombie():

    row = random.randint(0, 4)

    st.session_state.zombies.append({
        "row": row,
        "col": 8,
        "hp": 100,
        "max_hp": 100
    })


# =========================
# BẮN ĐẬU
# =========================

def tao_dan():

    for (row, col), plant in st.session_state.plants.items():

        if plant["type"] == "pea":

            co_zombie = False

            for zombie in st.session_state.zombies:

                if zombie["row"] == row and zombie["col"] > col:
                    co_zombie = True
                    break

            if co_zombie:

                st.session_state.bullets.append({
                    "row": row,
                    "col": col + 1
                })


# =========================
# ĐẠN DI CHUYỂN
# =========================

def cap_nhat_dan():

    dan_moi = []

    for bullet in st.session_state.bullets:

        bullet["col"] += 1

        trung = False

        for zombie in st.session_state.zombies:

            if (
                zombie["row"] == bullet["row"]
                and zombie["col"] >= bullet["col"]
                and zombie["col"] <= bullet["col"] + 1
            ):

                zombie["hp"] -= 25
                trung = True

                if zombie["hp"] <= 0:
                    st.session_state.score += 10

                break

        if not trung and bullet["col"] < 9:
            dan_moi.append(bullet)

    st.session_state.bullets = dan_moi

    st.session_state.zombies = [
        z for z in st.session_state.zombies
        if z["hp"] > 0
    ]


# =========================
# CHERRY BOMB
# =========================

def xu_ly_cherry():

    cherry_can_xoa = []

    for (row, col), plant in st.session_state.plants.items():

        if plant["type"] != "cherry":
            continue

        co_zombie = False

        for zombie in st.session_state.zombies:

            if (
                abs(zombie["row"] - row) <= 1
                and abs(zombie["col"] - col) <= 1
            ):
                co_zombie = True
                break

        if co_zombie:

            zombie_moi = []

            for zombie in st.session_state.zombies:

                if (
                    abs(zombie["row"] - row) <= 1
                    and abs(zombie["col"] - col) <= 1
                ):
                    st.session_state.score += 10
                else:
                    zombie_moi.append(zombie)

            st.session_state.zombies = zombie_moi

            cherry_can_xoa.append((row, col))

    for key in cherry_can_xoa:
        del st.session_state.plants[key]


# =========================
# ZOMBIE ĂN CÂY
# =========================

def zombie_an_cay():

    for zombie in st.session_state.zombies:

        row = zombie["row"]
        col = zombie["col"]

        cell = (row, col)

        if cell in st.session_state.plants:

            plant = st.session_state.plants[cell]

            plant["hp"] -= 10

            if plant["hp"] <= 0:
                del st.session_state.plants[cell]


# =========================
# ZOMBIE DI CHUYỂN
# =========================

def zombie_di_chuyen():

    for zombie in st.session_state.zombies:

        row = zombie["row"]
        col = zombie["col"]

        if (row, col) not in st.session_state.plants:
            zombie["col"] -= 1

        if zombie["col"] <= 0:
            st.session_state.game_over = True
            st.session_state.running = False


# =========================
# NHẶT MẶT TRỜI
# =========================

def tao_mat_troi():

    if time.time() - st.session_state.sun_time >= 8:

        st.session_state.sun += 25
        st.session_state.sun_time = time.time()


# =========================
# RESET
# =========================

def choi_lai():

    st.session_state.sun = 150
    st.session_state.plants = {}
    st.session_state.zombies = []
    st.session_state.bullets = []
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.running = False
    st.session_state.last_time = time.time()
    st.session_state.sun_time = time.time()
    st.session_state.zombie_time = time.time()


# =========================
# GAME TICK
# =========================

def game_tick():

    now = time.time()

    # Zombie xuất hiện
    if now - st.session_state.zombie_time >= 5:

        tao_zombie()

        st.session_state.zombie_time = now

    # Mặt trời
    tao_mat_troi()

    # Đậu bắn
    tao_dan()

    # Đạn
    cap_nhat_dan()

    # Cherry
    xu_ly_cherry()

    # Zombie ăn cây
    zombie_an_cay()

    # Zombie di chuyển
    zombie_di_chuyen()

    st.session_state.last_time = now


# =========================
# GIAO DIỆN
# =========================

khoi_tao()

st.title("🌱 PLANTS VS ZOMBIES MINI")

st.write(
    "Trồng cây để bảo vệ ngôi nhà khỏi zombie!"
)

# Thông tin
c1, c2, c3 = st.columns(3)

with c1:
    st.metric("☀️ Mặt trời", st.session_state.sun)

with c2:
    st.metric("🏆 Điểm", st.session_state.score)

with c3:
    st.metric("🧟 Zombie", len(st.session_state.zombies))


# =========================
# CHỌN CÂY
# =========================

st.subheader("🌱 Chọn cây")

plant_choice = st.radio(
    "Chọn cây muốn trồng:",
    [
        "🌱 Đậu - 50",
        "🥜 Óc chó - 50",
        "🍒 Cherry - 100"
    ],
    horizontal=True
)

if plant_choice.startswith("🌱"):
    selected = "pea"

elif plant_choice.startswith("🥜"):
    selected = "wall"

else:
    selected = "cherry"


# =========================
# NÚT GAME
# =========================

c1, c2, c3 = st.columns(3)

with c1:

    if st.button("▶️ BẮT ĐẦU", use_container_width=True):

        st.session_state.running = True
        st.session_state.last_time = time.time()

with c2:

    if st.button("☀️ +25 MẶT TRỜI", use_container_width=True):

        st.session_state.sun += 25

with c3:

    if st.button("🔄 CHƠI LẠI", use_container_width=True):

        choi_lai()
        st.rerun()


# =========================
# GAME OVER
# =========================

if st.session_state.game_over:

    st.error("💀 GAME OVER!")

    st.write(
        f"🏆 Điểm của bạn: {st.session_state.score}"
    )

    if st.button("🔄 CHƠI LẠI NGAY"):

        choi_lai()
        st.rerun()

    st.stop()


# =========================
# CẬP NHẬT GAME
# =========================

if st.session_state.running:

    game_tick()


# =========================
# BÀN CỜ
# =========================

st.subheader("🌿 BÃI CỎ")

for row in range(5):

    cols = st.columns(9)

    for col in range(9):

        cell = (row, col)

        text = "🟩"

        # Cây
        if cell in st.session_state.plants:

            plant = st.session_state.plants[cell]

            if plant["type"] == "pea":
                text = "🌱"

            elif plant["type"] == "wall":
                text = "🥜"

            elif plant["type"] == "cherry":
                text = "🍒"

        # Đạn
        for bullet in st.session_state.bullets:

            if (
                bullet["row"] == row
                and bullet["col"] == col
            ):
                text = "🟢"

        # Zombie
        for zombie in st.session_state.zombies:

            if (
                zombie["row"] == row
                and zombie["col"] == col
            ):
                text = "🧟"

        # Nút ô đất
        if cols[col].button(
            text,
            key=f"cell_{row}_{col}",
            use_container_width=True
        ):

            if not st.session_state.running:
                st.warning("Hãy bấm ▶️ BẮT ĐẦU trước!")

            else:

                trong_cay(
                    row,
                    col,
                    selected
                )

                st.rerun()


# =========================
# HƯỚNG DẪN
# =========================

st.divider()

st.subheader("🎮 Cách chơi")

st.write("""
☀️ Mặt trời: dùng để mua cây.

🌱 Đậu: 50 mặt trời, tự bắn zombie.

🥜 Óc chó: 50 mặt trời, có nhiều máu và chặn zombie.

🍒 Cherry: 100 mặt trời, nổ khi zombie đến gần.

🧟 Zombie: xuất hiện bên phải và đi về bên trái.

💥 Nếu zombie đi đến cuối sân → GAME OVER.

🏆 Tiêu diệt zombie để tăng điểm.
""")

# Tự chạy
if st.session_state.running and not st.session_state.game_over:

    time.sleep(0.5)
    st.rerun()
```
