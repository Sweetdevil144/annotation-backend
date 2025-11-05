from . import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(
        db.String(50), nullable=False, default="pending"
    )  # admin, annotator, reviewer
    organization = db.Column(db.String(150))
    status = db.Column(db.String(50), default="pending")
    otp = db.Column(db.String(6), nullable=True)
    otp_expiration = db.Column(db.DateTime, nullable=True)

    annotator_assignments = db.relationship(
        "Assignment",
        foreign_keys="Assignment.annotator_id",
        back_populates="annotator",
        lazy=True,
        cascade="all, delete-orphan",
    )
    reviewer_assignments = db.relationship(
        "Assignment",
        foreign_keys="Assignment.reviewer_id",
        back_populates="reviewer",
        lazy=True,
        cascade="all, delete-orphan",
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Project(db.Model):
    __tablename__ = "project"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    language = db.Column(
        db.String(50), nullable=False, default="hindi"
    )  # Add this line

    chapters = db.relationship(
        "Chapter", back_populates="project", lazy=True, cascade="all, delete-orphan"
    )


class Chapter(db.Model):
    __tablename__ = "chapter"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    language = db.Column(
        db.String(50), nullable=False, default="hindi"
    )  # Add this line

    project = db.relationship("Project", back_populates="chapters")
    sentences = db.relationship(
        "Sentence", back_populates="chapter", lazy=True, cascade="all, delete-orphan"
    )


class Sentence(db.Model):
    __tablename__ = "sentence"

    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey("chapter.id"), nullable=False)
    text = db.Column(db.Text, nullable=False)
    sentence_id = db.Column(db.String(100))  # e.g., Geo_nios_3ch_0002
    language = db.Column(
        db.String(50), nullable=False, default="hindi"
    )  # Add this line

    chapter = db.relationship("Chapter", back_populates="sentences")
    segments = db.relationship(
        "Segment", back_populates="sentence", lazy=True, cascade="all, delete-orphan"
    )


class Segment(db.Model):
    __tablename__ = "segment"

    id = db.Column(db.Integer, primary_key=True)
    sentence_id = db.Column(db.Integer, db.ForeignKey("sentence.id"), nullable=False)
    text = db.Column(db.Text, nullable=False)
    wxtext = db.Column(db.Text)
    englishtext = db.Column(db.Text)
    segment_id = db.Column(db.String(100))  # e.g., Geo_nios_3ch_0002
    language = db.Column(
        db.String(50), nullable=False, default="hindi"
    )  # Add this line

    sentence = db.relationship("Sentence", back_populates="segments")
    usrs = db.relationship(
        "USR", back_populates="segment", lazy=True, cascade="all, delete-orphan"
    )
    assignments = db.relationship(
        "Assignment", back_populates="segment", lazy=True, cascade="all, delete-orphan"
    )


class USR(db.Model):
    __tablename__ = "usr"

    id = db.Column(db.Integer, primary_key=True)
    segment_id = db.Column(db.Integer, db.ForeignKey("segment.id"), nullable=False)
    status = db.Column(db.String(50), default="Pending")
    sentence_type = db.Column(db.String(100))  # e.g., %affirmative
    language = db.Column(db.String(50), nullable=False, default="hindi")
    # Relationships
    segment = db.relationship("Segment", back_populates="usrs")
    lexical_info = db.relationship(
        "LexicalInfo", back_populates="usr", lazy=True, cascade="all, delete-orphan"
    )
    dependency_info = db.relationship(
        "DependencyInfo", back_populates="usr", lazy=True, cascade="all, delete-orphan"
    )
    discourse_coref_info = db.relationship(
        "DiscourseCorefInfo",
        back_populates="usr",
        lazy=True,
        cascade="all, delete-orphan",
    )
    construction_info = db.relationship(
        "ConstructionInfo",
        back_populates="usr",
        lazy=True,
        cascade="all, delete-orphan",
    )
    sentence_type_info = db.relationship(
        "SentenceTypeInfo",
        back_populates="usr",
        lazy=True,
        cascade="all, delete-orphan",
    )
    assignments = db.relationship(
        "Assignment", back_populates="usr", lazy=True, cascade="all, delete-orphan"
    )


