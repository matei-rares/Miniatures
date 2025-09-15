import * as THREE from 'three'
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import RAPIER from '@dimforge/rapier3d-compat';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';


// --- Three.js setup ---
const container = document.getElementById('app');
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.setSize(innerWidth, innerHeight);
renderer.shadowMap.enabled = true;

container.appendChild(renderer.domElement);

// Scene
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0b5020);

//Camera
const camera = new THREE.PerspectiveCamera(60, innerWidth / innerHeight, 0.1, 200);
const cameraDefaultPos = new THREE.Vector3(0, 5, 7)
camera.position.set(cameraDefaultPos.x, cameraDefaultPos.y, cameraDefaultPos.z);

//View Target
const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(0, 0, 0);
controls.enableDamping = true;

// Lights
const hemi = new THREE.HemisphereLight(0xffffff, 0x333366, 0.6);
scene.add(hemi);
const dir = new THREE.DirectionalLight(0xffffff, 1.0);
dir.position.set(5, 10, 4);
dir.castShadow = true;
dir.shadow.mapSize.set(1024, 1024);
scene.add(dir);

// Ground (visual)
const groundGeo = new THREE.PlaneGeometry(40, 40);
const groundMat = new THREE.MeshStandardMaterial({ color: 0x20273a, metalness: 0.0, roughness: 1.9 });
const ground = new THREE.Mesh(groundGeo, groundMat);
ground.rotation.x = -Math.PI / 2;
ground.receiveShadow = true;
scene.add(ground);

// --- Rapier physics setup ---
await RAPIER.init();
const gravity = { x: 0.0, y: -9.81, z: 0.0 };
const world = new RAPIER.World(gravity);

// Ground (physics): large static box under y=0
{
    const groundBodyDesc = RAPIER.RigidBodyDesc.fixed().setTranslation(0, -0.5, 0);
    const groundBody = world.createRigidBody(groundBodyDesc);
    const groundColliderDesc = RAPIER.ColliderDesc.cuboid(20, 0.5, 20).setFriction(0.5);
    world.createCollider(groundColliderDesc, groundBody);
}

// Utility: create a cube (Three + Rapier) and return pair
const boxes = [];
function makeCube({ position = [0, 1, 0], size = 1, color = 0x66aaff, name = 'cube' }) {
    const half = size / 2;

    // Three mesh (visuals)
    const geo = new THREE.BoxGeometry(size, size, size);
    const baseMat = new THREE.MeshStandardMaterial({ color, metalness: 0.1, roughness: 0.6, wireframe: true });
    const darkMat = new THREE.MeshStandardMaterial({ color: 0x335577, metalness: 0.1, roughness: 0.6 }); // make a face darker as the front of the cube
    const materials = [baseMat, baseMat, baseMat, baseMat, darkMat, baseMat];
    const mesh = new THREE.Mesh(geo, materials);
    mesh.castShadow = true; mesh.receiveShadow = true; mesh.name = name;
    scene.add(mesh);

    // Rapier body + collider (phisics)
    const rbDesc = RAPIER.RigidBodyDesc.dynamic()
        .setTranslation(position[0], position[1], position[2])
        .setCanSleep(true)
        .setLinearDamping(5.0); //Higher = stoping faster

    const body = world.createRigidBody(rbDesc);
    const colDesc = RAPIER.ColliderDesc.cuboid(half, half, half)
        .setFriction(0.8)
        .setRestitution(0.2);
    world.createCollider(colDesc, body);

    boxes.push({ mesh, body });
    return { mesh, body };
}



const loader = new GLTFLoader();
let player;

loader.load('/static/model.glb', (gltf) => {
  player = gltf.scene;
  player.scale.set(0.5,0.5, 0.5); // resize
  scene.add(player);
}, undefined, (error) => {
  console.error(error);
});

// --- Create two cubes ---
const initialCubePosition = [1.25, 3, 0]
makeCube({ position: initialCubePosition, size: 1, color: 0x66aaff, name: 'Cube A' });
makeCube({ position: [-1.25, 3, 0], size: 1, color: 0xff7780, name: 'Cube B' });
const mainCube = boxes[0]

