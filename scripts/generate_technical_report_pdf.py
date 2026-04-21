from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import textwrap

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "technical_report_final.pdf"
FIG_DIR = ROOT / "docs" / "figures"


def draw_text_page(pdf, title, body_lines, footer):
    fig = plt.figure(figsize=(8.27, 11.69))  # A4 portrait
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")

    ax.text(0.06, 0.96, title, fontsize=16, fontweight="bold", va="top")
    y = 0.92
    for line in body_lines:
        if line.startswith("## "):
            y -= 0.012
            ax.text(0.06, y, line[3:], fontsize=12.5, fontweight="bold", va="top")
            y -= 0.028
            continue
        if line.startswith("- "):
            wrapped = textwrap.wrap(line[2:], width=96)
            if wrapped:
                ax.text(0.08, y, f"- {wrapped[0]}", fontsize=10.2, va="top")
                y -= 0.018
                for w in wrapped[1:]:
                    ax.text(0.10, y, w, fontsize=10.2, va="top")
                    y -= 0.018
            else:
                y -= 0.018
            continue
        wrapped = textwrap.wrap(line, width=100)
        if not wrapped:
            y -= 0.014
            continue
        for w in wrapped:
            ax.text(0.06, y, w, fontsize=10.2, va="top")
            y -= 0.018

    ax.text(0.06, 0.03, footer, fontsize=9, color="#555")
    pdf.savefig(fig)
    plt.close(fig)


def draw_image_page(pdf, title, top_img, top_cap, bottom_img, bottom_cap, footer):
    fig = plt.figure(figsize=(8.27, 11.69))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")

    ax.text(0.06, 0.96, title, fontsize=16, fontweight="bold", va="top")

    img1 = plt.imread(top_img)
    img2 = plt.imread(bottom_img)

    ax1 = fig.add_axes([0.08, 0.57, 0.84, 0.30])
    ax1.imshow(img1)
    ax1.axis("off")
    ax.text(0.08, 0.54, top_cap, fontsize=10)

    ax2 = fig.add_axes([0.08, 0.16, 0.84, 0.30])
    ax2.imshow(img2)
    ax2.axis("off")
    ax.text(0.08, 0.13, bottom_cap, fontsize=10)

    ax.text(0.06, 0.03, footer, fontsize=9, color="#555")
    pdf.savefig(fig)
    plt.close(fig)


with PdfPages(OUT) as pdf:
    page1 = [
        "Module: XJCO3011 Web Services and Web Data",
        "Assessment: Coursework 1 (Individual API Development Project)",
        "Repository: https://github.com/Yuk11119/Web_Services_cw1",
        "API documentation: docs/api_documentation.pdf",
        "Presentation link: TBD_SLIDES_LINK (to be replaced in Step 3)",
        "",
        "## 1. Project Overview",
        "This project delivers a data-driven RESTful API for book metadata, authors, reviews, and analytics.",
        "It satisfies required CRUD behavior, SQL-backed persistence, endpoint documentation, and demonstration readiness.",
        "",
        "## 2. Stack Justification",
        "- FastAPI for rapid endpoint delivery, validation, and OpenAPI generation.",
        "- SQLAlchemy + relational schema constraints for structured data integrity.",
        "- Alembic for versioned, reproducible migration workflow.",
        "- JWT authentication for protected resources and standard API security.",
        "- Pytest integration tests for evidence-backed functional verification.",
        "",
        "## 3. Architecture and Design Decisions",
        "The backend uses router/service/repository/model layering to separate HTTP contracts, business logic, and persistence.",
        "Core entities are users, authors, books, and reviews, with unique ISBN, FK constraints, and rating bounds.",
    ]
    draw_text_page(pdf, "Technical Report: Book Metadata and Recommendation Analytics API", page1, "Page 1/5")

    draw_image_page(
        pdf,
        "Architecture and Data Model Visuals",
        FIG_DIR / "architecture.png",
        "Figure 1. Layered API architecture (router -> service -> repository -> database).",
        FIG_DIR / "er_diagram.png",
        "Figure 2. Entity-relationship model for users/authors/books/reviews.",
        "Page 2/5",
    )

    page3 = [
        "## 4. Implementation Highlights",
        "- Authentication: /auth/register, /auth/login",
        "- Authors CRUD: /authors",
        "- Books CRUD + filters (genre/year/author_id): /books",
        "- Reviews CRUD + filters (book_id/user_id/rating): /reviews",
        "- Analytics: /analytics/genre-trends, /analytics/rating-distribution, /analytics/recommendations/{user_id}",
        "",
        "Responses follow consistent envelopes:",
        "- success: { data: ..., meta: ... }",
        "- error: { error_code: ..., message: ..., details: ... }",
        "",
        "## 5. Testing Strategy and Evidence",
        "Integration-focused testing was implemented for auth, protected access, CRUD flow, conflict/validation, and analytics behavior.",
        "Latest execution evidence:",
        "- pytest -q -> 6 passed",
        "",
        "## 6. Challenges and Lessons Learned",
        "- Uniform error-contract handling across multiple routers.",
        "- SQL compatibility for aggregation/recommendation queries.",
        "- Maintaining modular architecture while preserving practical testability.",
        "",
        "Lessons: strict layering and early integration tests reduced downstream debugging and contract drift.",
    ]
    draw_text_page(pdf, "Implementation and Validation", page3, "Page 3/5")

    draw_image_page(
        pdf,
        "Runtime Flow and Test Evidence Visuals",
        FIG_DIR / "sequence.png",
        "Figure 3. Core request sequence from login to protected CRUD and analytics.",
        FIG_DIR / "test_coverage.png",
        "Figure 4. Integration evidence snapshot (pytest: 6 passed).",
        "Page 4/5",
    )

    page5 = [
        "## 7. Limitations and Future Work",
        "- Recommendation logic is heuristic and can be extended with collaborative/personalized methods.",
        "- External dataset ingestion pipeline is not yet productionized.",
        "- Advanced production controls (rate limiting, audit logging, token rotation) remain future work.",
        "",
        "## 8. Dataset and Licensing",
        "Current implementation uses small seeded demonstration data (scripts/seed_data.py).",
        "Planned extension datasets: Open Library, Google Books metadata, or Kaggle sources subject to license checks.",
        "Final submission must document exact dataset source URLs and terms.",
        "",
        "## 9. GenAI Declaration and Reflection",
        "Declared GenAI use included planning support, debugging assistance, and documentation drafting.",
        "Human verification was applied through manual review, local execution, and test confirmation before acceptance.",
        "",
        "Integrity statement:",
        "- AI outputs were treated as proposals, not authoritative final answers.",
        "- Final engineering decisions and submission responsibility remained with the student.",
        "- Report claims were restricted to implemented behavior in the repository.",
        "",
        "Supporting appendix and logs:",
        "- docs/genai_declaration_appendix.md",
        "- docs/genai_logs/ (including test evidence text file)",
    ]
    draw_text_page(pdf, "Limitations, Licensing, and GenAI Declaration", page5, "Page 5/5")

print(f"Generated {OUT} (5 pages)")
