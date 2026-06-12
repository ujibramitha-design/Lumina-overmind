"""
LUMINA OS - Workflow Engine API Endpoints
==========================================

Workflow deployment and management endpoints for the ReactFlow integration.
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid
import json
import logging

from ..middleware.jwt_auth import get_current_active_user, get_admin_user
from ..models.user import User

# Setup logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/workflows", tags=["workflows"])

# Pydantic models
class WorkflowNode(BaseModel):
    id: str
    type: str
    position: Dict[str, float]
    data: Dict[str, Any]

class WorkflowEdge(BaseModel):
    id: str
    source: str
    target: str
    sourceHandle: Optional[str] = None
    targetHandle: Optional[str] = None

class WorkflowDeployRequest(BaseModel):
    name: str
    description: str
    nodes: List[WorkflowNode]
    edges: List[WorkflowEdge]

class WorkflowDeployResponse(BaseModel):
    success: bool
    workflow_id: str
    message: str
    deployed_at: datetime
    node_count: int
    edge_count: int

class WorkflowStatusResponse(BaseModel):
    success: bool
    workflow_id: str
    status: str
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any]

# In-memory storage for workflows (in production, use database)
WORKFLOWS_DB: Dict[str, Dict[str, Any]] = {}

@router.post("/deploy", response_model=WorkflowDeployResponse)
async def deploy_workflow(
    workflow_data: WorkflowDeployRequest,
    current_user: User = Depends(get_current_active_user),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """
    Deploy a new workflow from ReactFlow data.
    
    This endpoint receives workflow nodes and edges from the frontend,
    validates them, and creates a deployable workflow configuration.
    """
    try:
        # Generate unique workflow ID
        workflow_id = f"workflow_{uuid.uuid4().hex[:8]}"
        
        # Validate workflow structure
        if not workflow_data.nodes:
            raise HTTPException(status_code=400, detail="Workflow must have at least one node")
        
        # Check for disconnected nodes
        node_ids = {node.id for node in workflow_data.nodes}
        edge_connections = set()
        for edge in workflow_data.edges:
            edge_connections.add(edge.source)
            edge_connections.add(edge.target)
        
        disconnected_nodes = node_ids - edge_connections
        if len(disconnected_nodes) > 1:  # Allow one disconnected node (trigger)
            logger.warning(f"Workflow {workflow_id} has {len(disconnected_nodes)} disconnected nodes")
        
        # Create workflow configuration
        workflow_config = {
            "id": workflow_id,
            "name": workflow_data.name,
            "description": workflow_data.description,
            "nodes": [node.dict() for node in workflow_data.nodes],
            "edges": [edge.dict() for edge in workflow_data.edges],
            "metadata": {
                "created_by": current_user.username,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
                "status": "deployed",
                "version": "1.0.0",
                "node_count": len(workflow_data.nodes),
                "edge_count": len(workflow_data.edges)
            }
        }
        
        # Store workflow
        WORKFLOWS_DB[workflow_id] = workflow_config
        
        # Background task for workflow processing
        background_tasks.add_task(process_workflow_deployment, workflow_id, workflow_config)
        
        logger.info(f"Workflow {workflow_id} deployed successfully by {current_user.username}")
        
        return WorkflowDeployResponse(
            success=True,
            workflow_id=workflow_id,
            message=f"Workflow '{workflow_data.name}' deployed successfully",
            deployed_at=datetime.utcnow(),
            node_count=len(workflow_data.nodes),
            edge_count=len(workflow_data.edges)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deploying workflow: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to deploy workflow: {str(e)}")

@router.get("/{workflow_id}", response_model=WorkflowStatusResponse)
async def get_workflow_status(
    workflow_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get the status and metadata of a deployed workflow."""
    
    if workflow_id not in WORKFLOWS_DB:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    workflow = WORKFLOWS_DB[workflow_id]
    
    return WorkflowStatusResponse(
        success=True,
        workflow_id=workflow_id,
        status=workflow["metadata"]["status"],
        created_at=datetime.fromisoformat(workflow["metadata"]["created_at"]),
        updated_at=datetime.fromisoformat(workflow["metadata"]["updated_at"]),
        metadata=workflow["metadata"]
    )

