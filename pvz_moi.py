
import streamlit as st
import streamlit.components.v1 as components


def main():

    st.set_page_config(
        page_title="PVZ",
        page_icon="👤",
        layout="wide"
    )

    html = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">

<style>

body {
    margin: 0;
    background: #b9e89b;
    font-family: Arial;
    text-align: center;
}

#info {
    font-size: 22px;
    font-weight: bold;
    margin: 8px;
}

canvas {
    width: 100%;
    max-width: 1000px;
    border: 4px solid #39752a;
    border-radius: 12px;
    background: #70bd45;
    touch-action: none;
}

.controls {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 7px;
    margin: 8px;
}

button {
    padding: 10px 14px;
    border-radius: 10px;
    border: 2px solid #555;
    background: white;
    font-size: 16px;
    font-weight: bold;
}

#selected {
    font-size: 18px;
    font-weight: bold;
}

</style>
</head>

<body>

<div id="info">
☀️ Sun: <span id="sun">200</span>
&nbsp;&nbsp;
🏆 Điểm: <span id="score">0</span>
</div>

<canvas id="game" width="1000" height="600"></canvas>

<div class="controls">

<button onclick="chonCay('sunflower')">
🌻 Mặt Trời - 50
</button>

<button onclick="chonCay('pea')">
🌱 Đậu - 50
</button>

<button onclick="chonCay('nut')">
🥜 Óc chó - 50
</button>

<button onclick="chonCay('cherry')">
🍒 Cherry - 100
</button>

<button onclick="choiLai()">
🔄 Chơi lại
</button>

</div>

<div id="selected">
Chưa chọn cây
</div>


<script>

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

const W = 1000;
const H = 600;

const ROWS = 5;
const COLS = 9;

const CW = 100;
const CH = 120;


let sun = 200;
let score = 0;

let selected = null;

let plants = [];
let zombies = [];
let peas = [];
let suns = [];
let explosions = [];

let mowers = [];

let gameOver = false;

let lastZombie = 0;
let lastSun = 0;
let lastShot = 0;


// ========================================
// MÁY CẮT CỎ
// ========================================

function taoMayCatCo() {

    mowers = [];

    for (let r = 0; r < ROWS; r++) {

        mowers.push({
            row: r,
            x: 15,
            active: false,
            used: false
        });

    }
}


// ========================================
// CHỌN CÂY
// ========================================

function chonCay(type) {

    selected = type;

    if (type === "sunflower") {

        document.getElementById("selected").innerText =
        "🌻 Đã chọn Cây Mặt Trời — chạm ô cỏ để trồng";

    }

    if (type === "pea") {

        document.getElementById("selected").innerText =
        "🌱 Đã chọn Đậu — chạm ô cỏ để trồng";

    }

    if (type === "nut") {

        document.getElementById("selected").innerText =
        "🥜 Đã chọn Óc chó — chạm ô cỏ để trồng";

    }

    if (type === "cherry") {

        document.getElementById("selected").innerText =
        "🍒 Đã chọn Cherry — chạm ô cỏ để trồng";

    }
}


// ========================================
// BẤM VÀO GAME
// ========================================

canvas.addEventListener("pointerdown", function(e) {

    e.preventDefault();

    if (gameOver) return;

    const rect = canvas.getBoundingClientRect();

    const x =
        (e.clientX - rect.left)
        * W / rect.width;

    const y =
        (e.clientY - rect.top)
        * H / rect.height;


    // ====================================
    // NHẶT MẶT TRỜI
    // ====================================

    for (let i = suns.length - 1; i >= 0; i--) {

        let s = suns[i];

        let dx = x - s.x;
        let dy = y - s.y;

        if (
            Math.sqrt(dx * dx + dy * dy) < 55
        ) {

            sun += 25;

            suns.splice(i, 1);

            capNhat();

            return;
        }
    }


    // ====================================
    // CHƯA CHỌN CÂY
    // ====================================

    if (!selected) return;


    // ====================================
    // TÍNH Ô
    // ====================================

    let col = Math.floor(x / CW);

    let row = Math.floor(y / CH);


    if (
        row < 0 ||
        row >= ROWS ||
        col < 0 ||
        col >= COLS
    ) {

        return;
    }


    // ====================================
    // KIỂM TRA ĐÃ CÓ CÂY
    // ====================================

    let daCoCay = plants.some(p =>
        p.row === row &&
        p.col === col
    );


    if (daCoCay) {

        return;
    }


    // ====================================
    // GIÁ CÂY
    // ====================================

    let gia = 0;

    if (selected === "sunflower") gia = 50;
    if (selected === "pea") gia = 50;
    if (selected === "nut") gia = 50;
    if (selected === "cherry") gia = 100;


    // ====================================
    // KHÔNG ĐỦ SUN
    // ====================================

    if (sun < gia) {

        document.getElementById("selected").innerText =
        "❌ Không đủ Sun!";

        return;
    }


    // ====================================
    // TRỪ SUN
    // ====================================

    sun -= gia;


    // ====================================
    // TRỒNG CÂY
    // ====================================

    plants.push({

        type: selected,

        row: row,

        col: col,

        hp:
            selected === "nut"
            ? 300
            : 100,

        timer: 0

    });


    capNhat();

});


