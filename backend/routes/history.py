from flask import Blueprint, render_template, redirect, url_for, flash, render_template_string
from flask_login import login_required, current_user
from datetime import datetime
from backend.models.models import Document

bp = Blueprint("history", __name__)


def _owns(doc: Document) -> bool:
    return (current_user.role == "admin") or (current_user.id == doc.uploader_id)


# 📜 LIST DOCUMENTS (Admin: all, User: own)
@bp.route("/history", methods=["GET"])
@login_required
def list():
    if current_user.role == "admin":
        docs = Document.query.order_by(Document.upload_date.desc()).all()
    else:
        docs = (
            Document.query
            .filter_by(uploader_id=current_user.id)
            .order_by(Document.upload_date.desc())
            .all()
        )

    return render_template("history_list.html", docs=docs)


# 📜 VERSION HISTORY
@bp.route("/history/<int:doc_id>", methods=["GET"])
@login_required
def show(doc_id):
    doc = Document.query.get_or_404(doc_id)

    if not _owns(doc):
        flash("Permission denied!", "danger")
        return redirect(url_for("history.list"))

    # Base and extension
    base, ext = (doc.filename.rsplit(".", 1) + [""])[:2]

    versions = (
        Document.query
        .filter(Document.filename.like(f"{base}%." + ext))
        .order_by(Document.version.desc())
        .all()
    )

    tmpl = """
    {% extends 'base.html' %}
    {% block title %}Version History · SmartDMS{% endblock %}
    {% block content %}
    <div class="container" style="max-width:900px;">
      <div class="card shadow-sm p-4">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <h5 class="fw-bold">Version History — {{ title }}</h5>
          <a href="{{ url_for('history.list') }}" class="btn btn-outline-secondary btn-sm">
            <i class="bi bi-arrow-left"></i> Back
          </a>
        </div>

        <div class="table-responsive">
          <table class="table align-middle">
            <thead>
              <tr>
                <th>Version</th>
                <th>Filename</th>
                <th>Uploaded</th>
                <th class="text-end">Actions</th>
              </tr>
            </thead>
            <tbody>
              {% for v in versions %}
              <tr>
                <td class="fw-semibold">v{{ v.version }}</td>
                <td>{{ v.filename }}</td>
                <td>
                  {% if v.upload_date %}
                    {{ v.upload_date.strftime('%d %b %Y %H:%M') }}
                  {% else %}
                    -
                  {% endif %}
                </td>
                <td class="text-end">
                  <a href="{{ url_for('documents.download', doc_id=v.id) }}" class="btn btn-sm btn-outline-success">
                    <i class="bi bi-download"></i>
                  </a>
                  <a href="{{ url_for('documents.preview', doc_id=v.id) }}" class="btn btn-sm btn-outline-primary">
                    <i class="bi bi-eye"></i>
                  </a>
                </td>
              </tr>
              {% else %}
              <tr>
                <td colspan="4" class="text-center text-muted">No versions found.</td>
              </tr>
              {% endfor %}
            </tbody>
          </table>
        </div>
      </div>
    </div>
    {% endblock %}
    """

    return render_template_string(tmpl, title=doc.title, versions=versions)
