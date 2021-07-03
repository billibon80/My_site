var _createClass = (function() {
  function defineProperties(target, props) {
    for (var i = 0; i < props.length; i++) {
      var descriptor = props[i];
      descriptor.enumerable = descriptor.enumerable || false;
      descriptor.configurable = true;
      if ("value" in descriptor) descriptor.writable = true;
      Object.defineProperty(target, descriptor.key, descriptor);
    }
  }
  return function(Constructor, protoProps, staticProps) {
    if (protoProps) defineProperties(Constructor.prototype, protoProps);
    if (staticProps) defineProperties(Constructor, staticProps);
    return Constructor;
  };
})();

function _classCallCheck(instance, Constructor) {
  if (!(instance instanceof Constructor)) {
    throw new TypeError("Cannot call a class as a function");
  }
}

var options = {
  drag: 1,
  gravity: 0,
  lifespan: 161,
  maxSpeed: 100,
  maxParticles: 500,
  particleColors: ["242, 167, 30", "241, 207, 160", "211, 79, 39"],
  particlesPerPress: 400,
  jitter: 0,
  randomness: 1,
  size: 10,
  sizeRange: 10,
  shrinkSpeed: 0.1
};

var ParticleSystem = (function() {
  function ParticleSystem() {
    _classCallCheck(this, ParticleSystem);
    this.particles = [];
  }
  _createClass(ParticleSystem, [
    {
      key: "addParticle",
      value: function addParticle(opts) {
        for (var i = 0; i < opts.numToAdd; i++) {
          this.particles.push(new Particle(opts));
        }
        while (this.particles.length > options.maxParticles) {
          this.removeParticle();
        }
      }
    },
    {
      key: "removeParticle",
      value: function removeParticle() {
        this.particles.shift();
      }
    },
    {
      key: "update",
      value: function update() {
        for (var i = 0; i < this.particles.length; i++) {
          if (this.particles[i].lifespan > 0) {
            this.particles[i].update();
          }
        }
      }
    },
    {
      key: "draw",
      value: function draw() {
        for (var i = 0; i < this.particles.length; i++) {
          this.particles[i].draw();
        }
      }
    }
  ]);
  return ParticleSystem;
})();

var Particle = (function() {
  function Particle(opts) {
    _classCallCheck(this, Particle);
    // How many frames particle will live
    this.lifespan = options.lifespan;

    // Color
    this.color =
      options.particleColors[
        Math.floor(Math.random() * options.particleColors.length)
      ];

    // Size
    this.size = options.size;
    this.size += Math.random() * options.sizeRange - options.sizeRange / 2;

    // Position and velocity
    this.x = opts.x;
    this.y = opts.y;

    var velXMin = -opts.leftSpread / (this.lifespan / 10);
    var velXMax = opts.rightSpread / (this.lifespan / 10);
    var velYMin = -opts.topSpread / (this.lifespan / 10);
    var velYMax = opts.bottomSpread / (this.lifespan / 10);

    var velXRange = velXMax - velXMin;
    var velYRange = velYMax - velYMin;

    var originLeftPercent =
      opts.leftSpread / (opts.leftSpread + opts.rightSpread);
    var originTopPercent =
      opts.topSpread / (opts.topSpread + opts.bottomSpread);

    this.velX = Math.random() * velXRange - velXRange * originLeftPercent;
    this.velY = Math.random() * velYRange - velYRange * originTopPercent;

    // Values for perlin noise
    this.xOff = Math.random() * 6400;
    this.yOff = Math.random() * 6400;

    // Opacity is reduced as lifespan gets close to 0
    this.opacity = 1;

    // Added to velY every frame
    this.gravity = options.gravity;

    // Multiply with velocity every frame
    this.drag = options.drag;
    this.drag = options.drag;
  }
  _createClass(Particle, [
    {
      key: "update",
      value: function update() {
        // Add gravity force to the y velocity
        this.velY += this.gravity;

        // Add randomness with perlin noise
        var randomX = noise.simplex2(this.xOff, 0);
        var randomY = noise.simplex2(this.yOff, 0);
        this.velX += randomX / (10 / options.randomness);
        this.velY += randomY / (10 / options.randomness);
        this.xOff += options.jitter;
        this.yOff += options.jitter;

        // // Apply drag
        this.velX *= this.drag;
        this.velY *= this.drag;

        // And the velocity to the position
        this.x += this.velX;
        this.y += this.velY;

        // Apply fade
        this.opacity = this.lifespan / 100;

        // Apply shrink
        this.size -= options.shrinkSpeed;
        this.size = Math.max(0, this.size);

        // Update lifespan
        this.lifespan -= 1;

        if (this.size <= 0.1 || this.opacity <= 0.01) {
          this.lifespan = 0;
        }
      }
    },
    {
      key: "draw",
      value: function draw() {
        // set the fill style to have the right alpha
        context.fillStyle = "rgba(" + this.color + ", " + this.opacity + ")";

        // draw a circle of the required size
        context.beginPath();
        context.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        context.closePath();

        // and fill it
        context.fill();
      }
    }
  ]);
  return Particle;
})();

function loop() {
  // Clear the canvas
  context.clearRect(0, 0, screenWidth, screenHeight);

  // Update and draw paricles
  ps.update();
  ps.draw();

  // RAF
  requestAnimationFrame(loop);
}

function explode(el, x, y) {
  var dialog = document.querySelector(".dialog");
  var rect = dialog.getBoundingClientRect();

  dialog.classList.remove("is-in");
  ps.addParticle({
    numToAdd: options.particlesPerPress,
    x: x,
    y: y,
    leftSpread: x - rect.left,
    rightSpread: rect.right - x,
    topSpread: y - rect.top,
    bottomSpread: rect.bottom - y
  });
}

// Globals
var ps = void 0;
var context = void 0;

var mouseX = void 0;
var mouseY = void 0;
var isPointerPressed = false;

// Get screen size variables
var screenWidth = window.innerWidth;
var screenHeight = window.innerHeight;
var halfWidth = window.innerWidth / 2;
var halfHeight = window.innerHeight / 2;

function updateCanvasAndScreenVars() {
  screenWidth = window.innerWidth;
  screenHeight = window.innerHeight;
  halfWidth = window.innerWidth / 2;
  halfHeight = window.innerHeight / 2;
  canvas.width = screenWidth;
  canvas.height = screenHeight;
}

// Initialize
console.clear();

// Create Canvas element
var canvas = document.createElement("canvas");
context = canvas.getContext("2d");

$(".shaker").append(canvas);

updateCanvasAndScreenVars();

$(window).on("resize", updateCanvasAndScreenVars);

$("button").on("click", function(e) {
  var shaker = document.querySelector(".shaker");
  shaker.classList.add("is-shaking");
  var dialog = document.querySelector(".dialog");

  explode(dialog, e.pageX, e.pageY);
  $(".dialog").hide();
  $(".message").fadeIn(2000);

  setTimeout(function() {
    $(dialog).css("z-index", 1);
  }, 200);
});

$("#stamp-footer").on("click", function(e) {
  var message = document.getElementById("part-one-message");
  message.scrollTop = 0;
  $(".message").hide();
  $(".dialog").show();
});

// Perlin Noise
noise.seed(Math.floor(Math.random() * 64000));

// Create Particle System
ps = new ParticleSystem();

loop();