// ========================================
// TẠO MẶT TRỜI
// ========================================

function taoMatTroi(x, y) {

    suns.push({

        x: x,

        y: y,

        life: 900

    });

}


// ========================================
// VẼ NỀN
// ========================================

function veNen() {

    ctx.fillStyle = "#72c44b";

    ctx.fillRect(
        0,
        0,
        W,
        H
    );


    for (let r = 0; r < ROWS; r++) {

        for (let c = 0; c < COLS; c++) {

            ctx.fillStyle =
                (r + c) % 2 === 0
                ? "#78ca50"
                : "#6fbd45";


            ctx.fillRect(
                c * CW,
                r * CH,
                CW,
                CH
            );


            ctx.strokeStyle =
                "rgba(40,90,30,0.25)";

            ctx.strokeRect(
                c * CW,
                r * CH,
                CW,
                CH
            );

        }

    }

}


// ========================================
// VẼ CÂY MẶT TRỜI
// ========================================

function veSunflower(p) {

    let x =
        p.col * CW + 50;

    let y =
        p.row * CH + 65;


    // thân

    ctx.strokeStyle = "#28752b";

    ctx.lineWidth = 10;

    ctx.beginPath();

    ctx.moveTo(
        x,
        y + 45
    );

    ctx.lineTo(
        x,
        y - 5
    );

    ctx.stroke();


    // lá trái

    ctx.fillStyle = "#3d9f3d";

    ctx.beginPath();

    ctx.ellipse(
        x - 20,
        y + 20,
        28,
        13,
        -0.4,
        0,
        Math.PI * 2
    );

    ctx.fill();


    // lá phải

    ctx.beginPath();

    ctx.ellipse(
        x + 20,
        y + 25,
        28,
        13,
        0.4,
        0,
        Math.PI * 2
    );

    ctx.fill();


    // cánh hoa

    for (let i = 0; i < 12; i++) {

        let a =
            i * Math.PI / 6;

        let px =
            x + Math.cos(a) * 27;

        let py =
            y - 15 +
            Math.sin(a) * 27;


        ctx.fillStyle = "#ffd52f";

        ctx.beginPath();

        ctx.arc(
            px,
            py,
            13,
            0,
            Math.PI * 2
        );

        ctx.fill();

    }


    // mặt

    ctx.fillStyle = "#8a571d";

    ctx.beginPath();

    ctx.arc(
        x,
        y - 15,
        25,
        0,
        Math.PI * 2
    );

    ctx.fill();


    // mắt

    ctx.fillStyle = "white";

    ctx.beginPath();

    ctx.arc(
        x - 9,
        y - 20,
        6,
        0,
        Math.PI * 2
    );

    ctx.fill();


    ctx.beginPath();

    ctx.arc(
        x + 9,
        y - 20,
        6,
        0,
        Math.PI * 2
    );

    ctx.fill();


    ctx.fillStyle = "black";

    ctx.beginPath();

    ctx.arc(
        x - 9,
        y - 20,
        3,
        0,
        Math.PI * 2
    );

    ctx.fill();


    ctx.beginPath();

    ctx.arc(
        x + 9,
        y - 20,
        3,
        0,
        Math.PI * 2
    );

    ctx.fill();


    // miệng

    ctx.strokeStyle = "#3e230c";

    ctx.lineWidth = 3;

    ctx.beginPath();

    ctx.arc(
        x,
        y - 12,
        9,
        0,
        Math.PI
    );

    ctx.stroke();

}


