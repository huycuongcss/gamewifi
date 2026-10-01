
import streamlit as st
import streamlit.components.v1 as components


def main():
    st.set_page_config(
        page_title="Cuộc chiến với zombie",
        page_icon="🌱",
        layout="wide"
    )

    game = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">

<style>
html, body {
    margin: 0;
    padding: 0;
    background: #182c18;
    overflow: hidden;
}

#game {
    width: 100%;
    display: flex;
    justify-content: center;
}

canvas {
    display: block;
    width: min(100vw, 1400px);
    height: auto;
    background: #75bd4a;
    touch-action: none;
}
</style>
</head>

<body>

<div id="game">
<canvas id="canvas" width="1400" height="850"></canvas>
</div>

<script>

const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

const W = 1400;
const H = 850;

const ROWS = 5;
const COLS = 9;

const TOP = 105;

const MOWER_W = 130;
const BOARD_X = 130;

const CW = 135;
const CH = 140;

let sun = 200;
let selectedPlant = null;

let plants = [];
let zombies = [];
let bullets = [];
let suns = [];
let mowers = [];

let zombieTimer = 0;
let naturalSunTimer = 0;

let gameOver = false;

let lastTime = performance.now();


// ==================================================
// HỖ TRỢ VẼ
// ==================================================

function circle(x, y, r, color) {
    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.fillStyle = color;
    ctx.fill();
}

function rect(x, y, w, h, color, radius = 0) {

    ctx.fillStyle = color;

    if (radius > 0) {

        ctx.beginPath();

        ctx.roundRect(
            x, y, w, h, radius
        );

        ctx.fill();

    } else {

        ctx.fillRect(
            x, y, w, h
        );
    }
}

function line(x1, y1, x2, y2, color, width = 2) {

    ctx.beginPath();

    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);

    ctx.strokeStyle = color;
    ctx.lineWidth = width;

    ctx.stroke();
}


// ==================================================
// MÁY CẮT CỎ
// ==================================================

function taoMayCatCo() {

    mowers = [];

    for (let r = 0; r < ROWS; r++) {

        mowers.push({
            row: r,
            x: 35,
            active: false
        });
    }
}

taoMayCatCo();


// ==================================================
// TRỒNG CÂY
// ==================================================

function trongCay(row, col, type) {

    if (
        row < 0 ||
        row >= ROWS ||
        col < 0 ||
        col >= COLS
    ) {
        return;
    }

    if (
        plants.some(
            p =>
            p.row === row &&
            p.col === col
        )
    ) {
        return;
    }

    let cost = 0;

    if (type === "sunflower") cost = 50;
    if (type === "pea") cost = 50;
    if (type === "wallnut") cost = 50;
    if (type === "cherry") cost = 100;

    if (sun < cost) return;

    sun -= cost;

    plants.push({
        row: row,
        col: col,
        type: type,
        hp:
            type === "wallnut"
            ? 350
            : 120,
        timer: 0
    });
}


// ==================================================
// MẶT TRỜI
// ==================================================

function taoMatTroi(x, y) {

    suns.push({
        x: x,
        y: y,
        life: 1000,
        r: 30
    });
}

function taoMatTroiTuNhien() {

    let col =
        Math.floor(
            Math.random() * COLS
        );

    let row =
        Math.floor(
            Math.random() * ROWS
        );

    let x =
        BOARD_X +
        col * CW +
        CW / 2;

    let y =
        TOP +
        row * CH +
        40;

    taoMatTroi(x, y);
}


// ==================================================
// ZOMBIE
// ==================================================

function taoZombie() {

    let row =
        Math.floor(
            Math.random() * ROWS
        );

    zombies.push({

        row: row,

        x: W + 60,

        hp: 160,

        maxHP: 160,

        speed:
            0.20 +
            Math.random() * 0.12,

        attackTimer: 0,

        walk: 0
    });
}


// ==================================================
// NỀN
// ==================================================

