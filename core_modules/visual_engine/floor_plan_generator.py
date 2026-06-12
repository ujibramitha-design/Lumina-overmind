#!/usr/bin/env python3
"""
Floor Plan Generator - Visual Engine
Interactive floor plan creation and visualization system
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

class FloorPlanType(Enum):
    """Types of floor plans"""
    ARCHITECTURAL = "architectural"
    FURNITURE_LAYOUT = "furniture_layout"
    ELECTRICAL = "electrical"
    PLUMBING = "plumbing"
    MEASUREMENT = "measurement"
    INTERIOR_DESIGN = "interior_design"

class FloorPlanStyle(Enum):
    """Floor plan styles"""
    MINIMALIST = "minimalist"
    DETAILED = "detailed"
    MODERN = "modern"
    CLASSIC = "classic"
    TECHNICAL = "technical"

class FloorPlanStatus(Enum):
    """Floor plan creation status"""
    DRAFTING = "drafting"
    MEASURING = "measuring"
    DESIGNING = "designing"
    REVIEWING = "reviewing"
    FINALIZING = "finalizing"
    PUBLISHED = "published"
    ARCHIVED = "archived"

@dataclass
class FloorPlan:
    """Floor plan data structure"""
    plan_id: str
    property_id: str
    plan_type: FloorPlanType
    title: str
    description: str
    style: FloorPlanStyle
    status: FloorPlanStatus
    floor_number: int
    total_area_sqm: float
    room_count: int
    scale: str
    dimensions: Dict
    created_at: datetime
    file_url: str
    thumbnail_url: str
    published_at: Optional[datetime] = None
    download_count: int = 0
    views: int = 0
    notes: str = ""

@dataclass
class Room:
    """Room data structure within floor plan"""
    room_id: str
    plan_id: str
    room_name: str
    room_type: str
    area_sqm: float
    dimensions: Dict
    position: Dict
    features: List[str]
    furniture: List[Dict]
    created_at: datetime = datetime.now()

@dataclass
class FloorPlanMeasurement:
    """Measurement data for floor plan"""
    measurement_id: str
    plan_id: str
    measurement_type: str
    value: float
    unit: str
    start_point: Dict
    end_point: Dict
    description: str
    created_at: datetime = datetime.now()

class FloorPlanGenerator:
    """Advanced floor plan generation and management system"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Initialize database
        self.db_path = 'data/floor_plans.db (SQLite - removed)
        self._init_database()
        
        # Floor plan configurations
        self.plan_configs = {
            FloorPlanType.ARCHITECTURAL: {
                'name': 'Architectural Floor Plan',
                'features': ['walls', 'doors', 'windows', 'structural_elements'],
                'detail_level': 'high',
                'typical_rooms': ['living_room', 'bedroom', 'kitchen', 'bathroom'],
                'pricing': {'minimalist': 1500000, 'detailed': 2500000, 'technical': 3500000}
            },
            FloorPlanType.FURNITURE_LAYOUT: {
                'name': 'Furniture Layout Plan',
                'features': ['furniture_placement', 'traffic_flow', 'space_optimization'],
                'detail_level': 'medium',
                'typical_rooms': ['living_room', 'bedroom', 'dining', 'office'],
                'pricing': {'minimalist': 1000000, 'modern': 2000000, 'classic': 2500000}
            },
            FloorPlanType.ELECTRICAL: {
                'name': 'Electrical Plan',
                'features': ['outlets', 'switches', 'lighting', 'circuit_breakers'],
                'detail_level': 'technical',
                'typical_rooms': ['all_rooms'],
                'pricing': {'technical': 3000000}
            },
            FloorPlanType.PLUMBING: {
                'name': 'Plumbing Plan',
                'features': ['water_supply', 'drainage', 'fixtures', 'valves'],
                'detail_level': 'technical',
                'typical_rooms': ['kitchen', 'bathroom', 'laundry'],
                'pricing': {'technical': 2500000}
            }
        }
        
        # Room templates
        self.room_templates = {
            'living_room': {
                'min_area': 12.0,
                'max_area': 40.0,
                'typical_dimensions': {'length': 5.0, 'width': 4.0},
                'features': ['sofa_area', 'entertainment_center', 'natural_lighting'],
                'furniture': ['sofa', 'coffee_table', 'tv_stand', 'side_table']
            },
            'bedroom': {
                'min_area': 8.0,
                'max_area': 25.0,
                'typical_dimensions': {'length': 4.0, 'width': 3.5},
                'features': ['bed_area', 'wardrobe_space', 'window'],
                'furniture': ['bed', 'wardrobe', 'nightstand', 'dresser']
            },
            'kitchen': {
                'min_area': 6.0,
                'max_area': 20.0,
                'typical_dimensions': {'length': 3.5, 'width': 3.0},
                'features': ['cooking_area', 'storage', 'sink', 'appliances'],
                'furniture': ['kitchen_cabinet', 'refrigerator', 'stove', 'dishwasher']
            },
            'bathroom': {
                'min_area': 3.0,
                'max_area': 12.0,
                'typical_dimensions': {'length': 2.5, 'width': 2.0},
                'features': ['shower', 'toilet', 'sink', 'ventilation'],
                'furniture': ['toilet', 'sink', 'shower', 'vanity']
            },
            'dining': {
                'min_area': 8.0,
                'max_area': 20.0,
                'typical_dimensions': {'length': 4.0, 'width': 3.0},
                'features': ['dining_table_area', 'lighting', 'serving_space'],
                'furniture': ['dining_table', 'chairs', 'buffet', 'sideboard']
            }
        }
        
        # File storage paths
        self.storage_paths = {
            'plans': 'floor_plans/',
            'thumbnails': 'floor_plans/thumbnails/',
            'exports': 'floor_plans/exports/',
            'measurements': 'floor_plans/measurements/'
        }
        
        # Ensure directories exist
        for path in self.storage_paths.values():
            os.makedirs(path, exist_ok=True)
    
    def _init_database(self):
        """Initialize floor plans database"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # Create floor plans table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS floor_plans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    plan_id TEXT UNIQUE NOT NULL,
                    property_id TEXT NOT NULL,
                    plan_type TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    style TEXT NOT NULL,
                    status TEXT NOT NULL,
                    floor_number INTEGER NOT NULL,
                    total_area_sqm REAL NOT NULL,
                    room_count INTEGER NOT NULL,
                    scale TEXT NOT NULL,
                    dimensions TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    published_at TEXT,
                    file_url TEXT,
                    thumbnail_url TEXT,
                    download_count INTEGER DEFAULT 0,
                    views INTEGER DEFAULT 0,
                    notes TEXT DEFAULT '',
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create rooms table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS rooms (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    room_id TEXT UNIQUE NOT NULL,
                    plan_id TEXT NOT NULL,
                    room_name TEXT NOT NULL,
                    room_type TEXT NOT NULL,
                    area_sqm REAL NOT NULL,
                    dimensions TEXT NOT NULL,
                    position TEXT NOT NULL,
                    features TEXT,
                    furniture TEXT,
                    created_at TEXT NOT NULL
                )
            ''')
            
            # Create measurements table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS floor_plan_measurements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    measurement_id TEXT UNIQUE NOT NULL,
                    plan_id TEXT NOT NULL,
                    measurement_type TEXT NOT NULL,
                    value REAL NOT NULL,
                    unit TEXT NOT NULL,
                    start_point TEXT NOT NULL,
                    end_point TEXT NOT NULL,
                    description TEXT,
                    created_at TEXT NOT NULL
                )
            ''')
            
            # Create floor plan analytics table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS floor_plan_analytics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    plan_id TEXT NOT NULL,
                    date TEXT NOT NULL,
                    views INTEGER DEFAULT 0,
                    downloads INTEGER DEFAULT 0,
                    avg_session_duration REAL DEFAULT 0,
                    popular_rooms TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create indexes
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_plans_property_id ON floor_plans(property_id)')
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_plans_status ON floor_plans(status)')
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_rooms_plan_id ON rooms(plan_id)')
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_measurements_plan_id ON floor_plan_measurements(plan_id)')
            
            # conn.commit() removed
            # conn.close() removed
            
            self.logger.info("Floor plans database initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Error initializing floor plans database: {e}")
            raise
    
    def create_floor_plan(self, property_id: str, plan_type: FloorPlanType, 
                         title: str, style: FloorPlanStyle, floor_number: int,
                         total_area_sqm: float, description: str = "") -> str:
        """Create new floor plan"""
        try:
            plan_id = f"plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Get plan configuration
            plan_config = self.plan_configs.get(plan_type)
            if not plan_config:
                self.logger.error(f"Unsupported plan type: {plan_type}")
                return ""
            
            # Generate plan specifications
            scale = "1:100"  # Standard architectural scale
            dimensions = self._generate_plan_dimensions(total_area_sqm)
            
            # Generate file paths
            file_url = f"{self.storage_paths['plans']}{plan_id}.dwg"
            thumbnail_url = f"{self.storage_paths['thumbnails']}{plan_id}_thumb.jpg"
            
            # Create floor plan
            plan = FloorPlan(
                plan_id=plan_id,
                property_id=property_id,
                plan_type=plan_type,
                title=title,
                description=description,
                style=style,
                status=FloorPlanStatus.DRAFTING,
                floor_number=floor_number,
                total_area_sqm=total_area_sqm,
                room_count=0,  # Will be updated after room creation
                scale=scale,
                dimensions=dimensions,
                created_at=datetime.now(),
                file_url=file_url,
                thumbnail_url=thumbnail_url
            )
            
            # Save plan
            self._save_plan(plan)
            
            # Create rooms based on plan type and area
            room_count = self._create_plan_rooms(plan_id, plan_type, total_area_sqm)
            
            # Update room count
            plan.room_count = room_count
            self._save_plan(plan)
            
            self.logger.info(f"Created floor plan {plan_id} for property {property_id}")
            return plan_id
            
        except Exception as e:
            self.logger.error(f"Error creating floor plan: {e}")
            return ""
    
    def _generate_plan_dimensions(self, total_area_sqm: float) -> Dict:
        """Generate plan dimensions based on total area"""
        try:
            # Calculate approximate dimensions (assuming rectangular shape)
            aspect_ratio = 1.4  # Length to width ratio
            width = (total_area_sqm / aspect_ratio) ** 0.5
            length = total_area_sqm / width
            
            return {
                'total_length': round(length, 2),
                'total_width': round(width, 2),
                'total_area': total_area_sqm,
                'perimeter': round(2 * (length + width), 2)
            }
            
        except Exception as e:
            self.logger.error(f"Error generating plan dimensions: {e}")
            return {'total_length': 10.0, 'total_width': 7.0, 'total_area': total_area_sqm}
    
    def _save_plan(self, plan: FloorPlan):
        """Save floor plan to database"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # cursor.execute() removed'''
                INSERT OR REPLACE INTO floor_plans 
                (plan_id, property_id, plan_type, title, description, style, status, 
                 floor_number, total_area_sqm, room_count, scale, dimensions, 
                 created_at, published_at, file_url, thumbnail_url, download_count, views, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                plan.plan_id,
                plan.property_id,
                plan.plan_type.value,
                plan.title,
                plan.description,
                plan.style.value,
                plan.status.value,
                plan.floor_number,
                plan.total_area_sqm,
                plan.room_count,
                plan.scale,
                json.dumps(plan.dimensions),
                plan.created_at.isoformat(),
                plan.published_at.isoformat() if plan.published_at else None,
                plan.file_url,
                plan.thumbnail_url,
                plan.download_count,
                plan.views,
                plan.notes
            ))
            
            # conn.commit() removed
            # conn.close() removed
            
        except Exception as e:
            self.logger.error(f"Error saving plan {plan.plan_id}: {e}")
            raise
    
    def _create_plan_rooms(self, plan_id: str, plan_type: FloorPlanType, total_area_sqm: float) -> int:
        """Create rooms for floor plan"""
        try:
            plan_config = self.plan_configs.get(plan_type)
            if not plan_config:
                return 0
            
            room_types = plan_config['typical_rooms']
            
            # Calculate room areas based on total area
            room_areas = self._calculate_room_areas(total_area_sqm, room_types)
            
            room_count = 0
            current_x = 0
            current_y = 0
            
            for room_type, area in room_areas.items():
                if room_type == 'all_rooms':
                    # For electrical/plumbing plans, create generic rooms
                    room_type = 'living_room'
                
                room_template = self.room_templates.get(room_type)
                if not room_template:
                    continue
                
                # Generate room dimensions
                room_dimensions = self._generate_room_dimensions(area)
                
                # Generate room position
                room_position = {'x': current_x, 'y': current_y, 'z': 0}
                
                # Update position for next room
                current_x += room_dimensions['length'] + 0.5  # Add spacing
                
                # Create room
                room_id = f"room_{plan_id}_{room_count + 1}"
                
                room = Room(
                    room_id=room_id,
                    plan_id=plan_id,
                    room_name=room_type.replace('_', ' ').title(),
                    room_type=room_type,
                    area_sqm=area,
                    dimensions=room_dimensions,
                    position=room_position,
                    features=room_template['features'],
                    furniture=room_template['furniture']
                )
                
                self._save_room(room)
                room_count += 1
            
            self.logger.info(f"Created {room_count} rooms for plan {plan_id}")
            return room_count
            
        except Exception as e:
            self.logger.error(f"Error creating plan rooms: {e}")
            return 0
    
    def _calculate_room_areas(self, total_area_sqm: float, room_types: List[str]) -> Dict:
        """Calculate room areas based on total area"""
        try:
            room_areas = {}
            
            # Room area distribution percentages
            area_percentages = {
                'living_room': 0.25,
                'bedroom': 0.20,
                'kitchen': 0.15,
                'bathroom': 0.08,
                'dining': 0.12,
                'office': 0.10,
                'laundry': 0.05,
                'storage': 0.05
            }
            
            if 'all_rooms' in room_types:
                # For electrical/plumbing, create equal areas
                num_rooms = 5  # Default number of rooms
                room_area = total_area_sqm / num_rooms
                
                for i in range(num_rooms):
                    room_areas[f'room_{i+1}'] = room_area
            else:
                # Calculate areas based on percentages
                used_percentage = 0
                
                for room_type in room_types:
                    if room_type in area_percentages:
                        room_area = total_area_sqm * area_percentages[room_type]
                        room_areas[room_type] = room_area
                        used_percentage += area_percentages[room_type]
                
                # Distribute remaining area proportionally
                if used_percentage < 1.0:
                    remaining_area = total_area_sqm * (1.0 - used_percentage)
                    if room_areas:
                        additional_area = remaining_area / len(room_areas)
                        for room_type in room_areas:
                            room_areas[room_type] += additional_area
            
            return room_areas
            
        except Exception as e:
            self.logger.error(f"Error calculating room areas: {e}")
            return {}
    
    def _generate_room_dimensions(self, area_sqm: float) -> Dict:
        """Generate room dimensions based on area"""
        try:
            # Calculate dimensions (assuming rectangular shape)
            aspect_ratio = 1.2  # Typical room aspect ratio
            width = (area_sqm / aspect_ratio) ** 0.5
            length = area_sqm / width
            
            return {
                'length': round(length, 2),
                'width': round(width, 2),
                'area': area_sqm,
                'height': 3.0  # Standard ceiling height
            }
            
        except Exception as e:
            self.logger.error(f"Error generating room dimensions: {e}")
            return {'length': 3.0, 'width': 3.0, 'area': area_sqm, 'height': 3.0}
    
    def _save_room(self, room: Room):
        """Save room to database"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # cursor.execute() removed'''
                INSERT INTO rooms 
                (room_id, plan_id, room_name, room_type, area_sqm, dimensions, 
                 position, features, furniture, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                room.room_id,
                room.plan_id,
                room.room_name,
                room.room_type,
                room.area_sqm,
                json.dumps(room.dimensions),
                json.dumps(room.position),
                json.dumps(room.features),
                json.dumps(room.furniture),
                room.created_at.isoformat()
            ))
            
            # conn.commit() removed
            # conn.close() removed
            
        except Exception as e:
            self.logger.error(f"Error saving room {room.room_id}: {e}")
            raise
    
    def update_plan_status(self, plan_id: str, new_status: FloorPlanStatus, 
                          notes: str = "") -> bool:
        """Update floor plan status"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            update_fields = ['status = ?', 'updated_at = ?']
            update_values = [new_status.value, datetime.now().isoformat()]
            
            if new_status == FloorPlanStatus.PUBLISHED:
                update_fields.append('published_at = ?')
                update_values.append(datetime.now().isoformat())
            
            update_values.append(notes)
            update_values.append(plan_id)
            
            # cursor.execute() removedf'''
                UPDATE floor_plans 
                SET {', '.join(update_fields)}, notes = ?
                WHERE plan_id = ?
            ''', update_values)
            
            # conn.commit() removed
            # conn.close() removed
            
            self.logger.info(f"Updated plan {plan_id} status to {new_status.value}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error updating plan {plan_id} status: {e}")
            return False
    
    def add_measurement(self, plan_id: str, measurement_type: str, 
                       value: float, unit: str, start_point: Dict, 
                       end_point: Dict, description: str = "") -> str:
        """Add measurement to floor plan"""
        try:
            measurement_id = f"meas_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            measurement = FloorPlanMeasurement(
                measurement_id=measurement_id,
                plan_id=plan_id,
                measurement_type=measurement_type,
                value=value,
                unit=unit,
                start_point=start_point,
                end_point=end_point,
                description=description
            )
            
            # Save measurement
            self._save_measurement(measurement)
            
            self.logger.info(f"Added measurement {measurement_id} to plan {plan_id}")
            return measurement_id
            
        except Exception as e:
            self.logger.error(f"Error adding measurement: {e}")
            return ""
    
    def _save_measurement(self, measurement: FloorPlanMeasurement):
        """Save measurement to database"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # cursor.execute() removed'''
                INSERT INTO floor_plan_measurements 
                (measurement_id, plan_id, measurement_type, value, unit, 
                 start_point, end_point, description, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                measurement.measurement_id,
                measurement.plan_id,
                measurement.measurement_type,
                measurement.value,
                measurement.unit,
                json.dumps(measurement.start_point),
                json.dumps(measurement.end_point),
                measurement.description,
                measurement.created_at.isoformat()
            ))
            
            # conn.commit() removed
            # conn.close() removed
            
        except Exception as e:
            self.logger.error(f"Error saving measurement {measurement.measurement_id}: {e}")
            raise
    
    def generate_plan_report(self, property_id: Optional[str] = None) -> Dict:
        """Generate comprehensive floor plan report"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            if property_id:
                # cursor.execute() removed'SELECT * FROM floor_plans WHERE property_id = ?', (property_id,))
            else:
                # cursor.execute() removed'SELECT * FROM floor_plans')
            
            plans = []
            for row in cursor.fetchall():
                columns = [desc[0] for desc in cursor.description]
                plan_data = dict(zip(columns, row))
                plans.append(plan_data)
            
            # Calculate statistics
            total_plans = len(plans)
            total_area = sum(plan['total_area_sqm'] for plan in plans)
            total_rooms = sum(plan['room_count'] for plan in plans)
            avg_views = sum(plan['views'] for plan in plans) / max(total_plans, 1)
            
            # Status distribution
            status_counts = {}
            type_counts = {}
            style_counts = {}
            
            for plan in plans:
                status = plan['status']
                plan_type = plan['plan_type']
                style = plan['style']
                
                status_counts[status] = status_counts.get(status, 0) + 1
                type_counts[plan_type] = type_counts.get(plan_type, 0) + 1
                style_counts[style] = style_counts.get(style, 0) + 1
            
            # conn.close() removed
            
            report = {
                'generated_at': datetime.now().isoformat(),
                'property_id': property_id,
                'summary_statistics': {
                    'total_plans': total_plans,
                    'total_area_sqm': total_area,
                    'total_rooms': total_rooms,
                    'average_views': avg_views,
                    'published_plans': status_counts.get('published', 0)
                },
                'distribution_analysis': {
                    'status_distribution': status_counts,
                    'type_distribution': type_counts,
                    'style_distribution': style_counts
                },
                'detailed_plans': plans
            }
            
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating plan report: {e}")
            return {}
    
    def create_sample_plans(self) -> int:
        """Create sample floor plans for testing"""
        try:
            sample_properties = [
                {'id': 'prop_001', 'name': 'Rumah Cipocok Jaya', 'type': 'house', 'area': 120},
                {'id': 'prop_002', 'name': 'Apartemen Serang', 'type': 'apartment', 'area': 65},
                {'id': 'prop_003', 'name': 'Ruko Ciruas', 'type': 'commercial', 'area': 80}
            ]
            
            plan_types = [FloorPlanType.ARCHITECTURAL, FloorPlanType.FURNITURE_LAYOUT, FloorPlanType.ELECTRICAL]
            styles = [FloorPlanStyle.DETAILED, FloorPlanStyle.MODERN, FloorPlanStyle.TECHNICAL]
            
            created_count = 0
            
            for i, property_data in enumerate(sample_properties):
                plan_type = plan_types[i % len(plan_types)]
                style = styles[i % len(styles)]
                
                plan_id = self.create_floor_plan(
                    property_data['id'],
                    plan_type,
                    f"Floor Plan {property_data['name']}",
                    style,
                    1,  # Ground floor
                    property_data['area'],
                    f"Professional {plan_type.value} plan for {property_data['name']}"
                )
                
                if plan_id:
                    # Simulate plan processing
                    self.update_plan_status(plan_id, FloorPlanStatus.MEASURING, "Taking precise measurements")
                    self.update_plan_status(plan_id, FloorPlanStatus.DESIGNING, "Creating detailed design")
                    self.update_plan_status(plan_id, FloorPlanStatus.REVIEWING, "Quality review in progress")
                    self.update_plan_status(plan_id, FloorPlanStatus.FINALIZING, "Finalizing plan details")
                    self.update_plan_status(plan_id, FloorPlanStatus.PUBLISHED, "Plan published and ready")
                    
                    # Add some measurements
                    self.add_measurement(
                        plan_id,
                        "wall_length",
                        5.2,
                        "meters",
                        {"x": 0, "y": 0, "z": 0},
                        {"x": 5.2, "y": 0, "z": 0},
                        "Main living room wall"
                    )
                    
                    self.add_measurement(
                        plan_id,
                        "room_width",
                        4.1,
                        "meters",
                        {"x": 0, "y": 0, "z": 0},
                        {"x": 0, "y": 4.1, "z": 0},
                        "Living room width"
                    )
                    
                    created_count += 1
            
            self.logger.info(f"Created {created_count} sample floor plans")
            return created_count
            
        except Exception as e:
            self.logger.error(f"Error creating sample plans: {e}")
            return 0

def main():
    """Main function to demonstrate floor plan generator"""
    print("=" * 60)
    print("📐 FLOOR PLAN GENERATOR - VISUAL ENGINE")
    print("=" * 60)
    
    # Initialize floor plan generator
    fpg = FloorPlanGenerator()
    
    # Create sample plans
    print("🏠 Creating sample floor plans...")
    created = fpg.create_sample_plans()
    print(f"✅ Created {created} sample plans")
    
    # Generate plan report
    print("\n📊 Generating floor plan report...")
    report = fpg.generate_plan_report()
    
    if report:
        print("📈 Plan Statistics:")
        summary = report.get('summary_statistics', {})
        print(f"  - Total Plans: {summary.get('total_plans', 0)}")
        print(f"  - Total Area: {summary.get('total_area_sqm', 0):.1f} m²")
        print(f"  - Total Rooms: {summary.get('total_rooms', 0)}")
        print(f"  - Published Plans: {summary.get('published_plans', 0)}")
        print(f"  - Average Views: {summary.get('average_views', 0):.1f}")
        
        distribution = report.get('distribution_analysis', {})
        print(f"\n📋 Distribution Analysis:")
        print(f"  - Status: {distribution.get('status_distribution', {})}")
        print(f"  - Types: {distribution.get('type_distribution', {})}")
        print(f"  - Styles: {distribution.get('style_distribution', {})}")
    
    # Show plan details
    detailed_plans = report.get('detailed_plans', [])
    if detailed_plans:
        sample_plan = detailed_plans[0]
        print(f"\n📐 Sample Plan Details:")
        print(f"  - Title: {sample_plan['title']}")
        print(f"  - Type: {sample_plan['plan_type']}")
        print(f"  - Style: {sample_plan['style']}")
        print(f"  - Floor: {sample_plan['floor_number']}")
        print(f"  - Area: {sample_plan['total_area_sqm']:.1f} m²")
        print(f"  - Rooms: {sample_plan['room_count']}")
        print(f"  - Scale: {sample_plan['scale']}")
        print(f"  - Dimensions: {sample_plan['dimensions']}")
    
    # Save report
    report_file = 'floor_plan_report.json'
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n📁 Report saved to: {report_file}")
    
    print("\n" + "=" * 60)
    print("✅ FLOOR PLAN GENERATOR SETUP COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()
