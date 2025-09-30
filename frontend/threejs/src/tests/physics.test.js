import { test, expect } from 'vitest';
import * as THREE from 'three';
import RAPIER from '@dimforge/rapier3d-compat';



await RAPIER.init();
const gravity = { x: 0.0, y: -9.81, z: 0.0 };
const world = new RAPIER.World(gravity);

test('forward input produces correct movement vector', () => {
  const dir = new THREE.Vector3(0, 0, 1); // simulate W input
  const camera = new THREE.PerspectiveCamera();
  camera.lookAt(0, 0, -1);

  // simplified movement relative to camera
  const yaw = new THREE.Vector3();
  camera.getWorldDirection(yaw);
  yaw.y = 0; yaw.normalize();

  const camVect = new THREE.Vector3();
  camVect.addScaledVector(yaw, dir.z);

  expect(camVect.z).toBeLessThan(0); // should move into -Z
});

test('rigid body moves with setLinvel', () => {


  const rbDesc = RAPIER.RigidBodyDesc.dynamic().setTranslation(0, 0, 0);
  const body = world.createRigidBody(rbDesc);

  body.setLinvel({ x: 1, y: 0, z: 0 }, true);

  for (let i = 0; i < 60; i++) {
    world.step(); // simulate ~1 second at 60fps
  }

  const t = body.translation();
  expect(t.x).toBeGreaterThan(0.5);
});