function veNen() {

    // Bầu trời
    rect(
        0,
        0,
        W,
        TOP,
        "#263d24"
    );

    // Cỏ toàn màn hình
    rect(
        0,
        TOP,
        W,
        H - TOP,
        "#5eae3d"
    );

    // Khu máy cắt cỏ
    rect(
        0,
        TOP,
        MOWER_W,
        ROWS * CH,
        "#477e31"
    );

    // Đường viền khu máy
    line(
        MOWER_W,
        TOP,
        MOWER_W,
        TOP + ROWS * CH,
        "#294c20",
        5
    );

    // Bàn cỏ 5 × 9
    for (let row = 0; row < ROWS; row++) {

        for (let col = 0; col < COLS; col++) {

            let x =
                BOARD_X +
                col * CW;

            let y =
                TOP +
                row * CH;

            let color =
                (row + col) % 2 === 0
                ? "#73c84b"
                : "#68bc43";

            rect(
                x,
                y,
                CW,
                CH,
                color
            );

            // Các vệt cỏ
            for (let k = 0; k < 7; k++) {

                let gx =
                    x +
                    12 +
                    ((k * 29 + row * 17) % 105);

                let gy =
                    y +
                    20 +
                    ((k * 31 + col * 13) % 105);

                line(
                    gx,
                    gy,
                    gx + 3,
                    gy - 7,
                    "rgba(35,110,35,0.25)",
                    2
                );
            }

            // Viền ô
            ctx.strokeStyle =
                "rgba(35,90,25,0.25)";

            ctx.lineWidth = 2;

            ctx.strokeRect(
                x,
                y,
                CW,
                CH
            );
        }
    }

    // Hàng đất cuối
    rect(
        BOARD_X,
        TOP + ROWS * CH,
        COLS * CW,
        45,
        "#6b472b"
    );

    // đá nhỏ
    for (let i = 0; i < 18; i++) {

        let x =
            BOARD_X +
            ((i * 97) % 1180);

        let y =
            TOP +
            ROWS * CH +
            10 +
            ((i * 13) % 22);

        circle(
            x,
            y,
            3,
            "#987052"
        );
    }
}


// ==================================================
// THANH ĐIỀU KHIỂN
// ==================================================

function veThanhDieuKhien() {

    rect(
        15,
        15,
        190,
        70,
        "#172617",
        14
    );

    circle(
        55,
        50,
        24,
        "#ffd735"
    );

    // tia mặt trời
    for (let i = 0; i < 8; i++) {

        let a =
            i * Math.PI / 4;

        line(
            55 + Math.cos(a) * 30,
            50 + Math.sin(a) * 30,
            55 + Math.cos(a) * 38,
            50 + Math.sin(a) * 38,
            "#ffd735",
            5
        );
    }

    ctx.fillStyle = "#fff";
    ctx.font = "bold 27px Arial";
    ctx.textAlign = "left";

    ctx.fillText(
        sun,
        90,
        59
    );


    let buttons = [

        {
            x: 225,
            type: "sunflower",
            name: "MẶT TRỜI",
            cost: 50
        },

        {
            x: 395,
            type: "pea",
            name: "ĐẬU",
            cost: 50
        },

        {
            x: 565,
            type: "wallnut",
            name: "ÓC CHÓ",
            cost: 50
        },

        {
            x: 735,
            type: "cherry",
            name: "CHERRY",
            cost: 100
        }
    ];


    for (let b of buttons) {

        let active =
            selectedPlant === b.type;

        rect(
            b.x,
            10,
            155,
            80,
            active
            ? "#f7e47a"
            : "#d9ead0",
            12
        );

        ctx.strokeStyle =
            active
            ? "#fff000"
            : "#355c2b";

        ctx.lineWidth = 4;

        ctx.strokeRect(
            b.x,
            10,
            155,
            80
        );

        veCayNho(
            b.type,
            b.x + 42,
            50,
            0.55
        );

        ctx.fillStyle = "#1d351b";
        ctx.font = "bold 15px Arial";
        ctx.textAlign = "left";

        ctx.fillText(
            b.name,
            b.x + 72,
            43
        );

        ctx.font = "bold 18px Arial";

        ctx.fillText(
            b.cost,
            b.x + 72,
            68
        );
    }
}


