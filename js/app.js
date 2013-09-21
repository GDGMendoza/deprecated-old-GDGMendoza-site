var app = angular.module('gdgApp', ['ngRoute','ngAnimate','ngSanitize','ui.tinymce']);

////////////////////////////////////////////////// START ROUTING ///////////////////////////////////////////////////////
app.config(function($routeProvider, $httpProvider) {
    $routeProvider.when('/', {
        templateUrl:'homeView.html',
        controller:"HomeCtrl"
    })
        .when('/blog', {
            templateUrl: 'postListView.html',
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
            templateUrl: 'postView.html',
            controller: "PostCtrl",
            resolve: {
                data: function($q, $route, $rootScope, $timeout, dataService){
                    var defer = $q.defer();
                    var postId = $route.current.params.postid;
                    /*var post = {};
                    //eval("dataService.data.posts[sd].")
                    for(i=0; i<dataService.data.posts.length; i++){
                        if(dataService.data.posts[i].postid === $route.current.params.postid){
                            post = dataService.data.posts[i];
                        }
                    }
                    if(typeof post.postid != "undefined"){
                        defer.resolve(post);
                    } else {*/
                    dataService.getData('blog','getPost',postId).then(function(response){
                        console.log(response.data)
                        defer.resolve(response.data);

                        //Una vez que muestra el post, quiero que traiga los comentarios
                        var agregarComentarios = function(comentariosNuevos){
                            angular.forEach(comentariosNuevos, function(value, key){
                                response.data.comments.push(value);//Agrego los resultados que hayan
                            });
                        };
                        var traerMasComentarios = function(longitud){

                            var fechaUltimoComentario = longitud > 0 ? response.data.comments[longitud - 1].date : 'none';

                            console.log(postId)
                            console.log(fechaUltimoComentario)

                            dataService.getCristianData('get', 'comments', {'id': postId, 'date': fechaUltimoComentario}).then(function(result){
                                console.log(result.data)
                                if(result.data != 'empty'){
                                    agregarComentarios(result.data);
                                }
                            });
                        };
                        var timeout = function(){
                            $timeout(function(){
                            var longitudComentarios = response.data.comments.length;
                            traerMasComentarios(longitudComentarios);
                            timeout();
                            },10000);//Cada 10 segundos
                        };
                        timeout();//Llamo por primera vez a timeout
                        var mirarCambio = $rootScope.$on('$routeChangeStart', function(next, current){//Al comenzar un cambio de ruta
                            timeout = function(){};//Vacío la función por lo que no se volvera a llamar
                            mirarCambio();//Al llamar a mirarCambio, se desactiva el evento.
                        });

                    });
                    //}
                    return defer.promise;
                }
            }
        }).when('/events',{
            templateUrl: 'eventsView.html',
            controller: "EventsCtrl"
        }).when('/debug',{
            templateUrl: 'debug.html',
            controller: "DebugCtrl"
        }).when('/who-we-are',{
            templateUrl: 'whoWeAre.html',
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
app.service('dataService', function($http, $location){
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

    this.getCristianData = function(controller, method, data, q, redireccionar, callback){
        return $http.post(controller + "/" + method,{
            'data': data
        },{cache:true}).error(function(){
                if(q){
                    q.reject();//Si hay error, rechazo lo que tenía que hacer q. Así continua.
                }
                if(redireccionar){
                    $location.path(redireccionar)//Si hay que redireccionar en caso de error, lo hago
                }
                if(callback){
                    callback();
                }
                return
        });
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
    $scope.getPostTemplate = function(index){
        if(index%4==0){
            return 'postPreviewBigComponent.html';
        }else{
            return 'postPreviewTinyComponent.html';
        }
    }
});

app.controller('WWACtrl',function($scope,dataService){
    $scope.contributorList = dataService.data.contributors;
})

app.controller('PostCtrl', function($scope, $routeParams, $q, data, dataService){
    $scope.post = data;
    $scope.configTinymce = {language: 'es', plugins:'image link', resize: false, preview_styles: false, statusbar: false, menubar: false, toolbar: 'bold italic underline strikethrough alignleft aligncenter alignright alignjustify bullist numlist removeformat link image', height: 200};
    $scope.escribir = {
        contenido: ''
    };
    $scope.palabra = 'Send comment';
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