import sys
import os

# Make sure the app package is discoverable, just like in run.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions import db
from app.models import (
    Interface,
    InterfaceEndpoint,
    EndpointParameter,
    EndpointResponse,
    InterfaceChangeLog,
)


def upsert_interface():
    app = create_app()
    with app.app_context():
        iface = Interface.query.filter_by(slug="annotation-service").first()
        if not iface:
            iface = Interface(
                name="Annotation Service API",
                slug="annotation-service",
                description="APIs supporting USR annotation workflows for Machine Translation.",
                version="1.0.0",
                status="active",
                category="annotation",
                visibility="internal",
                contact_email="owner@example.com",
                tags=["usr", "mt"],
            )
            db.session.add(iface)
            db.session.flush()

        # Endpoint 1: List annotator tasks
        ep1 = InterfaceEndpoint.query.filter_by(
            interface_id=iface.id, method="GET", path="/api/annotator/dashboard"
        ).first()
        if not ep1:
            ep1 = InterfaceEndpoint(
                interface_id=iface.id,
                method="GET",
                path="/api/annotator/dashboard",
                summary="Annotator dashboard metrics",
                description="Returns task statistics for the logged-in annotator.",
                auth_required=True,
                rate_limit_per_minute=120,
                version_added="1.0.0",
            )
            db.session.add(ep1)
            db.session.flush()
            db.session.add(EndpointResponse(endpoint_id=ep1.id, http_status=200))

        # Endpoint 2: Admin list projects
        ep2 = InterfaceEndpoint.query.filter_by(
            interface_id=iface.id, method="GET", path="/api/admin/projects"
        ).first()
        if not ep2:
            ep2 = InterfaceEndpoint(
                interface_id=iface.id,
                method="GET",
                path="/api/admin/projects",
                summary="List projects",
                description="Lists all projects managed by admin.",
                auth_required=True,
                rate_limit_per_minute=60,
                version_added="1.0.0",
            )
            db.session.add(ep2)
            db.session.flush()
            db.session.add(EndpointParameter(
                endpoint_id=ep2.id,
                name="page",
                location="query",
                type="integer",
                required=False,
                description="Page number for pagination",
            ))
            db.session.add(EndpointResponse(endpoint_id=ep2.id, http_status=200))

        # Changelog
        cl = InterfaceChangeLog.query.filter_by(interface_id=iface.id, version="1.0.0").first()
        if not cl:
            db.session.add(
                InterfaceChangeLog(
                    interface_id=iface.id,
                    version="1.0.0",
                    change_type="added",
                    description="Initial version documented for presentation.",
                )
            )

        db.session.commit()
        print("Seeded Interface: annotation-service")


if __name__ == "__main__":
    upsert_interface()