// ==================================================
// VẼ MẶT TRỜI
// ==================================================

function veSun(s) {

    // tia
    for (let i = 0; i < 12; i++) {

        let a =
            i * Math.PI / 6;

        line(
            s.x + Math.cos(a) * 34,
            s.y + Math.sin(a) * 34,
            s.x + Math.cos(a) * 44,
            s.y + Math.sin(a) * 44,
            "#ffc400",
            5
        );
    }

    circle(
        s.x,
        s.y,
        s.r,
        "#ffd83d"
    );

    circle(
        s.x - 8,
        s.y - 7,
        4,
        "#9b6b00"
    );

    circle(
        s.x + 8,
        s.y - 7,
        4,
        "#9b6b00"
    );

    ctx.beginPath();

    ctx.arc(
        s.x,
        s.y + 2,
        10,
        0,
        Math.PI
    );

    ctx.strokeStyle = "#9b6b00";
    ctx.lineWidth = 3;

    ctx.stroke();
}


// ==================================================
// VẼ CÂY MẶT TRỜI
// ==================================================

function veSunflower(x, y, scale) {

    // thân
    line(
        x,
        y + 25 * scale,
        x,
        y + 72 * scale,
        "#27752c",
        9 * scale
    );

    // lá
    ctx.beginPath();

    ctx.ellipse(
        x - 22 * scale,
        y + 48 * scale,
        25 * scale,
        11 * scale,
        -0.4,
        0,
        Math.PI * 2
    );

    ctx.fillStyle = "#3eaa3d";
    ctx.fill();

    ctx.beginPath();

    ctx.ellipse(
        x + 22 * scale,
        y + 55 * scale,
        25 * scale,
        11 * scale,
        0.4,
        0,
        Math.PI * 2
    );

    ctx.fill();

    // cánh hoa
    for (let i = 0; i < 12; i++) {

        let a =
            i * Math.PI / 6;

        circle(
            x + Math.cos(a) * 30 * scale,
            y + Math.sin(a) * 30 * scale,
            14 * scale,
            "#f7c928"
        );
    }

    circle(
        x,
        y,
        24 * scale,
        "#6b451c"
    );

    circle(
        x - 8 * scale,
        y - 5 * scale,
        3 * scale,
        "#222"
    );

    circle(
        x + 8 * scale,
        y - 5 * scale,
        3 * scale,
        "#222"
    );
}


// ==================================================
// VẼ CÂY ĐẬU
// ==================================================

function vePea(x, y, scale) {

    // thân
    line(
        x,
        y + 30 * scale,
        x,
        y + 78 * scale,
        "#27752c",
        10 * scale
    );

    // lá
    ctx.beginPath();

    ctx.ellipse(
        x - 22 * scale,
        y + 50 * scale,
        26 * scale,
        13 * scale,
        -0.5,
        0,
        Math.PI * 2
    );

    ctx.fillStyle = "#3fa83b";
    ctx.fill();

    // đầu cây
    circle(
        x,
        y,
        31 * scale,
        "#4bb844"
    );

    // miệng súng
    circle(
        x + 24 * scale,
        y - 3 * scale,
        17 * scale,
        "#369635"
    );

    circle(
        x + 30 * scale,
        y - 3 * scale,
        9 * scale,
        "#245f29"
    );

    // mắt
    circle(
        x - 10 * scale,
        y - 8 * scale,
        6 * scale,
        "#fff"
    );

    circle(
        x - 8 * scale,
        y - 8 * scale,
        3 * scale,
        "#222"
    );
}


// ==================================================
// VẼ ÓC CHÓ
// ==================================================

