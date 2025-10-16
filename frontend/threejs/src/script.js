import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import RAPIER from '@dimforge/rapier3d-compat';
import { CubeObject } from './objects/cubes';
import { CarObject } from './objects/car';
import {RapierDebugRenderer} from './objects/RapierDebugRenderer'
import GUI from 'lil-gui'
//https://github.com/brunosimon/folio-2019/tree/master/static/models/car
/**
 * Debug
 */
const gui = new GUI()

// Renderer
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.setSize(innerWidth, innerHeight);
renderer.shadowMap.enabled = true;
document.getElementById('app').appendChild(renderer.domElement);

// Scene
const scene = new THREE.Scene();
scene.background = new THREE.Color(0xd2f7ff);

//Camera settings
const camera = new THREE.PerspectiveCamera(60, innerWidth / innerHeight, 0.1, 200);
const cameraDefaultPos = new THREE.Vector3(5, 3, 4);
camera.position.set(cameraDefaultPos.x, cameraDefaultPos.y, cameraDefaultPos.z);

//View Target (Controlling camera)
const controls = new OrbitControls(camera, renderer.domElement);
controls.enabled = true; //enable moving camera with mouse
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
const gravity = { x: 0.0, y: -20.81, z: 0.0 };
const world = new RAPIER.World(gravity);

// Ground (visual)
const groundGeo = new THREE.PlaneGeometry(40, 40);
const groundMat = new THREE.MeshStandardMaterial({ color: 0x2c4d04, metalness: 0.0, roughness: 1.9 });
const ground = new THREE.Mesh(groundGeo, groundMat);
ground.rotation.x = -Math.PI / 2;
ground.receiveShadow = true;
scene.add(ground);

// Ground (physics): large static box under y=0
const groundBodyDesc = RAPIER.RigidBodyDesc.fixed().setTranslation(0, -0.5, 0);
const groundBody = world.createRigidBody(groundBodyDesc);
const groundColliderDesc = RAPIER.ColliderDesc.cuboid(20, 0.5, 20).setFriction(0.5);
world.createCollider(groundColliderDesc, groundBody);

// Handle resize
// addEventListener('resize', () => {
//   camera.aspect = innerWidth / innerHeight;
//   camera.updateProjectionMatrix();
//   renderer.setSize(innerWidth + 10, innerHeight + 10);
// });


//Declaration of objects--------------------------------------

const CUBES = new CubeObject(scene, world)
const CAR= new CarObject(scene,world,gui)
const debugRenderer = new RapierDebugRenderer(scene, world);


// --- Animation loop with fixed-step accumulator ---
let last = performance.now();
const FIXED_TIMESTEP = 1 / 60; // seconds
let accumulator = 0;

//main function--------------------------------------------
function animate(now = performance.now()) {
  requestAnimationFrame(animate);

  // Step physics at a fixed rate for stability
  const dt = Math.min(0.033, (now - last) / 1000);
  last = now;
  accumulator += dt;
  while (accumulator >= FIXED_TIMESTEP) {
    world.timestep = FIXED_TIMESTEP; // optional explicit step
    world.step();
    accumulator -= FIXED_TIMESTEP;
  }
  //Use of objects--------------------------------------------

  CUBES.update();
  CAR.update();
  debugRenderer.update()
  
  //End of main function---------------------------------------
  controls.update();
  //controls.target.set(0, 0, 0 );
  //camera.position.set(mainCube.mesh.position.x + cameraDefaultPos.x, mainCube.mesh.position.y + cameraDefaultPos.y, mainCube.mesh.position.z + cameraDefaultPos.z);
  renderer.render(scene, camera);
}
animate();
