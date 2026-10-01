
import streamlit as st
import streamlit.components.v1 as components


def main():
    st.set_page_config(
        page_title="Vườn chiến đấu",
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
    background: #111;
    overflow: hidden;
    touch-action: none;
}

canvas {
    display: block;
    margin: auto;
    background: #79bd4b;
    touch-action: none;
}
</style>
</head>

<body>

<canvas id="game" width="1400" height="900"></canvas>

<script>

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

const W = 1400;
const H = 900;

const ROWS = 5;
const COLS = 9;

const TOP = 115;
const MOWER_W = 130;
const BOARD_X = 130;

const CW = 135;
const CH = 145;

let sun = 200;
let selected = "sunflower";

let gameOver = false;
let frame = 0;

let plants = [];
let zombies = [];
let bullets = [];
let suns = [];
let mowers = [];


// =============================
// CÁC LOẠI CÂY
// =============================

const plantInfo = {

    sunflower: {
        name: "Hướng dương",
        cost: 50
    },

    pea: {
        name: "Đậu",
        cost: 50
    },

    wallnut: {
        name: "Wall-nut",
        cost: 50
    },

    cherry: {
        name: "Cherry",
        cost: 100
    },

    chomper: {
        name: "Cây ăn thịt",
        cost: 125
    }
};


// =============================
// MÁY CẮT CỎ
// =============================

for (let r = 0; r < ROWS; r++) {

    mowers.push({
        row: r,
        x: 35,
        y: TOP + r * CH + CH / 2,
        active: false
    });

}


// =============================
// HÀM VẼ
// =============================

function rect(x, y, w, h, color) {
    ctx.fillStyle = color;
    ctx.fillRect(x, y, w, h);
}


function circle(x, y, r, color) {
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.fill();
}


function line(x1, y1, x2, y2, color, width = 2) {
    ctx.strokeStyle = color;
    ctx.lineWidth = width;
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.stroke();
}


function text(t, x, y, size, color = "#000", align = "center") {
    ctx.fillStyle = color;
    ctx.font = "bold " + size + "px Arial";
    ctx.textAlign = align;
    ctx.fillText(t, x, y);
}


// =============================
// THANH TRÊN
// =============================

function drawTop() {

    rect(0, 0, W, TOP, "#d8d8d8");

    rect(15, 15, 155, 82, "#fff1a8");

    circle(55, 55, 27, "#ffd52e");

    for (let i = 0; i < 8; i++) {

        let a = i * Math.PI / 4;

        line(
            55 + Math.cos(a) * 33,
            55 + Math.sin(a) * 33,
            55 + Math.cos(a) * 43,
            55 + Math.sin(a) * 43,
            "#e7a900",
            3
        );
    }

    text(String(sun), 110, 65, 27, "#222", "left");


    let cards = [
        ["sunflower", 190],
        ["pea", 330],
        ["wallnut", 470],
        ["cherry", 610],
        ["chomper", 750]
    ];


    for (let item of cards) {

        let type = item[0];
        let x = item[1];

        let info = plantInfo[type];

        let active = selected === type;

        rect(
            x,
            10,
            125,
            90,
            active ? "#c7a5e8" : "#eeeeee"
        );

        ctx.strokeStyle =
            active ? "#6d239e" : "#777";

        ctx.lineWidth =
            active ? 4 : 2;

        ctx.strokeRect(
            x,
            10,
            125,
            90
        );

        drawPlantSmall(
            type,
            x + 32,
            55
        );

        text(
            info.name,
            x + 70,
            39,
            13,
            "#111"
        );

        text(
            info.cost,
            x + 70,
            75,
            17,
            info.cost <= sun
                ? "#075f16"
                : "#a00000"
        );
    }


    text(
        "Chọn cây rồi chạm vào ô cỏ để trồng",
        920,
        45,
        18,
        "#222",
        "left"
    );

    text(
        "Zombie thường - Xô - Big",
        920,
        75,
        17,
        "#333",
        "left"
    );
}


