document.addEventListener("DOMContentLoaded", () => {
    const imageSection = document.querySelector(".image-section");
    const imageBlocks = document.querySelectorAll(".image-block");

    // Функция для генерации случайного числа в заданном диапазоне
    function getRandomNumber(min, max) {
        return Math.random() * (max - min) + min;
    }

    // Устанавливаем случайные позиции для блоков
    function setRandomPositions() {
        imageBlocks.forEach(block => {
            const sectionRect = imageSection.getBoundingClientRect();
            const blockWidth = block.offsetWidth;
            const blockHeight = block.offsetHeight;

            const initialX = getRandomNumber(0, sectionRect.width - blockWidth);
            const initialY = getRandomNumber(0, sectionRect.height - blockHeight);

            block.style.left = `${initialX}px`;
            block.style.top = `${initialY}px`;
        });
    }

    // Вызываем функцию для установки начальных позиций
    setRandomPositions();

    // Обработчик для реакции на курсор
    imageBlocks.forEach(block => {
        let lastMouseX = 0;
        let lastMouseY = 0;

        block.addEventListener("mousemove", (event) => {
            const rect = block.getBoundingClientRect();
            const mouseX = event.clientX;
            const mouseY = event.clientY;

            const dx = mouseX - (rect.left + rect.width / 2);
            const dy = mouseY - (rect.top + rect.height / 2);
            const distance = Math.sqrt(dx * dx + dy * dy);

            // Если курсор близко, убегаем
            if (distance < 100) {
                const moveX = -dx / distance * 50;
                const moveY = -dy / distance * 50;

                // Учитываем вектор движения курсора
                const velocityX = mouseX - lastMouseX;
                const velocityY = mouseY - lastMouseY;

                block.style.transform = `translate(${moveX + velocityX}px, ${moveY + velocityY}px)`;
            }

            lastMouseX = mouseX;
            lastMouseY = mouseY;
        });

        // Обработчик для возврата на место
        block.addEventListener("mouseleave", () => {
            block.style.transform = "translate(0, 0)";
        });
    });

    // Случайное движение блоков
    function randomMovement(block) {
        const sectionRect = imageSection.getBoundingClientRect();
        const blockWidth = block.offsetWidth;
        const blockHeight = block.offsetHeight;

        const moveX = getRandomNumber(-5, 5);
        const moveY = getRandomNumber(-5, 5);

        let currentX = parseFloat(block.style.left) + moveX;
        let currentY = parseFloat(block.style.top) + moveY;

        // Проверка границ
        if (currentX < -blockWidth / 4) currentX = -blockWidth / 4;
        if (currentX > sectionRect.width - blockWidth + blockWidth / 4) currentX = sectionRect.width - blockWidth + blockWidth / 4;
        if (currentY < -blockHeight / 4) currentY = -blockHeight / 4;
        if (currentY > sectionRect.height - blockHeight + blockHeight / 4) currentY = sectionRect.height - blockHeight + blockHeight / 4;

        block.style.left = `${currentX}px`;
        block.style.top = `${currentY}px`;
    }

    // Проверка столкновений и отталкивание
    function checkCollisions() {
        imageBlocks.forEach((block1, index) => {
            const rect1 = block1.getBoundingClientRect();
            imageBlocks.forEach((block2, index2) => {
                if (index !== index2) {
                    const rect2 = block2.getBoundingClientRect();
                    const overlapX = Math.max(0, Math.min(rect1.right, rect2.right) - Math.max(rect1.left, rect2.left));
                    const overlapY = Math.max(0, Math.min(rect1.bottom, rect2.bottom) - Math.max(rect1.top, rect2.top));
                    const overlapArea = overlapX * overlapY;
                    const blockArea = rect1.width * rect1.height;

                    if (overlapArea > blockArea / 4) {
                        const dx = (rect1.left + rect1.width / 2) - (rect2.left + rect2.width / 2);
                        const dy = (rect1.top + rect1.height / 2) - (rect2.top + rect2.height / 2);
                        const distance = Math.sqrt(dx * dx + dy * dy);

                        if (distance < rect1.width / 2 + rect2.width / 2) {
                            const angle = Math.atan2(dy, dx);
                            const speed = 5;
                            block1.style.left = `${parseFloat(block1.style.left) + Math.cos(angle) * speed}px`;
                            block1.style.top = `${parseFloat(block1.style.top) + Math.sin(angle) * speed}px`;
                        }
                    }
                }
            });
        });
    }

    function animateBlocks() {
        imageBlocks.forEach(block => {
            randomMovement(block);
        });
        checkCollisions();
        requestAnimationFrame(animateBlocks);
    }

    // Запускаем анимацию
    animateBlocks();
});
