import os

def replace_in_file(file_path, old_text, new_text):
    if not os.path.exists(file_path):
        print(f'File not found: {file_path}')
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if old_text not in content:
        print(f'Old text not found in {file_path}')
        return
    
    new_content = content.replace(old_text, new_text)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f'Successfully updated {file_path}')

# Fix projects.py
replace_in_file(
    'api/endpoints/projects.py',
    'from prisma import Client as PrismaClient\n\n# Database dependency\ndef get_db():\n    db = PrismaClient()\n    return db',
    'from core_modules.db_manager import prisma_manager\n\n# Database dependency\nasync def get_db():\n    db = await prisma_manager.get_db()\n    return db'
)

# Fix main.py routers
old_routers = '''# Import and include routers
try:
    from api.endpoints.intelligence import router as intelligence_router
    app.include_router(intelligence_router, prefix="/api/intelligence", tags=["Intelligence"])
    logger.info("✅ Intelligence router included")
except ImportError as e:
    logger.warning(f"⚠️ Intelligence router not available: {e}")

try:
    from api.endpoints.visual import router as visual_router
    app.include_router(visual_router, prefix="/api/visual", tags=["Visual"])
    logger.info("✅ Visual router included")
except ImportError as e:
    logger.warning(f"⚠️ Visual router not available: {e}")

try:
    from api.endpoints.vr import router as vr_router
    app.include_router(vr_router, prefix="/api/vr", tags=["VR"])
    logger.info("✅ VR router included")
except ImportError as e:
    logger.warning(f"⚠️ VR router not available: {e}")

try:
    from api.endpoints.notifications import router as notifications_router
    app.include_router(notifications_router, prefix="/api/notifications", tags=["Notifications"])
    logger.info("✅ Notifications router included")
except ImportError as e:
    logger.warning(f"⚠️ Notifications router not available: {e}")

# Temporarily disabled due to Prisma client issues
# try:
#     from api.endpoints.projects import router as projects_router
#     app.include_router(projects_router, tags=["Projects"])
#     logger.info("✅ Projects router included")
# except ImportError as e:
#     logger.warning(f"⚠️ Projects router not available: {e}")

# Temporarily disabled due to syntax errors in conversational_ai.py
# try:
#     from api.endpoints.jarvis import router as jarvis_router
#     app.include_router(jarvis_router, tags=["J.A.R.V.I.S."])
#     logger.info("✅ J.A.R.V.I.S. router included")
# except ImportError as e:
#     logger.warning(f"⚠️ J.A.R.V.I.S. router not available: {e}")'''

new_routers = '''# Import and include routers
try:
    from api.endpoints.intelligence import router as intelligence_router
    app.include_router(intelligence_router, prefix="/api/intelligence", tags=["Intelligence"])
    logger.info("✅ Intelligence router included")
except ImportError as e:
    logger.warning(f"⚠️ Intelligence router not available: {e}")

try:
    from api.endpoints.leads import router as leads_router
    app.include_router(leads_router, tags=["Leads"])
    logger.info("✅ Leads router included")
except ImportError as e:
    logger.warning(f"⚠️ Leads router not available: {e}")

try:
    from api.endpoints.visual import router as visual_router
    app.include_router(visual_router, prefix="/api/visual", tags=["Visual"])
    logger.info("✅ Visual router included")
except ImportError as e:
    logger.warning(f"⚠️ Visual router not available: {e}")

try:
    from api.endpoints.vr import router as vr_router
    app.include_router(vr_router, prefix="/api/vr", tags=["VR"])
    logger.info("✅ VR router included")
except ImportError as e:
    logger.warning(f"⚠️ VR router not available: {e}")

try:
    from api.endpoints.notifications import router as notifications_router
    app.include_router(notifications_router, prefix="/api/notifications", tags=["Notifications"])
    logger.info("✅ Notifications router included")
except ImportError as e:
    logger.warning(f"⚠️ Notifications router not available: {e}")

# Projects router
try:
    from api.endpoints.projects import router as projects_router
    app.include_router(projects_router, tags=["Projects"])
    logger.info("✅ Projects router included")
except ImportError as e:
    logger.warning(f"⚠️ Projects router not available: {e}")

# J.A.R.V.I.S. router
try:
    from api.endpoints.jarvis import router as jarvis_router
    app.include_router(jarvis_router, tags=["J.A.R.V.I.S."])
    logger.info("✅ J.A.R.V.I.S. router included")
except ImportError as e:
    logger.warning(f"⚠️ J.A.R.V.I.S. router not available: {e}")'''

replace_in_file('api/main.py', old_routers, new_routers)
