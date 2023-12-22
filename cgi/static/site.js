function publishClick() {
    fetch("/product", {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${window.localStorage.getItem('token')}`
        },
        body: JSON.stringify({
            name: 'Коробка 10х10х10',
            price: 19.50,
            img_url: 'box2.jpg'
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
angular
    .module('app', [])
    .directive('products', function () {
        return {
            restrict: 'E',
            transclude: true,
            scope: {},
            controller: function ($scope, $http) {
                console.log('123')
                $scope.products = [];
                $http
                .get('/product')
                .then(r => {$scope.products = r.data.data
                console.log(r)});
            },
            templateUrl:'/static/tpl/product.html',
            replace: true
        };
    })
