import * as THREE from 'three';
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
scene.background = new THREE.Color(0xd2f7ff);

//Camera
const camera = new THREE.PerspectiveCamera(60, innerWidth / innerHeight, 0.1, 200);
const cameraDefaultPos = new THREE.Vector3(3, 2, 4);
camera.position.set(cameraDefaultPos.x, cameraDefaultPos.y, cameraDefaultPos.z);

//View Target
const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(0, 0, 0);
controls.enableDamping = true;

// Lights
// const hemi = new THREE.HemisphereLight(0xd2f7ff, 0x222222, 1);
// scene.add(hemi);
const dir = new THREE.DirectionalLight(0xffffff, 5);
dir.position.set(5, 10, 4);
dir.castShadow = true;
dir.shadow.mapSize.set(1024, 1024);
scene.add(dir);

// --- Rapier physics setup ---
await RAPIER.init();
const gravity = { x: 0.0, y: -9.81, z: 0.0 };
const world = new RAPIER.World(gravity);

// Ground (physics): large static box under y=0
{
    // Ground (visual)
    const groundGeo = new THREE.PlaneGeometry(40, 40);
    const groundMat = new THREE.MeshStandardMaterial({ color: 0x2c4d04, metalness: 0.0, roughness: 1.9 });
    const ground = new THREE.Mesh(groundGeo, groundMat);
    ground.rotation.x = -Math.PI / 2;
    ground.receiveShadow = true;
    scene.add(ground);

    const groundBodyDesc = RAPIER.RigidBodyDesc.fixed().setTranslation(0, -0.5, 0);
    const groundBody = world.createRigidBody(groundBodyDesc);
    const groundColliderDesc = RAPIER.ColliderDesc.cuboid(20, 0.5, 20).setFriction(0.5);
    world.createCollider(groundColliderDesc, groundBody);
}

//-----------------------------------------------------------------------------------------------------------------------//
// Create a cube (Three + Rapier) and return pair
const boxes = [];
function makeCube({ position = [0, 1, 0], size = 1, color = 0x66aaff, name = 'cube' }) {
    const half = size / 2;

    // Three mesh (visuals)
    const geo = new THREE.BoxGeometry(size, size, size);
    const baseMat = new THREE.MeshStandardMaterial({ color, metalness: 0.1, roughness: 0.6, wireframe: true });
    const darkMat = new THREE.MeshStandardMaterial({ color: 0x335577, metalness: 0.1, roughness: 0.6 }); // make a face darker as the front of the cube
    const materials = [baseMat, baseMat, baseMat, baseMat, darkMat, baseMat];
    const mesh = new THREE.Mesh(geo, materials);
    mesh.castShadow = true;
    mesh.receiveShadow = true;
    mesh.name = name;
    scene.add(mesh);

    // Rapier body + collider (phisics)
    const rbDesc = RAPIER.RigidBodyDesc.dynamic().setTranslation(position[0], position[1], position[2]).setCanSleep(true).setLinearDamping(5.0); //Higher = stoping faster

    const rigidBody = world.createRigidBody(rbDesc);
    const colDesc = RAPIER.ColliderDesc.cuboid(half, half, half).setFriction(0.8).setRestitution(0.2);
    world.createCollider(colDesc, rigidBody);

    boxes.push({ mesh, rigidBody });
    return { mesh, rigidBody };
}
// --- Create two cubes ---
const initialCubePosition = [1.25, 3, 0];
makeCube({ position: initialCubePosition, size: 1, color: 0x66aaff, name: 'Cube A' });
makeCube({ position: [-1.25, 3, 0], size: 1, color: 0xff7780, name: 'Cube B' });
const mainCube = boxes[0];

const loader = new GLTFLoader();
let carMesh, carRigidBody;
let carRigidBodyHelper, carCollider;

const wheels = [];
let car = { mesh: 0, rigidBody: 0 }
const wheelOffsetY = 0.2;

