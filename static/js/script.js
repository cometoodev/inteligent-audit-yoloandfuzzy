// static/js/script.js

document.addEventListener("DOMContentLoaded", () => {
    // 1. Efek Fade-In pada seluruh elemen kartu (glass-panel, glass-card, history-card)
    const glassPanels = document.querySelectorAll('.glass-panel, .glass-card, .history-card, .login-card');
    glassPanels.forEach((panel, index) => {
        panel.style.opacity = '0';
        panel.style.transform = 'translateY(20px)';
        setTimeout(() => {
            panel.style.transition = 'all 0.6s ease';
            panel.style.opacity = '1';
            panel.style.transform = 'translateY(0)';
        }, index * 100); // Muncul bergantian dengan jeda 100ms
    });

    // 2. Efek Ripple (Gelombang Air) pada Tombol
    const buttons = document.querySelectorAll('.btn-glass, .btn-custom, .btn-success');
    buttons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            let x = e.clientX - e.target.getBoundingClientRect().left;
            let y = e.clientY - e.target.getBoundingClientRect().top;
            let ripple = document.createElement('span');
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.style.position = 'absolute';
            ripple.style.background = 'rgba(255, 255, 255, 0.4)';
            ripple.style.borderRadius = '50%';
            ripple.style.transform = 'translate(-50%, -50%)';
            ripple.style.animation = 'ripple-anim 0.6s linear';
            
            // Pastikan tombol relative agar ripple tidak keluar batas
            if (window.getComputedStyle(this).position === 'static') {
                this.style.position = 'relative';
            }
            this.style.overflow = 'hidden';
            
            this.appendChild(ripple);
            setTimeout(() => { ripple.remove(); }, 600);
        });
    });
});

// Tambahkan keyframes ripple langsung via JS ke document head
const style = document.createElement('style');
style.innerHTML = `
    @keyframes ripple-anim {
        0% { width: 0; height: 0; opacity: 0.5; }
        100% { width: 400px; height: 400px; opacity: 0; }
    }
`;
document.head.appendChild(style);