// chat/static/chat/notification_settings.js
document.addEventListener('DOMContentLoaded', () => {
    const volumeSlider = document.getElementById('volume-slider');
    const volumeValue = document.getElementById('volume-value');
    const delayInput = document.getElementById('delay-input');
    const testBtn = document.getElementById('test-notification-btn');
    
    // Načtení zvuku
    const notificationSound = new Audio(document.getElementById('notification-sound-src').getAttribute('src'));

    // Načtení uložených hodnot, nebo nastavení výchozích
    volumeSlider.value = localStorage.getItem('notification_volume') || 1;
    delayInput.value = localStorage.getItem('notification_delay') || 5;
    volumeValue.textContent = `${Math.round(volumeSlider.value * 100)}%`;

    // Uložení hlasitosti při změně
    volumeSlider.addEventListener('input', () => {
        const volume = volumeSlider.value;
        localStorage.setItem('notification_volume', volume);
        volumeValue.textContent = `${Math.round(volume * 100)}%`;
    });

    // Uložení prodlevy při změně
    delayInput.addEventListener('input', () => {
        localStorage.setItem('notification_delay', delayInput.value);
    });

    // Testovací tlačítko
    testBtn.addEventListener('click', () => {
        notificationSound.volume = localStorage.getItem('notification_volume') || 1;
        notificationSound.play();
    });
});