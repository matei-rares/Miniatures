import * as THREE from 'three';
import RAPIER from '@dimforge/rapier3d-compat';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';


var carDefaultPostion = new THREE.Vector3(1, 3, 2);

export class CarObject {
  constructor(scene, world) {
    this.loader = new GLTFLoader();
    this.wheels = [];
    this.car = { mesh: 0, rigidBody: 0 };
    console.log(window.location.href);
    console.log(window.location.pathname);
    console.log(import.meta.url);
    this.isLoaderCarDone = false;
    this.isLoaderWheelDone = false;
    this.wheel = { mesh: 0, rigidBody: 0 };

    this.loadCar(scene, world);
    this.loadWheels(scene, world);
    this.wheelFL = {};
    this.wheelFR = {};
    this.wheelBL = {};
    this.wheelBR = {};
    this.wheels = [];
   

    let pressed = {};
    window.addEventListener('keydown', (e) => (e.preventDefault(), (pressed[e.code] = true)));
    window.addEventListener('keyup', (e) => (e.preventDefault(), (pressed[e.code] = false)));
  }

  loadCar(scene, world){
     this.loader.load(
      './static/lowsss.gltf',
      (gltf) => {
        console.log('load car');
        this.deleteUnusedProperties(gltf);
        const size = 10;
        let carGLTF = gltf.scene;
        carGLTF.scale.set(size, size, size);

        const carObject = carGLTF.children[0];
        const carMaterial = carObject.material;
        const carGeometry = carObject.geometry;
        const carMesh = new THREE.Mesh(carGeometry, carMaterial);
        console.log(carObject);
        carMaterial.wireframe = true;
        carMesh.castShadow = true;
        carMesh.receiveShadow = true;
        carMesh.position.set(carDefaultPostion.x, carDefaultPostion.y, carDefaultPostion.z);
        scene.add(carMesh);

        carGeometry.computeBoundingBox();
        const rigidBodyDesc = RAPIER.RigidBodyDesc.dynamic().setTranslation(carMesh.position.x, carMesh.position.y, carMesh.position.z).setGravityScale(0.5); //
        const rigidBody = world.createRigidBody(rigidBodyDesc);
        const colliderDesc = RAPIER.ColliderDesc.trimesh(carGeometry.attributes.position.array, carGeometry.index.array); //vertices,indices
        console.log(colliderDesc);
        console.log(rigidBody);
        world.createCollider(colliderDesc, rigidBody);

        //rigidBody.setAngvel({ x: 5, y: 0, z: 0 }, true);
        this.car = { mesh: carMesh, rigidBody };

        // for (const [index, wheel] of carObject.children.entries()) {

        //     const wheelGeometry = wheel.geometry;
        //     const wheelMaterial = wheel.material;
        //     console.log(wheelMaterial)
        //     const wheelMesh = new THREE.Mesh(wheelGeometry, wheelMaterial);
        //     wheelMesh.castShadow = true;
        //     wheelMesh.receiveShadow = true;
        //     wheelMesh.position.x += carDefaultPostion.x;
        //     wheelMesh.position.y += 1;
        //     wheelMesh.position.z += carDefaultPostion.z;

        //     console.log(index);
        //     scene.add(wheelMesh);

        //     wheelGeometry.computeBoundingBox();
        //     const rigidBodyDesc = RAPIER.RigidBodyDesc.dynamic().setTranslation(wheelMesh.position.x, wheelMesh.position.y, wheelMesh.position.z);
        //     const rigidBody = world.createRigidBody(rigidBodyDesc);
        //     const colliderDesc = RAPIER.ColliderDesc.trimesh(wheelGeometry.attributes.position.array, wheelGeometry.index.array); //vertices,indices
        //     world.createCollider(colliderDesc, rigidBody);
        //     //rigidBody.setAngvel({ x: 5, y: 0, z: 0 }, true);

        //     this.wheels.push({ mesh: wheelMesh, rigidBody });

        //     const rbPosition = rigidBody.translation(); // returns {x, y, z}

        // }
        // console.log(this.wheels);
        console.log('loaded car');

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

        this.isLoaderCarDone = true;
      },
      // called when loading has errors
      function (error) {
        console.log(error);
        console.log('An error happened');
      }
    );
  }

