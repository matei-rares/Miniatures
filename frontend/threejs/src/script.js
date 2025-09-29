import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import RAPIER from '@dimforge/rapier3d-compat';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import GUI from 'lil-gui'
import { CubeObject } from './cubes';
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





//-----------------------------------------------------------------------------------------------------------------------//


const loader = new GLTFLoader();
const wheels = [];
let car = { mesh: 0, rigidBody: 0 };
loader.load(
  '/static/lowsss.gltf',
  function (gltf) {
    delete gltf.animations;
    delete gltf.cameras;
    delete gltf.asset;
    delete gltf.scenes;
    delete gltf.userData;
    const size = 10;
    let carGLTF = gltf.scene;
    carGLTF.scale.set(size, size, size);

    const carObject = carGLTF.children[0];
    const carMaterial = carObject.material;
    const carGeometry = carObject.geometry;
    const carMesh = new THREE.Mesh(carGeometry, carMaterial);
    let carDefaultPostion = new THREE.Vector3(1, 3, 2);
    console.log(carObject);
    carMaterial.wireframe = true;
    carMesh.castShadow = true;
    carMesh.receiveShadow = true;
    carMesh.position.set(carDefaultPostion.x, carDefaultPostion.y, carDefaultPostion.z);
    scene.add(carMesh);

    carGeometry.computeBoundingBox();
    const rigidBodyDesc = RAPIER.RigidBodyDesc.dynamic().setTranslation(carMesh.position.x, carMesh.position.y, carMesh.position.z).setGravityScale(0); // 🚀 This makes it weightless

    const rigidBody = world.createRigidBody(rigidBodyDesc);
    
    const colliderDesc = RAPIER.ColliderDesc.trimesh(carGeometry.attributes.position.array, carGeometry.index.array); //vertices,indices
    world.createCollider(colliderDesc, rigidBody);

    //rigidBody.setAngvel({ x: 5, y: 0, z: 0 }, true);
    car = { mesh: carMesh, rigidBody };

    for (const [index, wheel] of carObject.children.entries()) {
      
      const wheelGeometry = wheel.geometry;
      const wheelMaterial = wheel.material;
      console.log(wheelMaterial)
      const wheelMesh = new THREE.Mesh(wheelGeometry, wheelMaterial);
      wheelMesh.castShadow = true;
      wheelMesh.receiveShadow = true;
      wheelMesh.position.x += carDefaultPostion.x;
       wheelMesh.position.y += 1;
      wheelMesh.position.z += carDefaultPostion.z;



      console.log(index);
      scene.add(wheelMesh);

      wheelGeometry.computeBoundingBox();
      const rigidBodyDesc = RAPIER.RigidBodyDesc.dynamic().setTranslation(wheelMesh.position.x, wheelMesh.position.y, wheelMesh.position.z);
      const rigidBody = world.createRigidBody(rigidBodyDesc);
      const colliderDesc = RAPIER.ColliderDesc.trimesh(wheelGeometry.attributes.position.array, wheelGeometry.index.array); //vertices,indices
      world.createCollider(colliderDesc, rigidBody);
      //rigidBody.setAngvel({ x: 5, y: 0, z: 0 }, true);


      wheels.push({ mesh: wheelMesh, rigidBody });

const rbPosition = rigidBody.translation(); // returns {x, y, z}

      
    }
    console.log(wheels);


//?????????????????????????????????????
//  world.createImpulseJoint(RAPIER.JointData.fixed(
//     { x: -1.0 , y: 0.0, z: -1.0 }, { w: 1.0, x: 0.0, y: 0.0, z: 0.0 },
//     { x: -1.0 , y: 1.0, z: -1.0 }, { w: 1.0, x: 0.0, y: 0.0, z: 0.0 }
// ), car.rigidBody, wheels[0].rigidBody, true);
//  world.createImpulseJoint(RAPIER.JointData.fixed(
//     { x: 1.0 , y: 0.0, z: -1.0 }, { w: 1.0, x: 0.0, y: 0.0, z: 0.0 },
//     { x: 1.0 , y: 1.0, z: -1.0 }, { w: 1.0, x: 0.0, y: 0.0, z: 0.0 }
// ), car.rigidBody, wheels[0].rigidBody, true);
// world.createImpulseJoint(RAPIER.JointData.fixed(
//     { x: 1.0 , y: 0.0, z: 1.0 }, { w: 1.0, x: 0.0, y: 0.0, z: 0.0 },
//     { x: 1.0 , y: 1.0, z: 1.0 }, { w: 1.0, x: 0.0, y: 0.0, z: 0.0 }
// ), car.rigidBody, wheels[0].rigidBody, true);
// world.createImpulseJoint(RAPIER.JointData.fixed(
//     { x: -1.0 , y: 0.0, z: 1.0 }, { w: 1.0, x: 0.0, y: 0.0, z: 0.0 },
//     { x: -1.0 , y: 1.0, z: 1.0 }, { w: 1.0, x: 0.0, y: 0.0, z: 0.0 }
// ), car.rigidBody, wheels[0].rigidBody, true);





  },
  // called when loading has errors
  function (error) {
    console.log(error);
    console.log('An error happened');
  }
);

