import React, { useRef, useEffect } from 'react';
import * as THREE from 'three';
import { gsap } from 'gsap';

interface SentinelGazeReactionProps {
  scene: THREE.Scene;
  camera: THREE.PerspectiveCamera;
  renderer: THREE.WebGLRenderer;
}

const SentinelGazeReaction: React.FC<SentinelGazeReactionProps> = ({
  scene,
  camera,
  renderer
}) => {
  const raycaster = useRef<THREE.Raycaster>(new THREE.Raycaster());
  const mouse = useRef<THREE.Vector2>(new THREE.Vector2());
  const intersectedObject = useRef<THREE.Object3D | null>(null);
  const intersectionTimer = useRef<number>(0);
  const spotlight = useRef<THREE.SpotLight | null>(null);
  
  useEffect(() => {
    // Create spotlight for subliminal effect
    const spotLight = new THREE.SpotLight(0xffffff, 2, 10, Math.PI / 6, 0.5);
    spotLight.position.set(0, 5, 0);
    spotLight.target.position.set(0, 0, 0);
    scene.add(spotLight);
    spotlight.current = spotLight;
    
    // Handle mouse movement
    const handleMouseMove = (event: MouseEvent) => {
      mouse.current.x = (event.clientX / window.innerWidth) * 2 - 1;
      mouse.current.y = -(event.clientY / window.innerHeight) * 2 + 1;
      
      // Update raycaster
      raycaster.current.setFromCamera(mouse.current, camera);
      
      // Check for intersections
      const intersects = raycaster.current.intersectObjects(scene.children);
      
      if (intersects.length > 0) {
        const object = intersects[0].object;
        
        if (intersectedObject.current === object) {
          // Same object, increment timer
          intersectionTimer.current += 1;
          
          // Trigger subliminal beauty effect after 3 seconds
          if (intersectionTimer.current === 180) { // 3 seconds at 60fps
            triggerSubliminalBeauty(object);
          }
        } else {
          // New object, reset timer
          intersectedObject.current = object;
          intersectionTimer.current = 0;
        }
      } else {
        // No intersection
        intersectedObject.current = null;
        intersectionTimer.current = 0;
      }
    };
    
    const triggerSubliminalBeauty = (object: THREE.Object3D) => {
      if (!spotlight.current) return;
      
      // Animate material properties
      const material = object.material as THREE.MeshStandardMaterial;
      
      // Increase envMapIntensity
      gsap.to(material, {
        envMapIntensity: material.envMapIntensity * 1.5,
        metalness: Math.min(material.metalness + 0.3, 1.0),
        roughness: Math.max(material.roughness - 0.2, 0.0)
      }, {
        duration: 1.5,
        ease: "power2.inOut"
      });
      
      // Animate spotlight to target object
      const objectPosition = object.getWorldPosition(new THREE.Vector3());
      
      gsap.to(spotlight.current.position, {
        x: objectPosition.x,
        y: objectPosition.y + 2,
        z: objectPosition.z
      }, {
        duration: 1.0,
        ease: "power2.inOut",
        onUpdate: () => {
          spotlight.current!.target.position.copy(objectPosition);
        }
      });
      
      // Add glow effect
      const glowColor = new THREE.Color(0xffffff);
      glowColor.setHex(0xffff00); // Warm glow
      
      gsap.to(material.emissive, {
        r: glowColor.r * 0.3,
        g: glowColor.g * 0.3,
        b: glowColor.b * 0.3
      }, {
        duration: 1.0,
        ease: "power2.inOut",
        yoyo: true,
        repeat: 1
      });
      
      // Reset after animation
      setTimeout(() => {
        gsap.to(material, {
          envMapIntensity: material.envMapIntensity / 1.5,
          metalness: Math.max(material.metalness - 0.3, 0.0),
          roughness: Math.min(material.roughness + 0.2, 1.0)
        }, {
          duration: 1.5,
          ease: "power2.inOut"
        });
        
        gsap.to(material.emissive, {
          r: 0,
          g: 0,
          b: 0
        }, {
          duration: 1.0,
          ease: "power2.inOut"
        });
      }, 3000); // 3 seconds after initial effect
    };
    
    // Add event listener
    window.addEventListener('mousemove', handleMouseMove);
    
    // Animation loop
    const animate = () => {
      requestAnimationFrame(animate);
      renderer.render(scene, camera);
    };
    
    animate();
    
    // Cleanup
    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      if (spotlight.current) {
        scene.remove(spotlight.current);
      }
    };
  }, [scene, camera, renderer]);
  
  return null; // This component doesn't render anything, it just manages the scene
};

export default SentinelGazeReaction;
