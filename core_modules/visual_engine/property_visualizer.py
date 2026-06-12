"""
Property Visualizer - Visual Engine
Advanced property visualization and virtual tour generation
"""

import json
import random
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO
import base64
import math

class PropertyVisualizer:
    """Advanced property visualization and virtual tour generator"""
    
    def __init__(self):
        self.name = "Property Visualizer"
        self.version = "1.0.0"
        self.virtual_tours = {}
        self.property_models = {}
        self.visualization_configs = {}
        self.matterport_api_key = None
        self.kuula_api_key = None
    
    def set_api_keys(self, matterport_api_key=None, kuula_api_key=None):
        """Set API keys for 3D tour services"""
        self.matterport_api_key = matterport_api_key
        self.kuula_api_key = kuula_api_key
    
    def create_virtual_tour(self, tour_config):
        """Create virtual property tour"""
        tour = {
            'tour_id': f"VT_TOUR_{len(self.virtual_tours) + 1:03d}",
            'property_id': tour_config.get('property_id'),
            'tour_type': tour_config.get('tour_type', '360_virtual'),
            'property_data': tour_config.get('property_data', {}),
            'tour_settings': tour_config.get('tour_settings', {}),
            'scenes': self._create_tour_scenes(tour_config),
            'navigation': self._create_tour_navigation(tour_config),
            'interactive_elements': tour_config.get('interactive_elements', []),
            'status': 'created',
            'created_at': datetime.now().isoformat()
        }
        
        # Generate tour based on type
        if tour_config.get('tour_type') == 'matterport':
            tour['matterport_id'] = self._create_matterport_tour(tour_config)
        elif tour_config.get('tour_type') == 'kuula':
            tour['kuula_id'] = self._create_kuula_tour(tour_config)
        elif tour_config.get('tour_type') == 'custom_360':
            tour['custom_tour_data'] = self._create_custom_360_tour(tour_config)
        
        self.virtual_tours[tour['tour_id']] = tour
        return tour
    
    def _create_tour_scenes(self, tour_config):
        """Create tour scenes"""
        property_data = tour_config.get('property_data', {})
        
        scenes = [
            {
                'scene_id': 'exterior',
                'name': 'Property Exterior',
                'description': 'Beautiful exterior view of the property',
                'image_url': property_data.get('exterior_image', ''),
                'hotspots': [
                    {'x': 50, 'y': 30, 'type': 'info', 'content': 'Modern architectural design'},
                    {'x': 70, 'y': 50, 'type': 'navigation', 'target': 'living_room'}
                ],
                'duration': 15
            },
            {
                'scene_id': 'living_room',
                'name': 'Living Room',
                'description': 'Spacious living area with natural light',
                'image_url': property_data.get('living_room_image', ''),
                'hotspots': [
                    {'x': 30, 'y': 40, 'type': 'info', 'content': 'Open concept design'},
                    {'x': 60, 'y': 60, 'type': 'navigation', 'target': 'kitchen'}
                ],
                'duration': 20
            },
            {
                'scene_id': 'kitchen',
                'name': 'Kitchen',
                'description': 'Modern kitchen with premium appliances',
                'image_url': property_data.get('kitchen_image', ''),
                'hotspots': [
                    {'x': 40, 'y': 50, 'type': 'info', 'content': 'Premium stainless steel appliances'},
                    {'x': 80, 'y': 40, 'type': 'navigation', 'target': 'master_bedroom'}
                ],
                'duration': 15
            },
            {
                'scene_id': 'master_bedroom',
                'name': 'Master Bedroom',
                'description': 'Comfortable master bedroom with en-suite',
                'image_url': property_data.get('bedroom_image', ''),
                'hotspots': [
                    {'x': 50, 'y': 30, 'type': 'info', 'content': 'Spacious walk-in closet'},
                    {'x': 70, 'y': 70, 'type': 'navigation', 'target': 'bathroom'}
                ],
                'duration': 20
            },
            {
                'scene_id': 'bathroom',
                'name': 'Bathroom',
                'description': 'Modern bathroom with premium fixtures',
                'image_url': property_data.get('bathroom_image', ''),
                'hotspots': [
                    {'x': 40, 'y': 40, 'type': 'info', 'content': 'Luxury marble finishes'},
                    {'x': 60, 'y': 60, 'type': 'navigation', 'target': 'backyard'}
                ],
                'duration': 15
            },
            {
                'scene_id': 'backyard',
                'name': 'Backyard',
                'description': 'Beautiful backyard with garden',
                'image_url': property_data.get('backyard_image', ''),
                'hotspots': [
                    {'x': 50, 'y': 50, 'type': 'info', 'content': 'Perfect for entertaining'},
                    {'x': 30, 'y': 30, 'type': 'navigation', 'target': 'exterior'}
                ],
                'duration': 15
            }
        ]
        
        return scenes
    
    def _create_tour_navigation(self, tour_config):
        """Create tour navigation"""
        return {
            'navigation_type': 'hotspot_based',
            'auto_play': tour_config.get('auto_play', True),
            'auto_advance_interval': tour_config.get('auto_advance_interval', 15),
            'navigation_controls': {
                'previous_scene': True,
                'next_scene': True,
                'scene_menu': True,
                'fullscreen': True,
                'vr_mode': True
            },
            'progress_bar': True,
            'scene_transitions': {
                'type': 'fade',
                'duration': 1.0,
                'easing': 'ease-in-out'
            }
        }
    
    def _create_matterport_tour(self, tour_config):
        """Create Matterport virtual tour"""
        if not self.matterport_api_key:
            return {
                'status': 'error',
                'message': 'Matterport API key not configured'
            }
        
        # Simulate Matterport API call
        return f"MP_TOUR_{random.randint(10000, 99999)}"
    
    def _create_kuula_tour(self, tour_config):
        """Create Kuula virtual tour"""
        if not self.kuula_api_key:
            return {
                'status': 'error',
                'message': 'Kuula API key not configured'
            }
        
        # Simulate Kuula API call
        return f"KUULA_TOUR_{random.randint(10000, 99999)}"
    
    def _create_custom_360_tour(self, tour_config):
        """Create custom 360-degree tour"""
        tour_data = {
            'tour_format': 'equirectangular',
            'viewer_type': 'pannellum',
            'initial_view': {
                'hfov': 110,
                'pitch': 0,
                'yaw': 0
            },
            'scenes': self._create_360_scenes(tour_config),
            'hotspots': self._create_360_hotspots(tour_config),
            'auto_rotate': tour_config.get('auto_rotate', True),
            'auto_rotate_speed': tour_config.get('auto_rotate_speed', 0.5)
        }
        
        return tour_data
    
    def _create_360_scenes(self, tour_config):
        """Create 360-degree scenes"""
        property_data = tour_config.get('property_data', {})
        
        scenes = []
        room_types = ['living_room', 'kitchen', 'master_bedroom', 'bathroom', 'backyard']
        
        for i, room_type in enumerate(room_types):
            scene = {
                'id': room_type,
                'title': room_type.replace('_', ' ').title(),
                'image': property_data.get(f'{room_type}_360_image', ''),
                'hfov': 110,
                'pitch': 0,
                'yaw': 0,
                'type': 'equirectangular'
            }
            scenes.append(scene)
        
        return scenes
    
    def _create_360_hotspots(self, tour_config):
        """Create 360-degree hotspots"""
        hotspots = [
            {
                'pitch': -10,
                'yaw': 45,
                'type': 'info',
                'text': 'Premium finishes throughout',
                'CSSClass': 'custom-hotspot'
            },
            {
                'pitch': 0,
                'yaw': 90,
                'type': 'scene',
                'sceneId': 'kitchen',
                'targetPitch': 0,
                'targetYaw': 0,
                'text': 'Go to Kitchen'
            }
        ]
        
        return hotspots
    
    def create_property_model(self, model_config):
        """Create 3D property model"""
        model = {
            'model_id': f"PROP_MODEL_{len(self.property_models) + 1:03d}",
            'property_id': model_config.get('property_id'),
            'model_type': model_config.get('model_type', 'architectural'),
            'property_data': model_config.get('property_data', {}),
            'model_settings': model_config.get('model_settings', {}),
            'textures': model_config.get('textures', {}),
            'lighting': model_config.get('lighting', {}),
            'camera_positions': self._create_camera_positions(model_config),
            'render_settings': model_config.get('render_settings', {}),
            'status': 'created',
            'created_at': datetime.now().isoformat()
        }
        
        self.property_models[model['model_id']] = model
        return model
    
    def _create_camera_positions(self, model_config):
        """Create camera positions for 3D model"""
        positions = [
            {
                'position': [5, 2, 5],
                'target': [0, 0, 0],
                'name': 'Front View',
                'description': 'Front exterior view'
            },
            {
                'position': [0, 3, 8],
                'target': [0, 0, 0],
                'name': 'Top View',
                'description': 'Bird\'s eye view'
            },
            {
                'position': [8, 1.5, 0],
                'target': [0, 0, 0],
                'name': 'Side View',
                'description': 'Side exterior view'
            },
            {
                'position': [2, 1.8, 2],
                'target': [0, 0, 0],
                'name': 'Interior View',
                'description': 'Interior perspective'
            }
        ]
        
        return positions
    
    def create_floor_plan_visualization(self, floor_plan_config):
        """Create interactive floor plan visualization"""
        floor_plan = {
            'floor_plan_id': f"FLOOR_PLAN_{len(self.property_models) + 1:03d}",
            'property_id': floor_plan_config.get('property_id'),
            'floor_number': floor_plan_config.get('floor_number', 1),
            'dimensions': floor_plan_config.get('dimensions', {'width': 1000, 'height': 800}),
            'rooms': self._create_floor_plan_rooms(floor_plan_config),
            'interactive_elements': floor_plan_config.get('interactive_elements', []),
            'measurements': floor_plan_config.get('measurements', {}),
            'furniture_layout': floor_plan_config.get('furniture_layout', {}),
            'status': 'created',
            'created_at': datetime.now().isoformat()
        }
        
        self.property_models[floor_plan['floor_plan_id']] = floor_plan
        return floor_plan
    
    def _create_floor_plan_rooms(self, floor_plan_config):
        """Create floor plan rooms"""
        rooms = [
            {
                'room_id': 'living_room',
                'name': 'Living Room',
                'dimensions': {'width': 400, 'height': 350},
                'position': {'x': 50, 'y': 50},
                'color': '#E8F4F8',
                'area': 140,  # square meters
                'features': ['Large windows', 'Open concept', 'High ceilings']
            },
            {
                'room_id': 'kitchen',
                'name': 'Kitchen',
                'dimensions': {'width': 250, 'height': 200},
                'position': {'x': 450, 'y': 50},
                'color': '#FFF4E6',
                'area': 50,
                'features': ['Modern appliances', 'Island', 'Pantry']
            },
            {
                'room_id': 'master_bedroom',
                'name': 'Master Bedroom',
                'dimensions': {'width': 300, 'height': 280},
                'position': {'x': 50, 'y': 400},
                'color': '#F0F8FF',
                'area': 84,
                'features': ['En-suite bathroom', 'Walk-in closet', 'Balcony']
            },
            {
                'room_id': 'bathroom',
                'name': 'Bathroom',
                'dimensions': {'width': 200, 'height': 150},
                'position': {'x': 350, 'y': 400},
                'color': '#E6F3FF',
                'area': 30,
                'features': ['Modern fixtures', 'Double vanity', 'Shower']
            },
            {
                'room_id': 'bedroom_2',
                'name': 'Bedroom 2',
                'dimensions': {'width': 250, 'height': 200},
                'position': {'x': 550, 'y': 400},
                'color': '#F0FFF0',
                'area': 50,
                'features': ['Built-in closet', 'Large window']
            }
        ]
        
        return rooms
    
    def generate_floor_plan_image(self, floor_plan_id, output_format='PNG'):
        """Generate floor plan image"""
        floor_plan = self.property_models.get(floor_plan_id)
        if not floor_plan:
            return {'error': 'Floor plan not found'}
        
        try:
            # Create image
            width = floor_plan.get('dimensions', {'width': 1000, 'height': 800})['width']
            height = floor_plan.get('dimensions', {'width': 1000, 'height': 800})['height']
            
            image = Image.new('RGB', (width, height), (255, 255, 255))
            draw = ImageDraw.Draw(image)
            
            # Draw rooms
            rooms = floor_plan.get('rooms', [])
            for room in rooms:
                position = room.get('position', {'x': 0, 'y': 0})
                dimensions = room.get('dimensions', {'width': 100, 'height': 100})
                color = room.get('color', '#FFFFFF')
                
                # Convert hex color to RGB
                hex_color = color.lstrip('#')
                rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
                
                # Draw room rectangle
                draw.rectangle([
                    (position['x'], position['y']),
                    (position['x'] + dimensions['width'], position['y'] + dimensions['height'])
                ], fill=rgb_color, outline='black', width=2)
                
                # Draw room label
                draw.text((
                    position['x'] + dimensions['width']//2 - 50,
                    position['y'] + dimensions['height']//2 - 10
                ), room.get('name', ''), fill='black', font=ImageFont.truetype("Arial", 12, "bold"))
            
            # Draw room dimensions
            for room in rooms:
                position = room.get('position', {'x': 0, 'y': 0})
                dimensions = room.get('dimensions', {'width': 100, 'height': 100})
                area = room.get('area', 0)
                
                # Draw area text
                draw.text((
                    position['x'] + 5,
                    position['y'] + dimensions['height'] - 20
                ), f"{area}m²", fill='black', font=ImageFont.truetype("Arial", 10, "normal"))
            
            # Add title
            draw.text((width//2 - 100, 20), f"Floor {floor_plan.get('floor_number', 1)} Plan", 
                     fill='black', font=ImageFont.truetype("Arial", 16, "bold"))
            
            # Add scale
            draw.text((50, height - 30), "Scale: 1:100", fill='black', font=ImageFont.truetype("Arial", 10, "normal"))
            
            # Save to BytesIO
            img_buffer = BytesIO()
            image.save(img_buffer, format=output_format)
            
            return {
                'floor_plan_id': floor_plan_id,
                'image_data': img_buffer.getvalue(),
                'file_name': f"floor_plan_{floor_plan_id}.{output_format}",
                'file_size': len(img_buffer.getvalue()),
                'format': output_format,
                'status': 'generated'
            }
            
        except Exception as e:
            return {
                'floor_plan_id': floor_plan_id,
                'status': 'error',
                'error': str(e)
            }
    
    def create_property_comparison_visualization(self, comparison_config):
        """Create property comparison visualization"""
        comparison = {
            'comparison_id': f"PROP_COMPARE_{len(self.property_models) + 1:03d}",
            'properties': comparison_config.get('properties', []),
            'comparison_criteria': comparison_config.get('criteria', ['price', 'area', 'bedrooms', 'bathrooms']),
            'visualization_type': comparison_config.get('visualization_type', 'radar_chart'),
            'chart_data': self._generate_comparison_chart_data(comparison_config),
            'status': 'created',
            'created_at': datetime.now().isoformat()
        }
        
        self.property_models[comparison['comparison_id']] = comparison
        return comparison
    
    def _generate_comparison_chart_data(self, comparison_config):
        """Generate comparison chart data"""
        properties = comparison_config.get('properties', [])
        criteria = comparison_config.get('criteria', ['price', 'area', 'bedrooms', 'bathrooms'])
        
        chart_data = {
            'labels': criteria,
            'datasets': []
        }
        
        for i, property in enumerate(properties):
            dataset = {
                'label': property.get('name', f'Property {i+1}'),
                'data': [],
                'backgroundColor': self._get_property_color(i),
                'borderColor': self._get_property_color(i),
                'borderWidth': 2
            }
            
            for criterion in criteria:
                value = property.get(criterion, 0)
                # Normalize values for radar chart
                if criterion == 'price':
                    normalized_value = min(100, (value / 1000000) * 100)  # Normalize by 1M
                elif criterion == 'area':
                    normalized_value = min(100, (value / 500) * 100)  # Normalize by 500m²
                elif criterion in ['bedrooms', 'bathrooms']:
                    normalized_value = min(100, (value / 10) * 100)  # Normalize by 10
                else:
                    normalized_value = 50
                
                dataset['data'].append(normalized_value)
            
            chart_data['datasets'].append(dataset)
        
        return chart_data
    
    def _get_property_color(self, index):
        """Get property color for chart"""
        colors = [
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)'
        ]
        return colors[index % len(colors)]
    
    def create_neighborhood_visualization(self, neighborhood_config):
        """Create neighborhood visualization"""
        visualization = {
            'visualization_id': f"NEIGHBORHOOD_{len(self.property_models) + 1:03d}",
            'property_id': neighborhood_config.get('property_id'),
            'neighborhood_data': neighborhood_config.get('neighborhood_data', {}),
            'visualization_type': neighborhood_config.get('visualization_type', 'map_based'),
            'map_data': self._generate_neighborhood_map_data(neighborhood_config),
            'amenities': self._generate_amenity_data(neighborhood_config),
            'transportation': self._generate_transportation_data(neighborhood_config),
            'status': 'created',
            'created_at': datetime.now().isoformat()
        }
        
        self.property_models[visualization['visualization_id']] = visualization
        return visualization
    
    def _generate_neighborhood_map_data(self, neighborhood_config):
        """Generate neighborhood map data"""
        return {
            'center': {
                'lat': -6.1255,  # Serang coordinates
                'lng': 106.1641
            },
            'zoom': 14,
            'markers': [
                {
                    'type': 'property',
                    'position': {'lat': -6.1255, 'lng': 106.1641},
                    'title': 'Property Location',
                    'icon': 'home'
                },
                {
                    'type': 'school',
                    'position': {'lat': -6.1300, 'lng': 106.1700},
                    'title': 'Local School',
                    'icon': 'school'
                },
                {
                    'type': 'hospital',
                    'position': {'lat': -6.1200, 'lng': 106.1600},
                    'title': 'Hospital',
                    'icon': 'hospital'
                },
                {
                    'type': 'shopping',
                    'position': {'lat': -6.1350, 'lng': 106.1750},
                    'title': 'Shopping Center',
                    'icon': 'shopping-cart'
                }
            ],
            'boundaries': [
                {'lat': -6.1100, 'lng': 106.1500},
                {'lat': -6.1400, 'lng': 106.1500},
                {'lat': -6.1400, 'lng': 106.1800},
                {'lat': -6.1100, 'lng': 106.1800}
            ]
        }
    
    def _generate_amenity_data(self, neighborhood_config):
        """Generate amenity data"""
        return {
            'schools': [
                {'name': 'SDN Serang', 'distance': '0.5 km', 'rating': 4.2},
                {'name': 'SMPN 1 Serang', 'distance': '1.2 km', 'rating': 4.5},
                {'name': 'SMAN 1 Serang', 'distance': '2.0 km', 'rating': 4.3}
            ],
            'hospitals': [
                {'name': 'RSUD Serang', 'distance': '1.5 km', 'rating': 4.1},
                {'name': 'RS Sari Asih', 'distance': '3.0 km', 'rating': 4.4}
            ],
            'shopping': [
                {'name': 'Serang Mall', 'distance': '2.5 km', 'rating': 4.0},
                {'name': 'Pasar Serang', 'distance': '1.0 km', 'rating': 3.8}
            ],
            'parks': [
                {'name': 'Taman Kota Serang', 'distance': '0.8 km', 'rating': 4.2},
                {'name': 'Alun-alun Serang', 'distance': '1.5 km', 'rating': 4.5}
            ]
        }
    
    def _generate_transportation_data(self, neighborhood_config):
        """Generate transportation data"""
        return {
            'public_transport': [
                {'type': 'Bus', 'stop': 'Halte Serang', 'distance': '0.3 km', 'routes': ['A1', 'B2']},
                {'type': 'Angkot', 'stop': 'Terminal Serang', 'distance': '1.0 km', 'routes': ['C3', 'D4']}
            ],
            'roads': [
                {'name': 'Jalan Raya Serang', 'type': 'Main Road', 'distance': '0.2 km'},
                {'name': 'Jalan Sudirman', 'type': 'Secondary Road', 'distance': '0.5 km'}
            ],
            'airports': [
                {'name': 'Soekarno-Hatta', 'distance': '80 km', 'travel_time': '1.5 hours'},
                {'name': 'Halim Perdanakusuma', 'distance': '70 km', 'travel_time': '1.2 hours'}
            ]
        }
    
    def create_property_heatmap(self, heatmap_config):
        """Create property value heatmap"""
        heatmap = {
            'heatmap_id': f"HEATMAP_{len(self.property_models) + 1:03d}",
            'region': heatmap_config.get('region', 'Serang'),
            'data_type': heatmap_config.get('data_type', 'property_values'),
            'heatmap_data': self._generate_heatmap_data(heatmap_config),
            'color_scale': heatmap_config.get('color_scale', 'viridis'),
            'intervals': heatmap_config.get('intervals', 10),
            'status': 'created',
            'created_at': datetime.now().isoformat()
        }
        
        self.property_models[heatmap['heatmap_id']] = heatmap
        return heatmap
    
    def _generate_heatmap_data(self, heatmap_config):
        """Generate heatmap data"""
        region = heatmap_config.get('region', 'Serang')
        data_type = heatmap_config.get('data_type', 'property_values')
        
        # Generate grid data
        grid_size = 20
        heatmap_data = []
        
        for i in range(grid_size):
            for j in range(grid_size):
                lat = -6.1100 + (i * 0.0015)
                lng = 106.1500 + (j * 0.0015)
                
                # Generate value based on data type
                if data_type == 'property_values':
                    value = random.uniform(300000000, 800000000)  # Property prices
                elif data_type == 'demand':
                    value = random.uniform(0, 100)  # Demand percentage
                elif data_type == 'growth':
                    value = random.uniform(5, 15)  # Growth percentage
                else:
                    value = random.uniform(0, 100)
                
                heatmap_data.append({
                    'lat': lat,
                    'lng': lng,
                    'value': value,
                    'weight': value / 100
                })
        
        return heatmap_data
    
    def create_property_timeline(self, timeline_config):
        """Create property development timeline visualization"""
        timeline = {
            'timeline_id': f"TIMELINE_{len(self.property_models) + 1:03d}",
            'property_id': timeline_config.get('property_id'),
            'timeline_type': timeline_config.get('timeline_type', 'construction'),
            'events': self._generate_timeline_events(timeline_config),
            'milestones': timeline_config.get('milestones', []),
            'status': 'created',
            'created_at': datetime.now().isoformat()
        }
        
        self.property_models[timeline['timeline_id']] = timeline
        return timeline
    
    def _generate_timeline_events(self, timeline_config):
        """Generate timeline events"""
        events = [
            {
                'date': '2024-01-15',
                'title': 'Ground Breaking',
                'description': 'Construction begins',
                'type': 'milestone',
                'status': 'completed'
            },
            {
                'date': '2024-03-20',
                'title': 'Foundation Complete',
                'description': 'Building foundation finished',
                'type': 'progress',
                'status': 'completed'
            },
            {
                'date': '2024-06-15',
                'title': 'Structure Complete',
                'description': 'Main structure finished',
                'type': 'milestone',
                'status': 'completed'
            },
            {
                'date': '2024-09-01',
                'title': 'Interior Finishing',
                'description': 'Interior work in progress',
                'type': 'progress',
                'status': 'in_progress'
            },
            {
                'date': '2024-11-15',
                'title': 'Project Completion',
                'description': 'Property ready for handover',
                'type': 'milestone',
                'status': 'upcoming'
            }
        ]
        
        return events
    
    def generate_visualization_report(self, visualization_id):
        """Generate comprehensive visualization report"""
        visualization = self.property_models.get(visualization_id)
        if not visualization:
            return {'error': 'Visualization not found'}
        
        report = {
            'visualization_id': visualization_id,
            'visualization_type': visualization.get('visualization_type', 'unknown'),
            'performance_metrics': self._calculate_visualization_performance(visualization_id),
            'usage_statistics': self._get_visualization_usage(visualization_id),
            'engagement_data': self._get_visualization_engagement(visualization_id),
            'optimization_recommendations': self._generate_visualization_recommendations(visualization_id),
            'generated_at': datetime.now().isoformat()
        }
        
        return report
    
    def _calculate_visualization_performance(self, visualization_id):
        """Calculate visualization performance metrics"""
        return {
            'total_views': random.randint(100, 1000),
            'unique_viewers': random.randint(50, 500),
            'average_view_time': random.randint(30, 180),  # seconds
            'completion_rate': random.uniform(60, 95),  # percentage
            'interaction_rate': random.uniform(10, 40),  # percentage
            'share_rate': random.uniform(5, 20),  # percentage
            'conversion_rate': random.uniform(2, 8)  # percentage
        }
    
    def _get_visualization_usage(self, visualization_id):
        """Get visualization usage statistics"""
        return {
            'daily_views': [random.randint(5, 50) for _ in range(30)],
            'peak_hours': ['10:00', '14:00', '18:00'],
            'device_breakdown': {
                'desktop': random.randint(40, 60),
                'mobile': random.randint(30, 50),
                'tablet': random.randint(5, 15)
            },
            'browser_breakdown': {
                'chrome': random.randint(40, 60),
                'safari': random.randint(20, 30),
                'firefox': random.randint(10, 20),
                'other': random.randint(5, 15)
            }
        }
    
    def _get_visualization_engagement(self, visualization_id):
        """Get visualization engagement data"""
        return {
            'hotspot_interactions': random.randint(20, 200),
            'scene_transitions': random.randint(50, 500),
            'info_popups_opened': random.randint(30, 300),
            'navigation_menu_usage': random.randint(40, 400),
            'fullscreen_usage': random.randint(20, 200),
            'vr_mode_usage': random.randint(10, 100)
        }
    
    def _generate_visualization_recommendations(self, visualization_id):
        """Generate visualization optimization recommendations"""
        recommendations = []
        
        performance = self._calculate_visualization_performance(visualization_id)
        
        if performance['completion_rate'] < 70:
            recommendations.append({
                'type': 'engagement',
                'priority': 'high',
                'recommendation': 'Improve scene transitions and reduce loading times',
                'reason': f'Low completion rate: {performance["completion_rate"]:.1f}%'
            })
        
        if performance['interaction_rate'] < 20:
            recommendations.append({
                'type': 'interactivity',
                'priority': 'medium',
                'recommendation': 'Add more interactive elements and hotspots',
                'reason': f'Low interaction rate: {performance["interaction_rate"]:.1f}%'
            })
        
        if performance['average_view_time'] < 60:
            recommendations.append({
                'type': 'content',
                'priority': 'medium',
                'recommendation': 'Enhance content quality and add more detailed information',
                'reason': f'Short average view time: {performance["average_view_time"]} seconds'
            })
        
        return recommendations
    
    def export_visualization_data(self, format='json'):
        """Export all visualization data"""
        data = {
            'virtual_tours': self.virtual_tours,
            'property_models': self.property_models,
            'visualization_configs': self.visualization_configs,
            'performance_summary': self._calculate_overall_performance()
        }
        
        if format == 'json':
            return data
        elif format == 'csv':
            # Convert to CSV format
            import csv
            import io
            
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Write headers
            writer.writerow(['visualization_id', 'type', 'property_id', 'status', 'created_at'])
            
            # Write visualization data
            for viz_id, viz in self.property_models.items():
                writer.writerow([
                    viz_id,
                    viz.get('visualization_type', 'unknown'),
                    viz.get('property_id', ''),
                    viz.get('status', ''),
                    viz.get('created_at', '')
                ])
            
            return output.getvalue()
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def _calculate_overall_performance(self):
        """Calculate overall visualization performance"""
        total_visualizations = len(self.property_models)
        
        if total_visualizations == 0:
            return {
                'total_visualizations': 0,
                'total_views': 0,
                'average_completion_rate': 0,
                'average_interaction_rate': 0
            }
        
        total_views = sum(random.randint(100, 1000) for _ in range(total_visualizations))
        avg_completion = sum(random.uniform(60, 95) for _ in range(total_visualizations)) / total_visualizations
        avg_interaction = sum(random.uniform(10, 40) for _ in range(total_visualizations)) / total_visualizations
        
        return {
            'total_visualizations': total_visualizations,
            'total_views': total_views,
            'average_completion_rate': avg_completion,
            'average_interaction_rate': avg_interaction,
            'generated_at': datetime.now().isoformat()
        }
    
    def get_visualization_list(self):
        """Get all visualizations"""
        return list(self.property_models.keys())
    
    def get_virtual_tour_list(self):
        """Get all virtual tours"""
        return list(self.virtual_tours.keys())
    
    def delete_visualization(self, visualization_id):
        """Delete visualization"""
        if visualization_id in self.property_models:
            del self.property_models[visualization_id]
            return True
        return False
    
    def delete_virtual_tour(self, tour_id):
        """Delete virtual tour"""
        if tour_id in self.virtual_tours:
            del self.virtual_tours[tour_id]
            return True
        return False
