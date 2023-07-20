document.addEventListener('DOMContentLoaded', function(){
    document.querySelector('#submitBtn').addEventListener('click', () => submitForm());
});

function submitForm() {
        $('#chat-form').submit();
}