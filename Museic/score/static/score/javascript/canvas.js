var pos = {
    drawable: false,
    x: -1,
    y: -1
}
var canvas, ctx;

window.onload = function(){
    canvas = document.getElementsByClassName("canvas");
    for(var i = 0; i<canvas.length; i++){
        ctx = canvas[i].getContext("2d");
        ctx.strokeRect(0, 0, 400, 100);
        ctx.beginPath();
        ctx.moveTo(0, 25);
        ctx.lineTo(400, 25);
        ctx.stroke();
        ctx.moveTo(0, 50);
        ctx.lineTo(400, 50);
        ctx.stroke();
        ctx.moveTo(0, 75);
        ctx.lineTo(400, 75);
        ctx.stroke();
        ctx.moveTo(0, 100);
        ctx.lineTo(400, 100);
        ctx.stroke();
        ctx.closePath();
        ctx.beginPath();
        ctx.lineWidth = 5;
        ctx.moveTo(397, 100);
        ctx.lineTo(397, 0);
        ctx.stroke();
        ctx.closePath();
    }
    canvas = document.getElementById("curCanvas");
    ctx = canvas.getContext("2d");
    canvas.addEventListener("mousedown", listener);
    canvas.addEventListener("mousemove", listener);
    canvas.addEventListener("mouseup", listener);
    canvas.addEventListener("mouseout", listener);
}

function listener(event){
    switch(event.type){
        case "mousedown":
            initDraw(event);
            break;
        case"mousemove":
            if(pos.drawable)
                draw(event);
            break;
        case "mouseout":
        case "mouseup":
            finishDraw();
            break;
    }
}

function initDraw(event){
    ctx.beginPath();
    pos.drawable = true;
    var coors = getPosition(event);
    pos.X = coors.X;
    pos.Y = coors.Y;
    ctx.moveTo(pos.X, pos.Y);
}

function draw(event){
    var coors = getPosition(event);
    ctx.lineTo(coors.X, coors.Y);
    pos.X = coors.X;
    pos.Y = coors.Y;
    ctx.stroke();
}

function finishDraw(){
    pos.drawable = false;
    pos.X = -1;
    pos.Y = -1;
}

function getPosition(event){
    var x = event.pageX - canvas.offsetLeft;
    var y = event.pageY - canvas.offsetTop;
    return {X:x, Y:y};
}