// ========================================
// VẼ ĐẬU
// ========================================

function veDau(p) {

    let x =
        p.col * CW + 50;

    let y =
        p.row * CH + 65;


    ctx.strokeStyle = "#28752b";

    ctx.lineWidth = 10;

    ctx.beginPath();

    ctx.moveTo(x, y + 45);

    ctx.lineTo(x, y);

    ctx.stroke();


    ctx.fillStyle = "#3c9f3c";

    ctx.beginPath();

    ctx.ellipse(
        x - 20,
        y + 20,
        27,
        12,
        -0.4,
        0,
        Math.PI * 2
    );

    ctx.fill();


    ctx.fillStyle = "#4caf50";

    ctx.beginPath();

    ctx.arc(
        x,
        y - 20,
        32,
        0,
        Math.PI * 2
    );

    ctx.fill();


    // miệng súng

    ctx.fillStyle = "#337f36";

    ctx.beginPath();

    ctx.ellipse(
        x + 28,
        y - 20,
        25,
        16,
        0,
        0,
        Math.PI * 2
    );

    ctx.fill();


    // mắt

    ctx.fillStyle = "white";

    ctx.beginPath();

    ctx.arc(
        x - 10,
        y - 25,
        7,
        0,
        Math.PI * 2
    );

    ctx.fill();


    ctx.beginPath();

    ctx.arc(
        x + 7,
        y - 25,
        7,
        0,
        Math.PI * 2
    );

    ctx.fill();


    ctx.fillStyle = "black";

    ctx.beginPath();

    ctx.arc(
        x - 9,
        y - 25,
        3,
        0,
        Math.PI * 2
    );

    ctx.fill();


    ctx.beginPath();

    ctx.arc(
        x + 8,
        y - 25,
        3,
        0,
        Math.PI * 2
    );

    ctx.fill();

}


// ========================================
// VẼ ÓC CHÓ
// ========================================

function veOcCho(p) {

    let x =
        p.col * CW + 50;

    let y =
        p.row * CH + 60;


    ctx.fillStyle = "#a86a2b";

    ctx.beginPath();

    ctx.arc(
        x,
        y,
        38,
        0,
        Math.PI * 2
    );

    ctx.fill();


    ctx.strokeStyle = "#704117";

    ctx.lineWidth = 4;

    ctx.stroke();


    // vết nứt

    ctx.strokeStyle = "#60350f";

    ctx.beginPath();

    ctx.moveTo(
        x - 5,
        y - 30
    );

    ctx.lineTo(
        x - 12,
        y - 5
    );

    ctx.lineTo(
        x + 5,
        y + 5
    );

    ctx.lineTo(
        x,
        y + 25
    );

    ctx.stroke();


    // mắt

    ctx.fillStyle = "white";

    ctx.beginPath();

    ctx.arc(
        x - 12,
        y - 8,
        7,
        0,
        Math.PI * 2
    );

    ctx.fill();


    ctx.beginPath();

    ctx.arc(
        x + 12,
        y - 8,
        7,
        0,
        Math.PI * 2
    );

    ctx.fill();


    ctx.fillStyle = "black";

    ctx.beginPath();

    ctx.arc(
        x - 12,
        y - 8,
        3,
        0,
        Math.PI * 2
    );

    ctx.fill();


    ctx.beginPath();

    ctx.arc(
        x + 12,
        y - 8,
        3,
        0,
        Math.PI * 2
    );

    ctx.fill();

}


// ========================================
// VẼ CHERRY
// ========================================

function veCherry(p) {

    let x =
        p.col * CW + 50;

    let y =
        p.row * CH + 65;


    ctx.strokeStyle = "#176e24";

    ctx.lineWidth = 5;

    ctx.beginPath();

    ctx.moveTo(
        x,
        y - 20
    );

    ctx.lineTo(
        x - 10,
        y - 50
    );

    ctx.stroke();


    ctx.beginPath();

    ctx.moveTo(
        x,
        y - 20
    );

    ctx.lineTo(
        x + 10,
        y - 50
    );

    ctx.stroke();


    ctx.fillStyle = "#d92828";


    ctx.beginPath();

    ctx.arc(
        x - 20,
        y,
        25,
        0,
        Math.PI * 2
    );

    ctx.fill();


    ctx.beginPath();

    ctx.arc(
        x + 20,
        y,
        25,
        0,
        Math.PI * 2
    );

    ctx.fill();

}


