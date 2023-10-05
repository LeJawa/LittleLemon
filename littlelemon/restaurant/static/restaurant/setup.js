
// Add numbering to form headers
const form_headers = document.querySelectorAll('.form-header');

form_headers.forEach((header, index) => {
const numbering = document.createElement('p');
numbering.classList.add('numbering');
numbering.innerHTML = `${index + 1}.`;

header.insertBefore(numbering, header.firstChild);
})