/**
 * Replay Player
 * Contains the actors' drawing functions.
 */

MapCanvas.prototype.drawChampion = function(context, actor) {
    var c = actor.position.toICoords();

    // Draw the colored circle.
    context.beginPath();
    context.arc(
        (c.x - this.window.coords.x) * this.window.zoom,
        (c.y - this.window.coords.y) * this.window.zoom,
        17 * this.window.zoom,
        0,
        2 * Math.PI
    );
    if (!actor.isDead)
        context.fillStyle = COLORS[actor.team];
    else
        context.fillStyle = "#AAAAAA";
    context.fill();

    // Draw the line to the champion's current target.
    if (actor.target && actor.target in this.actors && !actor.target.isDead) {
        var target = this.actors[actor.target];
        var t = target.position.toICoords();

        context.beginPath();
        context.moveTo(
            (c.x - this.window.coords.x) * this.window.zoom,
            (c.y - this.window.coords.y) * this.window.zoom
        );
        context.lineTo(
            (t.x - this.window.coords.x) * this.window.zoom,
            (t.y - this.window.coords.y) * this.window.zoom
        );
        context.lineWidth = 3;
        context.strokeStyle = COLORS[actor.team];
        context.stroke();
    } else
        actor.target = null;

    // Draw the champion's image.
    var topX = c.x - this.window.coords.x - 16;
    var leftY = c.y - this.window.coords.y - 16;
    context.drawImage(
        this.images[actor.getBaseName()],
        topX * this.window.zoom, leftY * this.window.zoom,
        32 * this.window.zoom, 32 * this.window.zoom
    );

    // Draw the champion's health bar.
    context.beginPath()
    context.rect(
        topX * this.window.zoom, (leftY - 10) * this.window.zoom,
        32 * this.window.zoom, 5 * this.window.zoom
    );
    context.fillStyle = "#ABABAB";
    context.fill();

    // Draw the champion's health.
    context.beginPath()
    context.rect(
        topX * this.window.zoom, (leftY - 10) * this.window.zoom,
        32 * this.window.zoom * actor.pHealth, 5 * this.window.zoom
    );
    context.fillStyle = "#00FF00";
    context.fill();
}

MapCanvas.prototype.drawBase = function(context, actor) {
    var c = actor.position.toICoords();

    // Draw the colored circle.
    context.beginPath();
    context.arc(
        (c.x - this.window.coords.x) * this.window.zoom,
        (c.y - this.window.coords.y) * this.window.zoom,
        32 * this.window.zoom,
        0,
        2 * Math.PI
    );
    context.fillStyle = COLORS[actor.team];
    context.fill();

    // Draw the base's health bar.
    context.beginPath()
    context.rect(
        (c.x - this.window.coords.x - 32) * this.window.zoom,
        (c.y - this.window.coords.y - 42) * this.window.zoom,
        64 * this.window.zoom, 5 * this.window.zoom
    );
    context.fillStyle = "#ABABAB";
    context.fill();

    // Draw the base's health.
    context.beginPath()
    context.rect(
        (c.x - this.window.coords.x - 32) * this.window.zoom,
        (c.y - this.window.coords.y - 42) * this.window.zoom,
        64 * this.window.zoom * actor.pHealth, 5 * this.window.zoom
    );
    context.fillStyle = "#00FF00";
    context.fill();
}

MapCanvas.prototype.drawTower = function(context, actor) {
    var c = actor.position.toICoords();
    var topX = c.x - this.window.coords.x - 63/2;
    var topY = c.y - this.window.coords.y - 79/2;

    // Draw the tower's icon.
    if (!actor.isDead)
        var image = this.images[actor.actor];
    else
        var image = this.images["tower_down"]
    context.drawImage(
        this.images[actor.actor],
        topX * this.window.zoom,
        topY * this.window.zoom,
        63 * this.window.zoom,
        79 * this.window.zoom
    );

    // Draw the tower's health bar.
    context.beginPath()
    context.rect(
        topX * this.window.zoom,
        (topY - 10) * this.window.zoom,
        64 * this.window.zoom, 5 * this.window.zoom
    );
    context.fillStyle = "#ABABAB";
    context.fill();

    // Draw the tower's health.
    context.beginPath()
    context.rect(
        topX * this.window.zoom,
        (topY - 10) * this.window.zoom,
        64 * this.window.zoom * actor.pHealth, 5 * this.window.zoom
    );
    context.fillStyle = "#00FF00";
    context.fill();
}

MapCanvas.prototype.drawMinion = function(context, actor) {
    var c = actor.position.toICoords();

    // Draw the colored circle.
    context.beginPath();
    context.arc(
        (c.x - this.window.coords.x) * this.window.zoom,
        (c.y - this.window.coords.y) * this.window.zoom,
        5 * this.window.zoom,
        0,
        2 * Math.PI
    );
    context.fillStyle = COLORS[actor.team];
    context.fill();
}