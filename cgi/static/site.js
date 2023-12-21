function publishClick() {
    fetch("/product", {
        method:'PUT',
        headers: {
            'Authorization': `Bearer ${window.localStorage.getItem('token')}`
        },
        body: JSON.stringify({
            name:'Коробка 10х10х10',
            price: 19.50
        })
    })
        .then(r => r.json())
        .then(console.log);
}

function authClick() {
    // fetch("/auth?login=user&password=1234") //! переводимо на схему Basic
    const cred = btoa('user:1234');
    fetch("/auth", {
        headers: {
            'Authorization': `Basic ${cred}`
        }
    })
        .then(r => r.json())
        .then(j => {
            window.localStorage.setItem('token', j.token)
        });
}

function infoClick() {
    const authToken = window.localStorage.getItem('token')
    console.log('token: ', authToken);
    if (authToken) {
        fetch("/auth", {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        })
            .then(r => r.json())
            .then(console.log);
    }
}