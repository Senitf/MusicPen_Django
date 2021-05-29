var tmp = document.getElementsByTagName("canvas");
var canvasCnt = 0;
var canvas = tmp[canvasCnt];
var ctx = canvas.getContext("2d");

var width = canvas.width, height = canvas.height;
var curX, curY, prevX, prevY;
var hold = false;
var fill_value = true, stroke_value = false;
var canvas_data = { "pencil": [], "line": [], "rectangle": [], "circle": [], "eraser": [] };
ctx.lineWidth = 2;
                        
function color (color_value){
    ctx.strokeStyle = color_value;
    ctx.fillStyle = color_value;
}    
        
function add_pixel (){
    ctx.lineWidth += 1;
}
        
function reduce_pixel (){
    if (ctx.lineWidth == 2)
        return;
    else
        ctx.lineWidth -= 1;
}
        
function fill (){
    fill_value = true;
    stroke_value = false;
}
        
function outline (){
    fill_value = false;
    stroke_value = true;
}
               
function reset (){
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    canvas_data = { "pencil": [], "line": [], "rectangle": [], "circle": [], "eraser": [] };
}

function base (ctx){
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

// pencil tool
        
function pencil (){
    base(ctx);

    canvas.onmousedown = function (e){
        curX = e.clientX - canvas.offsetLeft;
        curY = e.clientY - canvas.offsetTop;
        hold = true;
            
        prevX = curX;
        prevY = curY;
        ctx.beginPath();
        ctx.moveTo(prevX, prevY);
    };
        
    canvas.onmousemove = function (e){
        if(hold){
            curX = e.clientX - canvas.offsetLeft;
            curY = e.clientY - canvas.offsetTop;
            draw();
        }
    };
        
    canvas.onmouseup = function (e){
        hold = false;
    };
        
    canvas.onmouseout = function (e){
        hold = false;
    };
        
    function draw (){
        ctx.lineTo(curX, curY);
        ctx.stroke();
        canvas_data.pencil.push({ "startx": prevX, "starty": prevY, "endx": curX, "endy": curY, 
            "thick": ctx.lineWidth, "color": ctx.strokeStyle });
    }
}
        
// line tool
        
function line (){
           
    canvas.onmousedown = function (e){
        img = ctx.getImageData(0, 0, width, height);
        prevX = e.clientX - canvas.offsetLeft;
        prevY = e.clientY - canvas.offsetTop;
        hold = true;
    };
            
    canvas.onmousemove = function (e){
        if (hold){
            ctx.putImageData(img, 0, 0);
            curX = e.clientX - canvas.offsetLeft;
            curY = e.clientY - canvas.offsetTop;
            ctx.beginPath();
            ctx.moveTo(prevX, prevY);
            ctx.lineTo(curX, curY);
            ctx.stroke();
            canvas_data.line.push({ "starx": prevX, "starty": prevY, "endx": curX, "endY": curY,
                 "thick": ctx.lineWidth, "color": ctx.strokeStyle });
            ctx.closePath();
        }
    };
            
    canvas.onmouseup = function (e){
         hold = false;
    };
            
    canvas.onmouseout = function (e){
         hold = false;
    };
}
        
// rectangle tool
        
function rectangle (){
            
    canvas.onmousedown = function (e){
        img = ctx.getImageData(0, 0, width, height);
        prevX = e.clientX - canvas.offsetLeft;
        prevY = e.clientY - canvas.offsetTop;
        hold = true;
    };
            
    canvas.onmousemove = function (e){
        if (hold){
            ctx.putImageData(img, 0, 0);
            curX = e.clientX - canvas.offsetLeft - prevX;
            curY = e.clientY - canvas.offsetTop - prevY;
            ctx.strokeRect(prevX, prevY, curX, curY);
            if (fill_value){
                ctx.fillRect(prevX, prevY, curX, curY);
            }
            canvas_data.rectangle.push({ "starx": prevX, "stary": prevY, "width": curX, "height": curY, 
                "thick": ctx.lineWidth, "stroke": stroke_value, "stroke_color": ctx.strokeStyle, "fill": fill_value,
                "fill_color": ctx.fillStyle });
            
        }
    };
            
    canvas.onmouseup = function (e){
        hold = false;
    };
            
    canvas.onmouseout = function (e){
        hold = false;
    };
}
        
// circle tool
        
function circle (){
            
    canvas.onmousedown = function (e){
        img = ctx.getImageData(0, 0, width, height);
        prevX = e.clientX - canvas.offsetLeft;
        prevY = e.clientY - canvas.offsetTop;
        hold = true;
    };
            
    canvas.onmousemove = function (e){
        if (hold){
            ctx.putImageData(img, 0, 0);
            curX = e.clientX - canvas.offsetLeft;
            curY = e.clientY - canvas.offsetTop;
            ctx.beginPath();
            ctx.arc(Math.abs(curX + prevX)/2, Math.abs(curY + prevY)/2, 
                Math.sqrt(Math.pow(curX - prevX, 2) + Math.pow(curY - prevY, 2))/2, 0, Math.PI * 2, true);
            ctx.closePath();
            ctx.stroke();
            if (fill_value)
                ctx.fill();
            canvas_data.circle.push({ "starx": prevX, "stary": prevY, "radius": curX - prevX, "thick": ctx.lineWidth,
                "stroke": stroke_value, "stroke_color": ctx.strokeStyle, "fill": fill_value, "fill_color": ctx.fillStyle });
        }
    };
            
    canvas.onmouseup = function (e){
        hold = false;
    };
            
    canvas.onmouseout = function (e){
        hold = false;
    };
}
        
// eraser tool
        
function eraser (){
        
    /*canvas.onmousedown = function (e){
        hold = true;
    };
        
    canvas.onmousemove = function (e){
        if (hold){
            curX = e.clientX - canvas.offsetLeft;
            curY = e.clientY - canvas.offsetTop;
            ctx.clearRect(curX, curY, 20, 20);
            canvas_data.eraser.push({ "endx": curX, "endy": curY, "thick": ctx.lineWidth });
        }
    };
        
    canvas.onmouseup = function (e){
        hold = false;
    };
        
    canvas.onmouseout = function (e){
        hold = false;
    };
    */
    canvas.onmousedown = function (e){
        curX = e.clientX - canvas.offsetLeft;
        curY = e.clientY - canvas.offsetTop;
        hold = true;
            
        prevX = curX;
        prevY = curY;
        ctx.beginPath();
        ctx.moveTo(prevX, prevY);
    };
        
    canvas.onmousemove = function (e){
        if(hold){
            curX = e.clientX - canvas.offsetLeft;
            curY = e.clientY - canvas.offsetTop;
            draw();
        }
    };
        
    canvas.onmouseup = function (e){
        hold = false;
    };
        
    canvas.onmouseout = function (e){
        hold = false;
    };
        
    function draw (){
        ctx.lineTo(curX, curY);
        ctx.strokeStyle = "#ffffff";
        ctx.stroke();
        canvas_data.eraser.push({ "startx": prevX, "starty": prevY, "endx": curX, "endy": curY, 
            "thick": ctx.lineWidth, "color": ctx.strokeStyle });
    }
}

function save (){
    var data = JSON.stringify(canvas_data);
    var image = canvas.toDataURL();
    
    $.post("", { data: data, image: image });
    alert("saved");
    
}

function addCanvas() {
    var x = document.createElement("CANVAS");
    var ctx = x.getContext("2d");
    ctx.fillStyle = "#FF0000";
    ctx.fillRect(20, 20, 150, 100);
    document.body.appendChild(x);
/*
    var x = document.createElement("CANVAS");
    var ctx = x.getContext("2d");
    var canvasLine = document.getElementById("canvasLine");
    ctx.fillStyle = "#FF0000";
    ctx.fillRect(20, 20, 150, 100);
    document.canvasLine.appendChild(x);
*/
}

/* for navbar */
// When the user scrolls the page, execute myFunction
window.onscroll = function() {myFunction()};

// Get the navbar
var navbar = document.getElementById("navbar");

// Get the offset position of the navbar
var sticky = navbar.offsetTop;

// Add the sticky class to the navbar when you reach its scroll position. Remove "sticky" when you leave the scroll position
function myFunction() {
  if (window.pageYOffset >= sticky) {
    navbar.classList.add("sticky")
  } else {
    navbar.classList.remove("sticky");
  }
}