// Simple reset helper (press R)




// --- Animation loop with fixed-step accumulator ---
let last = performance.now();
const FIXED_TIMESTEP = 1 / 60; // seconds
let accumulator = 0;






// Handle resize
// addEventListener('resize', () => {
//   camera.aspect = innerWidth / innerHeight;
//   camera.updateProjectionMatrix();
//   renderer.setSize(innerWidth + 10, innerHeight + 10);
// });


let pressed = {};
      window.addEventListener('keydown', (e) => (e.preventDefault(), (pressed[e.code] = true)));
      window.addEventListener('keyup', (e) => (e.preventDefault(), (pressed[e.code] = false)));

function processMovement() {
    let moveX = 0;
    let moveZ = 0;
    let moveY = 0;
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
    if (pressed['Space']) {
      moveY += 1;
    }

    // create a direction vector
    let dir = new THREE.Vector3(moveX, moveY, moveZ);

    // normalize so diagonal speed = straight speed
    if (dir.length() > 0) {
      dir.normalize();

      // apply movement (example: impulse or set linvel)

      //obj.body.applyImpulse({ x: 5, y: 0, z: -5 }, true);
      //obj.body.setAngvel({ x: 0, y: 0, z: 0 }, true);
      for(let i = 0; i< wheels.length ; i++){
      wheels[i].rigidBody.setLinvel(
        {
          x: dir.x * movementSpeed,
          y: dir.y * movementSpeed, // mainCube.rigidBody.linvel().y, // keep current vertical velocity (gravity/jumps)
          z: dir.z * movementSpeed,
        },
        true
      );

      // 1. target yaw
      const targetAngle = Math.atan2(dir.x, dir.z);

      // 2. current yaw from Rapier body quaternion
      const rot = wheels[0].rigidBody.rotation();
      const q = new THREE.Quaternion(rot.x, rot.y, rot.z, rot.w);
      const euler = new THREE.Euler().setFromQuaternion(q, 'YXZ');
      const currentAngle = euler.y;

      // 3. shortest angle difference
      let delta = targetAngle - currentAngle;
      delta = Math.atan2(Math.sin(delta), Math.cos(delta)); // normalize to [-pi, pi]

      // 4. choose rotation speed
      const angVel = delta * turnSpeed;

      // 5. set angular velocity around Y axis
     wheels[i].rigidBody.setAngvel({ x: 0, y: angVel, z: 0 }, true);
    }
  }
}
  


//main function--------------------------------------------

const CUBES = new CubeObject(scene, world)

// for (let i = 0; i < wheels.length; i++) {
//   const joint = RAPIER.JointData.fixed(
//     { x: 0, y: 0, z: 0 }, // car anchor
//     { x: 0, y: 0, z: 0 }  // wheel anchor
//   );
//   world.createJoint(joint, wheels[i].rigidBody, wheels[i].rigidBody);
// }

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

  processMovement()
    //
  for (const wheel of wheels) {
    let t = wheel.rigidBody.translation();  
    let r = wheel.rigidBody.rotation();
    //
    wheel.mesh.position.set(t.x, t.y, t.z);
    wheel.mesh.quaternion.set(r.x, r.y, r.z, r.w);
    
  }



const t = car.rigidBody.translation();
const r = car.rigidBody.rotation();

// place car 1 unit higher than wheel[0]
const wheelY = wheels[0].mesh.position.y;
const wheelX = wheels[0].mesh.position.x;
car.mesh.position.set(wheelX, wheelY + 1, t.z);

car.mesh.quaternion.set(r.x, r.y, r.z, r.w);


  CUBES.updateCubes();

  controls.update();
  //controls.target.set(0, 0, 0 );
  //camera.position.set(mainCube.mesh.position.x + cameraDefaultPos.x, mainCube.mesh.position.y + cameraDefaultPos.y, mainCube.mesh.position.z + cameraDefaultPos.z);

  renderer.render(scene, camera);
}
animate();
