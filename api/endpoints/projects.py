"""
Twin-Dragon Engine - Project Management API Endpoint
Multi-tenant property management system for KOMERSIL and SUBSIDI projects
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from pydantic import BaseModel
from typing import List, Optional
import os
import json
from datetime import datetime
from prisma import Client as PrismaClient

# Database dependency
def get_db():
    db = PrismaClient()
    return db

router = APIRouter(prefix="/api/projects", tags=["projects"])

# Pydantic Models
class ProjectCreate(BaseModel):
    namaProyek: str
    tipeProyek: str  # "KOMERSIL" or "SUBSIDI"
    lokasi: str
    hargaStart: float
    targetMarket: str
    # Enhanced Location System
    tipeInputLokasi: str = "NAMA_WILAYAH"  # "NAMA_WILAYAH" or "KOORDINAT"
    namaWilayah: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    radiusKm: int = 5
    config: Optional[dict] = None
    aiPromptStyle: Optional[str] = None
    dorkingTargets: Optional[List[str]] = []

class ProjectUpdate(BaseModel):
    namaProyek: Optional[str] = None
    tipeProyek: Optional[str] = None
    lokasi: Optional[str] = None
    hargaStart: Optional[float] = None
    targetMarket: Optional[str] = None
    # Enhanced Location System
    tipeInputLokasi: Optional[str] = None
    namaWilayah: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    radiusKm: Optional[int] = None
    config: Optional[dict] = None
    aiPromptStyle: Optional[str] = None
    dorkingTargets: Optional[List[str]] = None
    isActive: Optional[bool] = None

class ProjectResponse(BaseModel):
    id: str
    namaProyek: str
    tipeProyek: str
    lokasi: str
    hargaStart: float
    targetMarket: str
    # Enhanced Location System
    tipeInputLokasi: str
    namaWilayah: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    radiusKm: int
    config: Optional[dict] = None
    aiPromptStyle: Optional[str] = None
    dorkingTargets: List[str] = []
    isActive: bool
    leadsCount: int
    hotLeadsCount: int
    conversionRate: float
    createdAt: datetime
    updatedAt: datetime

# Helper Functions
def create_project_folders(project_id: str, project_name: str):
    """
    Create folder structure for new project with comprehensive error handling
    """
    import logging
    import traceback
    
    # Setup logging
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"Creating project folders for {project_name} (ID: {project_id})")
        
        # Define folder paths
        kb_path = f"knowledge_base/projects/{project_id}"
        assets_path = f"static/assets/projects/{project_id}"
        logs_path = f"logs/projects/{project_id}"
        
        folders_created = []
        errors_encountered = []
        
        # Create knowledge base folder
        try:
            os.makedirs(kb_path, exist_ok=True)
            folders_created.append(kb_path)
            logger.info(f"✅ Knowledge base folder created: {kb_path}")
        except PermissionError as e:
            error_msg = f"Permission denied creating knowledge base folder: {str(e)}"
            errors_encountered.append(error_msg)
            logger.error(f"❌ {error_msg}")
        except OSError as e:
            error_msg = f"OS error creating knowledge base folder: {str(e)}"
            errors_encountered.append(error_msg)
            logger.error(f"❌ {error_msg}")
        except Exception as e:
            error_msg = f"Unexpected error creating knowledge base folder: {str(e)}"
            errors_encountered.append(error_msg)
            logger.error(f"❌ {error_msg}")
        
        # Create assets folder
        try:
            os.makedirs(assets_path, exist_ok=True)
            folders_created.append(assets_path)
            logger.info(f"✅ Assets folder created: {assets_path}")
        except PermissionError as e:
            error_msg = f"Permission denied creating assets folder: {str(e)}"
            errors_encountered.append(error_msg)
            logger.error(f"❌ {error_msg}")
        except OSError as e:
            error_msg = f"OS error creating assets folder: {str(e)}"
            errors_encountered.append(error_msg)
            logger.error(f"❌ {error_msg}")
        except Exception as e:
            error_msg = f"Unexpected error creating assets folder: {str(e)}"
            errors_encountered.append(error_msg)
            logger.error(f"❌ {error_msg}")
        
        # Create logs folder
        try:
            os.makedirs(logs_path, exist_ok=True)
            folders_created.append(logs_path)
            logger.info(f"✅ Logs folder created: {logs_path}")
        except PermissionError as e:
            error_msg = f"Permission denied creating logs folder: {str(e)}"
            errors_encountered.append(error_msg)
            logger.error(f"❌ {error_msg}")
        except OSError as e:
            error_msg = f"OS error creating logs folder: {str(e)}"
            errors_encountered.append(error_msg)
            logger.error(f"❌ {error_msg}")
        except Exception as e:
            error_msg = f"Unexpected error creating logs folder: {str(e)}"
            errors_encountered.append(error_msg)
            logger.error(f"❌ {error_msg}")
        
        # Create project info file (only if knowledge base folder was created successfully)
        if kb_path in folders_created:
            try:
                project_info = {
                    "project_id": project_id,
                    "project_name": project_name,
                    "created_at": datetime.now().isoformat(),
                    "folders_created": folders_created,
                    "errors_encountered": errors_encountered,
                    "folder_structure": {
                        "knowledge_base": kb_path,
                        "assets": assets_path,
                        "logs": logs_path
                    }
                }
                
                info_file_path = f"{kb_path}/project_info.json"
                with open(info_file_path, "w") as f:
                    json.dump(project_info, f, indent=2)
                
                logger.info(f"✅ Project info file created: {info_file_path}")
                
            except PermissionError as e:
                error_msg = f"Permission denied creating project info file: {str(e)}"
                errors_encountered.append(error_msg)
                logger.error(f"❌ {error_msg}")
            except OSError as e:
                error_msg = f"OS error creating project info file: {str(e)}"
                errors_encountered.append(error_msg)
                logger.error(f"❌ {error_msg}")
            except Exception as e:
                error_msg = f"Unexpected error creating project info file: {str(e)}"
                errors_encountered.append(error_msg)
                logger.error(f"❌ {error_msg}")
        
        # Log final results
        if errors_encountered:
            logger.warning(f"⚠️ Project folder creation completed with {len(errors_encountered)} errors")
            for error in errors_encountered:
                logger.warning(f"   - {error}")
            
            # Return partial success if at least some folders were created
            if folders_created:
                return True, f"Project folders created with warnings. {len(folders_created)} folders created, {len(errors_encountered)} errors encountered."
            else:
                return False, f"Failed to create any project folders. Errors: {'; '.join(errors_encountered)}"
        else:
            logger.info(f"✅ All project folders created successfully: {len(folders_created)} folders")
            return True, f"All project folders created successfully: {len(folders_created)} folders"
        
    except Exception as e:
        # Catch-all error handler for unexpected issues
        error_msg = f"Critical error in project folder creation: {str(e)}"
        logger.error(f"❌ {error_msg}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False, error_msg

def validate_project_folders(project_id: str) -> dict:
    """
    Validate that all required project folders exist and are accessible
    """
    import logging
    
    logger = logging.getLogger(__name__)
    
    try:
        kb_path = f"knowledge_base/projects/{project_id}"
        assets_path = f"static/assets/projects/{project_id}"
        logs_path = f"logs/projects/{project_id}"
        
        validation_results = {
            "project_id": project_id,
            "folders": {},
            "overall_status": "valid",
            "issues": []
        }
        
        # Check knowledge base folder
        try:
            if os.path.exists(kb_path) and os.path.isdir(kb_path):
                if os.access(kb_path, os.R_OK | os.W_OK):
                    validation_results["folders"]["knowledge_base"] = {"status": "ok", "path": kb_path}
                else:
                    validation_results["folders"]["knowledge_base"] = {"status": "permission_denied", "path": kb_path}
                    validation_results["issues"].append(f"No read/write access to knowledge base folder: {kb_path}")
                    validation_results["overall_status"] = "warning"
            else:
                validation_results["folders"]["knowledge_base"] = {"status": "missing", "path": kb_path}
                validation_results["issues"].append(f"Knowledge base folder missing: {kb_path}")
                validation_results["overall_status"] = "error"
        except Exception as e:
            validation_results["folders"]["knowledge_base"] = {"status": "error", "path": kb_path, "error": str(e)}
            validation_results["issues"].append(f"Error checking knowledge base folder: {str(e)}")
            validation_results["overall_status"] = "error"
        
        # Check assets folder
        try:
            if os.path.exists(assets_path) and os.path.isdir(assets_path):
                if os.access(assets_path, os.R_OK | os.W_OK):
                    validation_results["folders"]["assets"] = {"status": "ok", "path": assets_path}
                else:
                    validation_results["folders"]["assets"] = {"status": "permission_denied", "path": assets_path}
                    validation_results["issues"].append(f"No read/write access to assets folder: {assets_path}")
                    validation_results["overall_status"] = "warning"
            else:
                validation_results["folders"]["assets"] = {"status": "missing", "path": assets_path}
                validation_results["issues"].append(f"Assets folder missing: {assets_path}")
                validation_results["overall_status"] = "error"
        except Exception as e:
            validation_results["folders"]["assets"] = {"status": "error", "path": assets_path, "error": str(e)}
            validation_results["issues"].append(f"Error checking assets folder: {str(e)}")
            validation_results["overall_status"] = "error"
        
        # Check logs folder
        try:
            if os.path.exists(logs_path) and os.path.isdir(logs_path):
                if os.access(logs_path, os.R_OK | os.W_OK):
                    validation_results["folders"]["logs"] = {"status": "ok", "path": logs_path}
                else:
                    validation_results["folders"]["logs"] = {"status": "permission_denied", "path": logs_path}
                    validation_results["issues"].append(f"No read/write access to logs folder: {logs_path}")
                    validation_results["overall_status"] = "warning"
            else:
                validation_results["folders"]["logs"] = {"status": "missing", "path": logs_path}
                validation_results["issues"].append(f"Logs folder missing: {logs_path}")
                validation_results["overall_status"] = "error"
        except Exception as e:
            validation_results["folders"]["logs"] = {"status": "error", "path": logs_path, "error": str(e)}
            validation_results["issues"].append(f"Error checking logs folder: {str(e)}")
            validation_results["overall_status"] = "error"
        
        logger.info(f"Project folder validation completed for {project_id}: {validation_results['overall_status']}")
        return validation_results
        
    except Exception as e:
        logger.error(f"Critical error in project folder validation: {str(e)}")
        return {
            "project_id": project_id,
            "folders": {},
            "overall_status": "error",
            "issues": [f"Validation failed: {str(e)}"]
        }

def get_ai_prompt_style(tipe_proyek: str) -> str:
    """Generate AI prompt style based on project type"""
    if tipe_proyek.upper() == "KOMERSIL":
        return """
        Gaya bahasa FORMAL dan PRESTISI:
        - Sapa dengan 'Bapak/Ibu'
        - Fokus pada prestise, eksklusivitas, dan investasi
        - Highlight KPR reguler dan kemudahan approval
        - Target: Eksekutif, Pengusaha, Profesional
        - Keywords: mewah, eksklusif, investasi, prestise, premium
        """
    else:  # SUBSIDI
        return """
        Gaya bahasa RAMAH dan APPROACHABLE:
        - Sapa dengan 'Kak/Mas/Mbak'
        - Fokus pada KPR FLPP, subsidi, dan cicilan ringan
        - Highlight kemudahan proses dan bantuan pemerintah
        - Target: PNS, P3K, Pekerja UMR, Keluarga Muda
        - Keywords: terjangkau, subsidi, FLPP, cicilan ringan, keluarga
        """

def get_dorking_targets(tipe_proyek: str) -> List[str]:
    """Generate dorking targets based on project type"""
    if tipe_proyek.upper() == "KOMERSIL":
        return [
            "eksekutif mencari rumah mewah",
            "pengusaha cari properti investasi",
            "professional cari hunian premium",
            "KPR bank untuk properti komersial",
            "rumah elit di [lokasi]"
        ]
    else:  # SUBSIDI
        return [
            "PNS cari rumah subsidi FLPP",
            "KPR subsidi pemerintah",
            "rumah murah untuk pegawai negeri",
            "cicilan rumah ringan",
            "program rumah subsidi [lokasi]"
        ]

# API Endpoints
@router.post("/", response_model=ProjectResponse)
async def create_project(project: ProjectCreate, background_tasks: BackgroundTasks, db: PrismaClient = Depends(get_db)):
    """Create new project with automatic folder creation"""
    try:
        # Validation for location input type
        if project.tipeInputLokasi == "KOORDINAT":
            if project.latitude is None or project.longitude is None:
                raise HTTPException(
                    status_code=400, 
                    detail="Latitude dan longitude wajib diisi untuk tipe input koordinat"
                )
        elif project.tipeInputLokasi == "NAMA_WILAYAH":
            if not project.namaWilayah and not project.lokasi:
                raise HTTPException(
                    status_code=400, 
                    detail="Nama wilayah atau lokasi wajib diisi untuk tipe input nama wilayah"
                )
        
        # Set AI prompt style and dorking targets based on project type
        ai_prompt_style = project.aiPromptStyle or get_ai_prompt_style(project.tipeProyek)
        dorking_targets = project.dorkingTargets or get_dorking_targets(project.tipeProyek)
        
        # Create project in database
        new_project = await db.project.create({
            'namaProyek': project.namaProyek,
            'tipeProyek': project.tipeProyek,
            'lokasi': project.lokasi,
            'hargaStart': project.hargaStart,
            'targetMarket': project.targetMarket,
            'tipeInputLokasi': project.tipeInputLokasi,
            'namaWilayah': project.namaWilayah,
            'latitude': project.latitude,
            'longitude': project.longitude,
            'radiusKm': project.radiusKm,
            'config': project.config,
            'aiPromptStyle': ai_prompt_style,
            'dorkingTargets': dorking_targets,
            'isActive': True
        })
        
        # Create project folders in background
        background_tasks.add_task(
            create_project_folders, 
            new_project.id, 
            project.namaProyek
        )
        
        # Return response
        project_response = ProjectResponse(
            id=new_project.id,
            namaProyek=new_project.namaProyek,
            tipeProyek=new_project.tipeProyek,
            lokasi=new_project.lokasi,
            hargaStart=new_project.hargaStart,
            targetMarket=new_project.targetMarket,
            config=new_project.config,
            aiPromptStyle=new_project.aiPromptStyle,
            dorkingTargets=new_project.dorkingTargets,
            isActive=new_project.isActive,
            leadsCount=new_project.leadsCount,
            hotLeadsCount=new_project.hotLeadsCount,
            conversionRate=new_project.conversionRate,
            createdAt=new_project.createdAt,
            updatedAt=new_project.updatedAt
        )
        
        return project_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create project: {str(e)}")

@router.get("/", response_model=List[ProjectResponse])
async def get_projects(tipeProyek: Optional[str] = None, isActive: Optional[bool] = None, db: PrismaClient = Depends(get_db)):
    """Get all projects with optional filtering"""
    try:
        # Build where clause
        where_clause = {}
        if tipeProyek:
            where_clause['tipeProyek'] = tipeProyek
        if isActive is not None:
            where_clause['isActive'] = isActive
        
        # Query database
        projects = await db.project.find_many(
            where=where_clause,
            order={'createdAt': 'desc'}
        )
        
        # Convert to response format
        project_responses = []
        for project in projects:
            project_responses.append(ProjectResponse(
                id=project.id,
                namaProyek=project.namaProyek,
                tipeProyek=project.tipeProyek,
                lokasi=project.lokasi,
                hargaStart=project.hargaStart,
                targetMarket=project.targetMarket,
                config=project.config,
                aiPromptStyle=project.aiPromptStyle,
                dorkingTargets=project.dorkingTargets,
                isActive=project.isActive,
                leadsCount=project.leadsCount,
                hotLeadsCount=project.hotLeadsCount,
                conversionRate=project.conversionRate,
                createdAt=project.createdAt,
                updatedAt=project.updatedAt
            ))
        
        return project_responses
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch projects: {str(e)}")

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: str, db: PrismaClient = Depends(get_db)):
    """Get specific project by ID"""
    try:
        # Query database
        project = await db.project.find_unique(
            where={'id': project_id}
        )
        
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Return response
        return ProjectResponse(
            id=project.id,
            namaProyek=project.namaProyek,
            tipeProyek=project.tipeProyek,
            lokasi=project.lokasi,
            hargaStart=project.hargaStart,
            targetMarket=project.targetMarket,
            config=project.config,
            aiPromptStyle=project.aiPromptStyle,
            dorkingTargets=project.dorkingTargets,
            isActive=project.isActive,
            leadsCount=project.leadsCount,
            hotLeadsCount=project.hotLeadsCount,
            conversionRate=project.conversionRate,
            createdAt=project.createdAt,
            updatedAt=project.updatedAt
        )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch project: {str(e)}")

@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: str, project_update: ProjectUpdate, db: PrismaClient = Depends(get_db)):
    """Update existing project"""
    try:
        # Build update data
        update_data = {}
        if project_update.namaProyek is not None:
            update_data['namaProyek'] = project_update.namaProyek
        if project_update.tipeProyek is not None:
            update_data['tipeProyek'] = project_update.tipeProyek
            # Auto-update AI prompt style and dorking targets if project type changes
            update_data['aiPromptStyle'] = get_ai_prompt_style(project_update.tipeProyek)
            update_data['dorkingTargets'] = get_dorking_targets(project_update.tipeProyek)
        if project_update.lokasi is not None:
            update_data['lokasi'] = project_update.lokasi
        if project_update.hargaStart is not None:
            update_data['hargaStart'] = project_update.hargaStart
        if project_update.targetMarket is not None:
            update_data['targetMarket'] = project_update.targetMarket
        if project_update.config is not None:
            update_data['config'] = project_update.config
        if project_update.aiPromptStyle is not None:
            update_data['aiPromptStyle'] = project_update.aiPromptStyle
        if project_update.dorkingTargets is not None:
            update_data['dorkingTargets'] = project_update.dorkingTargets
        if project_update.isActive is not None:
            update_data['isActive'] = project_update.isActive
        
        # Update project in database
        project = await db.project.update(
            where={'id': project_id},
            data=update_data
        )
        
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Return response
        return ProjectResponse(
            id=project.id,
            namaProyek=project.namaProyek,
            tipeProyek=project.tipeProyek,
            lokasi=project.lokasi,
            hargaStart=project.hargaStart,
            targetMarket=project.targetMarket,
            config=project.config,
            aiPromptStyle=project.aiPromptStyle,
            dorkingTargets=project.dorkingTargets,
            isActive=project.isActive,
            leadsCount=project.leadsCount,
            hotLeadsCount=project.hotLeadsCount,
            conversionRate=project.conversionRate,
            createdAt=project.createdAt,
            updatedAt=project.updatedAt
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update project: {str(e)}")

@router.delete("/{project_id}")
async def delete_project(project_id: str, db: PrismaClient = Depends(get_db)):
    """Delete project (soft delete - set is_active=False)"""
    try:
        # Soft delete - set is_active=False
        project = await db.project.update(
            where={'id': project_id},
            data={'isActive': False}
        )
        
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        return {"message": f"Project {project_id} deactivated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete project: {str(e)}")

@router.post("/{project_id}/activate")
async def activate_project(project_id: str, db: PrismaClient = Depends(get_db)):
    """Activate project"""
    try:
        # Activate project - set is_active=True
        project = await db.project.update(
            where={'id': project_id},
            data={'isActive': True}
        )
        
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        return {"message": f"Project {project_id} activated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to activate project: {str(e)}")

@router.get("/{project_id}/stats")
async def get_project_stats(project_id: str):
    """Get project statistics"""
    try:
        # Mock implementation (replace with actual database query)
        return {
            "project_id": project_id,
            "total_leads": 25,
            "hot_leads": 8,
            "conversion_rate": 32.0,
            "campaigns_count": 3,
            "active_campaigns": 2,
            "last_updated": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch project stats: {str(e)}")
