var bh = 420;
var p = 0;
//var cw = bw + (p*2) + 1;
var canvas = document.getElementById("canvas");
var ctx = canvas.getContext("2d");

var interval;
var grid = [];
var pos,last,food_pos;
var food=false, end=false;
var score=0;
var denom=0

var colMap = {
  0: "#292b2c",
  1: "#2cbf53",
  2: "#0c6624",
  3: "#bab709",
};

action = {
    'up': [0,-1],
    'down': [0,1],
    'left': [-1,0],
    'right': [1,0],
}

action_enc = {
    'up': 0,
    'down': 1,
    'left': 2,
    'right': 3,
}

function getRandomInt(max) {
  return Math.floor(Math.random() * Math.floor(max));
}

function fetch_weights() {

}

function setMem(n) {
  mem = n;
  fetch_weights();
}

function setGrid(num) {
  n = num;
  fetch_weights();
}

function update_score() {
  document.getElementById("score").innerHTML = "Score: "+score.toString();
}

function draw_board() {
  //console.log(n);
  var size = bh/n;
  for (var x=0; x<n; x++) {
    for (var y=0; y<n; y++) {
      ctx.beginPath();
      ctx.rect(x*size, y*size, size, size);
      ctx.fillStyle = colMap[grid[x][y]];
      ctx.fill();
      ctx.closePath();
    }
  }
}

function get_state() {
  if (last.length < mem) {
    for (let i=0;i<mem;i++) {
      last.unshift(-1);
    }
  }

  if (mem == 3) {
    return  "("+pos[pos.length-1][1].toString()+", "+pos[pos.length-1][0].toString()
            +", "+food_pos[1].toString()+", "+food_pos[0].toString()+", "
            +last[last.length-1].toString()+", "+last[last.length-2].toString()
            +", "+last[last.length-3].toString()+")";
  }
  else if (mem == 2) {
    return  "("+pos[pos.length-1][1].toString()+", "+pos[pos.length-1][0].toString()
            +", "+food_pos[1].toString()+", "+food_pos[0].toString()+", "
            +last[last.length-1].toString()+", "+last[last.length-2].toString()+")";
  }
  else if (mem == 1) {
    return  "("+pos[pos.length-1][1].toString()+", "+pos[pos.length-1][0].toString()
            +", "+food_pos[1].toString()+", "+food_pos[0].toString()
            +", "+last[last.length-1].toString()+")";
  }
  else if (mem == 0) {
    return  "("+pos[pos.length-1][1].toString()+", "+pos[pos.length-1][0].toString()
            +", "+food_pos[1].toString()+", "+food_pos[0].toString()+")";
  }
}

function create_food() {
  let a = [];
  for (let i=0;i<n;i++) {
    for (let j=0;j<n;j++) {
      if (grid[i][j] == 0 && !(i==Math.floor(n/2) && j==Math.floor(n/2))) {
            a.push([i,j]);
      }
    }
  }
  let ind = getRandomInt(a.length);
  food_pos[0] = a[ind][0];
  food_pos[1] = a[ind][1];
  grid[food_pos[0]][food_pos[1]] = 3;
  food=true;
}

function move_rand(state) {
  let ind = getRandomInt(4);
  if (ind == 0) {
    return 'up';
  }
  else if (ind == 1) {
    return 'down';
  }
  else if (ind == 2) {
    return 'left';
  }
  else if (ind == 3) {
    return 'right';
  }
}

function move(state) {
  let mx = Math.max(...weights[state][0]);
  let a=[];
  for (let i=0;i<4;i++) {
    if (Math.abs(weights[state][0][i] - mx) < 0.001) {
      a.push(i);
    }
  }
  let ind = getRandomInt(a.length);
  ind = a[ind];
  //console.log(a,ind);
  if (ind == 0) {
    return 'up';
  }
  if (ind == 1) {
    return 'down';
  }
  if (ind == 2) {
    return 'left';
  }
  if (ind == 3) {
    return 'right';
  }
}

function next() {
  draw_board();
  update_score();

  st = get_state();
  //console.log(mem)
  //console.log('s',st);
  //console.log('w',weights[st]);
  act = move(st);
  //console.log('a',act);
  last.push(action_enc[act]);
  grid[pos[pos.length-1][0]][pos[pos.length-1][1]] = 1;
  let x=pos[pos.length-1][0],y=pos[pos.length-1][1];
  x += action[act][0];
  y += action[act][1];
  if (!(0<=x && x<n && 0<=y && y<n)) { // snake hits wall
    end = true;
  }
  else if (grid[x][y] == 1) { // snake hits itself
    end = true;
    pos.push([x,y])
    grid[x][y] = 2;
  }
  else if ( grid[pos[pos.length-1][0]][pos[pos.length-1][1]] == 3 ||  grid[x][y] == 3) { //snake finds food
    create_food();
    score += 1;
    grid[pos[pos.length-1][0]][pos[pos.length-1][1]] = 1;
    pos.push([x,y])
    grid[x][y] = 2;
  }
  else { // move
    grid[pos[0][0]][pos[0][1]] = 0;
    pos.shift();
    pos.push([x,y])
    grid[x][y] = 2;
  }

  if (end) {
    denom+=1;
    //reset();
    clearInterval(interval); // Needed for Chrome to end game
  }
}

function reset() {
  console.log(score/denom);
  grid = [];
  for(let i = 0; i < n; i++) {
    let l = []
    for(let j = 0; j < n; j++) {
      l.push(0);
    } grid.push(l);
  }
  pos = [[Math.floor(n/2),y=Math.floor(n/2)]];
  grid[pos[0][0]][pos[0][1]]=2
  last = [];
  food_pos = [-1,-1];
  food=false; end=false;
  score = 0;
  //console.log(score);
  create_food();

  clearInterval(interval); // Needed for Chrome to end game
  interval = setInterval(next, 200);
}

function mod_reset() {
  cons
  reset();
}

reset();
