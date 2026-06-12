import React, { useState, useEffect, useRef, Suspense } from 'react';
import { Canvas } from '@react-three/fiber';
import { useGLTF, useProgress, Html, OrbitControls, PerspectiveCamera, Environment, ContactShadows, PresentationControls, Stage } from '@react-three/drei';
import { Suspense as ReactSuspense } from 'react';
import * as THREE from 'three';
import { gsap } from 'gsap';
import { io } from 'socket.io-client';

// VR Components
const VirtualTour = ({ 
  modelPath, 
  skyboxImage, 
  onGazeData, 
  enableGazeTracking = true,
  enableTimeSync = true,
  initialPosition = [0, 2, 5],
  enableOrbit = true 
}) => {
  const [model, setModel] = useState(null);
  const [skybox, setSkybox] = setSkyboxState(null);
  const [gazeData, setGazeData] = useState({});
  const [currentTime, setCurrentTime] = useState(new Date());
  const [isDaytime, setIsDaytime] = useState(true);
  const [focusedObject, setFocusedObject] = useState(null);
  const [gazeStartTime, setGazeStartTime] = useState(null);
  const [socket, setSocket] = useState(null);
  const [sessionId] = useState(`session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`);
  
  const canvasRef = useRef();
  const cameraRef = useRef();
  const raycasterRef = useRef(new THREE.Raycaster());
  const mouseRef = useRef(new THREE.Vector2());
  const gazeTimerRef = useRef(null);
  const spotlightRef = useRef(null);
  
  // WebSocket connection for gaze tracking
  useEffect(() => {
    if (enableGazeTracking) {
      const newSocket = io('ws://localhost:8000', {
        transports: ['websocket']
      });
      
      newSocket.on('connect', () => {
        console.log('Connected to gaze tracking server');
        newSocket.emit('session_start', { sessionId });
      });
      
      newSocket.on('gaze_response', (data) => {
        console.log('Gaze response:', data);
      });
      
      setSocket(newSocket);
      
      return () => {
        newSocket.close();
      };
    }
  }, [enableGazeTracking, sessionId]);

  // Load 3D model with Draco compression
  useEffect(() => {
    if (modelPath) {
      const loader = new THREE.GLTFLoader();
      const dracoLoader = new THREE.DRACOLoader();
      dracoLoader.setDecoderPath('https://www.gstatic.com/draco/versioned/decoders/1.5.6/');
      loader.setDRACOLoader(dracoLoader);
      
      loader.load(
        modelPath,
        (gltf) => {
          const model = gltf.scene;
          
          // Optimize model for VR
          model.traverse((child) => {
            if (child.isMesh) {
              child.castShadow = true;
              child.receiveShadow = true;
              
              // Add metadata for gaze tracking
              child.userData = {
                ...child.userData,
                interactable: true,
                objectName: child.name || 'Unknown',
                roomType: determineRoomType(child.name),
                focusable: true
              };
            }
          });
          
          setModel(model);
        },
        (progress) => {
          console.log('Loading progress:', (progress.loaded / progress.total) * 100 + '%');
        },
        (error) => {
          console.error('Error loading model:', error);
        }
      );
    }
  }, [modelPath]);

  // Load AI-generated skybox
  useEffect(() => {
    if (skyboxImage) {
      const textureLoader = new THREE.TextureLoader();
      textureLoader.load(
        skyboxImage,
        (texture) => {
          // Create equirectangular skybox
          const skyboxGeometry = new THREE.SphereGeometry(500, 60, 40);
          const skyboxMaterial = new THREE.MeshBasicMaterial({
            map: texture,
            side: THREE.BackSide
          });
          
          const skyboxMesh = new THREE.Mesh(skyboxGeometry, skyboxMaterial);
          setSkybox(skyboxMesh);
        },
        undefined,
        (error) => {
          console.error('Error loading skybox:', error);
        }
      );
    }
  }, [skyboxImage]);

  // Time-synced illumination
  useEffect(() => {
    if (enableTimeSync) {
      const updateTime = () => {
        const now = new Date();
        setCurrentTime(now);
        
        const hours = now.getHours();
        const isDay = hours >= 6 && hours < 18;
        setIsDaytime(isDay);
        
        // Update lighting based on time
        updateLighting(isDay);
      };
      
      updateTime();
      const interval = setInterval(updateTime, 60000); // Update every minute
      
      return () => clearInterval(interval);
    }
  }, [enableTimeSync]);

  // Gaze tracking implementation
  useEffect(() => {
    if (!enableGazeTracking || !canvasRef.current) return;
    
    const handleMouseMove = (event) => {
      const canvas = canvasRef.current;
      const rect = canvas.getBoundingClientRect();
      
      mouseRef.current.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
      mouseRef.current.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
      
      checkGazeIntersection();
    };
    
    const canvas = canvasRef.current;
    canvas.addEventListener('mousemove', handleMouseMove);
    
    return () => {
      canvas.removeEventListener('mousemove', handleMouseMove);
    };
  }, [enableGazeTracking, model]);

  const checkGazeIntersection = () => {
    if (!cameraRef.current || !model) return;
    
    raycasterRef.current.setFromCamera(mouseRef.current, cameraRef.current);
    
    const intersects = raycasterRef.current.intersectObjects(model.children, true);
    
    if (intersects.length > 0) {
      const object = intersects[0].object;
      const objectName = object.userData.objectName || object.name;
      
      if (focusedObject === objectName) {
        // Same object, update gaze duration
        if (!gazeStartTime) {
          setGazeStartTime(Date.now());
        } else {
          const gazeDuration = Date.now() - gazeStartTime;
          
          // Trigger subliminal beauty effect after 5 seconds
          if (gazeDuration >= 5000) {
            triggerGazeEffect(object, objectName);
            setGazeStartTime(null); // Reset timer
          }
        }
      } else {
        // New object, reset timer
        setFocusedObject(objectName);
        setGazeStartTime(Date.now());
      }
      
      // Update gaze data
      const newGazeData = {
        sessionId,
        timestamp: new Date().toISOString(),
        objectName,
        gazeDuration: gazeStartTime ? Date.now() - gazeStartTime : 0,
        position: intersects[0].point,
        normal: intersects[0].face.normal,
        distance: intersects[0].distance,
        roomType: object.userData.roomType || 'Unknown'
      };
      
      setGazeData(newGazeData);
      
      // Send to server
      if (socket) {
        socket.emit('gaze_data', newGazeData);
      }
      
      // Call parent callback
      if (onGazeData) {
        onGazeData(newGazeData);
      }
    } else {
      // No intersection
      setFocusedObject(null);
      setGazeStartTime(null);
    }
  };

  const triggerGazeEffect = (object, objectName) => {
    if (!spotlightRef.current) return;
    
    console.log(`Gaze effect triggered on: ${objectName}`);
    
    // Animate material properties
    const material = object.material;
    
    gsap.to(material, {
      duration: 1.5,
      ease: "power2.inOut",
      onUpdate: () => {
        // Increase envMapIntensity
        if (material.envMapIntensity !== undefined) {
          material.envMapIntensity = Math.min(material.envMapIntensity * 1.5, 2.0);
        }
        
        // Increase metalness
        if (material.metalness !== undefined) {
          material.metalness = Math.min(material.metalness + 0.3, 1.0);
        }
        
        // Decrease roughness
        if (material.roughness !== undefined) {
          material.roughness = Math.max(material.roughness - 0.2, 0.0);
        }
      }
    });
    
    // Animate spotlight to target object
    const objectPosition = new THREE.Vector3();
    object.getWorldPosition(objectPosition);
    
    gsap.to(spotlightRef.current.position, {
      duration: 1.0,
      ease: "power2.inOut",
      x: objectPosition.x,
      y: objectPosition.y + 2,
      z: objectPosition.z,
      onUpdate: () => {
        spotlightRef.current.target.position.copy(objectPosition);
        spotlightRef.current.target.updateMatrixWorld();
      }
    });
    
    // Add glow effect
    const glowColor = new THREE.Color(0xffffff);
    glowColor.setHex(0xffff00); // Warm glow
    
    gsap.to(material.emissive, {
      duration: 1.0,
      ease: "power2.inOut",
      r: glowColor.r * 0.3,
      g: glowColor.g * 0.3,
      b: glowColor.b * 0.3,
      yoyo: true,
      repeat: 1,
      onComplete: () => {
        // Reset after animation
        gsap.to(material, {
          duration: 1.5,
          ease: "power2.inOut",
          onUpdate: () => {
            if (material.envMapIntensity !== undefined) {
              material.envMapIntensity = Math.max(material.envMapIntensity / 1.5, 0.5);
            }
            if (material.metalness !== undefined) {
              material.metalness = Math.max(material.metalness - 0.3, 0.0);
            }
            if (material.roughness !== undefined) {
              material.roughness = Math.min(material.roughness + 0.2, 1.0);
            }
          }
        });
        
        gsap.to(material.emissive, {
          duration: 1.0,
          ease: "power2.inOut",
          r: 0,
          g: 0,
          b: 0
        });
      }
    });
  };

  const updateLighting = (isDay) => {
    // This would update the scene lighting based on time
    // Implementation depends on your lighting setup
    console.log(`Updating lighting for ${isDay ? 'daytime' : 'nighttime'}`);
  };

  const determineRoomType = (objectName) => {
    const name = objectName.toLowerCase();
    if (name.includes('kitchen') || name.includes('dapur')) return 'Kitchen';
    if (name.includes('bedroom') || name.includes('kamar')) return 'Bedroom';
    if (name.includes('bathroom') || name.includes('kamar mandi')) return 'Bathroom';
    if (name.includes('living') || name.includes('ruang keluarga')) return 'Living Room';
    if (name.includes('dining') || name.includes('ruang makan')) return 'Dining Room';
    return 'Other';
  };

  function Loader() {
    const { progress } = useProgress();
    return (
      <Html center>
        <div style={{ color: 'white', fontSize: '16px' }}>
          Loading {Math.round(progress)}%
        </div>
      </Html>
    );
  }

  return (
    <div style={{ width: '100%', height: '100vh', position: 'relative' }}>
      {/* Time Display */}
      {enableTimeSync && (
        <div style={{
          position: 'absolute',
          top: '20px',
          right: '20px',
          color: 'white',
          fontSize: '14px',
          zIndex: 1000,
          background: 'rgba(0,0,0,0.5)',
          padding: '8px 12px',
          borderRadius: '4px'
        }}>
          <div>{currentTime.toLocaleTimeString()}</div>
          <div>{isDaytime ? '☀️ Day' : '🌙 Night'}</div>
        </div>
      )}

      {/* Gaze Info */}
      {enableGazeTracking && (
        <div style={{
          position: 'absolute',
          top: '20px',
          left: '20px',
          color: 'white',
          fontSize: '12px',
          zIndex: 1000,
          background: 'rgba(0,0,0,0.5)',
          padding: '8px 12px',
          borderRadius: '4px',
          maxWidth: '200px'
        }}>
          <div>Session: {sessionId}</div>
          {focusedObject && (
            <>
              <div>Focused: {focusedObject}</div>
              <div>Duration: {gazeStartTime ? Math.round((Date.now() - gazeStartTime) / 1000) : 0}s</div>
            </>
          )}
        </div>
      )}

      {/* 3D Canvas */}
      <Canvas
        ref={canvasRef}
        shadows
        camera={{ position: initialPosition, fov: 60 }}
        gl={{ 
          antialias: true, 
          alpha: false,
          powerPreference: "high-performance"
        }}
      >
        <ReactSuspense fallback={<Loader />}>
          {/* Lighting */}
          <ambientLight intensity={isDaytime ? 0.4 : 0.1} />
          <directionalLight
            position={[10, 10, 5]}
            intensity={isDaytime ? 1.0 : 0.3}
            castShadow
            shadow-mapSize={[2048, 2048]}
            shadow-camera-far={50}
            shadow-camera-left={-10}
            shadow-camera-right={10}
            shadow-camera-top={10}
            shadow-camera-bottom={-10}
          />
          
          {/* Sentinel Spotlight */}
          <spotLight
            ref={spotlightRef}
            position={[0, 5, 0]}
            angle={0.3}
            penumbra={0.5}
            intensity={0.5}
            castShadow
          />
          
          {/* Camera */}
          <PerspectiveCamera ref={cameraRef} makeDefault />
          
          {/* Controls */}
          {enableOrbit && (
            <OrbitControls
              enablePan={true}
              enableZoom={true}
              enableRotate={true}
              minDistance={1}
              maxDistance={20}
              maxPolarAngle={Math.PI / 2}
            />
          )}
          
          {/* Environment */}
          <Environment
            preset={isDaytime ? "sunset" : "night"}
            background={false}
          />
          
          {/* Skybox */}
          {skybox && <primitive object={skybox} />}
          
          {/* 3D Model */}
          {model && (
            <PresentationControls
              global
              rotation={[0, -Math.PI / 4, 0]}
              polar={[0, Math.PI / 4]}
              azimuth={[-Math.PI / 4, Math.PI / 4]}
              config={{ mass: 2, tension: 400, friction: 40 }}
              snap={{ mass: 4, tension: 400, friction: 40 }}
            >
              <Stage
                environment={isDaytime ? "sunset" : "night"}
                intensity={isDaytime ? 0.6 : 0.3}
                contactShadow={{ blur: 2, opacity: 0.5 }}
                shadows
              >
                <primitive object={model} />
              </Stage>
            </PresentationControls>
          )}
          
          {/* Contact Shadows */}
          <ContactShadows
            position={[0, -0.5, 0]}
            opacity={0.4}
            scale={10}
            blur={2}
            far={10}
          />
        </ReactSuspense>
      </Canvas>
    </div>
  );
};

// Hook for loading progress
const useProgress = () => {
  const [progress, setProgress] = useState(0);
  
  useEffect(() => {
    const interval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval);
          return 100;
        }
        return prev + 10;
      });
    }, 200);
    
    return () => clearInterval(interval);
  }, []);
  
  return { progress };
};

// Utility function to set skybox state
const setSkyboxState = (skybox) => {
  // This is a placeholder for state management
  // In a real implementation, you'd use useState or a state management library
  return skybox;
};

export default VirtualTour;
