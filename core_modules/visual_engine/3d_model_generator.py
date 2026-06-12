#!/usr/bin/env python3
"""
3D Model Generator - Visual Engine
Advanced 3D property model creation and visualization system
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import uuid
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ModelType(Enum):
    """Types of 3D models"""
    ARCHITECTURAL = "architectural"
    INTERIOR = "interior"
    EXTERIOR = "exterior"
    FURNITURE = "furniture"
    LANDSCAPE = "landscape"
    FULL_BUILDING = "full_building"

class ModelQuality(Enum):
    """3D model quality levels"""
    BASIC = "basic"
    STANDARD = "standard"
    PREMIUM = "premium"
    ULTRA = "ultra"

class ModelFormat(Enum):
    """3D model file formats"""
    OBJ = "obj"
    FBX = "fbx"
    GLTF = "gltf"
    THREE_JS = "three_js"
    SKETCHUP = "sketchup"
    BLENDER = "blender"

class ModelStatus(Enum):
    """Model creation status"""
    PLANNING = "planning"
    MODELING = "modeling"
    TEXTURING = "texturing"
    RENDERING = "rendering"
    OPTIMIZING = "optimizing"
    READY = "ready"
    PUBLISHED = "published"
    ARCHIVED = "archived"

@dataclass
class Model3D:
    """3D model data structure"""
    model_id: str
    property_id: str
    model_type: ModelType
    title: str
    description: str
    quality: ModelQuality
    format: ModelFormat
    status: ModelStatus
    file_size_mb: float
    polygon_count: int
    texture_resolution: str
    render_time_hours: float
    model_url: str
    thumbnail_url: str
    preview_url: str
    created_at: datetime
    published_at: Optional[datetime] = None
    download_count: int = 0
    rating: float = 0.0
    notes: str = ""

@dataclass
class ModelComponent:
    """Individual component within 3D model"""
    component_id: str
    model_id: str
    component_name: str
    component_type: str
    material: str
    color: str
    dimensions: Dict
    position: Dict
    rotation: Dict
    is_interactive: bool = False
    created_at: datetime = datetime.now()

@dataclass
class ModelRender:
    """3D model render configuration"""
    render_id: str
    model_id: str
    render_type: str
    lighting_setup: Dict
    camera_positions: List[Dict]
    resolution: str
    quality_preset: str
    output_format: str
    render_time: float
    file_size_mb: float
    render_url: str
    created_at: datetime = datetime.now()

class Model3DGenerator:
    """Advanced 3D model generation and management system"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Initialize database
        self.db_path = 'data/3d_models.db (SQLite - removed)
        self._init_database()
        
        # Model configurations
        self.model_configs = {
            ModelType.ARCHITECTURAL: {
                'name': 'Architectural Model',
                'components': ['walls', 'floors', 'ceilings', 'doors', 'windows'],
                'detail_level': 'medium',
                'polygon_range': (5000, 15000),
                'render_time_hours': 2,
                'pricing': {'basic': 3000000, 'standard': 5000000, 'premium': 8000000}
            },
            ModelType.INTERIOR: {
                'name': 'Interior Model',
                'components': ['furniture', 'fixtures', 'appliances', 'decorations'],
                'detail_level': 'high',
                'polygon_range': (10000, 25000),
                'render_time_hours': 3,
                'pricing': {'basic': 4000000, 'standard': 7000000, 'premium': 12000000}
            },
            ModelType.EXTERIOR: {
                'name': 'Exterior Model',
                'components': ['facade', 'roof', 'landscaping', 'lighting'],
                'detail_level': 'medium',
                'polygon_range': (8000, 20000),
                'render_time_hours': 2.5,
                'pricing': {'basic': 3500000, 'standard': 6000000, 'premium': 10000000}
            },
            ModelType.FULL_BUILDING: {
                'name': 'Full Building Model',
                'components': ['structure', 'interior', 'exterior', 'landscaping'],
                'detail_level': 'high',
                'polygon_range': (20000, 50000),
                'render_time_hours': 5,
                'pricing': {'standard': 10000000, 'premium': 15000000, 'ultra': 25000000}
            }
        }
        
        # Material library
        self.materials_library = {
            'walls': {
                'concrete': {'color': '#C0C0C0', 'texture': 'concrete_smooth'},
                'brick': {'color': '#8B4513', 'texture': 'brick_rough'},
                'plaster': {'color': '#F5F5DC', 'texture': 'plaster_smooth'},
                'wood': {'color': '#8B4513', 'texture': 'wood_grain'}
            },
            'floors': {
                'tile': {'color': '#F0F0F0', 'texture': 'ceramic_tile'},
                'wood': {'color': '#654321', 'texture': 'hardwood'},
                'marble': {'color': '#F8F8FF', 'texture': 'marble_polished'},
                'carpet': {'color': '#DC143C', 'texture': 'carpet_short'}
            },
            'furniture': {
                'fabric': {'color': '#4682B4', 'texture': 'fabric_upholstery'},
                'leather': {'color': '#8B4513', 'texture': 'leather_grain'},
                'metal': {'color': '#C0C0C0', 'texture': 'metal_brushed'},
                'plastic': {'color': '#FF6347', 'texture': 'plastic_smooth'}
            }
        }
        
        # File storage paths
        self.storage_paths = {
            'models': '3d_models/',
            'thumbnails': '3d_models/thumbnails/',
            'previews': '3d_models/previews/',
            'renders': '3d_models/renders/',
            'exports': '3d_models/exports/'
        }
        
        # Ensure directories exist
        for path in self.storage_paths.values():
            os.makedirs(path, exist_ok=True)
    
    def _init_database(self):
        """Initialize 3D models database"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # Create 3D models table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS models_3d (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    model_id TEXT UNIQUE NOT NULL,
                    property_id TEXT NOT NULL,
                    model_type TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    quality TEXT NOT NULL,
                    format TEXT NOT NULL,
                    status TEXT NOT NULL,
                    file_size_mb REAL NOT NULL,
                    polygon_count INTEGER NOT NULL,
                    texture_resolution TEXT,
                    render_time_hours REAL NOT NULL,
                    model_url TEXT,
                    thumbnail_url TEXT,
                    preview_url TEXT,
                    created_at TEXT NOT NULL,
                    published_at TEXT,
                    download_count INTEGER DEFAULT 0,
                    rating REAL DEFAULT 0,
                    notes TEXT DEFAULT '',
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create model components table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS model_components (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    component_id TEXT UNIQUE NOT NULL,
                    model_id TEXT NOT NULL,
                    component_name TEXT NOT NULL,
                    component_type TEXT NOT NULL,
                    material TEXT NOT NULL,
                    color TEXT NOT NULL,
                    dimensions TEXT NOT NULL,
                    position TEXT NOT NULL,
                    rotation TEXT NOT NULL,
                    is_interactive BOOLEAN DEFAULT 0,
                    created_at TEXT NOT NULL
                )
            ''')
            
            # Create model renders table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS model_renders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    render_id TEXT UNIQUE NOT NULL,
                    model_id TEXT NOT NULL,
                    render_type TEXT NOT NULL,
                    lighting_setup TEXT NOT NULL,
                    camera_positions TEXT NOT NULL,
                    resolution TEXT NOT NULL,
                    quality_preset TEXT NOT NULL,
                    output_format TEXT NOT NULL,
                    render_time REAL NOT NULL,
                    file_size_mb REAL NOT NULL,
                    render_url TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            ''')
            
            # Create model analytics table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS model_analytics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    model_id TEXT NOT NULL,
                    date TEXT NOT NULL,
                    views INTEGER DEFAULT 0,
                    downloads INTEGER DEFAULT 0,
                    avg_session_duration REAL DEFAULT 0,
                    interactions INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create indexes
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_models_property_id ON models_3d(property_id)')
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_models_status ON models_3d(status)')
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_components_model_id ON model_components(model_id)')
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_renders_model_id ON model_renders(model_id)')
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_analytics_model_id ON model_analytics(model_id)')
            
            # conn.commit() removed
            # conn.close() removed
            
            self.logger.info("3D models database initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Error initializing 3D models database: {e}")
            raise
    
    def create_3d_model(self, property_id: str, model_type: ModelType, 
                       title: str, quality: ModelQuality, format: ModelFormat,
                       description: str = "") -> str:
        """Create new 3D model"""
        try:
            model_id = f"model_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Get model configuration
            model_config = self.model_configs.get(model_type)
            if not model_config:
                self.logger.error(f"Unsupported model type: {model_type}")
                return ""
            
            # Calculate model specifications
            polygon_range = model_config['polygon_range']
            polygon_count = polygon_range[0] if quality == ModelQuality.BASIC else polygon_range[1]
            
            texture_resolution = self._get_texture_resolution(quality)
            render_time = model_config['render_time_hours'] * self._get_quality_multiplier(quality)
            file_size = polygon_count * 0.001  # Rough estimation
            
            # Generate file paths
            model_url = f"{self.storage_paths['models']}{model_id}.{format.value}"
            thumbnail_url = f"{self.storage_paths['thumbnails']}{model_id}_thumb.jpg"
            preview_url = f"{self.storage_paths['previews']}{model_id}_preview.jpg"
            
            # Create 3D model
            model = Model3D(
                model_id=model_id,
                property_id=property_id,
                model_type=model_type,
                title=title,
                description=description,
                quality=quality,
                format=format,
                status=ModelStatus.PLANNING,
                file_size_mb=file_size,
                polygon_count=polygon_count,
                texture_resolution=texture_resolution,
                render_time_hours=render_time,
                model_url=model_url,
                thumbnail_url=thumbnail_url,
                preview_url=preview_url,
                created_at=datetime.now()
            )
            
            # Save model
            self._save_model(model)
            
            # Create model components
            self._create_model_components(model_id, model_type)
            
            self.logger.info(f"Created 3D model {model_id} for property {property_id}")
            return model_id
            
        except Exception as e:
            self.logger.error(f"Error creating 3D model: {e}")
            return ""
    
    def _get_texture_resolution(self, quality: ModelQuality) -> str:
        """Get texture resolution based on quality"""
        resolutions = {
            ModelQuality.BASIC: "1024x1024",
            ModelQuality.STANDARD: "2048x2048",
            ModelQuality.PREMIUM: "4096x4096",
            ModelQuality.ULTRA: "8192x8192"
        }
        return resolutions.get(quality, "2048x2048")
    
    def _get_quality_multiplier(self, quality: ModelQuality) -> float:
        """Get quality multiplier for render time"""
        multipliers = {
            ModelQuality.BASIC: 0.5,
            ModelQuality.STANDARD: 1.0,
            ModelQuality.PREMIUM: 1.5,
            ModelQuality.ULTRA: 2.0
        }
        return multipliers.get(quality, 1.0)
    
    def _save_model(self, model: Model3D):
        """Save 3D model to database"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # cursor.execute() removed'''
                INSERT INTO models_3d 
                (model_id, property_id, model_type, title, description, quality, format, 
                 status, file_size_mb, polygon_count, texture_resolution, render_time_hours, 
                 model_url, thumbnail_url, preview_url, created_at, published_at, 
                 download_count, rating)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                model.model_id,
                model.property_id,
                model.model_type.value,
                model.title,
                model.description,
                model.quality.value,
                model.format.value,
                model.status.value,
                model.file_size_mb,
                model.polygon_count,
                model.texture_resolution,
                model.render_time_hours,
                model.model_url,
                model.thumbnail_url,
                model.preview_url,
                model.created_at.isoformat(),
                model.published_at.isoformat() if model.published_at else None,
                model.download_count,
                model.rating
            ))
            
            # conn.commit() removed
            # conn.close() removed
            
        except Exception as e:
            self.logger.error(f"Error saving model {model.model_id}: {e}")
            raise
    
    def _create_model_components(self, model_id: str, model_type: ModelType):
        """Create components for 3D model"""
        try:
            model_config = self.model_configs.get(model_type)
            if not model_config:
                return
            
            components = model_config['components']
            
            for i, component_type in enumerate(components):
                component_id = f"comp_{model_id}_{i+1:02d}"
                
                # Get material and color
                material_data = self._get_component_material(component_type)
                
                # Generate dimensions
                dimensions = self._generate_component_dimensions(component_type)
                
                # Generate position
                position = self._generate_component_position(component_type, i)
                
                # Generate rotation
                rotation = {'x': 0, 'y': 0, 'z': 0}
                
                component = ModelComponent(
                    component_id=component_id,
                    model_id=model_id,
                    component_name=component_type.title(),
                    component_type=component_type,
                    material=material_data['material'],
                    color=material_data['color'],
                    dimensions=dimensions,
                    position=position,
                    rotation=rotation,
                    is_interactive=component_type in ['doors', 'windows', 'furniture']
                )
                
                self._save_component(component)
            
            self.logger.info(f"Created {len(components)} components for model {model_id}")
            
        except Exception as e:
            self.logger.error(f"Error creating model components: {e}")
    
    def _get_component_material(self, component_type: str) -> Dict:
        """Get material data for component"""
        try:
            # Default material mappings
            material_mappings = {
                'walls': self.materials_library['walls']['plaster'],
                'floors': self.materials_library['floors']['tile'],
                'ceilings': self.materials_library['walls']['plaster'],
                'doors': self.materials_library['walls']['wood'],
                'windows': self.materials_library['walls']['metal'],
                'furniture': self.materials_library['furniture']['fabric'],
                'fixtures': self.materials_library['furniture']['metal'],
                'appliances': self.materials_library['furniture']['metal'],
                'decorations': self.materials_library['furniture']['plastic'],
                'facade': self.materials_library['walls']['brick'],
                'roof': self.materials_library['walls']['metal'],
                'landscaping': self.materials_library['walls']['concrete'],
                'lighting': self.materials_library['furniture']['metal'],
                'structure': self.materials_library['walls']['concrete']
            }
            
            return material_mappings.get(component_type, self.materials_library['walls']['plaster'])
            
        except Exception as e:
            self.logger.error(f"Error getting component material: {e}")
            return self.materials_library['walls']['plaster']
    
    def _generate_component_dimensions(self, component_type: str) -> Dict:
        """Generate dimensions for component"""
        try:
            dimensions = {
                'walls': {'length': 5.0, 'width': 0.2, 'height': 3.0},
                'floors': {'length': 5.0, 'width': 4.0, 'height': 0.1},
                'ceilings': {'length': 5.0, 'width': 4.0, 'height': 0.1},
                'doors': {'length': 0.9, 'width': 0.1, 'height': 2.1},
                'windows': {'length': 1.2, 'width': 0.1, 'height': 1.0},
                'furniture': {'length': 2.0, 'width': 1.0, 'height': 0.8},
                'fixtures': {'length': 0.5, 'width': 0.5, 'height': 0.3},
                'appliances': {'length': 0.6, 'width': 0.6, 'height': 0.9},
                'decorations': {'length': 0.3, 'width': 0.3, 'height': 0.3},
                'facade': {'length': 8.0, 'width': 0.2, 'height': 4.0},
                'roof': {'length': 8.5, 'width': 4.5, 'height': 0.3},
                'landscaping': {'length': 10.0, 'width': 10.0, 'height': 0.1},
                'lighting': {'length': 0.2, 'width': 0.2, 'height': 0.1},
                'structure': {'length': 8.0, 'width': 4.0, 'height': 3.5}
            }
            
            return dimensions.get(component_type, {'length': 1.0, 'width': 1.0, 'height': 1.0})
            
        except Exception as e:
            self.logger.error(f"Error generating component dimensions: {e}")
            return {'length': 1.0, 'width': 1.0, 'height': 1.0}
    
    def _generate_component_position(self, component_type: str, index: int) -> Dict:
        """Generate position for component"""
        try:
            positions = {
                'walls': {'x': 0.0, 'y': 0.0, 'z': index * 2.0},
                'floors': {'x': 0.0, 'y': 0.0, 'z': 0.0},
                'ceilings': {'x': 0.0, 'y': 3.0, 'z': 0.0},
                'doors': {'x': 2.0, 'y': 0.0, 'z': 0.0},
                'windows': {'x': 1.0, 'y': 1.0, 'z': 0.0},
                'furniture': {'x': index * 1.5, 'y': 0.0, 'z': index * 1.5},
                'fixtures': {'x': index * 1.0, 'y': 0.8, 'z': index * 1.0},
                'appliances': {'x': index * 1.2, 'y': 0.0, 'z': index * 1.2},
                'decorations': {'x': index * 0.8, 'y': 0.5, 'z': index * 0.8},
                'facade': {'x': 0.0, 'y': 0.0, 'z': 0.0},
                'roof': {'x': 0.0, 'y': 3.5, 'z': 0.0},
                'landscaping': {'x': 0.0, 'y': -0.1, 'z': 0.0},
                'lighting': {'x': index * 2.0, 'y': 2.5, 'z': index * 2.0},
                'structure': {'x': 0.0, 'y': 0.0, 'z': 0.0}
            }
            
            return positions.get(component_type, {'x': 0.0, 'y': 0.0, 'z': 0.0})
            
        except Exception as e:
            self.logger.error(f"Error generating component position: {e}")
            return {'x': 0.0, 'y': 0.0, 'z': 0.0}
    
    def _save_component(self, component: ModelComponent):
        """Save component to database"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # cursor.execute() removed'''
                INSERT INTO model_components 
                (component_id, model_id, component_name, component_type, material, 
                 color, dimensions, position, rotation, is_interactive, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                component.component_id,
                component.model_id,
                component.component_name,
                component.component_type,
                component.material,
                component.color,
                json.dumps(component.dimensions),
                json.dumps(component.position),
                json.dumps(component.rotation),
                component.is_interactive,
                component.created_at.isoformat()
            ))
            
            # conn.commit() removed
            # conn.close() removed
            
        except Exception as e:
            self.logger.error(f"Error saving component {component.component_id}: {e}")
            raise
    
    def update_model_status(self, model_id: str, new_status: ModelStatus, 
                          notes: str = "", file_size_mb: float = 0.0) -> bool:
        """Update model status and metadata"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            update_fields = ['status = ?', 'updated_at = ?']
            update_values = [new_status.value, datetime.now().isoformat()]
            
            if file_size_mb > 0:
                update_fields.append('file_size_mb = ?')
                update_values.append(file_size_mb)
            
            if new_status == ModelStatus.PUBLISHED:
                update_fields.append('published_at = ?')
                update_values.append(datetime.now().isoformat())
            
            update_values.append(notes)
            update_values.append(model_id)
            
            # cursor.execute() removedf'''
                UPDATE models_3d 
                SET {', '.join(update_fields)}, notes = ?
                WHERE model_id = ?
            ''', update_values)
            
            # conn.commit() removed
            # conn.close() removed
            
            self.logger.info(f"Updated model {model_id} status to {new_status.value}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error updating model {model_id} status: {e}")
            return False
    
    def create_model_render(self, model_id: str, render_type: str, 
                          resolution: str = "1920x1080") -> str:
        """Create render for 3D model"""
        try:
            render_id = f"render_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Generate render configuration
            lighting_setup = {
                'ambient': 0.3,
                'directional': 0.7,
                'point_lights': 3,
                'shadow_quality': 'high'
            }
            
            camera_positions = [
                {'position': {'x': 5, 'y': 2, 'z': 5}, 'target': {'x': 0, 'y': 1, 'z': 0}},
                {'position': {'x': -5, 'y': 2, 'z': 5}, 'target': {'x': 0, 'y': 1, 'z': 0}},
                {'position': {'x': 0, 'y': 4, 'z': 3}, 'target': {'x': 0, 'y': 0, 'z': 0}}
            ]
            
            quality_preset = 'high'
            output_format = 'jpg'
            render_time = 2.5  # Estimated render time
            file_size = 8.5  # Estimated file size
            render_url = f"{self.storage_paths['renders']}{render_id}.{output_format}"
            
            render = ModelRender(
                render_id=render_id,
                model_id=model_id,
                render_type=render_type,
                lighting_setup=lighting_setup,
                camera_positions=camera_positions,
                resolution=resolution,
                quality_preset=quality_preset,
                output_format=output_format,
                render_time=render_time,
                file_size_mb=file_size,
                render_url=render_url
            )
            
            # Save render
            self._save_render(render)
            
            self.logger.info(f"Created render {render_id} for model {model_id}")
            return render_id
            
        except Exception as e:
            self.logger.error(f"Error creating model render: {e}")
            return ""
    
    def _save_render(self, render: ModelRender):
        """Save render to database"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # cursor.execute() removed'''
                INSERT INTO model_renders 
                (render_id, model_id, render_type, lighting_setup, camera_positions, 
                 resolution, quality_preset, output_format, render_time, file_size_mb, render_url, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                render.render_id,
                render.model_id,
                render.render_type,
                json.dumps(render.lighting_setup),
                json.dumps(render.camera_positions),
                render.resolution,
                render.quality_preset,
                render.output_format,
                render.render_time,
                render.file_size_mb,
                render.render_url,
                render.created_at.isoformat()
            ))
            
            # conn.commit() removed
            # conn.close() removed
            
        except Exception as e:
            self.logger.error(f"Error saving render {render.render_id}: {e}")
            raise
    
    def generate_model_report(self, property_id: Optional[str] = None) -> Dict:
        """Generate comprehensive 3D model report"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            if property_id:
                # cursor.execute() removed'SELECT * FROM models_3d WHERE property_id = ?', (property_id,))
            else:
                # cursor.execute() removed'SELECT * FROM models_3d')
            
            models = []
            for row in cursor.fetchall():
                columns = [desc[0] for desc in cursor.description]
                model_data = dict(zip(columns, row))
                models.append(model_data)
            
            # Calculate statistics
            total_models = len(models)
            total_polygons = sum(model['polygon_count'] for model in models)
            total_file_size = sum(model['file_size_mb'] for model in models)
            avg_rating = sum(model['rating'] for model in models) / max(total_models, 1)
            
            # Status distribution
            status_counts = {}
            type_counts = {}
            quality_counts = {}
            format_counts = {}
            
            for model in models:
                status = model['status']
                model_type = model['model_type']
                quality = model['quality']
                format_type = model['format']
                
                status_counts[status] = status_counts.get(status, 0) + 1
                type_counts[model_type] = type_counts.get(model_type, 0) + 1
                quality_counts[quality] = quality_counts.get(quality, 0) + 1
                format_counts[format_type] = format_counts.get(format_type, 0) + 1
            
            # conn.close() removed
            
            report = {
                'generated_at': datetime.now().isoformat(),
                'property_id': property_id,
                'summary_statistics': {
                    'total_models': total_models,
                    'total_polygons': total_polygons,
                    'total_file_size_mb': total_file_size,
                    'average_rating': avg_rating,
                    'models_published': status_counts.get('published', 0)
                },
                'distribution_analysis': {
                    'status_distribution': status_counts,
                    'type_distribution': type_counts,
                    'quality_distribution': quality_counts,
                    'format_distribution': format_counts
                },
                'detailed_models': models
            }
            
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating model report: {e}")
            return {}
    
    def create_sample_models(self) -> int:
        """Create sample 3D models for testing"""
        try:
            sample_properties = [
                {'id': 'prop_001', 'name': 'Rumah Cipocok Jaya', 'type': 'house'},
                {'id': 'prop_002', 'name': 'Apartemen Serang', 'type': 'apartment'},
                {'id': 'prop_003', 'name': 'Ruko Ciruas', 'type': 'commercial'}
            ]
            
            model_types = [ModelType.ARCHITECTURAL, ModelType.INTERIOR, ModelType.FULL_BUILDING]
            qualities = [ModelQuality.STANDARD, ModelQuality.PREMIUM]
            formats = [ModelFormat.OBJ, ModelFormat.GLTF, ModelFormat.FBX]
            
            created_count = 0
            
            for i, property_data in enumerate(sample_properties):
                model_type = model_types[i % len(model_types)]
                quality = qualities[i % len(qualities)]
                format_type = formats[i % len(formats)]
                
                model_id = self.create_3d_model(
                    property_data['id'],
                    model_type,
                    f"3D Model {property_data['name']}",
                    quality,
                    format_type,
                    f"Professional {model_type.value} model for {property_data['name']}"
                )
                
                if model_id:
                    # Simulate model processing
                    self.update_model_status(model_id, ModelStatus.MODELING, "Creating 3D geometry")
                    self.update_model_status(model_id, ModelStatus.TEXTURING, "Applying materials and textures")
                    self.update_model_status(model_id, ModelStatus.RENDERING, "Generating high-quality renders")
                    self.update_model_status(model_id, ModelStatus.READY, "Model ready for review")
                    self.update_model_status(model_id, ModelStatus.PUBLISHED, "Model published", 25.8)
                    
                    # Create sample render
                    self.create_model_render(model_id, "exterior_view")
                    self.create_model_render(model_id, "interior_view")
                    
                    created_count += 1
            
            self.logger.info(f"Created {created_count} sample 3D models")
            return created_count
            
        except Exception as e:
            self.logger.error(f"Error creating sample models: {e}")
            return 0

def main():
    """Main function to demonstrate 3D model generator"""
    print("=" * 60)
    print("🏗️ 3D MODEL GENERATOR - VISUAL ENGINE")
    print("=" * 60)
    
    # Initialize 3D model generator
    model_gen = Model3DGenerator()
    
    # Create sample models
    print("🏠 Creating sample 3D models...")
    created = model_gen.create_sample_models()
    print(f"✅ Created {created} sample models")
    
    # Generate model report
    print("\n📊 Generating 3D model report...")
    report = model_gen.generate_model_report()
    
    if report:
        print("📈 Model Statistics:")
        summary = report.get('summary_statistics', {})
        print(f"  - Total Models: {summary.get('total_models', 0)}")
        print(f"  - Total Polygons: {summary.get('total_polygons', 0):,}")
        print(f"  - Total File Size: {summary.get('total_file_size_mb', 0):.1f} MB")
        print(f"  - Published Models: {summary.get('models_published', 0)}")
        print(f"  - Average Rating: {summary.get('average_rating', 0):.2f}")
        
        distribution = report.get('distribution_analysis', {})
        print(f"\n📋 Distribution Analysis:")
        print(f"  - Status: {distribution.get('status_distribution', {})}")
        print(f"  - Types: {distribution.get('type_distribution', {})}")
        print(f"  - Qualities: {distribution.get('quality_distribution', {})}")
        print(f"  - Formats: {distribution.get('format_distribution', {})}")
    
    # Show model details
    detailed_models = report.get('detailed_models', [])
    if detailed_models:
        sample_model = detailed_models[0]
        print(f"\n🏗️ Sample Model Details:")
        print(f"  - Title: {sample_model['title']}")
        print(f"  - Type: {sample_model['model_type']}")
        print(f"  - Quality: {sample_model['quality']}")
        print(f"  - Format: {sample_model['format']}")
        print(f"  - Polygons: {sample_model['polygon_count']:,}")
        print(f"  - File Size: {sample_model['file_size_mb']:.1f} MB")
        print(f"  - Render Time: {sample_model['render_time_hours']:.1f} hours")
        print(f"  - Texture Resolution: {sample_model['texture_resolution']}")
    
    # Save report
    report_file = '3d_model_report.json'
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n📁 Report saved to: {report_file}")
    
    print("\n" + "=" * 60)
    print("✅ 3D MODEL GENERATOR SETUP COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()