// =============================
// CÂY NHỎ TRÊN MENU
// =============================

function drawPlantSmall(type, x, y) {

    if (type === "sunflower") {

        circle(x, y, 15, "#9b5b22");

        for (let i = 0; i < 8; i++) {

            let a = i * Math.PI / 4;

            circle(
                x + Math.cos(a) * 17,
                y + Math.sin(a) * 17,
                8,
                "#ffd72e"
            );
        }
    }


    else if (type === "pea") {

        line(
            x,
            y + 22,
            x,
            y + 42,
            "#248a31",
            5
        );

        circle(x, y, 19, "#3caf35");

        circle(x - 7, y - 5, 3, "#111");
        circle(x + 7, y - 5, 3, "#111");

        circle(x + 19, y + 2, 7, "#167025");
    }


    else if (type === "wallnut") {

        ctx.fillStyle = "#a86627";

        ctx.beginPath();

        ctx.ellipse(
            x,
            y,
            22,
            29,
            0,
            0,
            Math.PI * 2
        );

        ctx.fill();

        circle(x - 7, y - 5, 3, "#111");
        circle(x + 7, y - 5, 3, "#111");
    }


    else if (type === "cherry") {

        circle(x - 10, y + 3, 13, "#d92828");
        circle(x + 10, y + 3, 13, "#d92828");

        line(
            x,
            y - 7,
            x + 8,
            y - 25,
            "#276c25",
            4
        );
    }


    // CÂY ĂN THỊT TÍM
    else if (type === "chomper") {

        line(
            x,
            y + 18,
            x,
            y + 42,
            "#57227a",
            5
        );

        circle(
            x - 14,
            y + 35,
            13,
            "#7334a3"
        );

        circle(
            x + 14,
            y + 35,
            13,
            "#7334a3"
        );

        circle(
            x,
            y,
            22,
            "#7b3fb0"
        );

        ctx.fillStyle = "#c78bea";

        ctx.beginPath();

        ctx.moveTo(
            x - 17,
            y + 4
        );

        ctx.quadraticCurveTo(
            x,
            y + 27,
            x + 17,
            y + 4
        );

        ctx.fill();

        circle(
            x - 7,
            y - 6,
            3,
            "#111"
        );

        circle(
            x + 7,
            y - 6,
            3,
            "#111"
        );
    }
}


// =============================
// VẼ CÂY
// =============================

