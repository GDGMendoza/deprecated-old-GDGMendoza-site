var app = angular.module('gdgApp', ['restangular','ngRoute','ngAnimate','ngSanitize', 'ui.tinymce']);

////////////////////////////////////////////////// START ROUTING ///////////////////////////////////////////////////////

app.config(function(RestangularProvider, $routeProvider) {
    RestangularProvider.setBaseUrl('api');
    $routeProvider
    .when('/', {
        templateUrl:'homeView.html',
        controller:"HomeCtrl"
    })
    .when('/blog', {
        templateUrl: 'postListView.html',
        controller: "PostListCtrl",
        resolve: {
            data: function($q, dataService, Restangular){

                var defer = $q.defer();

                var basePosts = Restangular.oneUrl('post');//Hago que apunte a la url del post

                basePosts.get().then(function(response){

                    dataService.saveData("posts", response.items)

                    defer.resolve();

                });

                return defer.promise;

            }
        }
    })
    .when('/blog/:postid',{
        templateUrl: 'postView.html',
        controller: "PostCtrl",
        resolve: {
            data: function($q, $route, dataService, Restangular){
                var defer = $q.defer();

                var basePost = Restangular.oneUrl('get/post');

                basePost.getList(false,{id: $route.current.params.postid}).then(function(response){

                    response.comments_all = JSON.parse(response.comments_all);

                    defer.resolve(response)

                });

                return defer.promise;
            }
        }
    })
    .when('/events',{
        templateUrl: 'eventsView.html',
        controller: "EventsCtrl"
    })
    .when('/who-we-are',{
        templateUrl: 'whoWeAre.html',
        controller: "WWACtrl",
        resolve: {
            data: function($q, dataService, Restangular){
                var defer = $q.defer();

                var baseContributor = Restangular.oneUrl('contributor');

                baseContributor.get().then(function(response){

                    dataService.saveData("contributors", response.items);

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
app.service('dataService', function(){

    this.data = {
        posts: []
    };

    this.saveData = function(controller, datos) {
        this.data[controller] = datos;
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
    //$scope.configTinymce = {language: 'es', plugins:'image link', resize: false, preview_styles: false, statusbar: false, menubar: false, toolbar: 'bold italic underline strikethrough alignleft aligncenter alignright alignjustify bullist numlist removeformat link image', height: 200};
    $scope.escribir = {
        contenido: ''
    };
    $scope.subir = function(){//Sube un comentario
        if($scope.escribir.contenido.trim() == 0) return;
        var defer = $q.defer();

        gapi.client.gdgmendoza.comment.insert({'post_id': $scope.post.id, 'content': $scope.escribir.contenido}).execute(function(response) {

            //Hay que activar la autentificación para que funcione.. al parecer..

            defer.resolve();

        });

        return defer.promise;
    };
    //return $scope.PostCtrl = this;
});

app.controller('LoginCtrl', function($scope){
    $scope.login = function(){
        console.log('Loguear')

    /*

        // Para probarlo creo que hay que registrar la App https://cloud.google.com/console

        gapi.auth.authorize({client_id: 'gdgmendoza.apps.googleusercontent.com',
            scope: 'https://www.googleapis.com/auth/userinfo.email', immediate: 'false',
            response_type: 'token id_token'},
        userAuthed);

        function userAuthed() {
          var request =
              gapi.client.oauth2.userinfo.get().execute(function(resp) {
             console.log(resp)
            if (!resp.code) {
              var token = gapi.auth.getToken();
              token.access_token = token.id_token;
              gapi.auth.setToken(token);
              // User is signed in, call my Endpoint
            }
          });
        }
    */
    }
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