class LexicalInfo(db.Model):
    __tablename__ = "lexical_info"

    id = db.Column(db.Integer, primary_key=True)
    usr_id = db.Column(db.Integer, db.ForeignKey("usr.id"), nullable=False)
    concept = db.Column(db.String(100), nullable=False)
    index = db.Column(db.Integer, nullable=False)
    semantic_category = db.Column(db.String(100))
    morpho_semantic = db.Column(db.String(100))
    speakers_view = db.Column(db.String(100))

    # Relationships
    usr = db.relationship("USR", back_populates="lexical_info")


class DependencyInfo(db.Model):
    __tablename__ = "dependency_info"

    id = db.Column(db.Integer, primary_key=True)
    usr_id = db.Column(db.Integer, db.ForeignKey("usr.id"), nullable=False)
    concept = db.Column(db.String(100), nullable=False)
    index = db.Column(db.Integer, nullable=False)
    head_index = db.Column(db.String(20))  # Changed from Integer
    relation = db.Column(db.String(100), nullable=False)

    # Relationships
    usr = db.relationship("USR", back_populates="dependency_info")


class DiscourseCorefInfo(db.Model):
    __tablename__ = "discourse_coref_info"

    id = db.Column(db.Integer, primary_key=True)
    usr_id = db.Column(db.Integer, db.ForeignKey("usr.id"), nullable=False)
    concept = db.Column(db.String(100), nullable=False)
    index = db.Column(db.Integer, nullable=False)
    head_index = db.Column(db.String(20))  # Changed from Integer
    relation = db.Column(db.String(100), nullable=False)

    # Relationships
    usr = db.relationship("USR", back_populates="discourse_coref_info")


class ConstructionInfo(db.Model):
    __tablename__ = "construction_info"

    id = db.Column(db.Integer, primary_key=True)
    usr_id = db.Column(db.Integer, db.ForeignKey("usr.id"), nullable=False)
    concept = db.Column(db.String(100), nullable=False)
    index = db.Column(db.Integer, nullable=False)
    cxn_index = db.Column(db.String(20))  # Changed from Integer
    component_type = db.Column(db.String(100), nullable=False)

    # Relationships
    usr = db.relationship("USR", back_populates="construction_info")


class SentenceTypeInfo(db.Model):
    __tablename__ = "sentence_type_info"

    id = db.Column(db.Integer, primary_key=True)
    usr_id = db.Column(db.Integer, db.ForeignKey("usr.id"), nullable=False)
    sentence_type = db.Column(db.String(100), nullable=False)
    scope = db.Column(db.String(100))

    # Relationships
    usr = db.relationship("USR", back_populates="sentence_type_info")


class Assignment(db.Model):
    __tablename__ = "assignment"

    id = db.Column(db.Integer, primary_key=True)
    usr_id = db.Column(db.Integer, db.ForeignKey("usr.id"))
    segment_id = db.Column(db.Integer, db.ForeignKey("segment.id"))
    annotator_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    reviewer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    annotation_status = db.Column(db.String(50), default="Unassigned")
    assign_lexical = db.Column(db.Boolean, default=False)
    assign_construction = db.Column(db.Boolean, default=False)
    assign_dependency = db.Column(db.Boolean, default=False)
    assign_discourse = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )
    # Relationships
    usr = db.relationship("USR", back_populates="assignments")
    segment = db.relationship("Segment", back_populates="assignments")
    annotator = db.relationship(
        "User", foreign_keys=[annotator_id], back_populates="annotator_assignments"
    )
    reviewer = db.relationship(
        "User", foreign_keys=[reviewer_id], back_populates="reviewer_assignments"
    )


