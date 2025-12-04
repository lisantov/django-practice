const imageContainers = document.querySelectorAll('.image-container');

imageContainers.forEach(container => {
    const afterContainer = container.querySelector('.after-image-container');
    const imageSlideHandle = container.querySelector('.image-slide');

    if (afterContainer && imageSlideHandle) {
        const containerRect = container.getBoundingClientRect();
        let isDragging = false;

        const mouseMoveHandler = (e) => {
            const newCoord = Math.min(Math.max(containerRect.left + 10, e.clientX), containerRect.right - 10);
            afterContainer.style.left = (newCoord - containerRect.left) + 'px';
        }

        imageSlideHandle.addEventListener('mousedown', (e) => {
            e.preventDefault();
            if (!isDragging) {
                isDragging = true;

                document.addEventListener('mousemove', mouseMoveHandler)
            }
        })

        document.addEventListener('mouseup', () => {
            if (isDragging)
                document.removeEventListener('mousemove', mouseMoveHandler)
                isDragging = false
        })
    }
})