function drawPlant(p) {

    let x =
        BOARD_X +
        p.col * CW +
        CW / 2;

    let y =
        TOP +
        p.row * CH +
        CH / 2;


    if (p.type === "sunflower") {

        line(
            x,
            y + 25,
            x,
            y + 58,
            "#257c29",
            7
        );

        circle(
            x - 15,
            y + 40,
            13,
            "#3c9e36"
        );

        circle(
            x + 15,
            y + 40,
            13,
            "#3c9e36"
        );

        for (let i = 0; i < 10; i++) {

            let a =
                i * Math.PI * 2 / 10;

            circle(
                x + Math.cos(a) * 31,
                y + Math.sin(a) * 31,
                14,
                "#ffd735"
            );
        }

        circle(
            x,
            y,
            25,
            "#8b5224"
        );

        circle(
            x - 9,
            y - 5,
            4,
            "#111"
        );

        circle(
            x + 9,
            y - 5,
            4,
            "#111"
        );
    }


    else if (p.type === "pea") {

        line(
            x,
            y + 28,
            x,
            y + 60,
            "#277c2d",
            8
        );

        circle(
            x - 17,
            y + 43,
            16,
            "#319d36"
        );

        circle(
            x + 17,
            y + 43,
            16,
            "#319d36"
        );

        circle(
            x,
            y,
            31,
            "#42ad3c"
        );

        circle(
            x - 10,
            y - 8,
            5,
            "#111"
        );

        circle(
            x + 10,
            y - 8,
            5,
            "#111"
        );

        circle(
            x + 29,
            y + 2,
            12,
            "#207c2a"
        );
    }


    else if (p.type === "wallnut") {

        ctx.fillStyle = "#a96828";

        ctx.beginPath();

        ctx.ellipse(
            x,
            y,
            40,
            50,
            0,
            0,
            Math.PI * 2
        );

        ctx.fill();

        ctx.strokeStyle = "#714117";
        ctx.lineWidth = 3;

        for (let i = -2; i <= 2; i++) {

            line(
                x + i * 10,
                y - 30,
                x + i * 13,
                y + 35,
                "#714117",
                2
            );
        }

        circle(
            x - 13,
            y - 8,
            6,
            "#111"
        );

        circle(
            x + 13,
            y - 8,
            6,
            "#111"
        );
    }


    else if (p.type === "cherry") {

        circle(
            x - 23,
            y + 5,
            28,
            "#d92828"
        );

        circle(
            x + 23,
            y + 5,
            28,
            "#d92828"
        );

        line(
            x,
            y - 15,
            x + 17,
            y - 48,
            "#286c25",
            7
        );

        circle(
            x + 23,
            y - 42,
            13,
            "#3d9c38"
        );
    }


    // ==================================
    // CÂY ĂN THỊT MÀU TÍM
    // ==================================

    else if (p.type === "chomper") {

        // thân tím đậm
        line(
            x,
            y + 28,
            x,
            y + 62,
            "#54206f",
            9
        );

        // lá tím
        circle(
            x - 20,
            y + 45,
            17,
            "#71359b"
        );

        circle(
            x + 20,
            y + 45,
            17,
            "#71359b"
        );

        // đầu tím
        circle(
            x,
            y,
            43,
            "#803bb5"
        );

        // phần miệng tím sáng
        ctx.fillStyle = "#d29af0";

        ctx.beginPath();

        ctx.moveTo(
            x - 34,
            y + 2
        );

        ctx.quadraticCurveTo(
            x,
            y + 43,
            x + 34,
            y + 2
        );

        ctx.quadraticCurveTo(
            x,
            y + 17,
            x - 34,
            y + 2
        );

        ctx.fill();


        // viền miệng
        ctx.strokeStyle = "#4c1768";
        ctx.lineWidth = 4;

        ctx.beginPath();

        ctx.moveTo(
            x - 34,
            y + 2
        );

        ctx.quadraticCurveTo(
            x,
            y + 43,
            x + 34,
            y + 2
        );

        ctx.stroke();


        // răng
        for (let i = -2; i <= 2; i++) {

            ctx.fillStyle = "#ffffff";

            ctx.beginPath();

            ctx.moveTo(
                x + i * 12 - 5,
                y + 7
            );

            ctx.lineTo(
                x + i * 12,
                y + 20
            );

            ctx.lineTo(
                x + i * 12 + 5,
                y + 7
            );

            ctx.fill();
        }


        // mắt
        circle(
            x - 13,
            y - 18,
            5,
            "#111"
        );

        circle(
            x + 13,
            y - 18,
            5,
            "#111"
        );


        // má
        circle(
            x - 31,
            y - 2,
            6,
            "#b96bdd"
        );

        circle(
            x + 31,
            y - 2,
            6,
            "#b96bdd"
        );
    }


    // thanh máu
    if (p.type !== "sunflower") {

        let hpWidth = 75;

        rect(
            x - hpWidth / 2,
            y + 67,
            hpWidth,
            7,
            "#7a0000"
        );

        rect(
            x - hpWidth / 2,
            y + 67,
            hpWidth *
            Math.max(
                0,
                p.hp / p.maxHp
            ),
            7,
            "#26a52f"
        );
    }
}


// =============================
// TRỒNG CÂY
// =============================