// Simple reset helper (press R)
function resetCubes() {
    const starts = [[-1.25, 3, 0], initialCubePosition];
    boxes.forEach((b, i) => {
        b.body.setTranslation({ x: starts[i][0], y: starts[i][1], z: starts[i][2] }, true);
        b.body.setLinvel({ x: 0, y: 0, z: 0 }, true);
        b.body.setAngvel({ x: 0, y: 0, z: 0 }, true);
    });
}

//Bind Keyboard keys Listeners (for Movement, reset)
const pressed = {}
{
    window.addEventListener("keydown", e => pressed[e.code] = true);
    window.addEventListener("keyup", e => pressed[e.code] = false);
}



function processMovement() {
    let moveX = 0;
    let moveZ = 0;
    const speed = 4.0;
    const turnSpeed = 10.0; // radians/sec
    // check keys
    if (pressed["KeyW"]) { moveZ -= 5; }   // forward
    if (pressed["KeyS"]) { moveZ += 5; }   // backward
    if (pressed["KeyA"]) { moveX -= 5; }  // left
    if (pressed["KeyD"]) { moveX += 5; }  // right

    // create a direction vector
    let dir = new THREE.Vector3(moveX, 0, moveZ);

    // normalize so diagonal speed = straight speed
    if (dir.length() > 0) {
        dir.normalize();

        // apply movement (example: impulse or set linvel)

        //obj.body.applyImpulse({ x: 5, y: 0, z: -5 }, true);
        //obj.body.setAngvel({ x: 0, y: 0, z: 0 }, true);
        mainCube.body.setLinvel({
            x: dir.x * speed,
            y: mainCube.body.linvel().y, // keep current vertical velocity (gravity/jumps)
            z: dir.z * speed,
        }, true
        );


        // 1. target yaw
        const targetAngle = Math.atan2(dir.x, dir.z);

        // 2. current yaw from Rapier body quaternion
        const rot = mainCube.body.rotation();
        const q = new THREE.Quaternion(rot.x, rot.y, rot.z, rot.w);
        const euler = new THREE.Euler().setFromQuaternion(q, 'YXZ');
        const currentAngle = euler.y;

        // 3. shortest angle difference
        let delta = targetAngle - currentAngle;
        delta = Math.atan2(Math.sin(delta), Math.cos(delta)); // normalize to [-pi, pi]

        // 4. choose rotation speed
        const angVel = delta * turnSpeed;

        // 5. set angular velocity around Y axis
        mainCube.body.setAngvel({ x: 0, y: angVel, z: 0 }, true);

    }
}

// --- Animation loop with fixed-step accumulator ---
let last = performance.now();
const FIXED_TIMESTEP = 1 / 60; // seconds
let accumulator = 0;

//main function--------------------------------------------
function animate(now = performance.now()) {
    requestAnimationFrame(animate);
    const dt = Math.min(0.033, (now - last) / 1000);
    last = now;
    accumulator += dt;
    // Step physics at a fixed rate for stability
    while (accumulator >= FIXED_TIMESTEP) {
        world.timestep = FIXED_TIMESTEP; // optional explicit step
        world.step();
        accumulator -= FIXED_TIMESTEP;
    }


    if (pressed["KeyR"]) resetCubes();

    processMovement();


    // Sync Three meshes from Rapier bodies
    for (const { mesh, body } of boxes) {
        const t = body.translation();
        const r = body.rotation();
        mesh.position.set(t.x, t.y, t.z);
        mesh.quaternion.set(r.x, r.y, r.z, r.w);
    }

    controls.update();
    controls.target.set(mainCube.mesh.position.x, mainCube.mesh.position.y, mainCube.mesh.position.z);
    camera.position.set(mainCube.mesh.position.x + cameraDefaultPos.x, mainCube.mesh.position.y + cameraDefaultPos.y, mainCube.mesh.position.z + cameraDefaultPos.z);

    renderer.render(scene, camera);
}
animate();

// Handle resize
addEventListener('resize', () => {
    camera.aspect = innerWidth / innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(innerWidth, innerHeight);
});