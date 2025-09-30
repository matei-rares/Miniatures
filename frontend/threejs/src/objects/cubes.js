import * as THREE from 'three';
import RAPIER from '@dimforge/rapier3d-compat';

export class CubeObject {
  constructor(scene, world) {
    this.boxes = [];

    // --- Create two cubes ---
    this.initialCubePosition = [1.25, 3, 0];
    this.makeCube(scene, world,{ position: this.initialCubePosition, size: 1, color: 0x66aaff, name: 'Cube A' });
    this.makeCube(scene, world, { position: [-1.25, 3, 0], size: 1, color: 0xff7780, name: 'Cube B' });
    this.mainCube = this.boxes[0];

    //Bind Keyboard keys Listeners (for Movement, reset)
    this.pressed = {};
      window.addEventListener('keydown', (e) => (e.preventDefault(), (this.pressed[e.code] = true)));
      window.addEventListener('keyup', (e) => (e.preventDefault(), (this.pressed[e.code] = false)));
  }

  makeCube(scene, world,{ position = [0, 1, 0], size = 1, color = 0x66aaff, name = 'cube' }) {
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

    this.boxes.push({ mesh, rigidBody });
    return { mesh, rigidBody };
  }

  processMovement() {
    let moveX = 0;
    let moveZ = 0;
    let moveY = 0;
    const movementSpeed = 6.0;
    const turnSpeed = 10.0; // radians/sec
    // check keys
    if (this.pressed['KeyW']) {
      moveZ -= 1;
    } // forward
    if (this.pressed['KeyS']) {
      moveZ += 1;
    } // backward
    if (this.pressed['KeyA']) {
      moveX -= 1;
    } // left
    if (this.pressed['KeyD']) {
      moveX += 1;
    } // right
    if (this.pressed['Space']) {
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
      this.mainCube.rigidBody.setLinvel(
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
      const rot = this.mainCube.rigidBody.rotation();
      const q = new THREE.Quaternion(rot.x, rot.y, rot.z, rot.w);
      const euler = new THREE.Euler().setFromQuaternion(q, 'YXZ');
      const currentAngle = euler.y;

      // 3. shortest angle difference
      let delta = targetAngle - currentAngle;
      delta = Math.atan2(Math.sin(delta), Math.cos(delta)); // normalize to [-pi, pi]

      // 4. choose rotation speed
      const angVel = delta * turnSpeed;

      // 5. set angular velocity around Y axis
     this.mainCube.rigidBody.setAngvel({ x: 0, y: angVel, z: 0 }, true);
    }
  }

updateMeshPositionByRigidBody(dict) {
  const t = dict.rigidBody.translation();
  const r = dict.rigidBody.rotation();
  dict.mesh.position.set(t.x, t.y, t.z);
  dict.mesh.quaternion.set(r.x, r.y, r.z, r.w);
}
    resetCubes() {
  const starts = [[-1.25, 3, 0], this.initialCubePosition];
  this.boxes.forEach((b, i) => {
    b.rigidBody.setTranslation({ x: starts[i][0], y: starts[i][1], z: starts[i][2] }, true);
    b.rigidBody.setLinvel({ x: 0, y: 0, z: 0 }, true);
    b.rigidBody.setAngvel({ x: 0, y: 0, z: 0 }, true);
  });
}

  updateCubes() {
    if (this.pressed['KeyR']) this.resetCubes();

    this.processMovement();

    for (const box of this.boxes) {
      this.updateMeshPositionByRigidBody(box);
    }
  }
}

// Create a cube (Three + Rapier) and return pair