class Concept(db.Model):
    __tablename__ = "concept"

    id = db.Column(db.Integer, primary_key=True)
    concept_label = db.Column(db.String(200), nullable=False, unique=True)
    hindi_label = db.Column(db.String(200))
    sanskrit_label = db.Column(db.String(200))
    english_label = db.Column(db.String(200))
    mrsc = db.Column(db.String(200))


class Interface(db.Model):
    __tablename__ = "interface"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    slug = db.Column(db.String(180), nullable=False, unique=True)
    description = db.Column(db.Text)
    version = db.Column(db.String(50), default="1.0.0")
    status = db.Column(db.String(40), default="active")
    category = db.Column(db.String(100))
    visibility = db.Column(db.String(40), default="internal")
    documentation_url = db.Column(db.String(255))
    repo_url = db.Column(db.String(255))
    contact_email = db.Column(db.String(150))
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    tags = db.Column(db.JSON, default=list)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    endpoints = db.relationship(
        "InterfaceEndpoint",
        back_populates="interface",
        lazy=True,
        cascade="all, delete-orphan",
    )
    changelog = db.relationship(
        "InterfaceChangeLog",
        back_populates="interface",
        lazy=True,
        cascade="all, delete-orphan",
        order_by="InterfaceChangeLog.created_at.desc()",
    )


class InterfaceEndpoint(db.Model):
    __tablename__ = "interface_endpoint"

    id = db.Column(db.Integer, primary_key=True)
    interface_id = db.Column(db.Integer, db.ForeignKey("interface.id"), nullable=False)
    method = db.Column(db.String(10), nullable=False)
    path = db.Column(db.String(255), nullable=False)
    summary = db.Column(db.String(255))
    description = db.Column(db.Text)
    auth_required = db.Column(db.Boolean, default=True)
    rate_limit_per_minute = db.Column(db.Integer)
    deprecated = db.Column(db.Boolean, default=False)
    version_added = db.Column(db.String(50))
    version_removed = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    interface = db.relationship("Interface", back_populates="endpoints")
    parameters = db.relationship(
        "EndpointParameter",
        back_populates="endpoint",
        lazy=True,
        cascade="all, delete-orphan",
    )
    responses = db.relationship(
        "EndpointResponse",
        back_populates="endpoint",
        lazy=True,
        cascade="all, delete-orphan",
    )


class EndpointParameter(db.Model):
    __tablename__ = "endpoint_parameter"

    id = db.Column(db.Integer, primary_key=True)
    endpoint_id = db.Column(
        db.Integer, db.ForeignKey("interface_endpoint.id"), nullable=False
    )
    name = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(20), nullable=False)  # path, query, header, body
    type = db.Column(db.String(50), nullable=False)
    required = db.Column(db.Boolean, default=False)
    default_value = db.Column(db.Text)
    description = db.Column(db.Text)
    example = db.Column(db.Text)

    endpoint = db.relationship("InterfaceEndpoint", back_populates="parameters")


class EndpointResponse(db.Model):
    __tablename__ = "endpoint_response"

    id = db.Column(db.Integer, primary_key=True)
    endpoint_id = db.Column(
        db.Integer, db.ForeignKey("interface_endpoint.id"), nullable=False
    )
    http_status = db.Column(db.Integer, nullable=False)
    content_type = db.Column(db.String(100), default="application/json")
    schema = db.Column(db.JSON)
    example = db.Column(db.Text)

    endpoint = db.relationship("InterfaceEndpoint", back_populates="responses")


class InterfaceChangeLog(db.Model):
    __tablename__ = "interface_change_log"

    id = db.Column(db.Integer, primary_key=True)
    interface_id = db.Column(db.Integer, db.ForeignKey("interface.id"), nullable=False)
    version = db.Column(db.String(50), nullable=False)
    change_type = db.Column(
        db.String(30),
        nullable=False,
    )  # added, changed, deprecated, removed, fixed, security
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    interface = db.relationship("Interface", back_populates="changelog")
