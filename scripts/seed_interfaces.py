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
    InterfaceFeature,
    InterfaceWorkflow,
    InterfaceHotkey,
)


def upsert_interface():
    app = create_app()
    with app.app_context():
        iface = Interface.query.filter_by(slug="annotation-ui").first()
        if not iface:
            iface = Interface(
                name="Annotation Interface (USR)",
                slug="annotation-ui",
                description="Web interface for USR annotation over MT output with evaluation, editing, feedback, alignment and tagging capabilities.",
                version="1.0.0",
                status="active",
                category="annotator-ui",
                visibility="internal",
                contact_email="owner@example.com",
                tags=["usr", "mt", "annotation"],
                supported_tasks=["evaluation", "editing", "feedback", "alignment", "tagging"],
                mt_engines=["IndicTrans2"],
                languages_supported=["hi", "en"],
                ui_routes=["/annotator", "/admin/assignments"],
                resources={"guide": "https://example.com/guide", "shortcuts": "https://example.com/shortcuts"},
            )
            db.session.add(iface)
            db.session.flush()

        # Features
        default_features = [
            ("MT Output Evaluation", "evaluation", "Rate MT quality with error tagging"),
            ("Inline Editing", "editing", "Edit MT output with keyboard-first UX"),
            ("Feedback Collection", "feedback", "Submit reviewer notes and justifications"),
            ("Source-Target Alignment", "alignment", "Align tokens/spans for analysis"),
            ("Linguistic Tagging", "tagging", "Tag gender, agreement, word order errors"),
        ]
        for name, category, desc in default_features:
            exists = InterfaceFeature.query.filter_by(interface_id=iface.id, name=name).first()
            if not exists:
                db.session.add(InterfaceFeature(interface_id=iface.id, name=name, category=category, description=desc))

        # Workflows
        wf_eval = InterfaceWorkflow.query.filter_by(interface_id=iface.id, name="Evaluation Workflow").first()
        if not wf_eval:
            db.session.add(
                InterfaceWorkflow(
                    interface_id=iface.id,
                    name="Evaluation Workflow",
                    description="Evaluate MT output and tag errors",
                    steps=[
                        "Open assigned task",
                        "Review source/MT pair",
                        "Tag errors (gender, word order, agreement)",
                        "Submit rating and notes",
                    ],
                )
            )

        wf_edit = InterfaceWorkflow.query.filter_by(interface_id=iface.id, name="Editing Workflow").first()
        if not wf_edit:
            db.session.add(
                InterfaceWorkflow(
                    interface_id=iface.id,
                    name="Editing Workflow",
                    description="Edit MT output and save corrections",
                    steps=[
                        "Open segment",
                        "Edit translation inline",
                        "Align changed spans if needed",
                        "Save correction",
                    ],
                )
            )

        # Hotkeys
        hotkeys = [
            ("Accept translation", "Ctrl+Enter", "editor"),
            ("Toggle alignment mode", "A", "alignment"),
            ("Add error tag", "T", "tagging"),
        ]
        for action, combo, context in hotkeys:
            hk = InterfaceHotkey.query.filter_by(interface_id=iface.id, combo=combo).first()
            if not hk:
                db.session.add(InterfaceHotkey(interface_id=iface.id, action=action, combo=combo, context=context))

        # Changelog
        cl = InterfaceChangeLog.query.filter_by(interface_id=iface.id, version="1.0.0").first()
        if not cl:
            db.session.add(
                InterfaceChangeLog(
                    interface_id=iface.id,
                    version="1.0.0",
                    change_type="added",
                    description="Initial UI documented for presentation (tasks, features, workflows, hotkeys).",
                )
            )

        db.session.commit()
        print("Seeded Annotation Interface (USR)")


if __name__ == "__main__":
    upsert_interface()
