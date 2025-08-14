import * as THREE from 'three';




// Scene
const scene = new THREE.Scene();

// Renderer
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setClearColor(0x001A00, 1); // 0xffffff = white, 1 = opacity
document.body.appendChild(renderer.domElement);

//Grid
const gridHelper = new THREE.GridHelper(100, 100); 
scene.add(gridHelper);

//Axes
const axesHelper = new THREE.AxesHelper(5); // size 5 units
scene.add(axesHelper);


//Listen keys
const keys = {};
document.addEventListener('keydown', (e) => keys[e.key.toLowerCase()] = true);
document.addEventListener('keyup', (e) => keys[e.key.toLowerCase()] = false);  





//Camera
const aspect = window.innerWidth / window.innerHeight;
const d = 6; // zoom level (smaller = zoom in)
const camera = new THREE.OrthographicCamera(
  -d * aspect, // left
  d * aspect,  // right
  d,           // top
  -d,          // bottom
  0,           // near
  100         // far
);

// Set camera position for isometric look
const offset = new THREE.Vector3(10, 6, 0); // offset from cube
camera.position.copy(offset); 
camera.lookAt(scene.position);

// Get camera's forward vector (direction it is looking at)
// Project onto XZ plane (ignore Y)
const forward = camera.getWorldDirection(new THREE.Vector3()).setY(0).normalize();
const left = new THREE.Vector3(forward.z, 0, -forward.x).normalize();
const right = new THREE.Vector3(-forward.z, 0, forward.x).normalize();

//CONSTANTS
const CUBE_SPEED = 0.1;




// Cube
const geometry = new THREE.BoxGeometry();
const geometry1 = new THREE.BoxGeometry();
const material = new THREE.MeshBasicMaterial({ color: 0x300000 });
const material2 = new THREE.MeshBasicMaterial({ color: 0xfF0000 });
const cube = new THREE.Mesh(geometry, material);
const cube1 = new THREE.Mesh(geometry1, material2);


cube1.position.set(2, 0, -3); // set position after creation

const box1 = new THREE.Box3().setFromObject(cube);
const box2 = new THREE.Box3().setFromObject(cube1);


scene.add(cube);
scene.add(cube1);





function handleCollision(){
  // Update the bounding boxes every frame
  box1.setFromObject(cube);
  box2.setFromObject(cube1);

  // Check for collision
  if (box1.intersectsBox(box2)) {
      console.log("Collision detected!");
      // Optional: show text on canvas
      console.log("collision")

      // Calculate push direction: from cube1 to cube2
    const pushDir = new THREE.Vector3().subVectors(cube1.position, cube.position).normalize();

    // Move cube2 slightly away along that direction
    const pushStrength = 0.1; 
    cube1.position.add(pushDir.multiplyScalar(pushStrength));
  } else {
      
  }
}

function handleCubeMovement(){
  const move = new THREE.Vector3();

  if (keys['w']) move.add(forward);
  if (keys['s']) move.add(forward.clone().negate());
  if (keys['a']) move.add(left);
  if (keys['d']) move.add(right);

  // Prevent diagonal speed boost
  if (move.length() > 0) {
    move.normalize();
    move.multiplyScalar(CUBE_SPEED);
    cube.position.add(move);
  }
}

function handleCamera(){
  camera.position.copy(cube.position).add(offset); // move camera relative to cubed
  camera.lookAt(cube.position);
}






// Animate
function animate() {
  requestAnimationFrame(animate);
  handleCubeMovement();
  handleCollision();
  handleCamera();
  renderer.render(scene, camera);
}
animate();




