"""
LUMINA OS - Sniper Links API
====================================

Dynamic Hyper-Personalized Link Generator
Creates personalized landing pages for each prospect with unique URLs

Features:
- Dynamic slug generation with UUID
- SQLite database for link storage
- Personalized content generation
- Mobile-responsive design
- Anti-spam protection
- Analytics tracking
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime
import uuid
import logging
import os
import sys
from pathlib import Path

# Add root directory to Python path
root_dir = Path(__file__).parent.parent.parent
sys.path.append(str(root_dir))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ANSI color codes for terminal output
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
BOLD = '\033[1m'
END = '\033[0m'

# Database setup
DB_PATH = root_dir / "data" / "leads.db (SQLite - removed)

# Create router
router = APIRouter()

# Pydantic models
class PersonalizedLinkRequest(BaseModel):
    """Request model for generating personalized links"""
    lead_name: str = Field(..., min_length=2, max_length=100, description="Prospect name")
    budget: Optional[str] = Field(None, description="Budget range (e.g., '300-500jt')")
    location: Optional[str] = Field(None, description="Preferred location")
    contact_info: Optional[str] = Field(None, description="Contact information")
    lead_id: Optional[int] = Field(None, description="Original lead ID from database")

class PersonalizedLinkResponse(BaseModel):
    """Response model for generated personalized links"""
    success: bool
    slug: str
    full_url: str
    lead_name: str
    budget: Optional[str]
    location: Optional[str]
    created_at: str
    qr_code_url: Optional[str] = None
    preview_url: Optional[str] = None

class LinkData(BaseModel):
    """Link data model for database storage"""
    slug: str
    lead_id: Optional[int]
    lead_name: str
    budget: Optional[str]
    location: Optional[str]
    contact_info: Optional[str]
    created_at: str
    updated_at: str
    view_count: int = 0
    status: str = "active"  # active, expired, converted

class SniperLinkManager:
    """
    Manages personalized links generation and tracking
    """
    
    def __init__(self):
        """Initialize the link manager"""
        self.logger = logging.getLogger(__name__)
        self.db_path = DB_PATH
        self.base_url = os.getenv('BASE_URL', 'http://localhost:3000')
        
        # Ensure data directory exists
        self.db_path.parent.mkdir(exist_ok=True)
        
        # Initialize database
        self._initialize_database()
        
        self.logger.info(f"{CYAN}🎯 SNIPER LINKS: Initialized{END}")
    
    def _initialize_database(self):
        """Initialize SQLite database for personalized links"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # Create personalized_links table
            # cursor.execute() removed"""
                CREATE TABLE IF NOT EXISTS personalized_links (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    slug TEXT UNIQUE NOT NULL,
                    lead_id INTEGER,
                    lead_name TEXT NOT NULL,
                    budget TEXT,
                    location TEXT,
                    contact_info TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    view_count INTEGER DEFAULT 0,
                    status TEXT DEFAULT 'active',
                    metadata TEXT,  -- JSON for additional data
                    FOREIGN KEY (lead_id) REFERENCES leads(id) ON DELETE SET NULL
                )
            """)
            
            # Create indexes for performance
            # cursor.execute() removed"CREATE INDEX IF NOT EXISTS idx_slug ON personalized_links(slug)")
            # cursor.execute() removed"CREATE INDEX IF NOT EXISTS idx_lead_id ON personalized_links(lead_id)")
            # cursor.execute() removed"CREATE INDEX IF NOT EXISTS idx_status ON personalized_links(status)")
            # cursor.execute() removed"CREATE INDEX IF NOT EXISTS idx_created_at ON personalized_links(created_at)")
            
            # conn.commit() removed
            # conn.close() removed
            
            self.logger.info(f"{GREEN}✅ DATABASE: personalized_links table ready{END}")
            
        except Exception as e:
            self.logger.error(f"{RED}❌ DATABASE ERROR: {str(e)}{END}")
            raise HTTPException(status_code=500, detail=f"Database initialization failed: {str(e)}")
    
    def generate_slug(self, lead_name: str) -> str:
        """Generate unique slug for personalized link"""
        try:
            # Clean and normalize name
            clean_name = lead_name.lower().strip()
            clean_name = ''.join(c if c.isalnum() or c in '-_' else '-' for c in clean_name)
            
            # Generate UUID for uniqueness
            unique_id = str(uuid.uuid4())[:8]
            
            # Create slug
            slug = f"penawaran-{clean_name}-{unique_id}"
            
            # Ensure uniqueness
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # Check if slug already exists
            # cursor.execute() removed"SELECT COUNT(*) FROM personalized_links WHERE slug = ?", (slug,))
            if cursor.fetchone()[0] > 0:
                # Generate new slug with different UUID
                unique_id = str(uuid.uuid4())[:8]
                slug = f"penawaran-{clean_name}-{unique_id}"
            
            # conn.close() removed
            
            return slug
            
        except Exception as e:
            self.logger.error(f"{RED}❌ SLUG GENERATION ERROR: {str(e)}{END}")
            # Fallback to timestamp-based slug
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            return f"penawaran-{lead_name.lower().replace(' ', '-')}-{timestamp}"
    
    def create_personalized_link(self, request: PersonalizedLinkRequest) -> PersonalizedLinkResponse:
        """Create personalized link for prospect"""
        try:
            self.logger.info(f"{CYAN}🔗 GENERATING LINK: {request.lead_name}{END}")
            
            # Generate unique slug
            slug = self.generate_slug(request.lead_name)
            
            # Create full URL
            full_url = f"{self.base_url}/p/{slug}"
            
            # Prepare metadata
            metadata = {
                "source": "sniper_api",
                "ip_address": "api_request",
                "user_agent": "lumina_os_api"
            }
            
            # Save to database
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # cursor.execute() removed"""
                INSERT INTO personalized_links 
                (slug, lead_id, lead_name, budget, location, contact_info, 
                 created_at, updated_at, status, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                slug,
                request.lead_id,
                request.lead_name,
                request.budget,
                request.location,
                request.contact_info,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'active',
                str(metadata)
            ))
            
            # conn.commit() removed
            # conn.close() removed
            
            # Generate QR code URL (placeholder for now)
            qr_code_url = f"https://api.qrserver.com/v1/create-qr-code/?data={full_url}"
            
            # Generate preview URL
            preview_url = f"{self.base_url}/api/sniper-links/{slug}/preview"
            
            self.logger.info(f"{GREEN}✅ LINK CREATED: {slug} for {request.lead_name}{END}")
            
            return PersonalizedLinkResponse(
                success=True,
                slug=slug,
                full_url=full_url,
                lead_name=request.lead_name,
                budget=request.budget,
                location=request.location,
                created_at=datetime.now().isoformat(),
                qr_code_url=qr_code_url,
                preview_url=preview_url
            )
            
        except Exception as e:
            self.logger.error(f"{RED}❌ LINK CREATION ERROR: {str(e)}{END}")
            raise HTTPException(status_code=500, detail=f"Failed to create personalized link: {str(e)}")
    
    def get_link_data(self, slug: str) -> Optional[LinkData]:
        """Get link data by slug"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # cursor.execute() removed"""
                SELECT slug, lead_id, lead_name, budget, location, contact_info,
                       created_at, updated_at, view_count, status, metadata
                FROM personalized_links 
                WHERE slug = ? AND status = 'active'
            """, (slug,))
            
            row = cursor.fetchone()
            # conn.close() removed
            
            if row:
                columns = [desc[0] for desc in cursor.description]
                link_data = dict(zip(columns, row))
                
                # Increment view count
                self._increment_view_count(slug)
                
                return link_data
            
            return None
            
        except Exception as e:
            self.logger.error(f"{RED}❌ LINK DATA ERROR: {str(e)}{END}")
            return None
    
    def _increment_view_count(self, slug: str) -> None:
        """Increment view count for analytics"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # cursor.execute() removed"""
                UPDATE personalized_links 
                SET view_count = view_count + 1, updated_at = ?
                WHERE slug = ?
            """, (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), slug))
            
            # conn.commit() removed
            # conn.close() removed
            
        except Exception as e:
            self.logger.error(f"{RED}❌ VIEW COUNT ERROR: {str(e)}{END}")
    
    def get_link_statistics(self) -> Dict[str, Any]:
        """Get link generation statistics"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # Total links
            # cursor.execute() removed"SELECT COUNT(*) FROM personalized_links")
            total_links = cursor.fetchone()[0]
            
            # Active links
            # cursor.execute() removed"SELECT COUNT(*) FROM personalized_links WHERE status = 'active'")
            active_links = cursor.fetchone()[0]
            
            # Links created today
            today = datetime.now().strftime('%Y-%m-%d')
            # cursor.execute() removed"SELECT COUNT(*) FROM personalized_links WHERE DATE(created_at) = ?", (today,))
            today_links = cursor.fetchone()[0]
            
            # Top viewed links
            # cursor.execute() removed"""
                SELECT slug, lead_name, view_count 
                FROM personalized_links 
                WHERE status = 'active'
                ORDER BY view_count DESC 
                LIMIT 10
            """)
            top_viewed = cursor.fetchall()
            
            # conn.close() removed
            
            return {
                "total_links": total_links,
                "active_links": active_links,
                "today_links": today_links,
                "top_viewed": [
                    {"slug": row[0], "lead_name": row[1], "view_count": row[2]}
                    for row in top_viewed
                ],
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"{RED}❌ STATISTICS ERROR: {str(e)}{END}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}

# Global link manager instance
link_manager = SniperLinkManager()

# API Endpoints
@router.post("/generate", response_model=PersonalizedLinkResponse)
async def generate_personalized_link(request: PersonalizedLinkRequest):
    """
    Generate personalized link for prospect
    """
    try:
        logger.info(f"{CYAN}📥 API REQUEST: Generate link for {request.lead_name}{END}")
        
        # Validate request
        if not request.lead_name or len(request.lead_name.strip()) < 2:
            raise HTTPException(
                status_code=400, 
                detail="Lead name must be at least 2 characters long"
            )
        
        # Generate personalized link
        result = link_manager.create_personalized_link(request)
        
        logger.info(f"{GREEN}✅ API SUCCESS: Link generated for {result.lead_name}{END}")
        return result
        
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"{RED}❌ API ERROR: {str(e)}{END}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/{slug}", response_model=LinkData)
async def get_personalized_link(slug: str):
    """
    Get personalized link data by slug
    """
    try:
        logger.info(f"{CYAN}📥 API REQUEST: Get link data for {slug}{END}")
        
        # Get link data
        link_data = link_manager.get_link_data(slug)
        
        if not link_data:
            raise HTTPException(
                status_code=404, 
                detail="Personalized link not found or expired"
            )
        
        logger.info(f"{GREEN}✅ API SUCCESS: Link data retrieved for {slug}{END}")
        return link_data
        
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"{RED}❌ API ERROR: {str(e)}{END}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/{slug}/preview", response_model=PersonalizedLinkResponse)
async def get_link_preview(slug: str):
    """
    Get link preview data (for admin/preview purposes)
    """
    try:
        logger.info(f"{CYAN}📥 API REQUEST: Get preview for {slug}{END}")
        
        # Get link data
        link_data = link_manager.get_link_data(slug)
        
        if not link_data:
            raise HTTPException(
                status_code=404, 
                detail="Personalized link not found or expired"
            )
        
        # Create preview response
        preview_response = PersonalizedLinkResponse(
            success=True,
            slug=link_data['slug'],
            full_url=f"{link_manager.base_url}/p/{link_data['slug']}",
            lead_name=link_data['lead_name'],
            budget=link_data['budget'],
            location=link_data['location'],
            created_at=link_data['created_at'],
            qr_code_url=f"https://api.qrserver.com/v1/create-qr-code/?data={link_manager.base_url}/p/{link_data['slug']}",
            preview_url=f"{link_manager.base_url}/api/sniper-links/{link_data['slug']}/preview"
        )
        
        logger.info(f"{GREEN}✅ API SUCCESS: Preview generated for {slug}{END}")
        return preview_response
        
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"{RED}❌ API ERROR: {str(e)}{END}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/statistics")
async def get_link_statistics():
    """
    Get link generation statistics
    """
    try:
        logger.info(f"{CYAN}📊 API REQUEST: Get statistics{END}")
        
        stats = link_manager.get_link_statistics()
        
        logger.info(f"{GREEN}✅ API SUCCESS: Statistics retrieved{END}")
        return stats
        
    except Exception as e:
        logger.error(f"{RED}❌ API ERROR: {str(e)}{END}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    # Test the sniper links API
    print(f"{MAGENTA}{'='*80}{END}")
    print(f"{CYAN}LUMINA OS - SNIPER LINKS API{END}")
    print(f"{MAGENTA}{'='*80}{END}")
    
    # Test link generation
    test_request = PersonalizedLinkRequest(
        lead_name="Budi Santoso",
        budget="300-500jt",
        location="Serang",
        contact_info="+62812345678"
    )
    
    try:
        result = link_manager.create_personalized_link(test_request)
        print(f"{GREEN}✅ TEST SUCCESS: {result.full_url}{END}")
        print(f"Slug: {result.slug}")
        print(f"Lead: {result.lead_name}")
        print(f"Budget: {result.budget}")
        print(f"Location: {result.location}")
        
        # Test link retrieval
        link_data = link_manager.get_link_data(result.slug)
        if link_data:
            print(f"{GREEN}✅ RETRIEVAL SUCCESS: {link_data['lead_name']} - Views: {link_data['view_count']}{END}")
        
        # Test statistics
        stats = link_manager.get_link_statistics()
        print(f"{GREEN}✅ STATISTICS: {stats['total_links']} total, {stats['active_links']} active{END}")
        
    except Exception as e:
        print(f"{RED}❌ TEST FAILED: {str(e)}{END}")
    
    print(f"{MAGENTA}{'='*80}{END}")
