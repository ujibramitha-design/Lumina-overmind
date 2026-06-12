#!/usr/bin/env python3
"""
Virtual Tour Generator - Visual Engine
Advanced virtual tour creation and management system for properties
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

class TourType(Enum):
    """Types of virtual tours"""
    TOUR_360 = "tour_360"
    MATTERPORT = "matterport"
    KUULA = "kuula"
    CUSTOM = "custom"
    VIDEO_WALKTHROUGH = "video_walkthrough"
    INTERACTIVE_FLOORPLAN = "interactive_floorplan"

class TourQuality(Enum):
    """Virtual tour quality levels"""
    BASIC = "basic"
    STANDARD = "standard"
    PREMIUM = "premium"
    ULTRA_HD = "ultra_hd"

class TourStatus(Enum):
    """Tour creation status"""
    PLANNING = "planning"
    FILMING = "filming"
    PROCESSING = "processing"
    READY = "ready"
    PUBLISHED = "published"
    ARCHIVED = "archived"

@dataclass
class VirtualTour:
    """Virtual tour data structure"""
    tour_id: str
    property_id: str
    tour_type: TourType
    title: str
    description: str
    quality: TourQuality
    status: TourStatus
    duration_minutes: int
    file_size_mb: float
    thumbnail_url: str
    tour_url: str
    embed_code: str
    created_at: datetime
    published_at: Optional[datetime] = None
    view_count: int = 0
    engagement_rate: float = 0.0
    notes: str = ""

@dataclass
class TourScene:
    """Individual scene within virtual tour"""
    scene_id: str
    tour_id: str
    scene_number: int
    title: str
    description: str
    image_url: str
    hotspot_data: Dict
    navigation_links: List[str]
    audio_narration: Optional[str] = None
    created_at: datetime = datetime.now()

@dataclass
class TourAnalytics:
    """Tour analytics and engagement data"""
    analytics_id: str
    tour_id: str
    date: datetime
    total_views: int
    unique_viewers: int
    avg_view_duration: float
    bounce_rate: float
    engagement_score: float
    popular_scenes: List[str]
    conversion_rate: float = 0.0

class VirtualTourGenerator:
    """Advanced virtual tour generation and management system"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Initialize database
        self.db_path = 'data/virtual_tours.db (SQLite - removed)
        self._init_database()
        
        # Tour templates and configurations
        self.tour_templates = {
            TourType.TOUR_360: {
                'name': '360° Virtual Tour',
                'scenes': 8,
                'duration': 15,
                'quality_options': [TourQuality.STANDARD, TourQuality.PREMIUM, TourQuality.ULTRA_HD],
                'features': ['panoramic_views', 'hotspot_navigation', 'zoom_capability'],
                'pricing': {'basic': 2500000, 'premium': 4000000, 'ultra_hd': 6000000}
            },
            TourType.MATTERPORT: {
                'name': 'Matterport 3D Tour',
                'scenes': 12,
                'duration': 20,
                'quality_options': [TourQuality.STANDARD, TourQuality.PREMIUM],
                'features': ['3d_model', 'dollhouse_view', 'floorplan', 'measurement_tools'],
                'pricing': {'standard': 5000000, 'premium': 8000000}
            },
            TourType.KUULA: {
                'name': 'Kuula Interactive Tour',
                'scenes': 6,
                'duration': 10,
                'quality_options': [TourQuality.BASIC, TourQuality.STANDARD],
                'features': ['panoramic', 'social_sharing', 'branding_options'],
                'pricing': {'basic': 1500000, 'standard': 2500000}
            },
            TourType.VIDEO_WALKTHROUGH: {
                'name': 'Video Walkthrough',
                'scenes': 1,
                'duration': 5,
                'quality_options': [TourQuality.STANDARD, TourQuality.PREMIUM],
                'features': ['professional_video', 'background_music', 'narration'],
                'pricing': {'standard': 3000000, 'premium': 5000000}
            }
        }
        
        # Scene types and configurations
        self.scene_types = {
            'exterior': {
                'name': 'Exterior View',
                'hotspots': ['entrance', 'parking', 'garden', 'facade'],
                'navigation': ['entrance_hall', 'living_room']
            },
            'living_room': {
                'name': 'Living Room',
                'hotspots': ['sofa_area', 'entertainment', 'lighting', 'windows'],
                'navigation': ['kitchen', 'bedroom', 'bathroom']
            },
            'kitchen': {
                'name': 'Kitchen',
                'hotspots': ['appliances', 'storage', 'countertop', 'dining'],
                'navigation': ['living_room', 'dining_area']
            },
            'master_bedroom': {
                'name': 'Master Bedroom',
                'hotspots': ['bed', 'wardrobe', 'balcony', 'ensuite'],
                'navigation': ['bathroom', 'hallway']
            },
            'bathroom': {
                'name': 'Bathroom',
                'hotspots': ['shower', 'vanity', 'bathtub', 'fixtures'],
                'navigation': ['bedroom', 'hallway']
            }
        }
        
        # File storage paths
        self.storage_paths = {
            'tours': 'virtual_tours/',
            'thumbnails': 'virtual_tours/thumbnails/',
            'scenes': 'virtual_tours/scenes/',
            'exports': 'virtual_tours/exports/'
        }
        
        # Ensure directories exist
        for path in self.storage_paths.values():
            os.makedirs(path, exist_ok=True)
    
    def _init_database(self):
        """Initialize virtual tours database"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # Create virtual tours table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS virtual_tours (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tour_id TEXT UNIQUE NOT NULL,
                    property_id TEXT NOT NULL,
                    tour_type TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    quality TEXT NOT NULL,
                    status TEXT NOT NULL,
                    duration_minutes INTEGER NOT NULL,
                    file_size_mb REAL NOT NULL,
                    thumbnail_url TEXT,
                    tour_url TEXT,
                    embed_code TEXT,
                    created_at TEXT NOT NULL,
                    published_at TEXT,
                    view_count INTEGER DEFAULT 0,
                    engagement_rate REAL DEFAULT 0,
                    notes TEXT DEFAULT '',
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create tour scenes table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS tour_scenes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    scene_id TEXT UNIQUE NOT NULL,
                    tour_id TEXT NOT NULL,
                    scene_number INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    image_url TEXT,
                    hotspot_data TEXT,
                    navigation_links TEXT,
                    audio_narration TEXT,
                    created_at TEXT NOT NULL
                )
            ''')
            
            # Create tour analytics table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS tour_analytics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    analytics_id TEXT UNIQUE NOT NULL,
                    tour_id TEXT NOT NULL,
                    date TEXT NOT NULL,
                    total_views INTEGER DEFAULT 0,
                    unique_viewers INTEGER DEFAULT 0,
                    avg_view_duration REAL DEFAULT 0,
                    bounce_rate REAL DEFAULT 0,
                    engagement_score REAL DEFAULT 0,
                    popular_scenes TEXT,
                    conversion_rate REAL DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create tour templates table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS tour_templates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    template_id TEXT UNIQUE NOT NULL,
                    template_name TEXT NOT NULL,
                    tour_type TEXT NOT NULL,
                    property_type TEXT NOT NULL,
                    scene_count INTEGER NOT NULL,
                    scene_config TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create indexes
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_tours_property_id ON virtual_tours(property_id)')
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_tours_status ON virtual_tours(status)')
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_scenes_tour_id ON tour_scenes(tour_id)')
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_analytics_tour_id ON tour_analytics(tour_id)')
            
            # conn.commit() removed
            # conn.close() removed
            
            self.logger.info("Virtual tours database initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Error initializing virtual tours database: {e}")
            raise
    
    def create_virtual_tour(self, property_id: str, tour_type: TourType, 
                          title: str, quality: TourQuality, 
                          description: str = "") -> str:
        """Create new virtual tour"""
        try:
            tour_id = f"tour_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Get tour configuration
            tour_config = self.tour_templates.get(tour_type)
            if not tour_config:
                self.logger.error(f"Unsupported tour type: {tour_type}")
                return ""
            
            # Generate file paths
            thumbnail_url = f"{self.storage_paths['thumbnails']}{tour_id}_thumb.jpg"
            tour_url = f"{self.storage_paths['tours']}{tour_id}/"
            embed_code = f'<iframe src="{tour_url}" width="800" height="600"></iframe>'
            
            # Create virtual tour
            tour = VirtualTour(
                tour_id=tour_id,
                property_id=property_id,
                tour_type=tour_type,
                title=title,
                description=description,
                quality=quality,
                status=TourStatus.PLANNING,
                duration_minutes=tour_config['duration'],
                file_size_mb=0.0,  # Will be updated after processing
                thumbnail_url=thumbnail_url,
                tour_url=tour_url,
                embed_code=embed_code,
                created_at=datetime.now()
            )
            
            # Save tour
            self._save_tour(tour)
            
            # Create scenes based on tour type
            self._create_tour_scenes(tour_id, tour_type)
            
            self.logger.info(f"Created virtual tour {tour_id} for property {property_id}")
            return tour_id
            
        except Exception as e:
            self.logger.error(f"Error creating virtual tour: {e}")
            return ""
    
    def _save_tour(self, tour: VirtualTour):
        """Save virtual tour to database"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # cursor.execute() removed'''
                INSERT INTO virtual_tours 
                (tour_id, property_id, tour_type, title, description, quality, status, 
                 duration_minutes, file_size_mb, thumbnail_url, tour_url, embed_code, 
                 created_at, published_at, view_count, engagement_rate, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                tour.tour_id,
                tour.property_id,
                tour.tour_type.value,
                tour.title,
                tour.description,
                tour.quality.value,
                tour.status.value,
                tour.duration_minutes,
                tour.file_size_mb,
                tour.thumbnail_url,
                tour.tour_url,
                tour.embed_code,
                tour.created_at.isoformat(),
                tour.published_at.isoformat() if tour.published_at else None,
                tour.view_count,
                tour.engagement_rate,
                tour.notes
            ))
            
            # conn.commit() removed
            # conn.close() removed
            
        except Exception as e:
            self.logger.error(f"Error saving tour {tour.tour_id}: {e}")
            raise
    
    def _create_tour_scenes(self, tour_id: str, tour_type: TourType):
        """Create scenes for virtual tour"""
        try:
            tour_config = self.tour_templates.get(tour_type)
            if not tour_config:
                return
            
            scene_count = tour_config['scenes']
            
            # Default scene sequence for property tours
            scene_sequence = ['exterior', 'living_room', 'kitchen', 'master_bedroom', 'bathroom']
            
            # Add more scenes for higher-end tours
            if tour_type in [TourType.MATTERPORT, TourType.TOUR_360]:
                scene_sequence.extend(['dining_area', 'balcony', 'garage'])
            
            # Create scenes
            for i in range(min(scene_count, len(scene_sequence))):
                scene_type = scene_sequence[i]
                scene_config = self.scene_types.get(scene_type, {})
                
                scene_id = f"scene_{tour_id}_{i+1:02d}"
                image_url = f"{self.storage_paths['scenes']}{scene_id}.jpg"
                
                # Generate hotspot data
                hotspots = self._generate_hotspot_data(scene_type)
                
                # Generate navigation links
                navigation_links = self._generate_navigation_links(scene_type, scene_sequence, i)
                
                scene = TourScene(
                    scene_id=scene_id,
                    tour_id=tour_id,
                    scene_number=i + 1,
                    title=scene_config.get('name', f'Scene {i+1}'),
                    description=f"View of {scene_config.get('name', 'property area')}",
                    image_url=image_url,
                    hotspot_data=hotspots,
                    navigation_links=navigation_links
                )
                
                self._save_scene(scene)
            
            self.logger.info(f"Created {min(scene_count, len(scene_sequence))} scenes for tour {tour_id}")
            
        except Exception as e:
            self.logger.error(f"Error creating tour scenes: {e}")
    
    def _generate_hotspot_data(self, scene_type: str) -> Dict:
        """Generate hotspot data for scene"""
        try:
            scene_config = self.scene_types.get(scene_type, {})
            hotspot_types = scene_config.get('hotspots', [])
            
            hotspots = {}
            for i, hotspot_type in enumerate(hotspot_types):
                hotspot_id = f"hotspot_{i+1}"
                hotspots[hotspot_id] = {
                    'type': hotspot_type,
                    'position': {'x': 20 + (i * 20), 'y': 50},
                    'title': hotspot_type.replace('_', ' ').title(),
                    'description': f"Click to explore {hotspot_type.replace('_', ' ')}",
                    'action': 'zoom' if hotspot_type in ['windows', 'balcony'] else 'info'
                }
            
            return hotspots
            
        except Exception as e:
            self.logger.error(f"Error generating hotspot data: {e}")
            return {}
    
    def _generate_navigation_links(self, current_scene: str, scene_sequence: List[str], 
                                 current_index: int) -> List[str]:
        """Generate navigation links between scenes"""
        try:
            links = []
            
            # Link to next scene
            if current_index < len(scene_sequence) - 1:
                next_scene = scene_sequence[current_index + 1]
                links.append(f"scene_{next_scene}")
            
            # Link to previous scene
            if current_index > 0:
                prev_scene = scene_sequence[current_index - 1]
                links.append(f"scene_{prev_scene}")
            
            # Add specific navigation based on scene type
            scene_config = self.scene_types.get(current_scene, {})
            specific_links = scene_config.get('navigation', [])
            
            for link in specific_links:
                if link in scene_sequence:
                    links.append(f"scene_{link}")
            
            return list(set(links))  # Remove duplicates
            
        except Exception as e:
            self.logger.error(f"Error generating navigation links: {e}")
            return []
    
    def _save_scene(self, scene: TourScene):
        """Save scene to database"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # cursor.execute() removed'''
                INSERT INTO tour_scenes 
                (scene_id, tour_id, scene_number, title, description, image_url, 
                 hotspot_data, navigation_links, audio_narration, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                scene.scene_id,
                scene.tour_id,
                scene.scene_number,
                scene.title,
                scene.description,
                scene.image_url,
                json.dumps(scene.hotspot_data),
                json.dumps(scene.navigation_links),
                scene.audio_narration,
                scene.created_at.isoformat()
            ))
            
            # conn.commit() removed
            # conn.close() removed
            
        except Exception as e:
            self.logger.error(f"Error saving scene {scene.scene_id}: {e}")
            raise
    
    def update_tour_status(self, tour_id: str, new_status: TourStatus, 
                          notes: str = "", file_size_mb: float = 0.0) -> bool:
        """Update tour status and metadata"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            update_fields = ['status = ?', 'updated_at = ?']
            update_values = [new_status.value, datetime.now().isoformat()]
            
            if file_size_mb > 0:
                update_fields.append('file_size_mb = ?')
                update_values.append(file_size_mb)
            
            if new_status == TourStatus.PUBLISHED:
                update_fields.append('published_at = ?')
                update_values.append(datetime.now().isoformat())
            
            update_values.append(notes)
            update_values.append(tour_id)
            
            # cursor.execute() removedf'''
                UPDATE virtual_tours 
                SET {', '.join(update_fields)}, notes = ?
                WHERE tour_id = ?
            ''', update_values)
            
            # conn.commit() removed
            # conn.close() removed
            
            self.logger.info(f"Updated tour {tour_id} status to {new_status.value}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error updating tour {tour_id} status: {e}")
            return False
    
    def get_tour_analytics(self, tour_id: str, days: int = 30) -> Dict:
        """Get tour analytics and engagement data"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # Get tour details
            # cursor.execute() removed'SELECT * FROM virtual_tours WHERE tour_id = ?', (tour_id,))
            tour_result = cursor.fetchone()
            
            if not tour_result:
                return {}
            
            columns = [desc[0] for desc in cursor.description]
            tour_data = dict(zip(columns, tour_result))
            
            # Get analytics data
            start_date = datetime.now() - timedelta(days=days)
            
            # cursor.execute() removed'''
                SELECT SUM(total_views), SUM(unique_viewers), AVG(avg_view_duration),
                       AVG(bounce_rate), AVG(engagement_score), AVG(conversion_rate)
                FROM tour_analytics 
                WHERE tour_id = ? AND date >= ?
            ''', (tour_id, start_date.isoformat()))
            
            analytics_result = cursor.fetchone()
            
            # Get popular scenes
            # cursor.execute() removed'''
                SELECT popular_scenes FROM tour_analytics 
                WHERE tour_id = ? AND date >= ?
                ORDER BY date DESC LIMIT 7
            ''', (tour_id, start_date.isoformat()))
            
            popular_scenes = []
            for row in cursor.fetchall():
                scenes = json.loads(row[0] or '[]')
                popular_scenes.extend(scenes)
            
            # Count scene popularity
            scene_counts = {}
            for scene in popular_scenes:
                scene_counts[scene] = scene_counts.get(scene, 0) + 1
            
            # Sort by popularity
            sorted_scenes = sorted(scene_counts.items(), key=lambda x: x[1], reverse=True)
            
            # conn.close() removed
            
            analytics = {
                'tour_id': tour_id,
                'tour_details': {
                    'title': tour_data['title'],
                    'tour_type': tour_data['tour_type'],
                    'quality': tour_data['quality'],
                    'duration_minutes': tour_data['duration_minutes'],
                    'view_count': tour_data['view_count'],
                    'engagement_rate': tour_data['engagement_rate']
                },
                'analytics_period': f'{days} days',
                'performance_metrics': {
                    'total_views': analytics_result[0] or 0,
                    'unique_viewers': analytics_result[1] or 0,
                    'avg_view_duration': analytics_result[2] or 0,
                    'bounce_rate': analytics_result[3] or 0,
                    'engagement_score': analytics_result[4] or 0,
                    'conversion_rate': analytics_result[5] or 0
                },
                'popular_scenes': sorted_scenes[:5]  # Top 5 scenes
            }
            
            return analytics
            
        except Exception as e:
            self.logger.error(f"Error getting tour analytics: {e}")
            return {}
    
    def generate_tour_report(self, property_id: Optional[str] = None) -> Dict:
        """Generate comprehensive tour report"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            if property_id:
                # cursor.execute() removed'SELECT * FROM virtual_tours WHERE property_id = ?', (property_id,))
            else:
                # cursor.execute() removed'SELECT * FROM virtual_tours')
            
            tours = []
            for row in cursor.fetchall():
                columns = [desc[0] for desc in cursor.description]
                tour_data = dict(zip(columns, row))
                tours.append(tour_data)
            
            # Calculate statistics
            total_tours = len(tours)
            total_views = sum(tour['view_count'] for tour in tours)
            avg_engagement = sum(tour['engagement_rate'] for tour in tours) / max(total_tours, 1)
            
            # Status distribution
            status_counts = {}
            type_counts = {}
            quality_counts = {}
            
            for tour in tours:
                status = tour['status']
                tour_type = tour['tour_type']
                quality = tour['quality']
                
                status_counts[status] = status_counts.get(status, 0) + 1
                type_counts[tour_type] = type_counts.get(tour_type, 0) + 1
                quality_counts[quality] = quality_counts.get(quality, 0) + 1
            
            # conn.close() removed
            
            report = {
                'generated_at': datetime.now().isoformat(),
                'property_id': property_id,
                'summary_statistics': {
                    'total_tours': total_tours,
                    'total_views': total_views,
                    'average_engagement_rate': avg_engagement,
                    'tours_published': status_counts.get('published', 0)
                },
                'distribution_analysis': {
                    'status_distribution': status_counts,
                    'type_distribution': type_counts,
                    'quality_distribution': quality_counts
                },
                'detailed_tours': tours
            }
            
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating tour report: {e}")
            return {}
    
    def create_sample_tours(self) -> int:
        """Create sample virtual tours for testing"""
        try:
            sample_properties = [
                {'id': 'prop_001', 'name': 'Rumah Cipocok Jaya', 'type': 'house'},
                {'id': 'prop_002', 'name': 'Apartemen Serang', 'type': 'apartment'},
                {'id': 'prop_003', 'name': 'Ruko Ciruas', 'type': 'commercial'}
            ]
            
            tour_types = [TourType.TOUR_360, TourType.MATTERPORT, TourType.VIDEO_WALKTHROUGH]
            qualities = [TourQuality.STANDARD, TourQuality.PREMIUM]
            
            created_count = 0
            
            for i, property_data in enumerate(sample_properties):
                tour_type = tour_types[i % len(tour_types)]
                quality = qualities[i % len(qualities)]
                
                tour_id = self.create_virtual_tour(
                    property_data['id'],
                    tour_type,
                    f"Virtual Tour {property_data['name']}",
                    quality,
                    f"Professional {tour_type.value} tour for {property_data['name']}"
                )
                
                if tour_id:
                    # Simulate tour processing
                    self.update_tour_status(tour_id, TourStatus.FILMING, "Photography in progress")
                    self.update_tour_status(tour_id, TourStatus.PROCESSING, "Processing 360 images")
                    self.update_tour_status(tour_id, TourStatus.READY, "Tour ready for review")
                    self.update_tour_status(tour_id, TourStatus.PUBLISHED, "Tour published", 150.5)
                    
                    created_count += 1
            
            self.logger.info(f"Created {created_count} sample virtual tours")
            return created_count
            
        except Exception as e:
            self.logger.error(f"Error creating sample tours: {e}")
            return 0

def main():
    """Main function to demonstrate virtual tour generator"""
    print("=" * 60)
    print("🎥 VIRTUAL TOUR GENERATOR - VISUAL ENGINE")
    print("=" * 60)
    
    # Initialize virtual tour generator
    vtg = VirtualTourGenerator()
    
    # Create sample tours
    print("🏠 Creating sample virtual tours...")
    created = vtg.create_sample_tours()
    print(f"✅ Created {created} sample tours")
    
    # Generate tour report
    print("\n📊 Generating virtual tour report...")
    report = vtg.generate_tour_report()
    
    if report:
        print("📈 Tour Statistics:")
        summary = report.get('summary_statistics', {})
        print(f"  - Total Tours: {summary.get('total_tours', 0)}")
        print(f"  - Total Views: {summary.get('total_views', 0)}")
        print(f"  - Published Tours: {summary.get('tours_published', 0)}")
        print(f"  - Avg Engagement: {summary.get('average_engagement_rate', 0):.2f}")
        
        distribution = report.get('distribution_analysis', {})
        print(f"\n📋 Distribution Analysis:")
        print(f"  - Status: {distribution.get('status_distribution', {})}")
        print(f"  - Types: {distribution.get('type_distribution', {})}")
        print(f"  - Qualities: {distribution.get('quality_distribution', {})}")
    
    # Get analytics for a specific tour
    detailed_tours = report.get('detailed_tours', [])
    if detailed_tours:
        sample_tour = detailed_tours[0]
        tour_id = sample_tour['tour_id']
        
        print(f"\n📊 Analytics for Tour: {sample_tour['title']}")
        analytics = vtg.get_tour_analytics(tour_id)
        
        if analytics:
            performance = analytics.get('performance_metrics', {})
            print(f"  - Total Views: {performance.get('total_views', 0)}")
            print(f"  - Unique Viewers: {performance.get('unique_viewers', 0)}")
            print(f"  - Avg Duration: {performance.get('avg_view_duration', 0):.1f} min")
            print(f"  - Engagement Score: {performance.get('engagement_score', 0):.2f}")
            print(f"  - Conversion Rate: {performance.get('conversion_rate', 0):.2f}")
            
            popular_scenes = analytics.get('popular_scenes', [])
            if popular_scenes:
                print(f"  - Popular Scenes: {popular_scenes}")
    
    # Save report
    report_file = 'virtual_tour_report.json'
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n📁 Report saved to: {report_file}")
    
    print("\n" + "=" * 60)
    print("✅ VIRTUAL TOUR GENERATOR SETUP COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()