function veWallnut(x, y, scale) {

    ctx.beginPath();

    ctx.ellipse(
        x,
        y + 20 * scale,
        43 * scale,
        55 * scale,
        0,
        0,
        Math.PI * 2
    );

    ctx.fillStyle = "#9a6234";
    ctx.fill();

    ctx.strokeStyle = "#5f351c";
    ctx.lineWidth = 5 * scale;
    ctx.stroke();

    // mặt
    circle(
        x - 14 * scale,
        y + 5 * scale,
        5 * scale,
        "#21160d"
    );

    circle(
        x + 14 * scale,
        y + 5 * scale,
        5 * scale,
        "#21160d"
    );

    ctx.beginPath();

    ctx.arc(
        x,
        y + 27 * scale,
        17 * scale,
        0,
        Math.PI
    );

    ctx.strokeStyle = "#432516";
    ctx.lineWidth = 4 * scale;

    ctx.stroke();

    // vân trên óc chó
    line(
        x - 25 * scale,
        y - 15 * scale,
        x - 10 * scale,
        y - 35 * scale,
        "#754521",
        4 * scale
    );

    line(
        x + 25 * scale,
        y - 15 * scale,
        x + 10 * scale,
        y - 35 * scale,
        "#754521",
        4 * scale
    );
}


// ==================================================
// VẼ CHERRY
// ==================================================

function veCherry(x, y, scale) {

    // thân
    line(
        x,
        y - 25 * scale,
        x + 10 * scale,
        y - 55 * scale,
        "#385d25",
        6 * scale
    );

    // lá
    ctx.beginPath();

    ctx.ellipse(
        x + 22 * scale,
        y - 52 * scale,
        18 * scale,
        9 * scale,
        -0.4,
        0,
        Math.PI * 2
    );

    ctx.fillStyle = "#3e9e36";
    ctx.fill();

    circle(
        x - 22 * scale,
        y + 15 * scale,
        27 * scale,
        "#d72e35"
    );

    circle(
        x + 22 * scale,
        y + 15 * scale,
        27 * scale,
        "#e33b3f"
    );

    circle(
        x - 30 * scale,
        y + 6 * scale,
        6 * scale,
        "#ff7777"
    );

    circle(
        x + 14 * scale,
        y + 6 * scale,
        6 * scale,
        "#ff7777"
    );

    // mắt
    circle(
        x - 29 * scale,
        y + 13 * scale,
        4 * scale,
        "#222"
    );

    circle(
        x + 15 * scale,
        y + 13 * scale,
        4 * scale,
        "#222"
    );
}


// ==================================================
// VẼ CÂY
// ==================================================

function veCayNho(type, x, y, scale) {

    if (type === "sunflower") {
        veSunflower(x, y, scale);
    }

    if (type === "pea") {
        vePea(x, y, scale);
    }

    if (type === "wallnut") {
        veWallnut(x, y, scale);
    }

    if (type === "cherry") {
        veCherry(x, y, scale);
    }
}

function veCay(p) {

    let x =
        BOARD_X +
        p.col * CW +
        CW / 2;

    let y =
        TOP +
        p.row * CH +
        62;

    veCayNho(
        p.type,
        x,
        y,
        1.0
    );

    // thanh máu
    let hpWidth = 75;

    rect(
        x - hpWidth / 2,
        y + 65,
        hpWidth,
        7,
        "#263326",
        4
    );

    rect(
        x - hpWidth / 2,
        y + 65,
        hpWidth * Math.max(
            0,
            p.hp /
            (p.type === "wallnut"
                ? 350
                : 120)
        ),
        7,
        "#38db45",
        4
    );
}


// ==================================================
// VẼ ZOMBIE
// ==================================================

