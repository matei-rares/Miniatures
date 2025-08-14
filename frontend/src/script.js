import * as THREE from 'three'
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import  RAPIER  from '@dimforge/rapier3d-compat';

// --- Three.js setup ---
const container = document.getElementById('app');
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.setSize(innerWidth, innerHeight);
renderer.shadowMap.enabled = true;

container.appendChild(renderer.domElement);

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0b1020);

const camera = new THREE.PerspectiveCamera(60, innerWidth / innerHeight, 0.1, 200);
camera.position.set(6, 4, 8);

const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(0, 1, 0);
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
const groundMat = new THREE.MeshStandardMaterial({ color: 0x20273a, metalness: 0.0, roughness: 0.9 });
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
    const groundColliderDesc = RAPIER.ColliderDesc.cuboid(20, 0.5, 20);
    world.createCollider(groundColliderDesc, groundBody);
}

// Utility: create a cube (Three + Rapier) and return pair
const boxes = [];
function makeCube({ position = [0, 1, 0], size = 1, color = 0x66aaff, dynamic = true, name = 'cube' }) {
    const half = size / 2;

    // Three mesh
    const geo = new THREE.BoxGeometry(size, size, size);
    const mat = new THREE.MeshStandardMaterial({ color, metalness: 0.1, roughness: 0.6 });
    const mesh = new THREE.Mesh(geo, mat);
    mesh.castShadow = true; mesh.receiveShadow = true; mesh.name = name;
    scene.add(mesh);

    // Rapier body + collider
    const rbDesc = (dynamic ? RAPIER.RigidBodyDesc.dynamic() : RAPIER.RigidBodyDesc.kinematicPositionBased())
        .setTranslation(position[0], position[1], position[2])
        .setCanSleep(true);
    const body = world.createRigidBody(rbDesc);
    const colDesc = RAPIER.ColliderDesc.cuboid(half, half, half)
        .setFriction(0.8)
        .setRestitution(0.2);
    world.createCollider(colDesc, body);

    boxes.push({ mesh, body });
    return { mesh, body };
}

// --- Create two cubes ---
makeCube({ position: [-1.25, 3, 0], size: 1, color: 0x66aaff, name: 'Cube A' });
makeCube({ position: [1.25, 5, 0], size: 1, color: 0xff7780, name: 'Cube B' });

// Simple reset helper (press R)
function resetCubes() {
    const starts = [[-1.25, 3, 0], [1.25, 5, 0]];
    boxes.forEach((b, i) => {
        b.body.setTranslation({ x: starts[i][0], y: starts[i][1], z: starts[i][2] }, true);
        b.body.setLinvel({ x: 0, y: 0, z: 0 }, true);
        b.body.setAngvel({ x: 0, y: 0, z: 0 }, true);
    });
}
addEventListener('keydown', (e) => { if (e.key.toLowerCase() === 'r') resetCubes(); });

// --- Animation loop with fixed-step accumulator ---
let last = performance.now();
const FIXED_TIMESTEP = 1 / 60; // seconds
let accumulator = 0;

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

    // Sync Three meshes from Rapier bodies
    for (const { mesh, body } of boxes) {
        const t = body.translation();
        const r = body.rotation();
        mesh.position.set(t.x, t.y, t.z);
        mesh.quaternion.set(r.x, r.y, r.z, r.w);
    }

    controls.update();
    renderer.render(scene, camera);
}
animate();

// Handle resize
addEventListener('resize', () => {
    camera.aspect = innerWidth / innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(innerWidth, innerHeight);
});