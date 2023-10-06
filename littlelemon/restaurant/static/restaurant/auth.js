function setLoggedStatus(token) {
    logStatus = document.getElementById("log-status");
    if (!token){
        logStatus.innerHTML = "Not logged in<br/><span id='log-user'>(Anon)</span>";
        return;
    }

    const headers = {};
    headers['Authorization'] = `Token ${token}`;
    fetch('/auth/users/me/', {method: 'GET', headers: headers})
    .then(response => {
        response.json().then(data => {
            const username = data.username;
            const isStaff = data.is_staff;
            let innerHTML = `Logged in as<br/><span id='log-user'>${username} `;
    
            if (isStaff) {
                innerHTML += "(Staff)";
            } else {
                innerHTML += "(User)";
            }

            logStatus.innerHTML = innerHTML + "</span>";
        });

    })
    .catch(error => {
        console.error(error);
    });
}
setLoggedStatus(null);