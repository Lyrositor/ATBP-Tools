/**
 * Replay Player
 * Utilities for modifying the map: moving actors, creating effects, etc.
 */

BACKGROUND = "img/map/AT_2L_Arena.png";

// Image Coordinates
function ICoords(x, y) {
    this.x = x;
    this.y = y;
}

// Game Coordinates
function GCoords(x, z) {
    this.x = x;
    this.z = z;
}

GCoords.prototype.toICoords = function() {
    return new ICoords(-this.x * 20 + 2560/2, this.z * 20 + 1536/2);
}

// Create the cross-platform version of requestAnimFrame.
window.requestAnimFrame = (function(callback) {
    return window.requestAnimationFrame || window.webkitRequestAnimationFrame || window.mozRequestAnimationFrame || window.oRequestAnimationFrame || window.msRequestAnimationFrame ||
        function(callback) {
            window.setTimeout(callback, 1000 / 60);
        };
})();

function MapCanvas(canvas_id) {
    this.canvas_id = canvas_id;
    this.actors = {};
    this.isDrawing = false;
    this.isPlaying = false;
    var canvas = document.getElementById(this.canvas_id);

    // Load the background image.
    this.background = new Image();
    this.background.src = BACKGROUND;

    // Load the images.
    this.images = {};
    for (champion in CHAMPIONS) {
        this.images[champion] = new Image();
        this.images[champion].src = "img/map/champions/" + champion + ".png"
    }
    var towers = ["tower1", "tower2", "tower_down"];
    for (var i in towers) {
        var tower = towers[i];
        this.images[tower] = new Image();
        this.images[tower].src = "img/map/towers/" + tower + ".png";
    }

    // Initialize the viewing window's properties.
    var startCoords = new GCoords(0, 0).toICoords();
    startCoords.x -= canvas.width/2;
    startCoords.y -= canvas.height/2;
    this.window = {
        "coords": startCoords,
        "zoom": 0.5
    };
    this.dragPrevious = null;

    // Bind the dragging functions.
    this.isDragging = false;
    var self = this;
    canvas.onmousedown = function(e) {
        self.isDragging = true;
        self.dragPrevious = {"x": e.x, "y": e.y};
    }
    canvas.onmouseup = function(e) {
        self.isDragging = false;
    }
    canvas.onmouseout = function(e) {
        self.isDragging = false;
    }
    canvas.onmousemove = function(e) {
        if (!self.isDragging)
            return;
        var dX = -(e.x - self.dragPrevious.x);
        var dY = -(e.y - self.dragPrevious.y);
        var w = self.window.coords;
        var z = self.window.zoom;
        if (w.x * z + dX >= 0 && w.x * z + dX + this.width <= self.background.width * z)
            self.window.coords.x += dX;
        if (w.y * z + dY >= 0 && w.y * z + dY + this.height <= self.background.height * z)
            self.window.coords.y += dY;
        self.dragPrevious = {"x": e.x, "y": e.y};
    }

    // Zooming function.
    canvas.addEventListener("mousewheel", function(e) {
        // Zoom in or out.
        e.preventDefault();
        if (e.wheelDelta > 0)
            var zoom = 0.1;
        else if (e.wheelDelta < 0)
            var zoom = -0.1;
        var z = self.window.zoom + zoom;
        if (z >= 0.5 && z <= 1.0)
            self.window.zoom = z;

        // Check if we're still within the authorized range.
        // If not, move the camera so that we are.
        var w = self.window.coords;
        var dX = w.x * z + this.width - self.background.width * z;
        var dY = w.y * z + this.height - self.background.height * z
        if (dX > 0)
            w.x -= dX;
        if (dY > 0)
            w.y -= dY;
    }, false);

    var isPlaying = false;
}

// Clears the canvas.
MapCanvas.prototype.clear = function() {
    var canvas = document.getElementById(this.canvas_id);
    var context = canvas.getContext("2d");
    context.clearRect(0, 0, canvas.width, canvas.height);
}

MapCanvas.prototype.draw = function(last) {
    if (!this.isDrawing)
        return;
    var canvas = document.getElementById(this.canvas_id);
    var context = canvas.getContext("2d");
    var now = new Date().getTime();
    var deltaTime = (now - last) / 1000;

    // Draw the background, as viewed through the window.
    context.drawImage(
        this.background,
        this.window.coords.x,
        this.window.coords.y,
        canvas.width / this.window.zoom,
        canvas.height / this.window.zoom,
        0,
        0,
        canvas.width,
        canvas.height
    );

    // Draw all the actors.
    for (id in this.actors) {
        var actor = this.actors[id];

        // If we're playing, run the simulations to update the game's status.
        if (this.isPlaying) {
            // Get the actor's new coordinates.
            if (actor.destination) {
                var remX = actor.destination.x - actor.position.x;
                var remZ = actor.destination.z - actor.position.z;
                var remDist = Math.sqrt(
                    Math.pow(remX, 2),
                    Math.pow(remZ, 2)
                );
                var deltaDist = actor.speed * deltaTime;
                if (remDist)
                    actor.position = new GCoords(
                        actor.position.x + deltaDist * remX/remDist,
                        actor.position.z + deltaDist * remZ/remDist
                    );
                else
                    actor.destination = null;
            }
        }

        if (actor.type == "CHAMPION")
            this.drawChampion(context, actor);
        else if (actor.type == "BASE")
            this.drawBase(context, actor);
        else if (actor.type == "TOWER" && actor.actor != "gumball_guardian")
            this.drawTower(context, actor);
        else if (actor.type == "MINION" || actor.type == "JUNGLE")
            this.drawMinion(context, actor);
    }

    // Draw the next frame.
    var self = this;
    requestAnimFrame(function() {
        self.draw(now);
    });
}

function Actor(actor, type, spawn_point, team) {
    this.actor = actor;
    this.isDead = false;
    this.pHealth = 1.0;
    this.speed = 0.0;
    this.target = null;
    this.team = team;
    this.type = type;

    this.position = new GCoords(spawn_point.x, spawn_point.z);
    this.destination = null;
}

Actor.prototype.getBaseName = function() {
    name = this.actor.replace("bot_", "");
    if (name.substring(0, 5) == "gnome")
        name = "gnome";
    else if (name.substring(0, 7) == "ironowl")
        name = "ironowl";
    else if (this.type == "CHAMPION")
        name = name.split("_")[0];
    return name;
}