// ========================================
// VẼ ZOMBIE
// ========================================

function veZombie(z) {

    let x = z.x;

    let y =
        z.row * CH + 65;


    // chân

    ctx.fillStyle = "#293e78";

    ctx.fillRect(
        x - 18,
        y + 30,
        12,
        35
    );

    ctx.fillRect(
        x + 8,
        y + 30,
        12,
        35
    );


    // thân

    ctx.fillStyle = "#587c3d";

    ctx.fillRect(
        x - 25,
        y - 5,
        50,
        50
    );


    // tay

    ctx.strokeStyle = "#587c3d";

    ctx.lineWidth = 12;

    ctx.beginPath();

    ctx.moveTo(
        x - 20,
        y
    );

    ctx.lineTo(
        x - 48,
        y + 20
    );

    ctx.stroke();


    ctx.beginPath();

    ctx.moveTo(
        x + 20,
        y
    );

    ctx.lineTo(
        x + 48,
        y + 20
    );

    ctx.stroke();


    // đầu

    ctx.fillStyle = "#789650";

    ctx.beginPath();

    ctx.arc(
        x,
        y - 30,
        31,
        0,
        Math.PI * 2
    );

    ctx.fill();


    // tóc

    ctx.fillStyle = "#38271d";

    ctx.beginPath();

    ctx.arc(
        x,
        y - 48,
        27,
        Math.PI,
        Math.PI * 2
    );

    ctx.fill();


    // mắt

    ctx.fillStyle = "white";

    ctx.beginPath();

    ctx.arc(
        x - 10,
        y - 32,
        7,
        0,
        Math.PI * 2
    );

    ctx.fill();


    ctx.beginPath();

    ctx.arc(
        x + 10,
        y - 32,
        7,
        0,
        Math.PI * 2
    );

    ctx.fill();


    ctx.fillStyle = "black";

    ctx.beginPath();

    ctx.arc(
        x - 10,
        y - 32,
        3,
        0,
        Math.PI * 2
    );

    ctx.fill();


    ctx.beginPath();

    ctx.arc(
        x + 10,
        y - 32,
        3,
        0,
        Math.PI * 2
    );

    ctx.fill();


    // miệng

    ctx.fillStyle = "#321";

    ctx.fillRect(
        x - 17,
        y - 12,
        34,
        10
    );


    // máu

    ctx.fillStyle = "#222";

    ctx.fillRect(
        x - 30,
        y - 72,
        60,
        7
    );

    ctx.fillStyle = "#e33";

    ctx.fillRect(
        x - 30,
        y - 72,
        60 * z.hp / 100,
        7
    );

}


// ========================================
// VẼ MÁY CẮT CỎ
// ========================================

function veMayCat(m) {

    let y =
        m.row * CH + 70;


    ctx.fillStyle =
        m.used ? "#777" : "#d63232";


    ctx.fillRect(
        m.x,
        y,
        50,
        30
    );


    ctx.strokeStyle = "#333";

    ctx.lineWidth = 6;

    ctx.beginPath();

    ctx.moveTo(
        m.x + 15,
        y
    );

    ctx.lineTo(
        m.x + 15,
        y - 35
    );

    ctx.lineTo(
        m.x + 45,
        y - 35
    );

    ctx.stroke();


    ctx.fillStyle = "#222";

    ctx.beginPath();

    ctx.arc(
        m.x + 10,
        y + 30,
        10,
        0,
        Math.PI * 2
    );

    ctx.fill();


    ctx.beginPath();

    ctx.arc(
        m.x + 40,
        y + 30,
        10,
        0,
        Math.PI * 2
    );

    ctx.fill();

}


// ========================================
// VẼ MẶT TRỜI
// ========================================

function veMatTroi(s) {

    ctx.save();

    ctx.translate(
        s.x,
        s.y
    );


    // tia sáng

    ctx.strokeStyle = "#ffbd00";

    ctx.lineWidth = 5;

    for (let i = 0; i < 12; i++) {

        let a =
            i * Math.PI / 6;


        ctx.beginPath();

        ctx.moveTo(
            Math.cos(a) * 32,
            Math.sin(a) * 32
        );

        ctx.lineTo(
            Math.cos(a) * 48,
            Math.sin(a) * 48
        );

        ctx.stroke();

    }


    // mặt trời

    ctx.fillStyle = "#ffd83d";

    ctx.beginPath();

    ctx.arc(
        0,
        0,
        32,
        0,
        Math.PI * 2
    );

    ctx.fill();


    // số 25

    ctx.fillStyle = "#8a6100";

    ctx.font = "bold 18px Arial";

    ctx.textAlign = "center";

    ctx.textBaseline = "middle";

    ctx.fillText(
        "25",
        0,
        0
    );


    ctx.restore();

}