function plantAt(row, col) {

    if (
        row < 0 ||
        row >= ROWS ||
        col < 0 ||
        col >= COLS
    ) {
        return;
    }

    let exists = plants.find(
        p =>
            p.row === row &&
            p.col === col
    );

    if (exists) return;

    let info =
        plantInfo[selected];

    if (sun < info.cost) return;

    sun -= info.cost;

    let hp = 120;

    if (selected === "wallnut") {
        hp = 350;
    }

    if (selected === "chomper") {
        hp = 180;
    }

    plants.push({

        type: selected,

        row: row,
        col: col,

        hp: hp,
        maxHp: hp,

        timer: 0,

        eating: false,
        eatTimer: 0
    });
}


// =============================
// BẮN ĐẠN
// =============================

function shoot(p) {

    let x =
        BOARD_X +
        p.col * CW +
        CW / 2 +
        35;

    let y =
        TOP +
        p.row * CH +
        CH / 2;

    bullets.push({

        x: x,
        y: y,

        row: p.row,

        speed: 10,

        damage: 25
    });
}


// =============================
// CẬP NHẬT CÂY
// =============================

function updatePlants() {

    for (
        let i = plants.length - 1;
        i >= 0;
        i--
    ) {

        let p = plants[i];

        p.timer++;


        // HƯỚNG DƯƠNG
        if (
            p.type === "sunflower"
        ) {

            if (p.timer >= 480) {

                p.timer = 0;

                suns.push({

                    x:
                        BOARD_X +
                        p.col * CW +
                        CW / 2,

                    y:
                        TOP +
                        p.row * CH +
                        35,

                    value: 25,

                    life: 600
                });
            }
        }


        // ĐẬU
        else if (
            p.type === "pea"
        ) {

            let target =
                zombies.find(
                    z =>
                        z.row === p.row &&
                        z.x >
                        BOARD_X +
                        p.col * CW
                );

            if (
                target &&
                p.timer >= 85
            ) {

                shoot(p);

                p.timer = 0;
            }
        }


        // CHERRY
        else if (
            p.type === "cherry"
        ) {

            if (p.timer >= 45) {

                let x =
                    BOARD_X +
                    p.col * CW +
                    CW / 2;

                let y =
                    TOP +
                    p.row * CH +
                    CH / 2;

                for (
                    let z of zombies
                ) {

                    let zy =
                        TOP +
                        z.row * CH +
                        CH / 2;

                    let d =
                        Math.hypot(
                            z.x - x,
                            zy - y
                        );

                    if (d < 190) {

                        z.hp -= 180;
                    }
                }

                plants.splice(i, 1);
            }
        }


        // CÂY ĂN THỊT
        else if (
            p.type === "chomper"
        ) {

            if (p.eating) {

                p.eatTimer--;

                if (
                    p.eatTimer <= 0
                ) {

                    p.eating = false;
                    p.timer = 0;
                }

                continue;
            }


            let px =
                BOARD_X +
                p.col * CW +
                CW / 2;

            let target = null;

            for (
                let z of zombies
            ) {

                if (
                    z.row !== p.row
                ) {
                    continue;
                }

                let distance =
                    z.x - px;

                if (
                    distance > -20 &&
                    distance < 100
                ) {

                    target = z;
                    break;
                }
            }


            if (target) {

                target.hp = 0;

                p.eating = true;

                p.eatTimer = 300;
            }
        }
    }
}


// =============================
// VẼ ĐẠN
// =============================

function drawBullets() {

    for (
        let b of bullets
    ) {

        circle(
            b.x,
            b.y,
            9,
            "#3a9e31"
        );

        circle(
            b.x - 3,
            b.y - 3,
            3,
            "#a6df72"
        );
    }
}


// =============================
// CẬP NHẬT ĐẠN
// =============================