loader.load(
    '/static/lows.gltf',
    function (gltf) {
        delete gltf.animations;
        delete gltf.cameras;
        delete gltf.asset;
        delete gltf.scenes;
        delete gltf.userData;
        const size = 1;
        let carGLTF = gltf.scene;
        carGLTF.scale.set(size, size, size);

        //    const geo = new THREE.BoxGeometry(size, size, size);
        // const baseMat = new THREE.MeshStandardMaterial({ color, metalness: 0.1, roughness: 0.6, wireframe: true });
        // const darkMat = new THREE.MeshStandardMaterial({ color: 0x335577, metalness: 0.1, roughness: 0.6 }); // make a face darker as the front of the cube
        // const materials = [baseMat, baseMat, baseMat, baseMat, darkMat, baseMat];
        // const mesh = new THREE.Mesh(geo, materials);
        // mesh.castShadow = true;
        // mesh.receiveShadow = true;
        // mesh.name = name;
        // scene.add(mesh);

        // // Rapier body + collider (phisics)
        // const rbDesc = RAPIER.RigidBodyDesc.dynamic().setTranslation(position[0], position[1], position[2]).setCanSleep(true).setLinearDamping(5.0); //Higher = stoping faster

        // const rigidBody = world.createRigidBody(rbDesc);
        // const colDesc = RAPIER.ColliderDesc.cuboid(half, half, half).setFriction(0.8).setRestitution(0.2);
        // world.createCollider(colDesc, rigidBody);

        // boxes.push({ mesh, rigidBody });
        const carObject = carGLTF.children[0];
        const carMaterial = carObject.material;
        const carGeometry = carObject.geometry;
        const carMesh = new THREE.Mesh(carGeometry, carMaterial);
        let carDefaultPostion = new THREE.Vector3(1, 2, 2);
        console.log(carObject);
        carMaterial.wireframe = true;
        carMesh.castShadow = true;
        carMesh.receiveShadow = true;
        carMesh.position.set(carDefaultPostion.x, carDefaultPostion.y, carDefaultPostion.z);
        scene.add(carMesh);

        carGeometry.computeBoundingBox();
        const rigidBodyDesc = RAPIER.RigidBodyDesc.dynamic().setTranslation(carMesh.position.x, carMesh.position.y, carMesh.position.z);
        const rigidBody = world.createRigidBody(rigidBodyDesc);
        const colliderDesc = RAPIER.ColliderDesc.trimesh(carGeometry.attributes.position.array, carGeometry.index.array);//vertices,indices
        world.createCollider(colliderDesc, rigidBody);

        rigidBody.setAngvel({ x: 5, y: 0, z: 0 }, true);
        car = { mesh: carMesh, rigidBody }

        for (const [index, wheel] of carObject.children.entries()) {
            const wheelGeometry = wheel.geometry
            const wheelMaterial = wheel.material
            const wheelMesh = new THREE.Mesh(wheelGeometry, wheelMaterial)
            wheelMesh.castShadow = true;
            wheelMesh.receiveShadow = true;
            wheelMesh.position.x += carDefaultPostion.x;
            wheelMesh.position.y += carDefaultPostion.y;
            wheelMesh.position.z += carDefaultPostion.z;

            console.log(index)
            scene.add(wheelMesh)

            wheelGeometry.computeBoundingBox();
            const rigidBodyDesc = RAPIER.RigidBodyDesc.dynamic().setTranslation(wheelMesh.position.x, wheelMesh.position.y, wheelMesh.position.z);
            const rigidBody = world.createRigidBody(rigidBodyDesc);
            const colliderDesc = RAPIER.ColliderDesc.trimesh(wheelGeometry.attributes.position.array, wheelGeometry.index.array);//vertices,indices
            world.createCollider(colliderDesc, rigidBody);
            rigidBody.setAngvel({ x: 5, y: 0, z: 0 }, true);

            wheels.push({ mesh: wheelMesh, rigidBody })

        }


    },
    // called when loading has errors
    function (error) {
        console.log(error);
        console.log('An error happened');
    }
);