// ========================================
// VẼ ĐẠN
// ========================================

function veDan(b) {

    ctx.fillStyle = "#43bd39";

    ctx.beginPath();

    ctx.arc(
        b.x,
        b.y,
        9,
        0,
        Math.PI * 2
    );

    ctx.fill();

}


// ========================================
// VẼ TẤT CẢ
// ========================================

function veGame() {

    veNen();


    // máy cắt cỏ

    for (let m of mowers) {

        if (!m.used) {

            veMayCat(m);

        }

    }


    // cây

    for (let p of plants) {

        if (p.type === "sunflower") {

            veSunflower(p);

        }

        if (p.type === "pea") {

            veDau(p);

        }

        if (p.type === "nut") {

            veOcCho(p);

        }

        if (p.type === "cherry") {

            veCherry(p);

        }

    }


    // đạn

    for (let b of peas) {

        veDan(b);

    }


    // zombie

    for (let z of zombies) {

        veZombie(z);

    }


    // mặt trời

    for (let s of suns) {

        veMatTroi(s);

    }


    // game over

    if (gameOver) {

        ctx.fillStyle =
            "rgba(0,0,0,0.65)";

        ctx.fillRect(
            0,
            0,
            W,
            H
        );


        ctx.fillStyle = "white";

        ctx.textAlign = "center";

        ctx.font = "bold 55px Arial";

        ctx.fillText(
            "GAME OVER",
            W / 2,
            H / 2
        );

        ctx.font = "bold 25px Arial";

        ctx.fillText(
            "Điểm: " + score,
            W / 2,
            H / 2 + 45
        );

    }

}


// ========================================
// CÂY MẶT TRỜI TẠO SUN
// ========================================

function capNhatCayMatTroi() {

    for (let p of plants) {

        if (p.type !== "sunflower") continue;


        p.timer++;


        // khoảng 8 giây tạo 1 mặt trời

        if (p.timer >= 480) {

            let x =
                p.col * CW + 50;

            let y =
                p.row * CH + 20;


            taoMatTroi(
                x,
                y
            );


            p.timer = 0;

        }

    }

}


// ========================================
// ĐẬU BẮN
// ========================================

function banDan() {

    for (let p of plants) {

        if (p.type !== "pea") continue;


        let px =
            p.col * CW + 75;

        let py =
            p.row * CH + 45;


        let coZombie =
            zombies.some(z =>
                z.row === p.row &&
                z.x > px
            );


        if (coZombie) {

            peas.push({

                x: px,

                y: py,

                row: p.row

            });

        }

    }

}


// ========================================
// CẬP NHẬT ĐẠN
// ========================================

function capNhatDan() {

    for (
        let i = peas.length - 1;
        i >= 0;
        i--
    ) {

        let b = peas[i];

        b.x += 7;


        let trung = false;


        for (
            let j = zombies.length - 1;
            j >= 0;
            j--
        ) {

            let z = zombies[j];


            if (
                z.row === b.row &&
                Math.abs(z.x - b.x) < 25
            ) {

                z.hp -= 25;

                peas.splice(i, 1);

                trung = true;


                if (z.hp <= 0) {

                    zombies.splice(j, 1);

                    score += 10;

                }

                break;

            }

        }


        if (
            !trung &&
            b.x > W
        ) {

            peas.splice(i, 1);

        }

    }

}


// ========================================
// ZOMBIE
// ========================================

function taoZombie() {

    let row =
        Math.floor(
            Math.random() * ROWS
        );


    zombies.push({

        x: W + 40,

        row: row,

        hp: 100,

        speed:
            0.25 +
            Math.random() * 0.15

    });

}


// ========================================
// CẬP NHẬT ZOMBIE
// ========================================

