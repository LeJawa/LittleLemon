var user_authtoken = null;      

function add_response_to_output(response) {
    console.log(response.status);
    const responsediv = document.createElement('div')
    responsediv.classList.add('response');
    const status = document.createElement('span');
    status.classList.add('status');

    if (response.status.toString().startsWith('4')){
        status.classList.add('status-red');
    } else if (response.status.toString().startsWith('5')){
        status.classList.add('status-blue');
    } else if (response.status.toString().startsWith('2')){
        status.classList.add('status-green');
    }
    const output = document.createElement('span');
    output.classList.add('data');
    status.innerHTML = response.status + " " + response.statusText;
    output.innerHTML = JSON.stringify(response.data, null, 1);

    document.getElementById("output-box").children[1].after(responsediv);
    responsediv.appendChild(status);
    responsediv.appendChild(output);
    document.getElementById('clear-output').removeAttribute('hidden');
    document.getElementById('placeholder-output').setAttribute('hidden', '');
}

function rightFetch(path, method, formData){
    const headers = {};
    if (user_authtoken) {
        headers['Authorization'] = `Token ${user_authtoken}`;
    }

    if (method == "GET") {
        return fetch(path, {method: method, headers: headers})
    }
    else if (method == "POST"){
        return fetch(path, {
        method: method,
        headers: headers,
        body: formData
        })
    }
}

function isSuccesful(response) {
    return response.status.toString().startsWith('2');
}

const FormAction = {
    LOGIN: 'login',
    LOGOUT: 'logout',
    STANDARD: 'standard'
}

function linkFormToOutput(formId, path, method, formAction = FormAction.STANDARD) {
    const form = document.getElementById(formId);

    form.addEventListener('submit', (event) => {
        event.preventDefault(); // The default action is to go to the page in path, but we want to stay on the same page

        const formData = new FormData(form);

        rightFetch(path, method, formData) // This function wraps fetch to be able to accept different methods using the same syntax
        .then(response => { // This step is necessary to inject the status code into the response object
            const status = response.status;
            const statusText = response.statusText;

            if (response.headers.get('Content-Length') == 0)
            {
                return { status, statusText, data: null };
            }
            return response.json().then(data => ({ status, statusText, data })); // I don't really understand this but it works


        })
        .then(response => {
            add_response_to_output(response);
            
            if (isSuccesful(response)) {
                if (formAction == FormAction.LOGIN) { // Saves the user_authtoken if a login form was used
                    user_authtoken = response.data.auth_token;
                }
                else if (formAction == FormAction.LOGOUT) { // Deletes the user_authtoken if a logout form was used
                    user_authtoken = null;
                }
            }
        })
        .catch(error => {
            console.error(error);
        });
    })
}