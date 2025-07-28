// JavaScript cho chức năng thanh toán QR
class QRPayment {
    constructor(orderId) {
        this.orderId = orderId;
        this.checkInterval = null;
        this.countdownInterval = null;
        this.timeLeft = 5;
    }

    init() {
        this.startCountdown();
        this.bindEvents();
    }

    startCountdown() {
        const self = this;
        this.countdownInterval = setInterval(function() {
            self.timeLeft--;
            const timerElement = document.getElementById('timer');
            if (timerElement) {
                timerElement.textContent = self.timeLeft;
            }
            
            if (self.timeLeft <= 0) {
                clearInterval(self.countdownInterval);
                self.checkPaymentStatus();
                self.timeLeft = 5;
                self.startCountdown();
            }
        }, 1000);
    }

    async checkPaymentStatus() {
        try {
            const response = await fetch(`/check-payment-status/${this.orderId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCsrfToken()
                }
            });

            const data = await response.json();
            
            if (data.status === 'paid') {
                this.handlePaymentSuccess();
            } else if (data.status === 'error') {
                console.error('Lỗi:', data.message);
            }
        } catch (error) {
            console.error('Lỗi khi kiểm tra trạng thái thanh toán:', error);
        }
    }

    handlePaymentSuccess() {
        clearInterval(this.countdownInterval);
        
        const statusElement = document.getElementById('payment-status');
        if (statusElement) {
            statusElement.innerHTML = `
                <div class="status-paid">
                    <i class="fas fa-check-circle fa-2x"></i>
                    <h5>Thanh toán thành công!</h5>
                    <p>Đơn hàng đã được xác nhận</p>
                </div>
            `;
        }

        const checkButton = document.getElementById('check-status-btn');
        if (checkButton) {
            checkButton.style.display = 'none';
        }

        // Chuyển hướng sau 3 giây
        setTimeout(() => {
            window.location.href = `/payment-success/${this.orderId}/`;
        }, 3000);
    }

    bindEvents() {
        const checkButton = document.getElementById('check-status-btn');
        if (checkButton) {
            checkButton.addEventListener('click', () => {
                this.checkPaymentStatus();
            });
        }
    }

    getCsrfToken() {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
        return csrfToken ? csrfToken.value : '';
    }
}

// Hàm copy to clipboard
function copyToClipboard(elementId) {
    const element = document.getElementById(elementId);
    const text = element.textContent || element.innerText;
    
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(function() {
            showCopySuccess(element);
        }).catch(function(err) {
            console.error('Không thể copy: ', err);
            fallbackCopyTextToClipboard(text, element);
        });
    } else {
        fallbackCopyTextToClipboard(text, element);
    }
}

function fallbackCopyTextToClipboard(text, element) {
    const textArea = document.createElement("textarea");
    textArea.value = text;
    
    textArea.style.top = "0";
    textArea.style.left = "0";
    textArea.style.position = "fixed";

    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();

    try {
        const successful = document.execCommand('copy');
        if (successful) {
            showCopySuccess(element);
        }
    } catch (err) {
        console.error('Fallback: Không thể copy', err);
    }

    document.body.removeChild(textArea);
}

function showCopySuccess(element) {
    const originalText = element.innerHTML;
    element.innerHTML = '<i class="fas fa-check text-success"></i> Đã copy';
    setTimeout(function() {
        element.innerHTML = originalText;
    }, 2000);
}