function updateBullets() {

    for (
        let i = bullets.length - 1;
        i >= 0;
        i--
    ) {

        let b = bullets[i];

        b.x += b.speed;

        let hit = false;

        for (
            let z of zombies
        ) {

            if (
                z.row !== b.row
            ) {
                continue;
            }

            let zy =
                TOP +
                z.row * CH +
                CH / 2;

            if (
                Math.abs(
                    z.x - b.x
                ) < 35 &&
                Math.abs(
                    zy - b.y
                ) < 45
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


// =============================
// TẠO ZOMBIE
// =============================

function spawnZombie() {

    let row =
        Math.floor(
            Math.random() * ROWS
        );

    let chance =
        Math.random();

    let type = "normal";

    if (
        chance < 0.20
    ) {

        type = "bucket";

    } else if (
        chance < 0.34
    ) {

        type = "big";
    }


    let hp = 120;
    let speed = 0.45;
    let scale = 1;


    if (
        type === "bucket"
    ) {

        hp = 300;
        speed = 0.38;
        scale = 1.05;
    }


    if (
        type === "big"
    ) {

        hp = 650;
        speed = 0.25;
        scale = 1.35;
    }


    zombies.push({

        type: type,

        row: row,

        x: W + 80,

        hp: hp,

        maxHp: hp,

        speed: speed,

        scale: scale,

        attackTimer: 0
    });
}


// =============================
// VẼ ZOMBIE
// =============================

function drawZombie(z) {

    let x = z.x;

    let y =
        TOP +
        z.row * CH +
        CH / 2;

    let s = z.scale;

    ctx.save();

    ctx.translate(x, y);

    ctx.scale(s, s);


    // chân
    rect(
        -25,
        45,
        18,
        48,
        "#333"
    );

    rect(
        8,
        45,
        18,
        48,
        "#333"
    );


    // thân
    rect(
        -38,
        -5,
        76,
        65,
        "#526b56"
    );


    // áo
    rect(
        -34,
        5,
        68,
        50,
        "#555d63"
    );


    // đầu
    circle(
        0,
        -45,
        42,
        "#91a875"
    );


    // tóc
    rect(
        -34,
        -83,
        68,
        16,
        "#32322d"
    );


    // mắt
    circle(
        -14,
        -50,
        6,
        "#111"
    );

    circle(
        14,
        -50,
        6,
        "#111"
    );


    // miệng
    ctx.strokeStyle = "#222";
    ctx.lineWidth = 4;

    ctx.beginPath();

    ctx.arc(
        0,
        -30,
        17,
        0.1,
        Math.PI - 0.1
    );

    ctx.stroke();


    // cà vạt
    ctx.fillStyle = "#8b2222";

    ctx.beginPath();

    ctx.moveTo(
        0,
        -2
    );

    ctx.lineTo(
        -9,
        25
    );

    ctx.lineTo(
        0,
        43
    );

    ctx.lineTo(
        9,
        25
    );

    ctx.fill();


    // ZOMBIE XÔ
    if (
        z.type === "bucket"
    ) {

        rect(
            -35,
            -102,
            70,
            34,
            "#888"
        );

        rect(
            -30,
            -108,
            60,
            9,
            "#555"
        );

        line(
            -35,
            -82,
            35,
            -82,
            "#444",
            5
        );
    }


    // ZOMBIE BIG
    if (
        z.type === "big"
    ) {

        circle(
            0,
            -105,
            18,
            "#4d4d4d"
        );

        rect(
            -58,
            55,
            116,
            18,
            "#3b3b3b"
        );
    }


    ctx.restore();


    let barW =
        75 * z.scale;

    rect(
        x - barW / 2,
        y - 105 * z.scale,
        barW,
        7,
        "#650000"
    );

    rect(
        x - barW / 2,
        y - 105 * z.scale,
        barW *
        Math.max(
            0,
            z.hp / z.maxHp
        ),
        7,
        "#22a52f"
    );
}


// =============================
// CẬP NHẬT ZOMBIE
// =============================

function updateZombies() {

    for (
        let i = zombies.length - 1;
        i >= 0;
        i--
    ) {

        let z = zombies[i];

        if (
            z.hp <= 0
        ) {

            zombies.splice(i, 1);

            continue;
        }


        let blocked = false;


        for (
            let p of plants
        ) {

            if (
                p.row !== z.row
            ) {
                continue;
            }

            let px =
                BOARD_X +
                p.col * CW +
                CW / 2;

            if (
                Math.abs(
                    z.x - px
                ) < 65
            ) {

                blocked = true;

                z.attackTimer++;

                if (
                    z.attackTimer >= 50
                ) {

                    z.attackTimer = 0;

                    p.hp -=
                        z.type === "big"
                            ? 18
                            : 10;
                }

                break;
            }
        }


        if (!blocked) {

            z.x -= z.speed;
        }


        // máy cắt cỏ
        for (
            let m of mowers
        ) {

            if (
                m.row === z.row &&
                !m.active &&
                z.x < BOARD_X + 50
            ) {

                m.active = true;
            }
        }


        if (
            z.x < 0
        ) {

            gameOver = true;
        }
    }
}


// =============================
// MÁY CẮT CỎ
// =============================

function updateMowers() {

    for (
        let m of mowers
    ) {

        if (!m.active) {
            continue;
        }

        m.x += 9;


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

                zombies.splice(i, 1);
            }
        }
    }
}


function drawMowers() {

    for (
        let m of mowers
    ) {

        let y = m.y;

        rect(
            m.x - 35,
            y - 22,
            70,
            35,
            "#c9362b"
        );

        circle(
            m.x - 22,
            y + 18,
            12,
            "#222"
        );

        circle(
            m.x + 22,
            y + 18,
            12,
            "#222"
        );

        line(
            m.x - 20,
            y - 20,
            m.x - 45,
            y - 55,
            "#222",
            7
        );

        line(
            m.x - 45,
            y - 55,
            m.x - 20,
            y - 65,
            "#222",
            7
        );

        circle(
            m.x + 27,
            y - 8,
            6,
            "#ffe84d"
        );
    }
}


// =============================
// BẢNG CỎ
// =============================

function drawBoard() {

    rect(
        0,
        TOP,
        W,
        H - TOP,
        "#67ad43"
    );


    rect(
        0,
        TOP,
        MOWER_W,
        ROWS * CH,
        "#4c8e36"
    );


    for (
        let r = 0;
        r < ROWS;
        r++
    ) {

        for (
            let c = 0;
            c < COLS;
            c++
        ) {

            let x =
                BOARD_X +
                c * CW;

            let y =
                TOP +
                r * CH;

            rect(
                x,
                y,
                CW - 2,
                CH - 2,
                (r + c) % 2 === 0
                    ? "#78bd4c"
                    : "#70b646"
            );


            for (
                let k = 0;
                k < 4;
                k++
            ) {

                let gx =
                    x +
                    20 +
                    k * 30;

                let gy =
                    y +
                    CH -
                    20;

                line(
                    gx,
                    gy,
                    gx - 3,
                    gy - 10,
                    "#4f9638",
                    2
                );
            }
        }
    }


    for (
        let r = 0;
        r <= ROWS;
        r++
    ) {

        line(
            BOARD_X,
            TOP + r * CH,
            BOARD_X + COLS * CW,
            TOP + r * CH,
            "#3c8230",
            2
        );
    }


    for (
        let c = 0;
        c <= COLS;
        c++
    ) {

        line(
            BOARD_X + c * CW,
            TOP,
            BOARD_X + c * CW,
            TOP + ROWS * CH,
            "#3c8230",
            2
        );
    }
}


// =============================
// MẶT TRỜI
// =============================

function drawSuns() {

    for (
        let s of suns
    ) {

        circle(
            s.x,
            s.y,
            24,
            "#ffd52e"
        );

        for (
            let i = 0;
            i < 8;
            i++
        ) {

            let a =
                i * Math.PI / 4;

            line(
                s.x + Math.cos(a) * 28,
                s.y + Math.sin(a) * 28,
                s.x + Math.cos(a) * 38,
                s.y + Math.sin(a) * 38,
                "#e9a900",
                3
            );
        }

        circle(
            s.x - 7,
            s.y - 4,
            3,
            "#111"
        );

        circle(
            s.x + 7,
            s.y - 4,
            3,
            "#111"
        );
    }
}


function spawnSun() {

    suns.push({

        x:
            BOARD_X +
            Math.random() *
            (COLS * CW),

        y:
            TOP +
            30 +
            Math.random() *
            (ROWS * CH - 60),

        value: 25,

        life: 800
    });
}


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

            suns.splice(i, 1);
        }
    }
}


