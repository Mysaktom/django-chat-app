document.addEventListener('DOMContentLoaded', () => {
    // Získáme jméno aktuálního uživatele z HTML (přidáme ho v dalším kroku)
    const currentUsername = JSON.parse(document.getElementById('current-user-json').textContent);
    
    // Vytvoříme unikátní klíče pro každého uživatele
    const volumeKey = `notification_volume_${currentUsername}`;
    const delayKey = `notification_delay_${currentUsername}`;

    const volumeSlider = document.getElementById('volume-slider');
    const volumeValue = document.getElementById('volume-value');
    const delayInput = document.getElementById('delay-input');
    const testBtn = document.getElementById('test-notification-btn');
    const notificationSound = document.getElementById('notification-sound-src');

    // Načítáme a ukládáme hodnoty pod unikátními klíči
    volumeSlider.value = localStorage.getItem(volumeKey) || 1;
    delayInput.value = localStorage.getItem(delayKey) || 5;
    volumeValue.textContent = `${Math.round(volumeSlider.value * 100)}%`;

    volumeSlider.addEventListener('input', () => {
        const volume = volumeSlider.value;
        localStorage.setItem(volumeKey, volume);
        volumeValue.textContent = `${Math.round(volume * 100)}%`;
    });

    delayInput.addEventListener('input', () => {
        localStorage.setItem(delayKey, delayInput.value);
    });

    testBtn.addEventListener('click', () => {
        notificationSound.volume = localStorage.getItem(volumeKey) || 1;
        notificationSound.play();
    });
});