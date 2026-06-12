"""
LUMINA OS - COMFYUI ORCHESTRATOR
=================================

Advanced ComfyUI integration with ControlNet, IC-Light, and SUPIR
for professional architectural visualization and rendering.

Features:
- ControlNet MLSD for precise floorplan analysis
- IC-Light for physically accurate relighting
- SUPIR for texture upscaling (fabric, wood, materials)
- Workflow automation and queue management
- Multi-node processing and load balancing
- Professional camera simulation and post-processing
"""

import os
import sys
import json
import asyncio
import logging
import uuid
import base64
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime
import requests
from PIL import Image
import numpy as np
import cv2
from io import BytesIO

# Add root directory to Python path
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(root_dir)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ComfyUIOrchestrator:
    """Advanced ComfyUI workflow orchestrator"""
    
    def __init__(self, comfyui_url: str = "http://localhost:8188"):
        self.comfyui_url = comfyui_url
        self.client_id = f"lumina_os_{uuid.uuid4().hex[:8]}"
        self.workflow_templates = self._load_workflow_templates()
        self.node_types = self._load_node_types()
        self.active_workflows = {}
        
    def _load_workflow_templates(self) -> Dict[str, Dict]:
        """Load predefined workflow templates"""
        return {
            'architectural_rendering': {
                'nodes': {
                    'checkpoint': {
                        'type': 'CheckpointLoaderSimple',
                        'inputs': {
                            'ckpt_name': 'sd_xl_base_1.0.safetensors'
                        }
                    },
                    'positive_prompt': {
                        'type': 'CLIPTextEncode',
                        'inputs': {
                            'text': '',
                            'clip': ['checkpoint', 1]
                        }
                    },
                    'negative_prompt': {
                        'type': 'CLIPTextEncode',
                        'inputs': {
                            'text': '',
                            'clip': ['checkpoint', 1]
                        }
                    },
                    'empty_latent': {
                        'type': 'EmptyLatentImage',
                        'inputs': {
                            'width': 1024,
                            'height': 1024,
                            'batch_size': 1
                        }
                    },
                    'ksampler': {
                        'type': 'KSampler',
                        'inputs': {
                            'seed': 42,
                            'steps': 20,
                            'cfg': 7.0,
                            'sampler_name': 'euler',
                            'scheduler': 'normal',
                            'denoise': 1.0,
                            'model': ['checkpoint', 0],
                            'positive': ['positive_prompt', 0],
                            'negative': ['negative_prompt', 0],
                            'latent_image': ['empty_latent', 0]
                        }
                    },
                    'vae_decode': {
                        'type': 'VAEDecode',
                        'inputs': {
                            'samples': ['ksampler', 0],
                            'vae': ['checkpoint', 2]
                        }
                    },
                    'save_image': {
                        'type': 'SaveImage',
                        'inputs': {
                            'filename_prefix': 'lumina_render',
                            'images': ['vae_decode', 0]
                        }
                    }
                }
            },
            'controlnet_mlsd': {
                'nodes': {
                    'controlnet': {
                        'type': 'ControlNetLoader',
                        'inputs': {
                            'control_net_name': 'control_v11p_sd15_mlsd.pth'
                        }
                    },
                    'controlnet_apply': {
                        'type': 'ControlNetApply',
                        'inputs': {
                            'strength': 1.0,
                            'conditioning': ['positive_prompt', 0],
                            'control_net': ['controlnet', 0],
                            'image': ['controlnet_preprocessor', 0]
                        }
                    }
                }
            },
            'ic_light_relighting': {
                'nodes': {
                    'ic_light_loader': {
                        'type': 'IC_LightLoader',
                        'inputs': {
                            'model_name': 'iclight_sd15_fc.safetensors'
                        }
                    },
                    'ic_light_apply': {
                        'type': 'IC_LightApply',
                        'inputs': {
                            'model': ['ic_light_loader', 0],
                            'image': ['vae_decode', 0],
                            'lighting_image': ['lighting_input', 0]
                        }
                    }
                }
            },
            'supir_upscale': {
                'nodes': {
                    'supir_loader': {
                        'type': 'SUPIRLoader',
                        'inputs': {
                            'model_name': 'SUPIR-v1Q.safetensors'
                        }
                    },
                    'supir_upscale': {
                        'type': 'SUPIRUpscale',
                        'inputs': {
                            'model': ['supir_loader', 0],
                            'image': ['ic_light_apply', 0],
                            'upscale_factor': 2,
                            'tile_size': 512,
                            'tile_overlap': 64
                        }
                    }
                }
            }
        }
    
    def _load_node_types(self) -> Dict[str, Dict]:
        """Load ComfyUI node types and configurations"""
        return {
            'CheckpointLoaderSimple': {
                'category': 'loaders',
                'description': 'Load Stable Diffusion checkpoint',
                'inputs': ['ckpt_name']
            },
            'CLIPTextEncode': {
                'category': 'conditioning',
                'description': 'Encode text prompts',
                'inputs': ['text', 'clip']
            },
            'EmptyLatentImage': {
                'category': 'latent',
                'description': 'Create empty latent image',
                'inputs': ['width', 'height', 'batch_size']
            },
            'KSampler': {
                'category': 'sampling',
                'description': 'Advanced sampling',
                'inputs': ['seed', 'steps', 'cfg', 'sampler_name', 'scheduler', 'denoise', 'model', 'positive', 'negative', 'latent_image']
            },
            'VAEDecode': {
                'category': 'latent',
                'description': 'Decode latent to image',
                'inputs': ['samples', 'vae']
            },
            'SaveImage': {
                'category': 'image',
                'description': 'Save generated image',
                'inputs': ['filename_prefix', 'images']
            },
            'ControlNetLoader': {
                'category': 'controlnet',
                'description': 'Load ControlNet model',
                'inputs': ['control_net_name']
            },
            'ControlNetApply': {
                'category': 'controlnet',
                'description': 'Apply ControlNet conditioning',
                'inputs': ['strength', 'conditioning', 'control_net', 'image']
            },
            'IC_LightLoader': {
                'category': 'lighting',
                'description': 'Load IC-Light model',
                'inputs': ['model_name']
            },
            'IC_LightApply': {
                'category': 'lighting',
                'description': 'Apply IC-Light relighting',
                'inputs': ['model', 'image', 'lighting_image']
            },
            'SUPIRLoader': {
                'category': 'upscale',
                'description': 'Load SUPIR upscaler',
                'inputs': ['model_name']
            },
            'SUPIRUpscale': {
                'category': 'upscale',
                'description': 'Apply SUPIR upscaling',
                'inputs': ['model', 'image', 'upscale_factor', 'tile_size', 'tile_overlap']
            }
        }
    
    def build_workflow(
        self,
        prompt: str,
        negative_prompt: str = "",
        width: int = 1024,
        height: int = 1024,
        steps: int = 20,
        cfg_scale: float = 7.0,
        seed: Optional[int] = None,
        controlnet_image: Optional[str] = None,
        controlnet_type: str = "mlsd",
        ic_light_image: Optional[str] = None,
        supir_upscale: bool = False,
        checkpoint_name: str = "sd_xl_base_1.0.safetensors"
    ) -> Dict[str, Any]:
        """
        Build ComfyUI workflow with advanced features
        
        Args:
            prompt: Main prompt for generation
            negative_prompt: Negative prompt
            width: Image width
            height: Image height
            steps: Number of steps
            cfg_scale: CFG scale
            seed: Random seed
            controlnet_image: Base64 encoded ControlNet input
            controlnet_type: Type of ControlNet
            ic_light_image: Base64 encoded IC-Light lighting image
            supir_upscale: Whether to use SUPIR upscaling
            checkpoint_name: Checkpoint model name
        
        Returns:
            Complete ComfyUI workflow
        """
        
        try:
            # Start with base architectural rendering workflow
            workflow = self.workflow_templates['architectural_rendering'].copy()
            
            # Update basic parameters
            workflow['nodes']['positive_prompt']['inputs']['text'] = prompt
            workflow['nodes']['negative_prompt']['inputs']['text'] = negative_prompt
            workflow['nodes']['empty_latent']['inputs']['width'] = width
            workflow['nodes']['empty_latent']['inputs']['height'] = height
            workflow['nodes']['ksampler']['inputs']['steps'] = steps
            workflow['nodes']['ksampler']['inputs']['cfg'] = cfg_scale
            workflow['nodes']['ksampler']['inputs']['seed'] = seed or np.random.randint(0, 2**32)
            workflow['nodes']['checkpoint']['inputs']['ckpt_name'] = checkpoint_name
            
            # Add ControlNet if provided
            if controlnet_image:
                controlnet_workflow = self._add_controlnet_workflow(
                    workflow, controlnet_image, controlnet_type
                )
                workflow = controlnet_workflow
            
            # Add IC-Light if provided
            if ic_light_image:
                ic_light_workflow = self._add_ic_light_workflow(workflow, ic_light_image)
                workflow = ic_light_workflow
            
            # Add SUPIR upscaling if requested
            if supir_upscale:
                supir_workflow = self._add_supir_workflow(workflow)
                workflow = supir_workflow
            
            # Add node IDs and connections
            workflow = self._finalize_workflow(workflow)
            
            logger.info(f"Built workflow with {len(workflow['nodes'])} nodes")
            return workflow
            
        except Exception as e:
            logger.error(f"Error building workflow: {e}")
            raise
    
    def _add_controlnet_workflow(
        self, 
        workflow: Dict[str, Any], 
        controlnet_image: str, 
        controlnet_type: str
    ) -> Dict[str, Any]:
        """Add ControlNet workflow to main workflow"""
        
        # Add ControlNet loader
        workflow['nodes']['controlnet'] = {
            'type': 'ControlNetLoader',
            'inputs': {
                'control_net_name': f'control_v11p_sd15_{controlnet_type}.pth'
            }
        }
        
        # Add ControlNet preprocessor
        workflow['nodes']['controlnet_preprocessor'] = {
            'type': 'ImagePreprocessor',
            'inputs': {
                'image': controlnet_image,
                'preprocessor': controlnet_type,
                'resolution': 1024
            }
        }
        
        # Add ControlNet apply
        workflow['nodes']['controlnet_apply'] = {
            'type': 'ControlNetApply',
            'inputs': {
                'strength': 1.0,
                'conditioning': ['positive_prompt', 0],
                'control_net': ['controlnet', 0],
                'image': ['controlnet_preprocessor', 0]
            }
        }
        
        # Update KSampler to use ControlNet conditioning
        workflow['nodes']['ksampler']['inputs']['positive'] = ['controlnet_apply', 0]
        
        return workflow
    
    def _add_ic_light_workflow(
        self, 
        workflow: Dict[str, Any], 
        ic_light_image: str
    ) -> Dict[str, Any]:
        """Add IC-Light workflow to main workflow"""
        
        # Add IC-Light loader
        workflow['nodes']['ic_light_loader'] = {
            'type': 'IC_LightLoader',
            'inputs': {
                'model_name': 'iclight_sd15_fc.safetensors'
            }
        }
        
        # Add lighting image input
        workflow['nodes']['lighting_input'] = {
            'type': 'LoadImage',
            'inputs': {
                'image': ic_light_image
            }
        }
        
        # Add IC-Light apply
        workflow['nodes']['ic_light_apply'] = {
            'type': 'IC_LightApply',
            'inputs': {
                'model': ['ic_light_loader', 0],
                'image': ['vae_decode', 0],
                'lighting_image': ['lighting_input', 0]
            }
        }
        
        # Update save image to use IC-Light output
        workflow['nodes']['save_image']['inputs']['images'] = ['ic_light_apply', 0]
        
        return workflow
    
    def _add_supir_workflow(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Add SUPIR upscaling workflow to main workflow"""
        
        # Add SUPIR loader
        workflow['nodes']['supir_loader'] = {
            'type': 'SUPIRLoader',
            'inputs': {
                'model_name': 'SUPIR-v1Q.safetensors'
            }
        }
        
        # Add SUPIR upscale
        workflow['nodes']['supir_upscale'] = {
            'type': 'SUPIRUpscale',
            'inputs': {
                'model': ['supir_loader', 0],
                'image': ['ic_light_apply', 0] if 'ic_light_apply' in workflow['nodes'] else ['vae_decode', 0],
                'upscale_factor': 2,
                'tile_size': 512,
                'tile_overlap': 64
            }
        }
        
        # Update save image to use SUPIR output
        workflow['nodes']['save_image']['inputs']['images'] = ['supir_upscale', 0]
        
        return workflow
    
    def _finalize_workflow(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Finalize workflow with proper node IDs and connections"""
        
        # Generate node IDs
        node_id = 1
        node_mapping = {}
        
        for node_name, node_config in workflow['nodes'].items():
            node_mapping[node_name] = str(node_id)
            node_id += 1
        
        # Build final workflow
        final_workflow = {
            'last_node_id': str(node_id - 1),
            'last_node': node_mapping['save_image'],
            'nodes': {}
        }
        
        # Add nodes with proper IDs
        for node_name, node_config in workflow['nodes'].items():
            node_id = node_mapping[node_name]
            
            # Update input connections
            updated_inputs = {}
            for input_name, input_value in node_config['inputs'].items():
                if isinstance(input_value, list) and len(input_value) == 2:
                    # This is a connection to another node
                    source_node = input_value[0]
                    if source_node in node_mapping:
                        updated_inputs[input_name] = [node_mapping[source_node], input_value[1]]
                    else:
                        updated_inputs[input_name] = input_value
                else:
                    updated_inputs[input_name] = input_value
            
            final_workflow['nodes'][node_id] = {
                'class_type': node_config['type'],
                'inputs': updated_inputs
            }
        
        return final_workflow
    
    async def submit_workflow(
        self, 
        workflow: Dict[str, Any],
        priority: int = 0
    ) -> Dict[str, Any]:
        """
        Submit workflow to ComfyUI server
        
        Args:
            workflow: ComfyUI workflow
            priority: Queue priority
        
        Returns:
            Submission result with prompt ID
        """
        
        try:
            # Submit workflow
            submit_url = f"{self.comfyui_url}/prompt"
            
            payload = {
                'prompt': workflow,
                'client_id': self.client_id,
                'priority': priority
            }
            
            response = requests.post(submit_url, json=payload)
            response.raise_for_status()
            
            result = response.json()
            prompt_id = result.get('prompt_id')
            
            if not prompt_id:
                raise Exception("No prompt ID received from ComfyUI")
            
            # Store active workflow
            self.active_workflows[prompt_id] = {
                'workflow': workflow,
                'submitted_at': datetime.now(),
                'status': 'queued'
            }
            
            logger.info(f"Workflow submitted with ID: {prompt_id}")
            return {
                'success': True,
                'prompt_id': prompt_id,
                'client_id': self.client_id,
                'submitted_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error submitting workflow: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def wait_for_completion(
        self, 
        prompt_id: str, 
        timeout: int = 300,
        check_interval: float = 1.0
    ) -> Dict[str, Any]:
        """
        Wait for workflow completion and retrieve results
        
        Args:
            prompt_id: Prompt ID to monitor
            timeout: Maximum wait time in seconds
            check_interval: Check interval in seconds
        
        Returns:
            Completion result with generated images
        """
        
        try:
            start_time = datetime.now()
            
            while (datetime.now() - start_time).total_seconds() < timeout:
                # Check status
                history_url = f"{self.comfyui_url}/history/{prompt_id}"
                response = requests.get(history_url)
                response.raise_for_status()
                
                history = response.json()
                
                if prompt_id in history:
                    prompt_data = history[prompt_id]
                    status = prompt_data.get('status', {})
                    
                    if status.get('completed', False):
                        # Retrieve generated images
                        images = await self._get_generated_images(prompt_id)
                        
                        # Update workflow status
                        if prompt_id in self.active_workflows:
                            self.active_workflows[prompt_id]['status'] = 'completed'
                        
                        return {
                            'success': True,
                            'prompt_id': prompt_id,
                            'status': 'completed',
                            'images': images,
                            'completed_at': datetime.now().isoformat()
                        }
                    elif status.get('executing', {}).get('current_node'):
                        # Still executing
                        current_node = status['executing']['current_node']
                        if prompt_id in self.active_workflows:
                            self.active_workflows[prompt_id]['status'] = 'executing'
                            self.active_workflows[prompt_id]['current_node'] = current_node
                        
                        logger.debug(f"Workflow {prompt_id} executing node: {current_node}")
                
                await asyncio.sleep(check_interval)
            
            # Timeout reached
            if prompt_id in self.active_workflows:
                self.active_workflows[prompt_id]['status'] = 'timeout'
            
            return {
                'success': False,
                'prompt_id': prompt_id,
                'error': f'Timeout after {timeout} seconds'
            }
            
        except Exception as e:
            logger.error(f"Error waiting for completion: {e}")
            if prompt_id in self.active_workflows:
                self.active_workflows[prompt_id]['status'] = 'error'
                self.active_workflows[prompt_id]['error'] = str(e)
            
            return {
                'success': False,
                'prompt_id': prompt_id,
                'error': str(e)
            }
    
    async def _get_generated_images(self, prompt_id: str) -> List[Dict[str, Any]]:
        """Retrieve generated images for a prompt"""
        
        try:
            # Get view data
            view_url = f"{self.comfyui_url}/view"
            params = {'filename': f'{prompt_id}.png'}
            
            response = requests.get(view_url, params=params)
            response.raise_for_status()
            
            # Convert to base64
            image_base64 = base64.b64encode(response.content).decode('utf-8')
            
            return [{
                'filename': f'{prompt_id}.png',
                'subfolder': '',
                'type': 'output',
                'data': image_base64
            }]
            
        except Exception as e:
            logger.error(f"Error retrieving generated images: {e}")
            return []
    
    async def get_queue_info(self) -> Dict[str, Any]:
        """Get current queue information"""
        
        try:
            queue_url = f"{self.comfyui_url}/queue"
            response = requests.get(queue_url)
            response.raise_for_status()
            
            queue_data = response.json()
            
            return {
                'queue_pending': queue_data.get('queue_pending', []),
                'queue_running': queue_data.get('queue_running', []),
                'total_pending': len(queue_data.get('queue_pending', [])),
                'total_running': len(queue_data.get('queue_running', []))
            }
            
        except Exception as e:
            logger.error(f"Error getting queue info: {e}")
            return {}
    
    async def get_system_stats(self) -> Dict[str, Any]:
        """Get ComfyUI system statistics"""
        
        try:
            stats_url = f"{self.comfyui_url}/system_stats"
            response = requests.get(stats_url)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            logger.error(f"Error getting system stats: {e}")
            return {}
    
    def get_active_workflows(self) -> Dict[str, Any]:
        """Get information about active workflows"""
        
        active_info = {}
        for prompt_id, workflow_data in self.active_workflows.items():
            active_info[prompt_id] = {
                'submitted_at': workflow_data['submitted_at'].isoformat(),
                'status': workflow_data['status'],
                'current_node': workflow_data.get('current_node'),
                'node_count': len(workflow_data['workflow']['nodes'])
            }
        
        return active_info
    
    def cancel_workflow(self, prompt_id: str) -> bool:
        """Cancel an active workflow"""
        
        try:
            # Send interrupt signal
            interrupt_url = f"{self.comfyui_url}/interrupt"
            response = requests.post(interrupt_url)
            response.raise_for_status()
            
            # Update workflow status
            if prompt_id in self.active_workflows:
                self.active_workflows[prompt_id]['status'] = 'cancelled'
            
            logger.info(f"Workflow {prompt_id} cancelled")
            return True
            
        except Exception as e:
            logger.error(f"Error cancelling workflow: {e}")
            return False
    
    def clear_queue(self) -> bool:
        """Clear the ComfyUI queue"""
        
        try:
            clear_url = f"{self.comfyui_url}/queue"
            response = requests.delete(clear_url)
            response.raise_for_status()
            
            logger.info("ComfyUI queue cleared")
            return True
            
        except Exception as e:
            logger.error(f"Error clearing queue: {e}")
            return False

# Convenience functions for external use
async def generate_comfyui_image(
    prompt: str,
    negative_prompt: str = "",
    width: int = 1024,
    height: int = 1024,
    steps: int = 20,
    cfg_scale: float = 7.0,
    seed: Optional[int] = None,
    controlnet_image: Optional[str] = None,
    controlnet_type: str = "mlsd",
    ic_light_image: Optional[str] = None,
    supir_upscale: bool = False
) -> Dict[str, Any]:
    """Generate image using ComfyUI with advanced features"""
    
    orchestrator = ComfyUIOrchestrator()
    
    # Build workflow
    workflow = orchestrator.build_workflow(
        prompt=prompt,
        negative_prompt=negative_prompt,
        width=width,
        height=height,
        steps=steps,
        cfg_scale=cfg_scale,
        seed=seed,
        controlnet_image=controlnet_image,
        controlnet_type=controlnet_type,
        ic_light_image=ic_light_image,
        supir_upscale=supir_upscale
    )
    
    # Submit workflow
    result = await orchestrator.submit_workflow(workflow)
    
    if not result['success']:
        return result
    
    # Wait for completion
    completion_result = await orchestrator.wait_for_completion(result['prompt_id'])
    
    if completion_result['success'] and completion_result['images']:
        # Return first image
        return {
            'success': True,
            'image': completion_result['images'][0]['data'],
            'prompt_id': result['prompt_id'],
            'completed_at': completion_result['completed_at']
        }
    else:
        return completion_result
