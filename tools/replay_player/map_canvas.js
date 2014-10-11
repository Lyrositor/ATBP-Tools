/**
 * Replay Player
 * Utilities for modifying the map: moving actors, creating effects, etc.
 */

BACKGROUND = "img/AT_2L_Arena.png";

// Checks if a point is in a rectangle.
// r_x and r_y are the top-left coordinates of the rectangle.
// r_w and r_h are the width and height of the rectangle.
function in_rectangle(p_x, p_y, r_x, r_y, r_w, r_h) {
    if (p_x < r_x || p_x > r_x + r_w)
        return false;
    if (p_y > r_y || p_y < r_y - r_h)
        return false;
    return true;
}

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
    return new ICoords(100, 100);
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
    this.actors = [];
    
    // Load the background image.
    this.background = new Image();
    this.background.src = BACKGROUND;

    // Initialize the viewing window's properties.
    this.window = {
        "coords": new GCoords(0, 0).toICoords(),
        "zoom": 0.8
    };
    this.dragPrevious = null;
    
    // Bind the dragging functions.
    this.isDragging = false;
    var canvas = document.getElementById(this.canvas_id);
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
    
    var isDrawing = false;
}

// Clears the canvas.
MapCanvas.prototype.clear = function() {
    var canvas = document.getElementById(this.canvas_id);
    var context = canvas.getContext("2d");
    context.clearRect(0, 0, canvas.width, canvas.height);
}

MapCanvas.prototype.draw = function(last) {
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
    
    // Draw the next frame if we're still drawing.
    if (this.isDrawing) {
        var self = this;
        requestAnimFrame(function() {
            self.draw(now);
        });
    }
}