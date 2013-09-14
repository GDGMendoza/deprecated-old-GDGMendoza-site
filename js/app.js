var app = angular.module('gdgApp', ['ngRoute','ngAnimate','ngSanitize','ui.tinymce']);

////////////////////////////////////////////////// START ROUTING ///////////////////////////////////////////////////////
app.config(function($routeProvider, $httpProvider) {
    $routeProvider.when('/', {
        templateUrl:'views/homeView.html',
        controller:"HomeCtrl"
    })
        .when('/blog', {
            templateUrl: 'views/postListView.html',
            controller: "PostListCtrl",
            resolve: {
                data: function($q, dataService){
                    var defer = $q.defer();
                    dataService.getData('blog','getPostList','').then(function(response){
                        dataService.saveData("posts", response.data);
                        defer.resolve();
                    });
                    return defer.promise;
                }
            }
        }).when('/blog/:postid',{
            templateUrl: 'views/postView.html',
            controller: "PostCtrl",
            resolve: {
                data: function($q, $route, dataService){
                    var defer = $q.defer();
                    var post = {};
                    for(i=0; i<dataService.data.posts.length; i++){
                        if(dataService.data.posts[i].postid === $route.current.params.postid){
                            post = dataService.data.posts[i];
                        }
                    }
                    if(typeof post.postid != "undefined"){
                        defer.resolve(post);
                    } else {
                        dataService.getData('blog','getPost',$route.current.params.postid).then(function(response){
                            console.log(response.data)
                            defer.resolve(response.data);
                        });
                    }
                    return defer.promise;
                }
            }
        }).when('/blog/:filter/:query',{
            templateUrl: 'views/postListView.html',
            controller: "SearchPostCtrl",
            resolve: {
                data: function($q, dataService){
                    var defer = $q.defer();
                    dataService.getData('blog','getPostList','-1').then(function(response){
                        dataService.saveData("filter", response.data);
                        defer.resolve();
                    });
                    return defer.promise;
                }
            }
        }).when('/events',{
            templateUrl: 'views/eventsView.html',
            controller: "EventsCtrl"
        }).when('/debug',{
            templateUrl: 'views/debug.html',
            controller: "DebugCtrl"
        }).when('/who-we-are',{
            templateUrl: 'views/whoWeAre.html',
            controller: "WWACtrl",
            resolve: {
                data: function($q, dataService){
                    var defer = $q.defer();
                    dataService.getData('contributor','getContributorList','-1').then(function(response){
                        dataService.saveData("contributors", response.data);
                        defer.resolve();
                    });
                    return defer.promise;
                }
            }
        })
        .otherwise({redirectTo:'/'});

});
////////////////////////////////////////////////// END ROUTING /////////////////////////////////////////////////////////

////////////////////////////////////////////////// START SERVICES //////////////////////////////////////////////////////
app.service('dataService', function($http){
    this.data = {
        posts: []
    };

    this.saveData = function(controller, datos) {
        this.data[controller] = datos;
    }

    this.getData = function(controller, method, id){
        return $http.post(controller + "/" + method,{
            'id': id
        },{cache:true});
    }

    this.getCristianData = function(controller, method, data){
        return $http.post(controller + "/" + method,{
            'data': data
        },{cache:true});
    }
});
////////////////////////////////////////////////// END SERVICES ////////////////////////////////////////////////////////

////////////////////////////////////////////////// STAR CONTROLLERS ////////////////////////////////////////////////////
app.controller("HomeCtrl", function($scope){
});

app.controller('EventsCtrl', function($scope){
});

app.controller('PostListCtrl', function($scope, dataService){
    $scope.postList = dataService.data.posts;
});

app.controller('WWACtrl',function($scope,dataService){
    $scope.contributorList = dataService.data.contributors;
})