@router.get("/", response_model=List[WorkflowStatusResponse])
async def list_workflows(
    current_user: User = Depends(get_current_active_user)
):
    """List all workflows deployed by the current user."""
    
    user_workflows = []
    for workflow_id, workflow in WORKFLOWS_DB.items():
        if workflow["metadata"]["created_by"] == current_user.username:
            user_workflows.append(WorkflowStatusResponse(
                success=True,
                workflow_id=workflow_id,
                status=workflow["metadata"]["status"],
                created_at=datetime.fromisoformat(workflow["metadata"]["created_at"]),
                updated_at=datetime.fromisoformat(workflow["metadata"]["updated_at"]),
                metadata=workflow["metadata"]
            ))
    
    return user_workflows

@router.delete("/{workflow_id}")
async def delete_workflow(
    workflow_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Delete a deployed workflow."""
    
    if workflow_id not in WORKFLOWS_DB:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    workflow = WORKFLOWS_DB[workflow_id]
    
    # Check if user owns the workflow or is admin
    if workflow["metadata"]["created_by"] != current_user.username and current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Not authorized to delete this workflow")
    
    # Delete workflow
    del WORKFLOWS_DB[workflow_id]
    
    logger.info(f"Workflow {workflow_id} deleted by {current_user.username}")
    
    return {"success": True, "message": f"Workflow {workflow_id} deleted successfully"}

@router.post("/{workflow_id}/execute")
async def execute_workflow(
    workflow_id: str,
    current_user: User = Depends(get_current_active_user),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """Execute a deployed workflow."""
    
    if workflow_id not in WORKFLOWS_DB:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    workflow = WORKFLOWS_DB[workflow_id]
    
    # Update status to running
    workflow["metadata"]["status"] = "running"
    workflow["metadata"]["updated_at"] = datetime.utcnow().isoformat()
    
    # Background task for workflow execution
    background_tasks.add_task(execute_workflow_tasks, workflow_id, workflow)
    
    logger.info(f"Workflow {workflow_id} execution started by {current_user.username}")
    
    return {"success": True, "message": f"Workflow {workflow_id} execution started"}

# Background tasks
async def process_workflow_deployment(workflow_id: str, workflow_config: Dict[str, Any]):
    """
    Background task to process workflow deployment.
    In production, this would:
    1. Validate node connections
    2. Check for required plugins
    3. Create execution plan
    4. Setup monitoring
    """
    try:
        # Simulate processing time
        import asyncio
        await asyncio.sleep(2)
        
        # Update workflow status
        if workflow_id in WORKFLOWS_DB:
            WORKFLOWS_DB[workflow_id]["metadata"]["status"] = "ready"
            WORKFLOWS_DB[workflow_id]["metadata"]["updated_at"] = datetime.utcnow().isoformat()
        
        logger.info(f"Workflow {workflow_id} processing completed")
        
    except Exception as e:
        logger.error(f"Error processing workflow {workflow_id}: {str(e)}")
        if workflow_id in WORKFLOWS_DB:
            WORKFLOWS_DB[workflow_id]["metadata"]["status"] = "error"
            WORKFLOWS_DB[workflow_id]["metadata"]["updated_at"] = datetime.utcnow().isoformat()

async def execute_workflow_tasks(workflow_id: str, workflow_config: Dict[str, Any]):
    """
    Background task to execute workflow tasks.
    In production, this would:
    1. Execute trigger nodes
    2. Process action nodes
    3. Send notifications
    4. Handle errors and retries
    """
    try:
        # Simulate execution
        import asyncio
        await asyncio.sleep(5)
        
        # Update workflow status
        if workflow_id in WORKFLOWS_DB:
            WORKFLOWS_DB[workflow_id]["metadata"]["status"] = "completed"
            WORKFLOWS_DB[workflow_id]["metadata"]["updated_at"] = datetime.utcnow().isoformat()
        
        logger.info(f"Workflow {workflow_id} execution completed")
        
    except Exception as e:
        logger.error(f"Error executing workflow {workflow_id}: {str(e)}")
        if workflow_id in WORKFLOWS_DB:
            WORKFLOWS_DB[workflow_id]["metadata"]["status"] = "failed"
            WORKFLOWS_DB[workflow_id]["metadata"]["updated_at"] = datetime.utcnow().isoformat()
