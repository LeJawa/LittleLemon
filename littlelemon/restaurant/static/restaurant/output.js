const clearOutputButton = document.getElementById('clear-output');

clearOutputButton.addEventListener('click', () => {
    const outputArticle = document.getElementById('output-box');
    const responseElements = outputArticle.querySelectorAll('.response');  

    responseElements.forEach((response) => {
        response.remove();
    })

    clearOutputButton.setAttribute('hidden', '');
    document.getElementById('placeholder-output').removeAttribute('hidden');
})