function collectSun(x, y) {

    for (
        let i = suns.length - 1;
        i >= 0;
        i--
    ) {

        let s = suns[i];

        if (
            Math.hypot(
                x - s.x,
                y - s.y
            ) < 45
        ) {

            sun += s.value;

            suns.splice(i, 1);

            return true;
        }
    }

    return false;
}


// =============================
// ĐIỀU KHIỂN
// =============================

function pointerDown(e) {

    e.preventDefault();

    let rc =
        canvas.getBoundingClientRect();

    let scaleX =
        W / rc.width;

    let scaleY =
        H / rc.height;

    let x =
        (e.clientX - rc.left) *
        scaleX;

    let y =
        (e.clientY - rc.top) *
        scaleY;


    if (gameOver) {

        location.reload();

        return;
    }


    if (
        collectSun(x, y)
    ) {

        return;
    }


    let cards = [
        ["sunflower", 190],
        ["pea", 330],
        ["wallnut", 470],
        ["cherry", 610],
        ["chomper", 750]
    ];


    for (
        let item of cards
    ) {

        let type = item[0];
        let bx = item[1];

        if (
            x >= bx &&
            x <= bx + 125 &&
            y >= 10 &&
            y <= 100
        ) {

            selected = type;

            return;
        }
    }


    if (
        x < BOARD_X
    ) {

        return;
    }


    if (
        y < TOP
    ) {

        return;
    }


    let col =
        Math.floor(
            (x - BOARD_X) / CW
        );

    let row =
        Math.floor(
            (y - TOP) / CH
        );


    plantAt(
        row,
        col
    );
}


