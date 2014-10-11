/**
 * ATBP Tools - Replay Player
 * Manages the replay data.
 */

var playerApp = angular.module("playerApp", ["angularFileUpload"]);

playerApp.controller("PlayerCtrl", function ($scope, $timeout) {

    $scope.replay = null;

    // "Fix" for the Math.ceil function.
    // Allows for rounding up to the nearest real number, as determined by the
    // precision.
    $scope.ceil = function(number, precision) {
        precision = Math.abs(parseInt(precision)) || 0;
        var coefficient = Math.pow(10, precision);
        return Math.ceil(number*coefficient)/coefficient;
    }
    
    $scope.loadReplay = function($files) {
        var file = $files[0];
        var reader = new FileReader();
        reader.onload = function openReplay(e) {
            $scope.$apply(function() {
                var map = new MapCanvas("player");
                $scope.replay = new Replay(reader.result, map, $timeout);
                $scope.replay.play();
            });
        }

        reader.readAsText(file);
    }
});