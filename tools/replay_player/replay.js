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
    this.KOFeed = [];
    this.players = {};
    this.startIndex = null;
    this.teams = {
        0: {
            players: [],
            score: 0
        },
        1: {
            players: [],
            score: 0
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
    this.map.isPlaying = true;
    var start = new Date().getTime();
    this.map.draw(start);

    // Start processing actions.
    this.processActions(start);
}

Replay.prototype.pause = function() {
    if (!this.isLoaded)
        return;

    this.map.isPlaying = false;
}

Replay.prototype.stop = function() {
    if (!this.isLoaded)
        return;

    this.map.isDrawing = false;
    this.map.isPlaying = false;
    this.map.clear();
    this.time = 0.0;
    this.currentIndex = this.startIndex;
}

Replay.prototype.processActions = function(last) {
    // Only run if the map is reflecting the game.
    // Essentially, this tells us whether the replay is paused/stopped or
    // playing.
    if (!this.map.isPlaying)
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

    // Update the KO feed.
    for (var i = 0; i < this.KOFeed.length; i++) {
        var ko = this.KOFeed[i];
        if ((now - ko.time) / 1000 > 5)
            ko.expired = true;
    }

    // Try to process the next batch of actions.
    if (action) {
        var self = this;
        this.$timeout(function() { self.processActions(now); }, 50);
    } else
        this.pause();
}

Replay.prototype.processAction = function(action) {
    var n = action.name;
    var p = action.params;

    if (n == "cmd_create_actor")
        this.map.actors[p.id] = new Actor(p.actor, p.actorType, p.spawn_point, p.team);

    else if (n == "cmd_update_actor_data") {
        var id = parseInt(p.id);
        if (p.id in this.map.actors && p.pHealth)
            this.map.actors[p.id].pHealth = p.pHealth;
        if (id in this.players) {
            player = this.players[id];
            if (p.currentHealth)
                player.health = p.currentHealth;
            if (p.maxHealth)
                player.maxHealth = p.maxHealth;
            if (p.xp)
                player.xp = p.xp;
        }
    }

    else if (n == "cmd_update_score") {
        this.teams[0].score = p.teamA;
        this.teams[1].score = p.teamB;
    }

    else if (n == "cmd_update_script_data") {
        var id = parseInt(p.id);
        if (id in this.players)
            this.players[id].updateScriptData(p);
    }

    else if (n == "cmd_move_actor") {
        if (p.i in this.map.actors) {
            var a = this.map.actors[p.i];
            a.speed = p.s;
            a.position = new GCoords(p.px, p.pz);
            a.destination = new GCoords(p.dx, p.dz);
        }
    }

    else if (n == "cmd_destroy_actor") {
        if (p.id in this.map.actors)
            delete this.map.actors[p.id];
    }

    else if (n == "cmd_knockout_actor") {
        // Update the actor's status.
        var killedActor = this.map.actors[p.id];
        var killerActor = this.map.actors[p.attackerId];
        if (killedActor) {
            killedActor.isDead = true;
            killedActor.pHealth = 0.0;
        }
        var killedName = killedActor.getBaseName();
        var killerName = killerActor.getBaseName();

        // Create the KO feed entry, but don't add it yet.
        var ko = {
            class: {},
            expired: false,
            killed: killedName,
            killer: killerName,
            time: new Date().getTime()
        };
        ko.class[killedActor.team] = "ko-red";
        ko.class[killerActor.team] = "ko-green";

        // Check if a player was killed or was the killer.
        var killedId = parseInt(p.id);
        var killerId = parseInt(p.attackerId);
        var killed = this.players[killedId];
        var killer = this.players[killerId];

        // Check if a player disconnected.
        if (killer && killer == killed) {
            ko.class[killedActor.team] = "ko-red";
            ko.class[killedActor.team == 1 ? 0 : 1] = "ko-green";
            killed.isDead = true;
            delete this.map.actors[p.id];
            this.KOFeed.push(ko);
        }

        // Otherwise, check if a player was killed.
        else if (killed) {
            killed.isDead = true;
            killed.health = 0;
            this.KOFeed.push(ko);

        // Otherwise, check if a player destroyed a tower.
        } else if (killer && killedActor.type == "TOWER")
            this.KOFeed.push(ko);
    }

    else if (n == "cmd_respawn_actor") {
        this.map.actors[p.id].isDead = false;
        var id = parseInt(p.id);
        var player = this.players[id];
        if (player)
            player.isDead = false;
    }

    else if (n == "cmd_play_sound") {
        if (p.id == "music" && p.name) {
            var audio = new Audio("sounds/" + p.name + ".ogg");
            audio.play();
        }
    }

    else if (n == "cmd_snap_actor") {
        var actor = this.map.actors[p.i];
        if (actor) {
            actor.position = new GCoords(p.px, p.pz);
            actor.destination = new GCoords(p.dx, p.dz);
        }
    }

    else if (n == "cmd_set_speed") {
        var actor = this.map.actors[p.id];
        if (actor)
            actor.speed = p.speed;
    }

    else if (n == "cmd_set_target") {
        var actor = this.map.actors[p.actor_id];
        if (actor)
            this.map.actors[p.actor_id].target = p.target_id;
    }
}

function Player(name, champion, backpack, elo, isTournamentEligible) {
    this.assists = 0;
    this.availableSpellPoints = 1;
    this.backpack = BACKPACKS[backpack];
    this.champion = champion.replace("bot_", "").split("_")[0];
    this.deaths = 0;
    this.elo = elo;
    this.health = 0;
    this.isDead = false;
    this.isTournamentEligible = isTournamentEligible;
    this.kills = 0;
    this.level = 1;
    this.maxHealth = 0;
    this.name = name;
    this.score = 0;
    this.spCategories = [0, 0, 0, 0, 0];
    this.xp = 0.0;
}

Player.prototype.updateScriptData = function(p) {
    if (p.sp_category1)
        this.spCategories[0] = p.sp_category1;
    if (p.sp_category2)
        this.spCategories[1] = p.sp_category2;
    if (p.sp_category3)
        this.spCategories[2] = p.sp_category3;
    if (p.sp_category4)
        this.spCategories[3] = p.sp_category4;
    if (p.sp_category5)
        this.spCategories[4] = p.sp_category5;
    if (p.availableSpellPoints)
        this.availableSpellPoints = p.availableSpellPoints;
    if (p.level)
        this.level = p.level;
    if (p.score)
        this.score = p.score;
    if (p.assists)
        this.assists = p.assists;
    if (p.deaths)
        this.deaths = p.deaths;
    if (p.kills)
        this.kills = p.kills;
}