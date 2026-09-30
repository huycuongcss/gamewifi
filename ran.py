
import streamlit as st


def main():

    game = r'''
<!DOCTYPE html>
<html>

<head>

<meta charset="UTF-8">

<style>

body {

    margin: 0;

    padding: 10px;

    font-family: Arial;

    text-align: center;

    background: #f5f5f5;

    user-select: none;

    -webkit-user-select: none;
}


h1 {

    margin: 5px;

    color: #1b5e20;

}


.info {

    font-size: 18px;

    font-weight: bold;

    margin: 8px;

}


#message {

    min-height: 55px;

    font-size: 20px;

    font-weight: bold;

    display: flex;

    align-items: center;

    justify-content: center;

}


#game {

    width: 400px;

    height: 400px;

    margin: auto;

    background: #111;

    border: 5px solid #333;

    display: grid;

    grid-template-columns: repeat(20, 1fr);

    grid-template-rows: repeat(20, 1fr);

    touch-action: none;

}


.cell {

    width: 100%;

    height: 100%;

}


.snake {

    background: #00e676;

}


.head {

    background: #76ff03;

}


.food {

    background: red;

    border-radius: 50%;

}


button {

    border: none;

    border-radius: 10px;

    padding: 10px 18px;

    margin: 4px;

    font-size: 20px;

    cursor: pointer;

    touch-action: manipulation;

}


.direction {

    background: #2196f3;

    color: white;

    width: 65px;

    height: 55px;

}


.restart {

    background: #4caf50;

    color: white;

}


.pause {

    background: #ff9800;

    color: white;

}


#mobile-help {

    font-size: 16px;

    margin-top: 10px;

}


@media (max-width: 600px) {

    #game {

        width: 90vw;

        height: 90vw;

        max-width: 400px;

        max-height: 400px;

    }

    button {

        font-size: 18px;

    }

}


</style>

</head>


<body>


<h1>🐍 RẮN SĂN MỒI</h1>


<div class="info">

Điểm:

<span id="score">0</span>

&nbsp;&nbsp;

Độ dài:

<span id="length">3</span>

&nbsp;&nbsp;

Tốc độ:

<span id="speed">0</span>

</div>


<div>

<button
class="restart"
id="restart">

🔄 CHƠI LẠI

</button>


<button
class="pause"
id="pause">

⏸️ TẠM DỪNG

</button>

</div>


<div id="message">

▶️ Bấm phím mũi tên để bắt đầu

</div>


<div id="game"></div>


<br>


<div>

<button
class="direction"
id="up">

⬆️

</button>

</div>


<div>

<button
class="direction"
id="left">

⬅️

</button>

<button
class="direction"
id="down">

⬇️

</button>

<button
class="direction"
id="right">

➡️

</button>

</div>


<div id="mobile-help">

💻 Máy tính: dùng phím mũi tên<br>

📱 Điện thoại: dùng các nút hoặc chạm màn hình

</div>


<script>


// ======================================
// CÀI ĐẶT GAME
// ======================================

const SIZE = 20;

const START_SPEED = 300;

const MIN_SPEED = 80;


// ======================================
// BIẾN GAME
// ======================================

let snake;

let food;

let direction;

let nextDirection;

let score;

let speed;

let timer;

let running;

let paused;


// ======================================
// RESET GAME
// ======================================

function resetGame() {

    clearInterval(timer);


    snake = [

        [10, 10],

        [9, 10],

        [8, 10]

    ];


    food = createFood();


    direction = null;

    nextDirection = null;


    score = 0;

    speed = START_SPEED;


    running = false;

    paused = false;


    document.getElementById(
        "message"
    ).innerText =

        "▶️ Bấm phím mũi tên để bắt đầu";


    document.getElementById(
        "pause"
    ).innerText =

        "⏸️ TẠM DỪNG";


    draw();

    updateInfo();

}


// ======================================
// TẠO MỒI
// ======================================

function createFood() {

    let x;

    let y;

    let ok;


    do {

        x = Math.floor(
            Math.random() * SIZE
        );


        y = Math.floor(
            Math.random() * SIZE
        );


        ok = true;


        for (
            let part of snake
        ) {

            if (

                part[0] === x &&

                part[1] === y

            ) {

                ok = false;

                break;

            }

        }

    }

    while (!ok);


    return [x, y];

}


// ======================================
// BẮT ĐẦU GAME
// ======================================

function startGame(newDirection) {

    direction = newDirection;

    nextDirection = newDirection;


    running = true;

    paused = false;


    document.getElementById(
        "message"
    ).innerText =

        "🐍 ĐANG CHƠI";


    clearInterval(timer);


    timer = setInterval(

        gameLoop,

        speed

    );


    updateInfo();

}


// ======================================
// GAME LOOP
// ======================================

function gameLoop() {

    if (!running) {

        return;

    }


    if (paused) {

        return;

    }


    direction = nextDirection;


    let head = [

        snake[0][0],

        snake[0][1]

    ];


    if (
        direction === "UP"
    ) {

        head[1]--;

    }


    else if (
        direction === "DOWN"
    ) {

        head[1]++;

    }


    else if (
        direction === "LEFT"
    ) {

        head[0]--;

    }


    else if (
        direction === "RIGHT"
    ) {

        head[0]++;

    }


    // ==================================
    // ĐỤNG TƯỜNG
    // ==================================

    if (

        head[0] < 0 ||

        head[0] >= SIZE ||

        head[1] < 0 ||

        head[1] >= SIZE

    ) {

        gameOver();

        return;

    }


    // ==================================
    // ĐỤNG THÂN
    // ==================================

    for (
        let part of snake
    ) {

        if (

            part[0] === head[0] &&

            part[1] === head[1]

        ) {

            gameOver();

            return;

        }

    }


    snake.unshift(head);


    // ==================================
    // ĂN MỒI
    // ==================================

    if (

        head[0] === food[0] &&

        head[1] === food[1]

    ) {

        score += 10;


        food = createFood();


        if (
            speed > MIN_SPEED
        ) {

            speed -= 15;

        }


        clearInterval(timer);


        timer = setInterval(

            gameLoop,

            speed

        );

    }


    else {

        snake.pop();

    }


    draw();

    updateInfo();

}


// ======================================
// VẼ GAME
// ======================================

function draw() {

    let board =

        document.getElementById(
            "game"
        );


    board.innerHTML = "";


    // VẼ RẮN

    for (

        let i = 0;

        i < snake.length;

        i++

    ) {

        let cell =

            document.createElement(
                "div"
            );


        if (i === 0) {

            cell.className =
                "cell head";

        }

        else {

            cell.className =
                "cell snake";

        }


        cell.style.gridColumn =

            snake[i][0] + 1;


        cell.style.gridRow =

            snake[i][1] + 1;


        board.appendChild(cell);

    }


    // VẼ MỒI

    let foodCell =

        document.createElement(
            "div"
        );


    foodCell.className =
        "cell food";


    foodCell.style.gridColumn =

        food[0] + 1;


    foodCell.style.gridRow =

        food[1] + 1;


    board.appendChild(foodCell);

}


// ======================================
// CẬP NHẬT THÔNG TIN
// ======================================

function updateInfo() {

    document.getElementById(
        "score"
    ).innerText = score;


    document.getElementById(
        "length"
    ).innerText = snake.length;


    if (running) {

        document.getElementById(
            "speed"
        ).innerText =

            Math.round(
                1000 / speed
            );

    }

    else {

        document.getElementById(
            "speed"
        ).innerText = 0;

    }

}


// ======================================
// GAME OVER
// ======================================

function gameOver() {

    running = false;

    paused = false;


    clearInterval(timer);


    let danhGia;


    if (score < 50) {

        danhGia =
            "😅 GÀ MỚI TẬP CHƠI";

    }

    else if (score < 100) {

        danhGia =
            "👍 KHÁ";

    }

    else if (score < 200) {

        danhGia =
            "🔥 GIỎI";

    }

    else {

        danhGia =
            "👑 CAO THỦ";

    }


    document.getElementById(
        "message"
    ).innerText =

        "💥 GAME OVER!  " +

        "Điểm: " +

        score +

        "  " +

        danhGia +

        " — BẤM PHÍM BẤT KỲ " +

        "HOẶC CHẠM MÀN HÌNH ĐỂ CHƠI LẠI";


    updateInfo();

}


// ======================================
// ĐỔI HƯỚNG
// ======================================

function changeDirection(
    newDirection
) {

    // Nếu chưa chơi
    // thì bắt đầu

    if (!running) {

        startGame(newDirection);

        return;

    }


    if (

        newDirection === "UP" &&

        direction !== "DOWN"

    ) {

        nextDirection = "UP";

    }


    else if (

        newDirection === "DOWN" &&

        direction !== "UP"

    ) {

        nextDirection = "DOWN";

    }


    else if (

        newDirection === "LEFT" &&

        direction !== "RIGHT"

    ) {

        nextDirection = "LEFT";

    }


    else if (

        newDirection === "RIGHT" &&

        direction !== "LEFT"

    ) {

        nextDirection = "RIGHT";

    }

}


// ======================================
// BẤM PHÍM
// ======================================

document.addEventListener(

    "keydown",

    function(event) {


        // ==============================
        // GAME OVER
        // ==============================

        if (!running) {

            resetGame();


            if (
                event.key === "ArrowUp"
            ) {

                changeDirection("UP");

            }

            else if (
                event.key === "ArrowDown"
            ) {

                changeDirection("DOWN");

            }

            else if (
                event.key === "ArrowLeft"
            ) {

                changeDirection("LEFT");

            }

            else if (
                event.key === "ArrowRight"
            ) {

                changeDirection("RIGHT");

            }

            else {

                changeDirection("RIGHT");

            }


            event.preventDefault();

            return;

        }


        // ==============================
        // ĐANG CHƠI
        // ==============================

        if (
            event.key === "ArrowUp"
        ) {

            event.preventDefault();

            changeDirection("UP");

        }


        else if (
            event.key === "ArrowDown"
        ) {

            event.preventDefault();

            changeDirection("DOWN");

        }


        else if (
            event.key === "ArrowLeft"
        ) {

            event.preventDefault();

            changeDirection("LEFT");

        }


        else if (
            event.key === "ArrowRight"
        ) {

            event.preventDefault();

            changeDirection("RIGHT");

        }


        else if (
            event.code === "Space"
        ) {

            event.preventDefault();

            togglePause();

        }

    }

);


// ======================================
// CHẠM MÀN HÌNH
// ======================================

document.addEventListener(

    "touchstart",

    function(event) {


        // GAME OVER

        if (!running) {

            resetGame();

            changeDirection("RIGHT");

            event.preventDefault();

            return;

        }

    },

    {
        passive: false
    }

);


// ======================================
// CLICK CHUỘT SAU GAME OVER
// ======================================

document.addEventListener(

    "click",

    function(event) {


        if (!running) {


            // Nếu bấm nút điều khiển
            // thì để xử lý riêng

            if (

                event.target.id === "up" ||

                event.target.id === "down" ||

                event.target.id === "left" ||

                event.target.id === "right" ||

                event.target.id === "pause" ||

                event.target.id === "restart"

            ) {

                return;

            }


            resetGame();

            changeDirection("RIGHT");

        }

    }

);


// ======================================
// NÚT ĐIỀU KHIỂN
// ======================================

document.getElementById(
    "up"
).onclick = function() {

    changeDirection("UP");

};


document.getElementById(
    "down"
).onclick = function() {

    changeDirection("DOWN");

};


document.getElementById(
    "left"
).onclick = function() {

    changeDirection("LEFT");

};


document.getElementById(
    "right"
).onclick = function() {

    changeDirection("RIGHT");

};


// ======================================
// TẠM DỪNG
// ======================================

function togglePause() {

    if (!running) {

        return;

    }


    paused = !paused;


    if (paused) {

        document.getElementById(
            "message"
        ).innerText =

            "⏸️ ĐANG TẠM DỪNG";


        document.getElementById(
            "pause"
        ).innerText =

            "▶️ TIẾP TỤC";

    }

    else {

        document.getElementById(
            "message"
        ).innerText =

            "🐍 ĐANG CHƠI";


        document.getElementById(
            "pause"
        ).innerText =

            "⏸️ TẠM DỪNG";

    }

}


document.getElementById(
    "pause"
).onclick = togglePause;


// ======================================
// NÚT CHƠI LẠI
// ======================================

document.getElementById(
    "restart"
).onclick = function() {

    resetGame();

};


// ======================================
// KHỞI ĐỘNG
// ======================================

resetGame();


</script>

</body>

</html>
'''


    st.components.v1.html(
        game,
        height=800,
        scrolling=True
    )


if __name__ == "__main__":
    main()