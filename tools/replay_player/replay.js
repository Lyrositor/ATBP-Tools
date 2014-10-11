/**
 * Replay Player
 * Replay file library.
 */
 
function Replay(data, map, $timeout) {
    this.map = map;
    this.$timeout = $timeout;

    this.reset();
    this.parseFile(data);
}

Replay.prototype.reset = function() {
    this.isLoaded = false;

    this.actions = [];
    this.currentIndex = null;
    this.players = {};
    this.startIndex = null;
    this.teams = {
        0: {
            "players": [],
            "score": 0
        },
        1: {
            "players": [],
            "score": 0
        },
    };
    this.time = 0.0;
    this.totalTime = 0.0;
}

Replay.prototype.parseFile = function (data) {
    // Load the YAML file.
    try {
        this.actions = [];
        var self = this;
        jsyaml.safeLoadAll(data, function(doc) { self.actions.push(doc); });
    } catch (e) {
        alert("Failed to parse replay file.");
        return;
    }
    
    // Load the replay's initial data.
    for (var i = 0; i < this.actions.length; i++) {
        var n = this.actions[i].name;
        var p = this.actions[i].params;

        // Add the players.
        if (n == "cmd_add_user") {
            this.players[p.id] = new Player(
                p.name,
                p.champion,
                p.backpack,
                p.elo,
                p.isTournamentEligible
            );
            this.teams[p.team].players.push(p.id);
        }
        
        // Check if the map is AT_2L_Arena.
        else if (n == "cmd_load_room" && p.set != "AT_2L_Arena") {
            alert("ERROR: Cannot play practice mode replays.");
            this.reset();
            return;
        }
        
        // Note the position of the actual match start, so that we can skip the
        // loading time when actually playing the replay.
        else if (n == "cmd_update_time" && this.startIndex == null)
            this.startIndex = i;
    }
    
    var a = this.actions;
    this.totalTime = a[a.length - 1].time - a[this.startIndex].time;
    this.currentIndex = this.startIndex;
    
    this.isLoaded = true;
}

Replay.prototype.play = function() {
    if (!this.isLoaded)
        return;
    
    // Start drawing.
    this.map.isDrawing = true;
    var start = new Date().getTime();
    this.map.draw(start);
    
    // Start processing actions.
    this.processActions(start);
}

Replay.prototype.pause = function() {
    if (!this.isLoaded)
        return;

    this.map.isDrawing = false;
}

Replay.prototype.stop = function() {
    if (!this.isLoaded)
        return;

    this.map.isDrawing = false;
    this.map.clear();
    this.time = 0.0;
    this.currentIndex = this.startIndex;
}

Replay.prototype.processActions = function(last) {
    // Only run if the map is reflecting the game.
    // Essentially, this tells us whether the replay is paused/stopped or
    // playing.
    if (!this.map.isDrawing)
        return;

    var now = new Date().getTime();
    this.time += (now - last) / 1000;
    
    var action = this.actions[this.currentIndex];
    var timeStart = this.actions[this.startIndex].time;
    while (action && action.time <= this.time + timeStart) {
        this.processAction(action);

        // Advance to the next action.
        this.currentIndex++;
        var action = this.actions[this.currentIndex];
    }
    
    // Try to process the next batch of actions.
    if (action) {
        var self = this;
        this.$timeout(function() { self.processActions(now); }, 50);
    } else
        this.pause();
}

Replay.prototype.processAction = function(action) {
    console.log(action.name);
}

function Player(name, champion, backpack, elo, isTournamentEligible) {
    this.availableSpellPoints = 1;
    this.backpack = BACKPACKS[backpack];
    this.champion = champion.replace("bot_", "");
    this.elo = elo;
    this.health = 0;
    this.isTournamentEligible = isTournamentEligible;
    this.level = 1;
    this.maxHealth = 0;
    this.name = name;
    this.replay = 0;
    this.score = 0;
    this.spCategories = [0, 0, 0, 0, 0];
    this.xp = 0.0;
}

Player.prototype.moveTo = function(dx, dz) {

}