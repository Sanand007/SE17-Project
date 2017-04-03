/*global angular*/
/*global scope*/
var app = angular.module("reviewApp", ['ui.bootstrap']);

app.controller("reviewCtrl", ['$scope','$http', function($scope, $http) {
    
    $scope.analysis="Sentiment Analysis of Amazon Reviews"
    
    //Data in form.
    $scope.data = {
        'review': $scope.review
    };
    
    
    //Submit the form.
    $scope.submitForm = function() {
    var endpoint = "https://gateway-a.watsonplatform.net/calls/text/TextGetTextSentiment?text="+ $scope.data.review +"&apikey=a30fe777004c3ebcf36730562690fdbddd72717c&outputMode=json";
    $http.post(endpoint).then(function(res) {
            $scope.result = res.data; //data that is sent back.
            var stuff = res.data;
            document.getElementById("Score").textContent = stuff.docSentiment.score;
            document.getElementById("sentiment").textContent = stuff.docSentiment.type;
            document.getElementById("stars").textContent = "";
            console.log($scope.result);
        }).catch(function(error, res) {
            console.log("Error:", error, res);
        });
    }
    
}]);

function getText(url){
    // read text from URL location
    var request = new XMLHttpRequest();
    request.open('GET', url, true);
    request.send(null);
    request.onreadystatechange = function () {
        if (request.readyState === 4 && request.status === 200) {
            var type = request.getResponseHeader('Content-Type');
            if (type.indexOf("text") !== 1) {
                return request.responseText;
            } else {
            	return "error";
            }
        }
    }
}

//function getText(url){
	    // read text from URL location
//	    var request = new XMLHttpRequest();
//	    request.open('GET', url, false);
//	    request.send(null);
//	    request.onreadystatechange = function () {
//	    	console.log("working");
//	        if (request.readyState === 4 && request.status === 200) {
//	            var type = request.getResponseHeader('Content-Type');
//	            if (type.indexOf("text") !== 1) {
//	                return request.responseText;
//	            } else {
//	            	return "error";
//	            }
//	        } else {
//	        	return "error";
//	        }
//	    }
//}
app.controller('fileCtrl', function($scope, $http) {
    
    $scope.data = {
        'url': $scope.url
    }

    //Submit the form.
    $scope.submitUrl = function() {
        var endpoint = "https://gateway-a.watsonplatform.net/calls/url/URLGetTextSentiment?url=" + $scope.data.url + "&apikey=a30fe777004c3ebcf36730562690fdbddd72717c&outputMode=json";
        $http.post(endpoint).then(function(res) {
        	//var outer_text = getText($scope.data.url);
        	//alert(outer_text);
            //outer_text = outer_text.split('\n');
            //alert(outer_text[0]);
            $scope.result = res.data; //data that is sent back.
            var stuff = res.data;
            var stars = ((5 - 0) / (1 - (-1))) * (stuff.docSentiment.score - 1) + 5
            document.getElementById("Score").textContent = stuff.docSentiment.score;
            document.getElementById("sentiment").textContent = stuff.docSentiment.type;
            document.getElementById("stars").textContent = stars;
            console.log($scope.result);
        }).catch(function(error, res) {
            console.log("Error:", error, res);
        });
    }


    // $scope.showContent = function($fileContent) {
    //     $scope.content = $fileContent;
    //     var data = $scope.content;
    //     var endpoint = "https://gateway-a.watsonplatform.net/calls/text/TextGetTextSentiment?text=" + data + "&apikey=a30fe777004c3ebcf36730562690fdbddd72717c&outputMode=json";
    //     $http.post(endpoint).then(function(res) {
    //         $scope.score = res.data; //data that is sent back.
    //         console.log($scope.score);
    //     }).catch(function(error, res) {
    //         console.log("Error:", error, res);
    //     });
    // }
});
