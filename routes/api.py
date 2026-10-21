"""
API Routes - RESTful API
Maps API requests to REST Controllers returning JSON payloads.
Organized into Direct (Resource-level) and Nested (Hierarchical / Relational) Routes.

Includes:
1. Direct Routes:
   - Users: /api/users
   - Announcements: /api/announcements
   - Job Postings: /api/jobs & /api/job-postings
   - Applications: /api/applications
2. Nested Relational Routes:
   - User Jobs: /api/users/{user_id}/jobs
   - User Announcements: /api/users/{user_id}/announcements
   - User Profile: /api/users/{user_id}/profile
   - User Applications: /api/users/{user_id}/applications
   - Job Applications: /api/jobs/{job_id}/applications
   - Job Author: /api/jobs/{id}/author
   - Application Job: /api/applications/{id}/job
   - Application Applicant: /api/applications/{id}/applicant
"""
from routes.router import Router
from controllers.api_user_controller import ApiUserController
from controllers.api_announcement_controller import ApiAnnouncementController
from controllers.api_job_controller import ApiJobController
from controllers.api_application_controller import ApiApplicationController


def register_api_routes(router: Router) -> Router:
    """Register all RESTful direct and nested API routes on the provided router."""

    # =========================================================================
    # 1. DIRECT ROUTES (Resource-Level CRUD)
    # =========================================================================

    # 1.1 Users (/api/users)
    router.get('/api/users', lambda params, body=None: ApiUserController.index())
    router.get('/api/users/{id}', lambda params, body=None: ApiUserController.show(params['id']))
    router.post('/api/users', lambda params, body=None: ApiUserController.store(body or {}))
    router.put('/api/users/{id}', lambda params, body=None: ApiUserController.update(params['id'], body or {}, partial=False))
    router.patch('/api/users/{id}', lambda params, body=None: ApiUserController.update(params['id'], body or {}, partial=True))
    router.delete('/api/users/{id}', lambda params, body=None: ApiUserController.destroy(params['id']))

    # 1.2 Announcements (/api/announcements)
    router.get('/api/announcements', lambda params, body=None: ApiAnnouncementController.index())
    router.get('/api/announcements/{id}', lambda params, body=None: ApiAnnouncementController.show(params['id']))
    router.post('/api/announcements', lambda params, body=None: ApiAnnouncementController.store(body or {}))
    router.put('/api/announcements/{id}', lambda params, body=None: ApiAnnouncementController.update(params['id'], body or {}, partial=False))
    router.patch('/api/announcements/{id}', lambda params, body=None: ApiAnnouncementController.update(params['id'], body or {}, partial=True))
    router.delete('/api/announcements/{id}', lambda params, body=None: ApiAnnouncementController.destroy(params['id']))

    # 1.3 Job Postings (/api/jobs & /api/job-postings alias)
    for prefix in ['/api/jobs', '/api/job-postings']:
        router.get(f'{prefix}', lambda params, body=None: ApiJobController.index())
        router.get(f'{prefix}/{{id}}', lambda params, body=None: ApiJobController.show(params['id']))
        router.post(f'{prefix}', lambda params, body=None: ApiJobController.store(body or {}))
        router.put(f'{prefix}/{{id}}', lambda params, body=None: ApiJobController.update(params['id'], body or {}, partial=False))
        router.patch(f'{prefix}/{{id}}', lambda params, body=None: ApiJobController.update(params['id'], body or {}, partial=True))
        router.delete(f'{prefix}/{{id}}', lambda params, body=None: ApiJobController.destroy(params['id']))

    # 1.4 Job Applications (/api/applications)
    router.get('/api/applications', lambda params, body=None: ApiApplicationController.index())
    router.get('/api/applications/{id}', lambda params, body=None: ApiApplicationController.show(params['id']))
    router.post('/api/applications', lambda params, body=None: ApiApplicationController.store(body or {}))
    router.put('/api/applications/{id}', lambda params, body=None: ApiApplicationController.update(params['id'], body or {}, partial=False))
    router.patch('/api/applications/{id}', lambda params, body=None: ApiApplicationController.update(params['id'], body or {}, partial=True))
    router.delete('/api/applications/{id}', lambda params, body=None: ApiApplicationController.destroy(params['id']))

    # =========================================================================
    # 2. NESTED ROUTES (Hierarchical Parent-Child Relationships)
    # =========================================================================

    # 2.1 User's Job Postings: /api/users/{user_id}/jobs
    router.get('/api/users/{user_id}/jobs', lambda params, body=None: ApiUserController.job_postings(params['user_id']))
    router.post('/api/users/{user_id}/jobs', lambda params, body=None: ApiUserController.store_job_posting(params['user_id'], body or {}))

    # 2.2 User's Announcements: /api/users/{user_id}/announcements
    router.get('/api/users/{user_id}/announcements', lambda params, body=None: ApiUserController.announcements(params['user_id']))

    # 2.3 User's Profile: /api/users/{user_id}/profile
    router.get('/api/users/{user_id}/profile', lambda params, body=None: ApiUserController.profile(params['user_id']))

    # 2.4 User's Job Applications: /api/users/{user_id}/applications
    router.get('/api/users/{user_id}/applications', lambda params, body=None: ApiApplicationController.by_user(params['user_id']))

    # 2.5 Job's Candidate Applications: /api/jobs/{job_id}/applications
    router.get('/api/jobs/{job_id}/applications', lambda params, body=None: ApiApplicationController.by_job(params['job_id']))
    router.post('/api/jobs/{job_id}/applications', lambda params, body=None: ApiApplicationController.store_for_job(params['job_id'], body or {}))

    # 2.6 Job's Author Profile: /api/jobs/{id}/author
    router.get('/api/jobs/{id}/author', lambda params, body=None: ApiJobController.author(params['id']))
    router.get('/api/job-postings/{id}/author', lambda params, body=None: ApiJobController.author(params['id']))

    # 2.7 Application's Job & Applicant Navigation
    router.get('/api/applications/{id}/job', lambda params, body=None: ApiApplicationController.get_job_rel(params['id']))
    router.get('/api/applications/{id}/applicant', lambda params, body=None: ApiApplicationController.get_applicant_rel(params['id']))

    return router