// Simple reset helper (press R)
function resetCubes() {
    const starts = [[-1.25, 3, 0], initialCubePosition];
    boxes.forEach((b, i) => {
        b.rigidBody.setTranslation({ x: starts[i][0], y: starts[i][1], z: starts[i][2] }, true);
        b.rigidBody.setLinvel({ x: 0, y: 0, z: 0 }, true);
        b.rigidBody.setAngvel({ x: 0, y: 0, z: 0 }, true);
    });
}

//Bind Keyboard keys Listeners (for Movement, reset)
const pressed = {};
{
    window.addEventListener('keydown', (e) => (pressed[e.code] = true));
    window.addEventListener('keyup', (e) => (pressed[e.code] = false));
}

function processMovement() {
    let moveX = 0;
    let moveZ = 0;
    const movementSpeed = 6.0;
    const turnSpeed = 10.0; // radians/sec
    // check keys
    if (pressed['KeyW']) {
        moveZ -= 1;
    } // forward
    if (pressed['KeyS']) {
        moveZ += 1;
    } // backward
    if (pressed['KeyA']) {
        moveX -= 1;
    } // left
    if (pressed['KeyD']) {
        moveX += 1;
    } // right

    // create a direction vector
    let dir = new THREE.Vector3(moveX, 0, moveZ);

    // normalize so diagonal speed = straight speed
    if (dir.length() > 0) {
        dir.normalize();

        // apply movement (example: impulse or set linvel)

        //obj.body.applyImpulse({ x: 5, y: 0, z: -5 }, true);
        //obj.body.setAngvel({ x: 0, y: 0, z: 0 }, true);
        mainCube.rigidBody.setLinvel(
            {
                x: dir.x * movementSpeed,
                y: mainCube.rigidBody.linvel().y, // keep current vertical velocity (gravity/jumps)
                z: dir.z * movementSpeed,
            },
            true
        );

        // 1. target yaw
        const targetAngle = Math.atan2(dir.x, dir.z);

        // 2. current yaw from Rapier body quaternion
        const rot = mainCube.rigidBody.rotation();
        const q = new THREE.Quaternion(rot.x, rot.y, rot.z, rot.w);
        const euler = new THREE.Euler().setFromQuaternion(q, 'YXZ');
        const currentAngle = euler.y;

        // 3. shortest angle difference
        let delta = targetAngle - currentAngle;
        delta = Math.atan2(Math.sin(delta), Math.cos(delta)); // normalize to [-pi, pi]

        // 4. choose rotation speed
        const angVel = delta * turnSpeed;

        // 5. set angular velocity around Y axis
        mainCube.rigidBody.setAngvel({ x: 0, y: angVel, z: 0 }, true);
    }
}

// --- Animation loop with fixed-step accumulator ---
let last = performance.now();
const FIXED_TIMESTEP = 1 / 60; // seconds
let accumulator = 0;

function updateMeshPositionByRigidBody(dict) {
    const t = dict.rigidBody.translation();
    const r = dict.rigidBody.rotation();
    dict.mesh.position.set(t.x, t.y, t.z);
    dict.mesh.quaternion.set(r.x, r.y, r.z, r.w);
}

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

    if (pressed['KeyR']) resetCubes();

    processMovement();

    // Sync Three meshes from Rapier bodies
    for (const box of boxes) {
        updateMeshPositionByRigidBody(box)
    }
//
     const t = car.rigidBody.translation();
    const r = car.rigidBody.rotation();
    car.mesh.position.set(t.x, t.y+wheelOffsetY, t.z);
    car.mesh.quaternion.set(r.x, r.y, r.z, r.w);
//
    for (const wheel of wheels) {
        let t = wheel.rigidBody.translation();
        let r = wheel.rigidBody.rotation();
        //
        wheel.mesh.position.set(t.x, t.y , t.z);
        wheel.mesh.quaternion.set(r.x, r.y, r.z, r.w);
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
    renderer.setSize(innerWidth + 10, innerHeight + 10);
});
