var canvasCnt = 0;
var canvas, ctx;
var tmp = 0;
var width = 400, height = 100;
var curX, curY, prevX, prevY, boundings;
var hold = false;
var fill_value = true, stroke_value = false;
var canvas_data = new Array(100);
var canvas_dataCnt = 0;

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
    ctx.lineWidth = 5;
}

function base (){
    canvas = document.getElementsByTagName("canvas")[canvasCnt];
    ctx = canvas.getContext('2d');
    width = canvas.width;
    height = canvas.height;
    ctx.lineWidth=2;
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

function init(){
    for(var i = 0; i < 4; i++){
        canvasCnt = i * 2;
        base();
    }
    canvasCnt = 1;
    pencil();
}

function selectCanvas(curCanvas){
    canvasCnt = (curCanvas * 2) + 1;
    reset();
    pencil();
}

// pencil tool
        
function pencil (){
    canvas = document.getElementsByTagName("canvas")[canvasCnt];
    ctx = canvas.getContext('2d');
    boundings = canvas.getBoundingClientRect();
    width = canvas.width;
    height = canvas.height;
    ctx.strokeStyle = 'black';
    ctx.lineWidth = 5;
    curX = 0;
    curY = 0;
    hold = false;

    // Mouse Down Event
    canvas.addEventListener('mousedown', function(event) {
        setMouseCoordinates(event);
        hold = true;

        // Start Drawing
        ctx.beginPath();
        ctx.moveTo(curX, curY);
    });
    // Mouse Move Event
    canvas.addEventListener('mousemove', function(event) {
        setMouseCoordinates(event);
        if(hold){
            ctx.lineTo(curX, curY);
            ctx.stroke();
        }
    });
    // Mouse Up Event
    canvas.addEventListener('mouseup', function(event) {
        setMouseCoordinates(event);
        hold = false;
    });
    // Handle Mouse Coordinates
    function setMouseCoordinates(event) {
        curX = event.clientX - boundings.left;
        curY = event.clientY - boundings.top;
    }
}

function save (){
    var image = canvas.toDataURL();
    console.log(image);
    reset();
    /*
    $.post("", { data: data, image: image });
    alert("saved");
    */
    $.ajax({
      type: "POST", // 데이터를 전송하는 방법을 지정
      url: "", // 통신할 url을 지정
      data: {'image':image, 'csrfmiddlewaretoken': '{{ csrf_token }}'}, // 서버로 데이터 전송시 옵션
      dataType: "json", // 서버측에서 전송한 데이터를 어떤 형식의 데이터로서 해석할 것인가를 지정, 없으면 알아서 판단
      // 서버측에서 전송한 Response 데이터 형식 (json)
      success: function(response){ 
        canvas = document.getElementsByTagName("canvas")[parseInt((tmp / 4) * 2)];
        ctx = canvas.getContext('2d');
        var img = new Image();
        img.onload = function() {
        ctx.drawImage(img, (tmp % 4) * 100 - 100, 0);
        };
        switch (response.output) {
            case 0:
                img.src = quarterIMG;
                break;
            case 1:
                img.src = halfIMG;
                break;
            case 2:
                img.src = _8thIMG;
                break;
            case 3:
                img.src = _16thIMG;
                break;
            case 4:
                img.src = dotquarterIMG;
                break;
            case 5:
                img.src = dothalfIMG;
                break;
            case 6:
                img.src = dot8thIMG;
                break;
            default:
                console.log("notfound");
        }
        canvas = document.getElementsByTagName("canvas")[canvasCnt];
        ctx = canvas.getContext('2d');
        pencil();
        tmp++;
      },
      error: function(request, status, error){ // 통신 실패시 - 로그인 페이지 리다이렉트
        alert("로그인이 필요합니다.")
        window.location.replace("")
        //  alert("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
      },
    });
}

function addCanvas() {

    canvas = document.createElement('canvas'); // creates new canvas element
    var tmpid = `canvas${canvasCnt}`;
    canvas.id = tmpid; // gives canvas id
    canvas.height = height; //get original canvas height
    canvas.width = width; // get original canvas width
    canvas.setAttribute("onclick", "save();");
    canvas.style.border = "1px solid black";
    canvas.style.backgroundColor = "white";
    canvas.style.position = "static";
    canvas.style.left = "130px";
    canvas.style.top = "40px";
    canvas.style.marginBottom = "40px";
    document.getElementById("content").appendChild(canvas); // adds the canvas to the body element
    canvas = document.getElementsByTagName("canvas")[canvasCnt++]; //find new canvas we created
    ctx = canvas.getContext('2d');
    pencil();

    /*
    hold = false;
    fill_value = true, stroke_value = false;
    canvas_data = { "pencil": [], "line": [], "rectangle": [], "circle": [], "eraser": [] };
    */
    /*
    document.getElementById('canvasLine').innerHTML += 
    '<canvas id="canvas1" width="400" height="100" onclick="save()">Update your browser to support HTML5 Canvas</canvas>'
    // replaces the inner HTML of #someBox to a canvas
    tmp = document.getElementsByTagName("canvas");
    canvas = tmp[canvasCnt++];
    ctx = canvas.getContext("2d");
    base(ctx)
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