app.controller('SearchPostCtrl', function($scope, $routeParams, $location, dataService){

    $scope.postList = dataService.data.filter;
    $scope.filterBy = {date: "", author: "", tags: ""};
    $scope.filter = $routeParams.filter;
    $scope.query = $routeParams.query;

    $scope.activeSearch = true;

    switch($scope.filter){
        case "date":
            if ($scope.filterBy.date != $scope.query) {
                $scope.filterBy.date = $scope.query;
                $scope.filterBy.tags = "";
                $scope.filterBy.author = "";
            } else{
                $scope.filterBy.date = "";
            };
            break;
        case "author":
            if ($scope.filterBy.author != $scope.query) {
                $scope.filterBy.author = $scope.query;
                $scope.filterBy.tags = "";
                $scope.filterBy.date = "";
            } else{
                $scope.filterBy.author = "";
            };
            break;
        case "tag":
            if ($scope.filterBy.tag != $scope.query) {
                $scope.filterBy.tags = $scope.query;
                $scope.filterBy.author = "";
                $scope.filterBy.date = "";
            } else{
                $scope.filterBy.tags = "";
            };
            break;
        default:
            $location.path("/blog");
            break;
    }
});

app.controller('PostCtrl', function($scope, $routeParams, $q, data, dataService){
    $scope.post = data;
    $scope.configTinymce = {language: 'es', plugins:'image link', resize: false, preview_styles: false, statusbar: false, menubar: false, toolbar: 'bold italic underline strikethrough alignleft aligncenter alignright alignjustify bullist numlist removeformat link image', height: 200};
    $scope.escribir = {
        contenido: ''
    };
    $scope.palabra = 'Comentar';
    $scope.subir = function(){//Sube un comentario
        if($scope.escribir.contenido.trim() == 0) return;
        var defer = $q.defer();
        dataService.getCristianData('put', 'comment', {'id': $scope.post.id, 'content': $scope.escribir.contenido, 'author': 'darkcause'/*dataService.data.login.usuario*/}).then(function(response){
            console.log(response.data)
            $scope.escribir.contenido = '';
            defer.resolve();
        });
        return defer.promise;
    };
    //return $scope.PostCtrl = this;
});

app.controller('DebugCtrl', function($scope,$http){
    $scope.pegar = function(){
        $http.post($scope.url, JSON.parse($scope.params)).then(function(response){
            $scope.response = response.data;
        });
    }
    //tenemos que agregar un campo único a todas las entidades para hacer consultas y convertir los id en autogenerados
    //para que no nos explote en la cara cuando crezca el tamaño del sitio :)
});
////////////////////////////////////////////////// END CONTROLLERS /////////////////////////////////////////////////////

////////////////////////////////////////////////// START DIRECTIVES ////////////////////////////////////////////////////
////////////////////////////////////////////////// START DOM ELEMENTS //////////////////////////////////////////////////
app.directive('iswhoweare',function($location){
    return {
        restrict: "C",
        link: function(scope,element,attrs){
            if($location.url()=='/who-we-are'){
                element.css({'max-width':'100%','padding-top':'0'});
            }else{
                element.css({'max-width':'940px','padding-top':'10px'});
            }
        }
    }
})
app.directive('contributor', function(){
    return {
        restrict: "E",
        scope:{
            author: '@',
            photo: '@',
            description: '@',
            gplus: '@',
            fb: '@',
            tw: '@'
        },
        templateUrl: 'components/contributorComponent.html'
    };
});

app.directive('postpreview', function(){
    return {
        restrict: "E",
        scope:{
            index: '@',
            post: '='
        },
        templateUrl:'components/postPreviewBigComponent.html'
    };
});

app.directive('post', function(){
    return {
        restrict: "E",
        scope:{
            title: '@',
            author: '@',
            content: '@',
            cover: '@',
            date: '@',
            tags: '='
        },
        templateUrl: 'components/postComponent.html'
    };
});

app.directive('commentsForm',function () {
    return {
        restrict: 'E',
        //scope: {},
        templateUrl: 'components/commentsFormComponent.html'
    }
});

app.directive('comment',function(){
    return {
        restrict: 'E',
        //scope: {},
        templateUrl: '  components/commentComponent.html'
    }
});

app.directive('paragraph', function(){
    return{
        restrict: 'E',
        //controller: 'CtrlSanitize',
        scope: {
            text: '='
        },
        template: '<div class="container-fluid"><p ng-bind-html="text"><p/></div>'
    }
});
////////////////////////////////////////////////// END DOM ELEMENTS ////////////////////////////////////////////////////
////////////////////////////////////////////////// END DIRECTIVES //////////////////////////////////////////////////////