function veZombie(z) {

    let x = z.x;
    let y = TOP + z.row * CH + 65;

    z.walk += 0.05;

    let legMove =
        Math.sin(z.walk) * 7;

    // bóng
    ctx.globalAlpha = 0.25;

    ctx.beginPath();

    ctx.ellipse(
        x,
        y + 65,
        38,
        10,
        0,
        0,
        Math.PI * 2
    );

    ctx.fillStyle = "#263d24";
    ctx.fill();

    ctx.globalAlpha = 1;

    // chân
    line(
        x - 15,
        y + 38,
        x - 18 + legMove,
        y + 70,
        "#27392b",
        12
    );

    line(
        x + 15,
        y + 38,
        x + 18 - legMove,
        y + 70,
        "#27392b",
        12
    );

    // thân áo
    rect(
        x - 32,
        y - 5,
        64,
        55,
        "#66746b",
        12
    );

    // cà vạt
    ctx.beginPath();

    ctx.moveTo(x, y + 5);
    ctx.lineTo(x - 8, y + 28);
    ctx.lineTo(x, y + 43);
    ctx.lineTo(x + 8, y + 28);
    ctx.closePath();

    ctx.fillStyle = "#8c2525";
    ctx.fill();

    // cổ
    rect(
        x - 13,
        y - 14,
        26,
        20,
        "#6f8970",
        7
    );

    // đầu
    circle(
        x,
        y - 42,
        36,
        "#7da76b"
    );

    // tai
    circle(
        x - 35,
        y - 42,
        10,
        "#719361"
    );

    circle(
        x + 35,
        y - 42,
        10,
        "#719361"
    );

    // tóc
    for (let i = -2; i <= 2; i++) {

        circle(
            x + i * 14,
            y - 73,
            10,
            "#38463b"
        );
    }

    // mắt
    circle(
        x - 13,
        y - 48,
        8,
        "#fff"
    );

    circle(
        x + 13,
        y - 48,
        8,
        "#fff"
    );

    circle(
        x - 11,
        y - 47,
        4,
        "#222"
    );

    circle(
        x + 15,
        y - 47,
        4,
        "#222"
    );

    // miệng
    ctx.beginPath();

    ctx.arc(
        x,
        y - 28,
        15,
        0,
        Math.PI
    );

    ctx.strokeStyle = "#384b38";
    ctx.lineWidth = 5;

    ctx.stroke();

    // thanh máu
    rect(
        x - 40,
        y - 95,
        80,
        8,
        "#222",
        4
    );

    rect(
        x - 40,
        y - 95,
        80 * Math.max(
            0,
            z.hp / z.maxHP
        ),
        8,
        "#e23a3a",
        4
    );
}


// ==================================================
// VẼ MÁY CẮT CỎ
// ==================================================

function veMayCat(m) {

    let y =
        TOP +
        m.row * CH +
        65;

    // bánh
    circle(
        m.x + 18,
        y + 30,
        15,
        "#222"
    );

    circle(
        m.x + 68,
        y + 30,
        15,
        "#222"
    );

    // thân máy
    rect(
        m.x,
        y - 15,
        80,
        45,
        "#d84a32",
        10
    );

    // tay cầm
    line(
        m.x + 65,
        y - 10,
        m.x + 92,
        y - 35,
        "#333",
        7
    );

    line(
        m.x + 92,
        y - 35,
        m.x + 105,
        y - 35,
        "#333",
        7
    );

    // đèn
    circle(
        m.x + 15,
        y - 3,
        6,
        "#ffe06b"
    );
}


// ==================================================
// ĐẠN
// ==================================================

function veDan(b) {

    circle(
        b.x,
        b.y,
        9,
        "#8be33e"
    );

    circle(
        b.x - 3,
        b.y - 3,
        3,
        "#d5ff92"
    );
}


// ==================================================
// BẮN
// ==================================================

function banDan(p) {

    let x =
        BOARD_X +
        p.col * CW +
        80;

    let y =
        TOP +
        p.row * CH +
        60;

    bullets.push({
        x: x,
        y: y,
        row: p.row,
        speed: 8,
        damage: 30
    });
}


// ==================================================
// CHERRY NỔ
// ==================================================