  loadWheels(scene, world){
     this.loader.load(
      './static/low.gltf',
      (gltf) => {
        console.log('modified');
        console.log(gltf);
        const size = 1;
        gltf = gltf.scene;
        let wheelsObj = [];
        for (var i = 0; i < 4; i++) {
          console.log(i);
          wheelsObj[i] = gltf.getObjectByName('wheel').clone(true);
          wheelsObj[i].scale.set(size, size, size);
          scene.add(wheelsObj[i]);

          const wheelGeometry = wheelsObj[i].geometry;
          wheelGeometry.computeBoundingBox();
          const rigidBodyDesc = RAPIER.RigidBodyDesc.dynamic().setTranslation(i, 1, 0); //.setGravityScale(0); //
          const rigidBody = world.createRigidBody(rigidBodyDesc);
          const colliderDesc = RAPIER.ColliderDesc.trimesh(wheelGeometry.attributes.position.array, wheelGeometry.index.array).setRestitution(0).setFriction(1); //vertices,indices
          console.log(colliderDesc);
          console.log(rigidBody);
          world.createCollider(colliderDesc, rigidBody);

          const targetAngle = Math.PI / 2;
          rigidBody.setRotation({ x: 0, y: -targetAngle , z: -targetAngle, w: 0 }, false);

          this.wheels[i] = { mesh: wheelsObj[i], rigidBody };
          console.log(this.wheels[i]);
        }

        this.wheelFL = this.wheels[0];
        this.wheelFL.rigidBody.setTranslation({ x:0, y: 3, z: 2.6 }, false);

        this.wheelFR = this.wheels[1];
                this.wheelFR.rigidBody.setTranslation({ x:0, y: 3, z: 1 }, false);

        this.wheelBL = this.wheels[2];
                this.wheelBL.rigidBody.setTranslation({ x:2, y: 3, z: 2.6 }, false);

        this.wheelBR = this.wheels[3];
                this.wheelBR.rigidBody.setTranslation({ x:2, y: 3, z: 1 }, false);


const joint = RAPIER.JointData.revolute(
  { x: 0.0, y: 0.0, z: 0.0 }, { w: 1.0, x: 0.0, y: 0.0, z: 0.0 }, // hood local frame
  { x: 0.0, y: 0.0, z: 0.0 }, { w: 1.0, x: 0.0, y: 0.0, z: 0.0 }  // wheel local frame
);

//world.createJoint(joint, carRigidBody, wheelRigidBody);



        console.log('modified');

        this.isLoaderWheelDone = true;
      },
      // called when loading has errors
      function (error) {
        console.log(error);
        console.log('An error happened');
      }
    );
  }

  deleteUnusedProperties(gltf) {
    delete gltf.animations;
    delete gltf.cameras;
    delete gltf.asset;
    delete gltf.scenes;
    delete gltf.userData;
  }

  processMovement() {
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
      for (let i = 0; i < wheels.length; i++) {
        this.wheels[i].rigidBody.setLinvel(
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
        const rot = this.wheels[0].rigidBody.rotation();
        const q = new THREE.Quaternion(rot.x, rot.y, rot.z, rot.w);
        const euler = new THREE.Euler().setFromQuaternion(q, 'YXZ');
        const currentAngle = euler.y;

        // 3. shortest angle difference
        let delta = targetAngle - currentAngle;
        delta = Math.atan2(Math.sin(delta), Math.cos(delta)); // normalize to [-pi, pi]

        // 4. choose rotation speed
        const angVel = delta * turnSpeed;

        // 5. set angular velocity around Y axis
        this.wheels[i].rigidBody.setAngvel({ x: 0, y: angVel, z: 0 }, true);
      }
    }
  }

  updateCar() {
    if (this.isLoaderCarDone) {
        this.car.rigidBody.setTranslation({x:carDefaultPostion.x, y:1, z:carDefaultPostion.z});


// OR: only lock specific axes
 this.car.rigidBody.setEnabledRotations(false, true, false, true);
// this.car.rigidBody.setAngvel({ x: 0, y: 0, z: 0 }, true);


      const t = this.car.rigidBody.translation();
      const r = this.car.rigidBody.rotation();

      this.car.mesh.position.set(t.x, t.y, t.z);
      this.car.mesh.quaternion.set(r.x, r.y, r.z, r.w);
    }

    if (this.isLoaderWheelDone) {
      for (let i = 0; i < this.wheels.length; i++) {
        const t = this.wheels[i].rigidBody.translation();
        const r = this.wheels[i].rigidBody.rotation();

        this.wheels[i].mesh.position.set(t.x, t.y, t.z);
        this.wheels[i].mesh.quaternion.set(r.x, r.y, r.z, r.w);
      }
    }
  }
}
