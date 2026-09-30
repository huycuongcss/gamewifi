
import streamlit as st
import streamlit.components.v1 as components


def main():

    st.set_page_config(
        page_title="🍎 Hứng Táo",
        page_icon="🍎",
        layout="centered"
    )

    st.title("🍎 HỨNG TÁO")
    st.write("📱 Điện thoại: chạm và kéo trái/phải")
    st.write("💻 Máy tính: di chuyển chuột để điều khiển giỏ")

    game = """
    <canvas id="game"></canvas>

    <style>

        body {
            margin: 0;
            padding: 0;
            background: white;
        }

        #game {
            display: block;
            width: 100%;
            max-width: 500px;
            height: auto;
            margin: auto;
            border: 4px solid #5D4037;
            border-radius: 15px;
            touch-action: none;
            background: #87CEEB;
        }

    </style>


    <script>

    const canvas = document.getElementById("game");

    const ctx = canvas.getContext("2d");


    // KÍCH THƯỚC GAME

    canvas.width = 500;
    canvas.height = 650;


    // =========================
    // GIỎ
    // =========================

    let basket = {

        x: 200,

        y: 565,

        width: 100,

        height: 30

    };


    // =========================
    // TÁO
    // =========================

    let apple = {

        x: 250,

        y: 50,

        radius: 18,

        speed: 4

    };


    // =========================
    // BIẾN GAME
    // =========================

    let score = 0;

    let gameOver = false;


    // =========================
    // PHÔNG NỀN
    // =========================

    function drawBackground() {


        // BẦU TRỜI

        let sky =
            ctx.createLinearGradient(
                0,
                0,
                0,
                450
            );

        sky.addColorStop(
            0,
            "#29B6F6"
        );

        sky.addColorStop(
            1,
            "#B3E5FC"
        );

        ctx.fillStyle = sky;

        ctx.fillRect(
            0,
            0,
            500,
            650
        );


        // MẶT TRỜI

        ctx.beginPath();

        ctx.fillStyle = "#FFD54F";

        ctx.arc(
            420,
            80,
            45,
            0,
            Math.PI * 2
        );

        ctx.fill();


        // MÂY

        drawCloud(
            80,
            100
        );

        drawCloud(
            280,
            150
        );


        // NÚI

        ctx.fillStyle = "#81C784";

        ctx.beginPath();

        ctx.moveTo(
            0,
            440
        );

        ctx.lineTo(
            100,
            300
        );

        ctx.lineTo(
            210,
            440
        );

        ctx.lineTo(
            340,
            280
        );

        ctx.lineTo(
            500,
            440
        );

        ctx.closePath();

        ctx.fill();


        // MẶT ĐẤT

        ctx.fillStyle = "#4CAF50";

        ctx.fillRect(
            0,
            440,
            500,
            210
        );


        // CÂY

        drawTree(
            55,
            440
        );

        drawTree(
            445,
            440
        );


        // CỎ

        ctx.strokeStyle =
            "#1B5E20";

        ctx.lineWidth = 2;


        for (
            let x = 0;
            x < 500;
            x += 15
        ) {

            ctx.beginPath();

            ctx.moveTo(
                x,
                450
            );

            ctx.lineTo(
                x + 5,
                440
            );

            ctx.stroke();

        }

    }


    // =========================
    // MÂY
    // =========================

    function drawCloud(
        x,
        y
    ) {

        ctx.fillStyle =
            "white";


        ctx.beginPath();


        ctx.arc(
            x,
            y,
            25,
            0,
            Math.PI * 2
        );


        ctx.arc(
            x + 30,
            y - 10,
            35,
            0,
            Math.PI * 2
        );


        ctx.arc(
            x + 65,
            y,
            25,
            0,
            Math.PI * 2
        );


        ctx.fill();

    }


    // =========================
    // CÂY
    // =========================

    function drawTree(
        x,
        y
    ) {


        // THÂN

        ctx.fillStyle =
            "#795548";


        ctx.fillRect(
            x - 12,
            y - 80,
            24,
            80
        );


        // TÁN CÂY

        ctx.fillStyle =
            "#2E7D32";


        ctx.beginPath();

        ctx.arc(
            x,
            y - 105,
            45,
            0,
            Math.PI * 2
        );

        ctx.fill();


        ctx.beginPath();

        ctx.arc(
            x - 30,
            y - 80,
            35,
            0,
            Math.PI * 2
        );

        ctx.fill();


        ctx.beginPath();

        ctx.arc(
            x + 30,
            y - 80,
            35,
            0,
            Math.PI * 2
        );

        ctx.fill();

    }


    // =========================
    // VẼ GIỎ
    // =========================

    function drawBasket() {


        // THÂN GIỎ

        ctx.fillStyle =
            "#A1887F";


        ctx.fillRect(
            basket.x,
            basket.y,
            basket.width,
            basket.height
        );


        // VIỀN

        ctx.strokeStyle =
            "#4E342E";

        ctx.lineWidth = 5;


        ctx.strokeRect(
            basket.x,
            basket.y,
            basket.width,
            basket.height
        );


        // QUAI GIỎ

        ctx.beginPath();


        ctx.arc(
            basket.x +
            basket.width / 2,

            basket.y,

            45,

            Math.PI,

            0
        );


        ctx.stroke();

    }


    // =========================
    // VẼ TÁO
    // =========================

    function drawApple() {


        // QUẢ TÁO

        ctx.beginPath();

        ctx.fillStyle =
            "#E53935";


        ctx.arc(
            apple.x,
            apple.y,
            apple.radius,
            0,
            Math.PI * 2
        );


        ctx.fill();


        // LÁ

        ctx.fillStyle =
            "#2E7D32";


        ctx.beginPath();


        ctx.ellipse(
            apple.x + 12,
            apple.y - 17,
            11,
            5,
            -0.5,
            0,
            Math.PI * 2
        );


        ctx.fill();


        // CUỐNG

        ctx.fillStyle =
            "#5D4037";


        ctx.fillRect(
            apple.x - 2,
            apple.y - 28,
            4,
            11
        );

    }


    // =========================
    // TÁO MỚI
    // =========================

    function newApple() {


        apple.x =
            Math.random() *
            440 + 30;


        apple.y = 20;

    }


    // =========================
    // CẬP NHẬT GAME
    // =========================

    function update() {


        if (gameOver) {

            return;

        }


        apple.y +=
            apple.speed;


        // KIỂM TRA HỨNG TÁO

        if (

            apple.y +
            apple.radius >=
            basket.y

            &&

            apple.x >=
            basket.x

            &&

            apple.x <=
            basket.x +
            basket.width

        ) {


            score++;


            // Càng chơi càng nhanh

            apple.speed +=
                0.15;


            newApple();

        }


        // TÁO RƠI

        if (
            apple.y >
            canvas.height
        ) {

            gameOver = true;

        }

    }


    // =========================
    // VẼ GAME
    // =========================

    function draw() {


        drawBackground();


        drawBasket();


        drawApple();


        // ĐIỂM

        ctx.fillStyle =
            "white";


        ctx.font =
            "bold 28px Arial";


        ctx.fillText(
            "🍎 Điểm: " +
            score,

            15,
            35
        );


        // GAME OVER

        if (gameOver) {


            // NỀN TỐI

            ctx.fillStyle =
                "rgba(0,0,0,0.65)";


            ctx.fillRect(
                0,
                0,
                canvas.width,
                canvas.height
            );


            ctx.textAlign =
                "center";


            ctx.fillStyle =
                "white";


            ctx.font =
                "bold 45px Arial";


            ctx.fillText(
                "GAME OVER",

                250,
                280
            );


            ctx.font =
                "26px Arial";


            ctx.fillText(
                "🍎 Điểm: " +
                score,

                250,
                330
            );


            ctx.fillText(
                "👆 Chạm để chơi lại",

                250,
                380
            );


            ctx.textAlign =
                "left";

        }

    }


    // =========================
    // ĐIỀU KHIỂN MÁY TÍNH
    // =========================

    canvas.addEventListener(
        "mousemove",

        function(event) {


            let rect =
                canvas.getBoundingClientRect();


            let scale =
                canvas.width /
                rect.width;


            basket.x =

                (
                    event.clientX -
                    rect.left
                )

                * scale

                -
                basket.width / 2;


            limitBasket();

        }

    );


    // =========================
    // ĐIỀU KHIỂN ĐIỆN THOẠI
    // =========================

    canvas.addEventListener(
        "touchstart",

        function(event) {

            event.preventDefault();


            moveBasket(
                event.touches[0]
            );


        },

        {
            passive: false
        }

    );


    canvas.addEventListener(
        "touchmove",

        function(event) {

            event.preventDefault();


            moveBasket(
                event.touches[0]
            );


        },

        {
            passive: false
        }

    );


    function moveBasket(
        touch
    ) {


        let rect =
            canvas.getBoundingClientRect();


        let scale =
            canvas.width /
            rect.width;


        basket.x =

            (
                touch.clientX -
                rect.left
            )

            * scale

            -
            basket.width / 2;


        limitBasket();

    }


    // =========================
    // GIỚI HẠN GIỎ
    // =========================

    function limitBasket() {


        if (
            basket.x < 0
        ) {

            basket.x = 0;

        }


        if (
            basket.x +
            basket.width >
            canvas.width
        ) {

            basket.x =
                canvas.width -
                basket.width;

        }

    }


    // =========================
    // CHƠI LẠI
    // =========================

    canvas.addEventListener(
        "click",

        function() {


            if (gameOver) {

                restartGame();

            }

        }

    );


    canvas.addEventListener(
        "touchend",

        function() {


            if (gameOver) {

                restartGame();

            }

        }

    );


    function restartGame() {


        score = 0;


        apple.speed = 4;


        gameOver = false;


        newApple();

    }


    // =========================
    // GAME LOOP
    // =========================

    function gameLoop() {


        update();


        draw();


        requestAnimationFrame(
            gameLoop
        );

    }


    // BẮT ĐẦU

    newApple();


    gameLoop();

    </script>
    """


    components.html(
        game,
        height=700
    )


if __name__ == "__main__":
    main()

