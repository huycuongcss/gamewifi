
import streamlit as st
import streamlit.components.v1 as components


def main():

    st.title("🍎 HỨNG TÁO")
    st.write("Di chuyển giỏ bằng chuột hoặc chạm màn hình để hứng táo!")

    html = """
    <canvas id="game" width="500" height="650"
        style="
            width:100%;
            max-width:500px;
            display:block;
            margin:auto;
            border:4px solid #5D4037;
            border-radius:15px;
            touch-action:none;
        ">
    </canvas>

    <script>

    const canvas = document.getElementById("game");
    const ctx = canvas.getContext("2d");

    let basket = {
        x: 200,
        y: 570,
        width: 100,
        height: 30
    };

    let apple = {
        x: 250,
        y: 50,
        radius: 18,
        speed: 4
    };

    let score = 0;
    let gameOver = false;


    // =========================
    // PHÔNG NỀN
    // =========================

    function drawBackground() {

        // BẦU TRỜI
        ctx.fillStyle = "#87CEEB";
        ctx.fillRect(0, 0, 500, 650);


        // MẶT TRỜI
        ctx.beginPath();
        ctx.fillStyle = "#FFD700";
        ctx.arc(420, 80, 45, 0, Math.PI * 2);
        ctx.fill();


        // MÂY 1
        drawCloud(80, 100);

        // MÂY 2
        drawCloud(300, 150);


        // NÚI
        ctx.fillStyle = "#81C784";

        ctx.beginPath();
        ctx.moveTo(0, 430);
        ctx.lineTo(120, 280);
        ctx.lineTo(250, 430);
        ctx.lineTo(370, 260);
        ctx.lineTo(500, 430);
        ctx.closePath();
        ctx.fill();


        // MẶT ĐẤT
        ctx.fillStyle = "#4CAF50";
        ctx.fillRect(0, 430, 500, 220);


        // CÂY
        drawTree(60, 430);
        drawTree(440, 430);


        // CỎ
        ctx.strokeStyle = "#1B5E20";
        ctx.lineWidth = 3;

        for (let x = 0; x < 500; x += 15) {

            ctx.beginPath();
            ctx.moveTo(x, 450);
            ctx.lineTo(x + 5, 440);
            ctx.stroke();
        }
    }


    // =========================
    // MÂY
    // =========================

    function drawCloud(x, y) {

        ctx.fillStyle = "white";

        ctx.beginPath();

        ctx.arc(x, y, 25, 0, Math.PI * 2);
        ctx.arc(x + 30, y - 10, 35, 0, Math.PI * 2);
        ctx.arc(x + 65, y, 25, 0, Math.PI * 2);

        ctx.fill();
    }


    // =========================
    // CÂY
    // =========================

    function drawTree(x, y) {

        // thân
        ctx.fillStyle = "#795548";

        ctx.fillRect(
            x - 12,
            y - 80,
            24,
            80
        );


        // tán cây
        ctx.fillStyle = "#2E7D32";

        ctx.beginPath();
        ctx.arc(x, y - 100, 45, 0, Math.PI * 2);
        ctx.fill();

        ctx.beginPath();
        ctx.arc(x - 30, y - 75, 35, 0, Math.PI * 2);
        ctx.fill();

        ctx.beginPath();
        ctx.arc(x + 30, y - 75, 35, 0, Math.PI * 2);
        ctx.fill();
    }


    // =========================
    // GIỎ
    // =========================

    function drawBasket() {

        // giỏ
        ctx.fillStyle = "#8D6E63";

        ctx.fillRect(
            basket.x,
            basket.y,
            basket.width,
            basket.height
        );


        // viền
        ctx.strokeStyle = "#4E342E";
        ctx.lineWidth = 4;

        ctx.strokeRect(
            basket.x,
            basket.y,
            basket.width,
            basket.height
        );


        // quai
        ctx.beginPath();

        ctx.arc(
            basket.x + basket.width / 2,
            basket.y,
            45,
            Math.PI,
            0
        );

        ctx.stroke();
    }


    // =========================
    // TÁO
    // =========================

    function drawApple() {

        // quả
        ctx.beginPath();

        ctx.fillStyle = "#E53935";

        ctx.arc(
            apple.x,
            apple.y,
            apple.radius,
            0,
            Math.PI * 2
        );

        ctx.fill();


        // lá
        ctx.fillStyle = "#2E7D32";

        ctx.beginPath();

        ctx.ellipse(
            apple.x + 12,
            apple.y - 17,
            10,
            5,
            -0.5,
            0,
            Math.PI * 2
        );

        ctx.fill();


        // cuống
        ctx.fillStyle = "#5D4037";

        ctx.fillRect(
            apple.x - 2,
            apple.y - 27,
            4,
            10
        );
    }


    // =========================
    // TẠO TÁO MỚI
    // =========================

    function newApple() {

        apple.x =
            Math.random() * 440 + 30;

        apple.y = 20;
    }


    // =========================
    // CẬP NHẬT
    // =========================

    function update() {

        if (gameOver) {
            return;
        }


        apple.y += apple.speed;


        // hứng được táo
        if (
            apple.y + apple.radius >= basket.y &&
            apple.x >= basket.x &&
            apple.x <= basket.x + basket.width
        ) {

            score++;

            apple.speed += 0.15;

            newApple();
        }


        // táo rơi mất
        if (apple.y > 650) {

            gameOver = true;
        }
    }


    // =========================
    // VẼ
    // =========================

    function draw() {

        drawBackground();

        drawBasket();

        drawApple();


        // điểm
        ctx.fillStyle = "white";

        ctx.font = "bold 28px Arial";

        ctx.fillText(
            "🍎 Điểm: " + score,
            15,
            35
        );


        // GAME OVER
        if (gameOver) {

            ctx.fillStyle = "rgba(0,0,0,0.65)";

            ctx.fillRect(
                0,
                0,
                500,
                650
            );


            ctx.fillStyle = "white";

            ctx.textAlign = "center";


            ctx.font = "bold 45px Arial";

            ctx.fillText(
                "GAME OVER",
                250,
                280
            );


            ctx.font = "26px Arial";

            ctx.fillText(
                "Điểm: " + score,
                250,
                330
            );


            ctx.fillText(
                "👆 Chạm để chơi lại",
                250,
                380
            );


            ctx.textAlign = "left";
        }
    }


    // =========================
    // CHUỘT
    // =========================

    canvas.addEventListener(
        "mousemove",
        function(event) {

            let rect =
                canvas.getBoundingClientRect();

            let scale =
                canvas.width / rect.width;

            basket.x =
                (event.clientX - rect.left)
                * scale
                - basket.width / 2;


            if (basket.x < 0) {
                basket.x = 0;
            }


            if (basket.x + basket.width > 500) {
                basket.x =
                    500 - basket.width;
            }
        }
    );


    // =========================
    // ĐIỆN THOẠI
    // =========================

    canvas.addEventListener(
        "touchmove",
        function(event) {

            event.preventDefault();

            let rect =
                canvas.getBoundingClientRect();

            let scale =
                canvas.width / rect.width;

            basket.x =
                (event.touches[0].clientX - rect.left)
                * scale
                - basket.width / 2;


            if (basket.x < 0) {
                basket.x = 0;
            }


            if (basket.x + basket.width > 500) {
                basket.x =
                    500 - basket.width;
            }
        },
        { passive: false }
    );


    // =========================
    // CHƠI LẠI
    // =========================

    canvas.addEventListener(
        "click",
        function() {

            if (gameOver) {

                score = 0;

                apple.speed = 4;

                gameOver = false;

                newApple();
            }
        }
    );


    canvas.addEventListener(
        "touchstart",
        function() {

            if (gameOver) {

                score = 0;

                apple.speed = 4;

                gameOver = false;

                newApple();
            }
        }
    );


    // =========================
    // GAME LOOP
    // =========================

    function gameLoop() {

        update();

        draw();

        requestAnimationFrame(gameLoop);
    }


    newApple();

    gameLoop();

    </script>
    """


    components.html(
        html,
        height=680
    )


if __name__ == "__main__":
    main()