function cherryNo(p) {

    let px =
        BOARD_X +
        p.col * CW +
        CW / 2;

    let py =
        TOP +
        p.row * CH +
        65;

    for (let z of zombies) {

        let zy =
            TOP +
            z.row * CH +
            65;

        let dx = z.x - px;
        let dy = zy - py;

        let d =
            Math.sqrt(
                dx * dx +
                dy * dy
            );

        if (d < 180) {
            z.hp -= 300;
        }
    }

    p.hp = 0;
}


// ==================================================
// CẬP NHẬT CÂY
// ==================================================

function updatePlants() {

    for (let p of plants) {

        p.timer++;

        if (
            p.type === "sunflower" &&
            p.timer >= 480
        ) {

            let x =
                BOARD_X +
                p.col * CW +
                CW / 2;

            let y =
                TOP +
                p.row * CH +
                25;

            taoMatTroi(
                x,
                y
            );

            p.timer = 0;
        }


        if (
            p.type === "pea" &&
            p.timer >= 85
        ) {

            let hasZombie =
                zombies.some(
                    z =>
                    z.row === p.row &&
                    z.x >
                    BOARD_X +
                    p.col * CW
                );

            if (hasZombie) {
                banDan(p);
            }

            p.timer = 0;
        }


        if (
            p.type === "cherry" &&
            p.timer >= 45
        ) {

            cherryNo(p);
        }
    }
}


// ==================================================
// ĐẠN
// ==================================================

function updateBullets() {

    for (
        let i = bullets.length - 1;
        i >= 0;
        i--
    ) {

        let b = bullets[i];

        b.x += b.speed;

        let hit = false;

        for (let z of zombies) {

            let zy =
                TOP +
                z.row * CH +
                65;

            if (
                z.row === b.row &&
                Math.abs(z.x - b.x) < 35 &&
                Math.abs(zy - b.y) < 60
            ) {

                z.hp -= b.damage;

                hit = true;

                break;
            }
        }

        if (
            hit ||
            b.x > W
        ) {

            bullets.splice(i, 1);
        }
    }
}


// ==================================================
// ZOMBIE
// ==================================================

function updateZombies() {

    for (
        let i = zombies.length - 1;
        i >= 0;
        i--
    ) {

        let z = zombies[i];

        let target = null;

        for (let p of plants) {

            let px =
                BOARD_X +
                p.col * CW +
                CW / 2;

            if (
                p.row === z.row &&
                Math.abs(z.x - px) < 65
            ) {

                target = p;
                break;
            }
        }


        if (target) {

            z.attackTimer++;

            if (z.attackTimer >= 55) {

                target.hp -= 10;

                z.attackTimer = 0;
            }

        } else {

            z.x -= z.speed;
        }


        if (z.hp <= 0) {

            zombies.splice(
                i,
                1
            );

            continue;
        }


        if (z.x < 0) {

            gameOver = true;
        }
    }
}


// ==================================================
// MÁY CẮT
// ==================================================

function updateMowers() {

    for (let m of mowers) {

        if (!m.active) {

            let danger =
                zombies.some(
                    z =>
                    z.row === m.row &&
                    z.x < BOARD_X + 50
                );

            if (danger) {
                m.active = true;
            }
        }


        if (m.active) {

            m.x += 7;

            for (
                let i = zombies.length - 1;
                i >= 0;
                i--
            ) {

                let z = zombies[i];

                if (
                    z.row === m.row &&
                    Math.abs(
                        z.x - m.x
                    ) < 70
                ) {

                    zombies.splice(
                        i,
                        1
                    );
                }
            }
        }
    }
}


// ==================================================
// MẶT TRỜI
// ==================================================

function updateSuns() {

    for (
        let i = suns.length - 1;
        i >= 0;
        i--
    ) {

        suns[i].life--;

        if (
            suns[i].life <= 0
        ) {

            suns.splice(
                i,
                1
            );
        }
    }
}


// ==================================================
// XÓA CÂY
// ==================================================

function removeDeadPlants() {

    plants =
        plants.filter(
            p => p.hp > 0
        );
}


