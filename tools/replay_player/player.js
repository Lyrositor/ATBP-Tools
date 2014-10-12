/**
 * ATBP Tools - Replay Player
 * Manages the replay data.
 */

var playerApp = angular.module("playerApp", ["angularFileUpload"])
    .filter("numberPad", function () {
        return function (n, len) {
            var num = parseInt(n, 10);
            len = parseInt(len, 10);
            if (isNaN(num) || isNaN(len))
                return n;
            num = "" + num;
            while (num.length < len)
                num = '0'+num;
            return num;
        };
    });

playerApp.controller("PlayerCtrl", function ($scope, $timeout) {

    $scope.replay = null;

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