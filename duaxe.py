import streamlit as st
import streamlit.components.v1 as components


def main():
    st.title("🏎️ GAME ĐUA XE")

    st.write("⬅️ ➡️ Di chuyển xe | 🚗 Tránh xe đối thủ | 💥 Va chạm = Game Over")
    st.write("👉 Khi Game Over, bấm phím bất kỳ để chơi lại.")

    game_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">

        <style>
            body {
                margin: 0;
                padding: 0;
                background: #eeeeee;
                font-family: Arial;
                text-align: center;
            }

            #game {
                position: relative;
                width: 400px;
                height: 600px;
                margin: auto;
                overflow: hidden;
                background: #555;
                border: 5px solid #222;
                box-sizing: border-box;
            }

            #road {
                position: absolute;
                left: 40px;
                top: 0;
                width: 320px;
                height: 100%;
                background: #333;
            }

            .side {
                position: absolute;
                top: 0;
                width: 40px;
                height: 100%;
                background: #228B22;
            }

            #leftSide {
                left: 0;
            }

            #rightSide {
                right: 0;
            }

            .line {
                position: absolute;
                width: 8px;
                height: 80px;
                background: white;
            }

            #score {
                position: absolute;
                top: 10px;
                left: 10px;
                color: white;
                font-size: 24px;
                font-weight: bold;
                z-index: 20;
            }

            #player {
                position: absolute;
                width: 50px;
                height: 90px;
                background: red;
                border-radius: 10px;
                bottom: 30px;
                left: 175px;
                z-index: 10;
            }

            #player::before {
                content: "";
                position: absolute;
                width: 32px;
                height: 35px;
                background: #55ccff;
                left: 9px;
                top: 10px;
                border-radius: 5px;
            }

            #player::after {
                content: "";
                position: absolute;
                width: 8px;
                height: 25px;
                background: yellow;
                left: 21px;
                bottom: 8px;
                border-radius: 3px;
            }

            .enemy {
                position: absolute;
                width: 50px;
                height: 90px;
                border-radius: 10px;
                z-index: 5;
            }

            .enemy::before {
                content: "";
                position: absolute;
                width: 32px;
                height: 35px;
                background: #88ddff;
                left: 9px;
                top: 10px;
                border-radius: 5px;
            }

            #gameOver {
                display: none;
                position: absolute;
                z-index: 100;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.8);
                color: white;
                align-items: center;
                justify-content: center;
                flex-direction: column;
            }

            #gameOver h1 {
                color: red;
                font-size: 42px;
                margin: 10px;
            }

            #gameOver p {
                font-size: 22px;
            }

            #startMessage {
                color: white;
                font-size: 20px;
                margin-top: 10px;
            }

            button {
                padding: 12px 25px;
                font-size: 18px;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                margin-top: 10px;
            }

            #mobileControls {
                margin-top: 10px;
            }

            #mobileControls button {
                width: 100px;
                height: 55px;
                font-size: 28px;
                margin: 5px;
            }
        </style>
    </head>

    <body>

        <div id="game">

            <div id="leftSide" class="side"></div>
            <div id="rightSide" class="side"></div>
            <div id="road"></div>

            <div id="score">Điểm: 0</div>

            <div id="player"></div>

            <div id="gameOver">
                <h1>💥 GAME OVER</h1>
                <p id="finalScore"></p>
                <p>🎮 Bấm phím bất kỳ để chơi lại</p>
                <button onclick="restartGame()">CHƠI LẠI</button>
            </div>

        </div>

        <div id="startMessage">
            ⬅️ Dùng phím mũi tên trái/phải để lái xe
        </div>

        <div id="mobileControls">
            <button onclick="moveLeft()">⬅️</button>
            <button onclick="moveRight()">➡️</button>
        </div>


        <script>

            const game = document.getElementById("game");
            const player = document.getElementById("player");
            const scoreText = document.getElementById("score");
            const gameOverScreen = document.getElementById("gameOver");
            const finalScore = document.getElementById("finalScore");

            let playerX = 175;
            let score = 0;
            let speed = 5;
            let gameRunning = true;

            let enemies = [];
            let lines = [];

            // =========================
            // TẠO VẠCH ĐƯỜNG
            // =========================

            for (let i = 0; i < 7; i++) {

                let line = document.createElement("div");

                line.className = "line";

                line.style.left = "196px";
                line.style.top = (i * 100 - 100) + "px";

                game.appendChild(line);

                lines.push(line);
            }


            // =========================
            // TẠO XE ĐỐI THỦ
            // =========================

            function createEnemy() {

                let enemy = document.createElement("div");

                enemy.className = "enemy";

                let colors = [
                    "blue",
                    "orange",
                    "purple",
                    "yellow",
                    "cyan"
                ];

                enemy.style.background =
                    colors[Math.floor(Math.random() * colors.length)];

                let lane =
                    Math.floor(Math.random() * 3);

                enemy.style.left =
                    (85 + lane * 100) + "px";

                enemy.style.top = "-120px";

                game.appendChild(enemy);

                enemies.push(enemy);
            }


            // =========================
            // DI CHUYỂN TRÁI
            // =========================

            function moveLeft() {

                if (!gameRunning) return;

                playerX -= 25;

                if (playerX < 50) {
                    playerX = 50;
                }

                player.style.left = playerX + "px";
            }


            // =========================
            // DI CHUYỂN PHẢI
            // =========================

            function moveRight() {

                if (!gameRunning) return;

                playerX += 25;

                if (playerX > 300) {
                    playerX = 300;
                }

                player.style.left = playerX + "px";
            }


            // =========================
            // BÀN PHÍM
            // =========================

            document.addEventListener("keydown", function(event) {

                if (!gameRunning) {

                    restartGame();

                    return;
                }

                if (event.key === "ArrowLeft") {
                    moveLeft();
                }

                if (event.key === "ArrowRight") {
                    moveRight();
                }

            });


            // =========================
            // KIỂM TRA VA CHẠM
            // =========================

            function collision(a, b) {

                let r1 = a.getBoundingClientRect();
                let r2 = b.getBoundingClientRect();

                return !(
                    r1.right < r2.left ||
                    r1.left > r2.right ||
                    r1.bottom < r2.top ||
                    r1.top > r2.bottom
                );
            }


            // =========================
            // GAME OVER
            // =========================

            function endGame() {

                gameRunning = false;

                finalScore.innerHTML =
                    "🏆 Điểm của bạn: " + score;

                gameOverScreen.style.display = "flex";
            }


            // =========================
            // CHƠI LẠI
            // =========================

            function restartGame() {

                enemies.forEach(function(enemy) {
                    enemy.remove();
                });

                enemies = [];

                score = 0;
                speed = 5;

                playerX = 175;

                player.style.left =
                    playerX + "px";

                gameOverScreen.style.display =
                    "none";

                gameRunning = true;
            }


            // =========================
            // VÒNG LẶP GAME
            // =========================

            function gameLoop() {

                if (gameRunning) {

                    // Vạch đường chạy xuống

                    lines.forEach(function(line) {

                        let y =
                            parseInt(line.style.top);

                        y += speed;

                        if (y > 600) {
                            y = -80;
                        }

                        line.style.top = y + "px";
                    });


                    // Xe đối thủ

                    enemies.forEach(function(enemy, index) {

                        let y =
                            parseInt(enemy.style.top);

                        y += speed;

                        enemy.style.top =
                            y + "px";


                        // Va chạm

                        if (collision(player, enemy)) {

                            endGame();
                        }


                        // Xe đi khỏi màn hình

                        if (y > 650) {

                            enemy.remove();

                            enemies.splice(index, 1);

                            score++;

                            scoreText.innerHTML =
                                "Điểm: " + score;

                            // Tăng tốc

                            if (score % 10 === 0) {

                                speed += 0.5;
                            }
                        }

                    });


                    // Tạo xe mới

                    if (
                        enemies.length < 3 &&
                        Math.random() < 0.025
                    ) {

                        createEnemy();
                    }
                }


                requestAnimationFrame(gameLoop);
            }


            gameLoop();

        </script>

    </body>
    </html>
    """

    components.html(
        game_html,
        height=700,
        scrolling=False
    )


if __name__ == "__main__":
    main()