// ==================================================
// VẼ
// ==================================================

function draw() {

    ctx.clearRect(
        0,
        0,
        W,
        H
    );

    veNen();

    veThanhDieuKhien();

    for (let m of mowers) {
        veMayCat(m);
    }

    for (let p of plants) {
        veCay(p);
    }

    for (let b of bullets) {
        veDan(b);
    }

    for (let z of zombies) {
        veZombie(z);
    }

    for (let s of suns) {
        veSun(s);
    }


    if (gameOver) {

        rect(
            0,
            0,
            W,
            H,
            "rgba(0,0,0,0.72)"
        );

        ctx.fillStyle = "#fff";
        ctx.textAlign = "center";

        ctx.font =
            "bold 70px Arial";

        ctx.fillText(
            "THUA RỒI",
            W / 2,
            H / 2 - 20
        );

        ctx.font =
            "bold 28px Arial";

        ctx.fillText(
            "Chạm màn hình để chơi lại",
            W / 2,
            H / 2 + 40
        );
    }
}


// ==================================================
// CHẠM / CLICK
// ==================================================

canvas.addEventListener(
    "pointerdown",
    function(e) {

        e.preventDefault();

        let rectCanvas =
            canvas.getBoundingClientRect();

        let x =
            (e.clientX -
             rectCanvas.left)
            * W /
            rectCanvas.width;

        let y =
            (e.clientY -
             rectCanvas.top)
            * H /
            rectCanvas.height;


        if (gameOver) {

            location.reload();

            return;
        }


        // THANH CHỌN CÂY
        if (y < TOP) {

            if (
                x >= 225 &&
                x < 380
            ) {

                selectedPlant =
                    "sunflower";

                return;
            }

            if (
                x >= 395 &&
                x < 550
            ) {

                selectedPlant =
                    "pea";

                return;
            }

            if (
                x >= 565 &&
                x < 720
            ) {

                selectedPlant =
                    "wallnut";

                return;
            }

            if (
                x >= 735 &&
                x < 890
            ) {

                selectedPlant =
                    "cherry";

                return;
            }
        }


        // NHẶT MẶT TRỜI
        for (
            let i = suns.length - 1;
            i >= 0;
            i--
        ) {

            let s = suns[i];

            let dx =
                x - s.x;

            let dy =
                y - s.y;

            if (
                Math.sqrt(
                    dx * dx +
                    dy * dy
                ) < 42
            ) {

                sun += 25;

                suns.splice(
                    i,
                    1
                );

                return;
            }
        }


        // KHU MÁY CẮT
        if (x < BOARD_X) {
            return;
        }


        // BÀN CỎ
        let col =
            Math.floor(
                (x - BOARD_X) /
                CW
            );

        let row =
            Math.floor(
                (y - TOP) /
                CH
            );


        if (
            row < 0 ||
            row >= ROWS ||
            col < 0 ||
            col >= COLS
        ) {

            return;
        }


        if (selectedPlant) {

            trongCay(
                row,
                col,
                selectedPlant
            );

            selectedPlant = null;
        }

    },
    {
        passive: false
    }
);


// ==================================================
// GAME LOOP
// ==================================================

function loop(time) {

    let delta =
        time - lastTime;

    lastTime = time;


    if (!gameOver) {

        zombieTimer += delta;

        naturalSunTimer += delta;


        if (
            zombieTimer >= 3500
        ) {

            taoZombie();

            zombieTimer = 0;
        }


        if (
            naturalSunTimer >= 7000
        ) {

            taoMatTroiTuNhien();

            naturalSunTimer = 0;
        }


        updatePlants();
        updateBullets();
        updateZombies();
        updateMowers();
        updateSuns();
        removeDeadPlants();
    }


    draw();

    requestAnimationFrame(
        loop
    );
}


requestAnimationFrame(
    loop
);

</script>

</body>
</html>
"""

    components.html(
        game,
        height=875,
        scrolling=False
    )


if __name__ == "__main__":
    main()

