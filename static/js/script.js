// /static/js/script.js
document.addEventListener('DOMContentLoaded', function () {
    console.log('JavaScript is connected and working!');
});
function showSpinner() {
    document.getElementById('spinner').style.display = 'block';
}
function toggleText(elementId, button) {
    const element = document.getElementById(elementId);
    if (element.classList.contains('text-truncate')) {
        element.classList.remove('text-truncate');
        element.style.maxHeight = 'none';
        button.textContent = 'Read Less';
    } else {
        element.classList.add('text-truncate');
        element.style.maxHeight = '80px';
        button.textContent = 'Read More';
    }
}