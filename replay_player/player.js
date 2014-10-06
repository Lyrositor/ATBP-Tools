/**
 * ATBP Tools - Replay Player
 * Manages the replay data.
 */
 
var playerApp = angular.module("playerApp", []);

playerApp.controller("PlayerCtrl", function ($scope, $timeout) {

$scope.BACKPACKS = {
    belt_bella_noche: "Bella Noche's Knapsack",
    belt_billys_bag: "Billy's Bag",
    belt_bindle_of_bravery: "Bindle of Bravery",
    belt_candy_monarch: "Candy Monarch Regalia",
    belt_champions: "Champion's Backpack",
    belt_enchanters: "Enchanted Ensemble",
    belt_fridjitsu: "Fridjitsu: Ninjas of the Ice",
    belt_hewers_haversack: "Hewer's Haversack",
    belt_ice_monarch: "Ice Monarch Regalia",
    belt_meta_science: "Meta-Science Sack",
    belt_sorcerous_satchel: "Sorcerous Satchel",
    belt_techno_tank: "Techno-Tank",
    belt_ultimate_wizard: "Nearly Ultimate Wizard Wear",
    belt_vampire_rocker: "Vampire Rocker Gear"
};

CHAMPIONS = {  // TODO: Update these stats.
    bmo: {
        startHealth: 407
    },
    finn: {
        startHealth: 550
    },
    fionna: {
        startHealth: 550
    },
    flame: {
        startHealth: 385
    },
    gunter: {
        startHealth: 350
    },
    iceking: {
        startHealth: 385
    },
    jake: {
        startHealth: 800
    },
    lemongrab: {
        startHealth: 540
    },
    lich: {
        startHealth: 400
    },
    lsp: {
        startHealth: 385
    },
    magicman: {
        startHealth: 390
    },
    marceline: {
        startHealth: 435
    },
    peppermintbutler: {
        startHealth: 450
    },
    princessbubblegum: {
        startHealth: 350
    },
    rattleballs: {
        startHealth: 460
    }
}

$scope.actions = [];
$scope.arena = null;
$scope.players = null;
$scope.teamScores = {"teamA": 0, "teamB": 0};
$scope.time = 0.0;

var actors = {};

// Create the cross-platform version of requestAnimFrame.
window.requestAnimFrame = (function(callback) {
    return window.requestAnimationFrame || window.webkitRequestAnimationFrame || window.mozRequestAnimationFrame || window.oRequestAnimationFrame || window.msRequestAnimationFrame ||
        function(callback) {
            window.setTimeout(callback, 1000 / 60);
        };
})();

function getPlayer(id) {
    var id = parseInt(id);
    player = null;
    for (var team in $scope.players) {
        if (id in $scope.players[team])
            player = $scope.players[team][id];
    }
    return player;
}

function parseReplayFile(data) {
    try {
        var actions = jsyaml.load(data);
        return actions;
    } catch (e) {
        alert("Failed to parse replay file.");
    }
    return null;
}

function playReplay(actions) {
    if (!actions)
        return;

    var start = new Date().getTime();
    var i = 0;
    $scope.players = {1: {}, 0: {}};

    // Start animating.
    var canvas = document.getElementById("player");
    var context = canvas.getContext("2d");
    draw(canvas, context, start);

    // Process the list of actions.
    function processActions() {
        $scope.time = (new Date().getTime() - start) / 1000;
        var action = actions[i];
        while (action.time <= $scope.time) {
            processAction(action);
            // Advance to the next action.
            i += 1;
            var action = actions[i];
        }
        $timeout(processActions, 100);
    }

    processActions();
}

function draw(canvas, context, start) {
    // Get the amount of time which has passed.
    var delta = new Date().getTime() - start;

    // Clear the canvas.
    context.clearRect(0, 0, canvas.width, canvas.height);

    // Draw every actor.
    for (var actor in actors) {
        context.beginPath();
        context.arc(50, 50, 2, 0, 2*Math.PI);
        context.fillStyle = "#FF0000";
        context.fill();
    }

    // Request the drawing of the next frame.
    requestAnimFrame(function() {
        draw(canvas, context, start);
    });
}

function convert_coords(game_x, game_z) {
    var canvas_x = 90 + game_x;
    var canvas_y = 230;
    return [canvas_x, canvas_y];
}

function processAction(action) {
    var n = action.name;
    var p = action.params;

    // Properties commands.
    if (n == "cmd_load_room") {
        if (p.set == "AT_2L_Arena")
            $scope.arena = "battle-lab";
        else if (p.set == "AT_1L_Arena") {
            $scope.arena = "candy-streets";
        }
    } else if (n == "cmd_add_user") {
        if (p.champion.slice(0, 4) == "bot_")
            var champion = p.champion.slice(4);
        else
            var champion = p.champion.split("_")[0];
        $scope.players[p.team][p.id] = {
            "backpack": p.backpack,
            "champion": champion,
            "currentHealth": CHAMPIONS[champion].startHealth,
            "elo": p.elo,
            "level": 1,
            "maxHealth": CHAMPIONS[champion].startHealth,
            "name": p.name,
            "score": 0,
            "tournament": p.isTournamentEligible,
            "xp": 0
        };
    } else if (n == "cmd_update_actor_data" || n == "cmd_update_script_data") {
        var player = getPlayer(p.id);
        if (!player)
            return;
        for (var property in p) {
            if (property in player) {
                player[property] = p[property];
            }
        }
    } else if (n == "cmd_update_score") {
        $scope.teamScores = p;
    }

    // Drawing commands.
    else if (n == "cmd_create_actor") {
        actors[p.id] = {
            "current_x": p.spawn_point.x,
            "current_z": p.spawn_point.z,
            "dest_x": p.spawn_point.x,
            "dest_z": p.spawn_point.z,
            "speed": 0.0,
            "type": null
        };
    }
}

window.onload = function() {
    var replayInput = document.getElementById("replay-input");

    replayInput.addEventListener("change", function(e) {
        var file = replayInput.files[0];
        var reader = new FileReader();
        reader.onload = function openReplay(e) {
            var actions = parseReplayFile(reader.result);
            playReplay(actions);
        }

        reader.readAsText(file);
    });
}
});