canvas.addEventListener(
    "pointerdown",
    pointerDown
);


// =============================
// VÒNG LẶP GAME
// =============================

function draw() {

    ctx.clearRect(
        0,
        0,
        W,
        H
    );

    drawBoard();

    drawTop();

    drawMowers();


    for (
        let p of plants
    ) {

        drawPlant(p);
    }


    drawBullets();


    for (
        let z of zombies
    ) {

        drawZombie(z);
    }


    drawSuns();


    if (gameOver) {

        rect(
            0,
            0,
            W,
            H,
            "rgba(0,0,0,0.65)"
        );

        text(
            "GAME OVER",
            W / 2,
            H / 2 - 35,
            65,
            "#ffffff"
        );

        text(
            "Chạm màn hình để chơi lại",
            W / 2,
            H / 2 + 35,
            25,
            "#ffffff"
        );
    }
}


function update() {

    if (gameOver) {
        return;
    }

    frame++;

    updatePlants();

    updateBullets();

    updateZombies();

    updateMowers();

    updateSuns();


    if (
        frame % 210 === 0
    ) {

        spawnZombie();
    }


    if (
        frame % 420 === 0
    ) {

        spawnSun();
    }


    for (
        let i = plants.length - 1;
        i >= 0;
        i--
    ) {

        if (
            plants[i].hp <= 0
        ) {

            plants.splice(i, 1);
        }
    }
}


function loop() {

    update();

    draw();

    requestAnimationFrame(loop);
}


loop();

</script>

</body>
</html>
"""

    components.html(
        game,
        height=905,
        scrolling=False
    )


if __name__ == "__main__":
    main()

