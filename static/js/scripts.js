const textarea = document.getElementById('question');
textarea.addEventListener('keydown', function(event) {
    if (event.keyCode === 13 && !event.shiftKey) {
        event.preventDefault();
        showSpinner();
        document.getElementById('ask').submit();
    }
});

function showSpinner() {
    var overlay = document.getElementById('overlay');
    overlay.classList.add('show');
};
