from flask import Blueprint, jsonify
from app.extensions import db
from app.models import (
    Interface,
    InterfaceEndpoint,
    EndpointParameter,
    EndpointResponse,
    InterfaceChangeLog,
)


interface_bp = Blueprint("interface", __name__)


def serialize_basic(i: Interface):
    return {
        "id": i.id,
        "name": i.name,
        "slug": i.slug,
        "description": i.description,
        "version": i.version,
        "status": i.status,
        "category": i.category,
        "visibility": i.visibility,
        "documentationUrl": i.documentation_url,
        "repoUrl": i.repo_url,
        "contactEmail": i.contact_email,
        "tags": i.tags or [],
        "createdAt": i.created_at.isoformat() if i.created_at else None,
        "updatedAt": i.updated_at.isoformat() if i.updated_at else None,
        "endpointCount": len(i.endpoints),
    }


def serialize_endpoint(e: InterfaceEndpoint):
    return {
        "id": e.id,
        "method": e.method,
        "path": e.path,
        "summary": e.summary,
        "description": e.description,
        "authRequired": e.auth_required,
        "rateLimitPerMinute": e.rate_limit_per_minute,
        "deprecated": e.deprecated,
        "versionAdded": e.version_added,
        "versionRemoved": e.version_removed,
        "parameters": [
            {
                "id": p.id,
                "name": p.name,
                "location": p.location,
                "type": p.type,
                "required": p.required,
                "default": p.default_value,
                "description": p.description,
                "example": p.example,
            }
            for p in e.parameters
        ],
        "responses": [
            {
                "id": r.id,
                "httpStatus": r.http_status,
                "contentType": r.content_type,
                "schema": r.schema,
                "example": r.example,
            }
            for r in e.responses
        ],
    }


def serialize_full(i: Interface):
    data = serialize_basic(i)
    data.update(
        {
            "endpoints": [serialize_endpoint(e) for e in i.endpoints],
            "changelog": [
                {
                    "id": c.id,
                    "version": c.version,
                    "changeType": c.change_type,
                    "description": c.description,
                    "createdAt": c.created_at.isoformat() if c.created_at else None,
                }
                for c in i.changelog
            ],
        }
    )
    return data


@interface_bp.get("/interfaces")
def list_interfaces():
    interfaces = Interface.query.order_by(Interface.name.asc()).all()
    return jsonify([serialize_basic(i) for i in interfaces])


@interface_bp.get("/interfaces/<id>")
def get_interface(id: int):
    interface = Interface.query.get(id)
    if interface is None:
        return jsonify({"message": "Interface not found"}), 404
    return jsonify(serialize_full(interface))


