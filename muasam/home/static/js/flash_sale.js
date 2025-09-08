document.addEventListener('DOMContentLoaded', function() {
    // Lấy tất cả bộ đếm ngược
    const countdownElements = document.querySelectorAll('.flash-sale-countdown');
    
    // Cập nhật đếm ngược mỗi giây
    function updateCountdowns() {
        countdownElements.forEach(element => {
            const endTime = new Date(element.dataset.endTime).getTime();
            const now = new Date().getTime();
            const timeRemaining = endTime - now;
            
            if (timeRemaining <= 0) {
                element.innerHTML = 'Flash Sale đã kết thúc!';
                return;
            }
            
            const hours = Math.floor((timeRemaining % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((timeRemaining % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((timeRemaining % (1000 * 60)) / 1000);
            
            element.querySelector('.countdown-hours').textContent = hours.toString().padStart(2, '0');
            element.querySelector('.countdown-minutes').textContent = minutes.toString().padStart(2, '0');
            element.querySelector('.countdown-seconds').textContent = seconds.toString().padStart(2, '0');
        });
    }
    
    // Cập nhật đếm ngược ngay lập tức và sau đó mỗi giây
    updateCountdowns();
    setInterval(updateCountdowns, 1000);
    
    // Xử lý trượt (slide) của carousel Flash Sale
    const prevButton = document.querySelector('.flash-sale-prev');
    const nextButton = document.querySelector('.flash-sale-next');
    const slideContainer = document.querySelector('.flash-sale-items');
    
    if (prevButton && nextButton && slideContainer) {
        const slideWidth = slideContainer.querySelector('.flash-sale-item').offsetWidth + 30; // 30 là margin
        const slidesCount = slideContainer.querySelectorAll('.flash-sale-item').length;
        const containerWidth = slideContainer.offsetWidth;
        const maxScroll = slidesCount * slideWidth - containerWidth;
        
        let currentScroll = 0;
        
        nextButton.addEventListener('click', function() {
            if (currentScroll < maxScroll) {
                currentScroll += slideWidth;
                if (currentScroll > maxScroll) currentScroll = maxScroll;
                slideContainer.scrollTo({
                    left: currentScroll,
                    behavior: 'smooth'
                });
            }
        });
        
        prevButton.addEventListener('click', function() {
            if (currentScroll > 0) {
                currentScroll -= slideWidth;
                if (currentScroll < 0) currentScroll = 0;
                slideContainer.scrollTo({
                    left: currentScroll,
                    behavior: 'smooth'
                });
            }
        });
    }
});