function capNhatZombie() {

    for (let z of zombies) {

        let dangAn = false;


        for (let p of plants) {

            if (
                p.row === z.row &&
                Math.abs(
                    z.x -
                    (p.col * CW + 50)
                ) < 45
            ) {

                dangAn = true;

                p.hp -= 0.3;

                break;

            }

        }


        if (!dangAn) {

            z.x -= z.speed;

        }

    }


    plants =
        plants.filter(p =>
            p.hp > 0
        );

}


// ========================================
// CHERRY NỔ
// ========================================

function capNhatCherry() {

    for (
        let i = plants.length - 1;
        i >= 0;
        i--
    ) {

        let p = plants[i];

        if (p.type !== "cherry") continue;


        let px =
            p.col * CW + 50;

        let py =
            p.row * CH + 60;


        let no = zombies.some(z => {

            let zx = z.x;

            let zy =
                z.row * CH + 60;


            let dx = zx - px;

            let dy = zy - py;


            return Math.sqrt(
                dx * dx +
                dy * dy
            ) < 110;

        });


        if (no) {

            for (
                let j = zombies.length - 1;
                j >= 0;
                j--
            ) {

                let z = zombies[j];

                let zx = z.x;

                let zy =
                    z.row * CH + 60;


                let dx = zx - px;

                let dy = zy - py;


                if (
                    Math.sqrt(
                        dx * dx +
                        dy * dy
                    ) < 180
                ) {

                    zombies.splice(j, 1);

                    score += 20;

                }

            }


            plants.splice(i, 1);

        }

    }

}


// ========================================
// MÁY CẮT CỎ
// ========================================

function capNhatMayCat() {

    for (let m of mowers) {

        if (m.used) continue;


        let zombieGan =
            zombies.some(z =>
                z.row === m.row &&
                z.x < 80
            );


        if (zombieGan) {

            m.active = true;

        }


        if (m.active) {

            m.x += 9;


            for (
                let i = zombies.length - 1;
                i >= 0;
                i--
            ) {

                let z = zombies[i];


                if (
                    z.row === m.row &&
                    z.x < m.x + 50
                ) {

                    zombies.splice(i, 1);

                    score += 10;

                }

            }


            if (m.x > W + 100) {

                m.used = true;

                m.active = false;

            }

        }

    }

}


// ========================================
// GAME OVER
// ========================================

function kiemTraGameOver() {

    for (let z of zombies) {

        if (z.x < 0) {

            gameOver = true;

        }

    }

}


// ========================================
// CẬP NHẬT
// ========================================

function update() {

    if (gameOver) return;


    let now =
        Date.now();


    // zombie

    if (
        now - lastZombie > 4500
    ) {

        taoZombie();

        lastZombie = now;

    }


    // mặt trời tự nhiên

    if (
        now - lastSun > 10000
    ) {

        taoMatTroi(
            100 + Math.random() * 800,
            70 + Math.random() * 400
        );

        lastSun = now;

    }


    // đậu bắn

    if (
        now - lastShot > 1100
    ) {

        banDan();

        lastShot = now;

    }


    capNhatCayMatTroi();

    capNhatDan();

    capNhatZombie();

    capNhatCherry();

    capNhatMayCat();

    kiemTraGameOver();


    // mặt trời hết thời gian

    for (
        let i = suns.length - 1;
        i >= 0;
        i--
    ) {

        suns[i].life--;


        if (
            suns[i].life <= 0
        ) {

            suns.splice(i, 1);

        }

    }


    capNhat();

}


// ========================================
// HIỂN THỊ
// ========================================

function capNhat() {

    document.getElementById("sun").innerText =
        sun;

    document.getElementById("score").innerText =
        score;

}


// ========================================
// CHƠI LẠI
// ========================================

function choiLai() {

    sun = 200;

    score = 0;

    selected = null;

    plants = [];

    zombies = [];

    peas = [];

    suns = [];

    explosions = [];

    gameOver = false;

    lastZombie = Date.now();

    lastSun = Date.now();

    lastShot = Date.now();

    taoMayCatCo();


    document.getElementById("selected").innerText =
        "Chưa chọn cây";

    capNhat();

}


// ========================================
// GAME LOOP
// ========================================

function loop() {

    update();

    veGame();

    requestAnimationFrame(loop);

}


choiLai();

loop();

</script>

</body>
</html>
"""

    components.html(
        html,
        height=760,
        scrolling=False
    )


if __name__ == "__main__":
    main()
