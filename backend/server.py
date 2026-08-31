from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.responses import Response
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime, timezone


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

app = FastAPI()
api_router = APIRouter(prefix="/api")

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# ---------------- Models ----------------
class Question(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    subject: str
    pattern: str  # mcq | fbk | 2m | 3m | 5m | numeric
    chapter: str
    difficulty: str = "Understanding"  # Knowledge | Understanding | Application | HOTS
    marks: int = 1
    question: str
    options: List[str] = []            # for mcq
    answer: str = ""                   # correct option / blank answer / final answer
    solution: str = ""                 # step-by-step / marking scheme
    teacher_note: str = ""
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class QuestionCreate(BaseModel):
    subject: str
    pattern: str
    chapter: str
    difficulty: str = "Understanding"
    marks: int = 1
    question: str
    options: List[str] = []
    answer: str = ""
    solution: str = ""
    teacher_note: str = ""


class QuestionUpdate(BaseModel):
    chapter: Optional[str] = None
    difficulty: Optional[str] = None
    marks: Optional[int] = None
    question: Optional[str] = None
    options: Optional[List[str]] = None
    answer: Optional[str] = None
    solution: Optional[str] = None
    teacher_note: Optional[str] = None


# ---------------- Static config ----------------
SUBJECTS = [
    {"id": "physics", "name": "Physics", "regional": "ಭೌತಶಾಸ್ತ್ರ", "code": "33", "icon": "Atom",
     "accent": "physics", "chapters": 14, "active": True, "readiness": 85, "lab_marks": 30, "coming_soon": False},
    {"id": "chemistry", "name": "Chemistry", "regional": "ರಸಾಯನಶಾಸ್ತ್ರ", "code": "34", "icon": "FlaskConical",
     "accent": "chemistry", "chapters": 10, "active": True, "readiness": 40, "lab_marks": 30, "coming_soon": False},
    {"id": "math", "name": "Mathematics", "regional": "ಗಣಿತ", "code": "35", "icon": "Sigma",
     "accent": "math", "chapters": 13, "active": True, "readiness": 35, "lab_marks": 0, "coming_soon": False},
    {"id": "biology", "name": "Biology", "regional": "ಜೀವಶಾಸ್ತ್ರ", "code": "36", "icon": "Dna",
     "accent": "bio", "chapters": 13, "active": True, "readiness": 30, "lab_marks": 30, "coming_soon": False},
    {"id": "cs", "name": "Computer Science", "regional": "ಗಣಕ ವಿಜ್ಞಾನ", "code": "41", "icon": "Cpu",
     "accent": "cs", "chapters": 14, "active": True, "readiness": 25, "lab_marks": 30, "coming_soon": False},
    {"id": "english", "name": "English", "regional": "ಇಂಗ್ಲಿಷ್", "code": "01", "icon": "BookOpen",
     "accent": "eng", "chapters": 14, "active": True, "readiness": 50, "lab_marks": 0, "coming_soon": False},
    {"id": "kannada", "name": "Kannada", "regional": "ಕನ್ನಡ", "code": "15", "icon": "Languages",
     "accent": "kannada", "chapters": 22, "active": True, "readiness": 45, "lab_marks": 0, "coming_soon": False},
    {"id": "hindi", "name": "Hindi", "regional": "ಹಿಂದಿ", "code": "16", "icon": "Languages",
     "accent": "hindi", "chapters": 32, "active": False, "readiness": 0, "lab_marks": 0, "coming_soon": True},
    {"id": "sanskrit", "name": "Sanskrit", "regional": "ಸಂಸ್ಕೃತ", "code": "17", "icon": "ScrollText",
     "accent": "sanskrit", "chapters": 10, "active": False, "readiness": 0, "lab_marks": 0, "coming_soon": True},
]

# Subject-specific question paper patterns (from Karnataka II PUC question paper pattern).
# `style` maps to the colour group; `type` is a unique key used for routing/react keys.
SUBJECT_PATTERNS = {
    "physics": [
        {"type": "mcq", "style": "mcq", "label": "MCQ", "full": "Multiple Choice", "count": "15 Questions", "num": 15, "each": 1, "total": 15, "equation": "15 × 1 = 15"},
        {"type": "fbk", "style": "fbk", "label": "FBK", "full": "Fill in the Blanks", "count": "5 Questions", "num": 5, "each": 1, "total": 5, "equation": "5 × 1 = 5"},
        {"type": "2m", "style": "2m", "label": "2M", "full": "Short Answer", "count": "5 of 8", "num": 5, "each": 2, "total": 10, "equation": "5 × 2 = 10"},
        {"type": "3m", "style": "3m", "label": "3M", "full": "Medium Answer", "count": "5 of 8", "num": 5, "each": 3, "total": 15, "equation": "5 × 3 = 15"},
        {"type": "5m", "style": "5m", "label": "5M", "full": "Long Answer", "count": "3 of 5", "num": 3, "each": 5, "total": 15, "equation": "3 × 5 = 15"},
        {"type": "numeric", "style": "numeric", "label": "Numeric", "full": "Problems", "count": "2 of 4", "num": 2, "each": 5, "total": 10, "equation": "2 × 5 = 10"},
    ],
    "chemistry": [
        {"type": "mcq", "style": "mcq", "label": "MCQ", "full": "Multiple Choice", "count": "15 Questions", "num": 15, "each": 1, "total": 15, "equation": "15 × 1 = 15"},
        {"type": "fbk", "style": "fbk", "label": "FBK", "full": "Fill in the Blanks", "count": "5 Questions", "num": 5, "each": 1, "total": 5, "equation": "5 × 1 = 5"},
        {"type": "2m", "style": "2m", "label": "2M", "full": "Short Answer", "count": "3 of 5", "num": 3, "each": 2, "total": 6, "equation": "3 × 2 = 6"},
        {"type": "3m-inorg", "style": "3m", "label": "3M", "full": "Inorganic", "count": "3 of 5", "num": 3, "each": 3, "total": 9, "equation": "3 × 3 = 9"},
        {"type": "3m-phys", "style": "3m", "label": "3M", "full": "Physical", "count": "2 of 4", "num": 2, "each": 3, "total": 6, "equation": "2 × 3 = 6"},
        {"type": "5m-org", "style": "5m", "label": "5M", "full": "Organic", "count": "4 of 6", "num": 4, "each": 5, "total": 20, "equation": "4 × 5 = 20"},
        {"type": "numeric", "style": "numeric", "label": "3M", "full": "Problems", "count": "3 of 6", "num": 3, "each": 3, "total": 9, "equation": "3 × 3 = 9"},
    ],
    "math": [
        {"type": "mcq", "style": "mcq", "label": "MCQ", "full": "Multiple Choice", "count": "15 Questions", "num": 15, "each": 1, "total": 15, "equation": "15 × 1 = 15"},
        {"type": "fbk", "style": "fbk", "label": "FBK", "full": "Fill in the Blanks", "count": "5 Questions", "num": 5, "each": 1, "total": 5, "equation": "5 × 1 = 5"},
        {"type": "2m", "style": "2m", "label": "2M", "full": "Short Answer", "count": "6 of 9", "num": 6, "each": 2, "total": 12, "equation": "6 × 2 = 12"},
        {"type": "3m", "style": "3m", "label": "3M", "full": "Medium Answer", "count": "6 of 9", "num": 6, "each": 3, "total": 18, "equation": "6 × 3 = 18"},
        {"type": "5m", "style": "5m", "label": "5M", "full": "Long Answer", "count": "4 of 7", "num": 4, "each": 5, "total": 20, "equation": "4 × 5 = 20"},
        {"type": "6p4m", "style": "numeric", "label": "6+4M", "full": "Long Answer (Part E)", "count": "½ + ½", "num": 1, "each": 10, "total": 10, "equation": "6 + 4 = 10"},
    ],
    "biology": [
        {"type": "mcq", "style": "mcq", "label": "MCQ", "full": "Multiple Choice", "count": "15 Questions", "num": 15, "each": 1, "total": 15, "equation": "15 × 1 = 15"},
        {"type": "fbk", "style": "fbk", "label": "FBK", "full": "Fill in the Blanks", "count": "5 Questions", "num": 5, "each": 1, "total": 5, "equation": "5 × 1 = 5"},
        {"type": "2m", "style": "2m", "label": "2M", "full": "Short Answer", "count": "5 of 7", "num": 5, "each": 2, "total": 10, "equation": "5 × 2 = 10"},
        {"type": "3m", "style": "3m", "label": "3M", "full": "Medium Answer", "count": "5 of 7", "num": 5, "each": 3, "total": 15, "equation": "5 × 3 = 15"},
        {"type": "5m", "style": "5m", "label": "5M", "full": "Long Answer", "count": "4 of 7", "num": 4, "each": 5, "total": 20, "equation": "4 × 5 = 20"},
        {"type": "5m-b", "style": "numeric", "label": "5M", "full": "Long Answer (Part E)", "count": "1 of 3", "num": 1, "each": 5, "total": 5, "equation": "1 × 5 = 5"},
    ],
    "cs": [
        {"type": "mcq", "style": "mcq", "label": "MCQ", "full": "Multiple Choice", "count": "15 Questions", "num": 15, "each": 1, "total": 15, "equation": "15 × 1 = 15"},
        {"type": "fbk", "style": "fbk", "label": "FBK", "full": "Fill in the Blanks", "count": "5 Questions", "num": 5, "each": 1, "total": 5, "equation": "5 × 1 = 5"},
        {"type": "2m", "style": "2m", "label": "2M", "full": "Short Answer", "count": "4 of 7", "num": 4, "each": 2, "total": 8, "equation": "4 × 2 = 8"},
        {"type": "3m", "style": "3m", "label": "3M", "full": "Medium Answer", "count": "4 of 7", "num": 4, "each": 3, "total": 12, "equation": "4 × 3 = 12"},
        {"type": "5m", "style": "5m", "label": "5M", "full": "Long Answer", "count": "4 of 7", "num": 4, "each": 5, "total": 20, "equation": "4 × 5 = 20"},
        {"type": "numeric", "style": "numeric", "label": "5M", "full": "Problems", "count": "2 of 3", "num": 2, "each": 5, "total": 10, "equation": "2 × 5 = 10"},
    ],
    "kannada": [
        {"type": "one", "style": "mcq", "label": "I", "full": "ಅ - ವಿಭಾಗ", "total": 20, "equation": "20 ಅಂಕ",
         "children": [
             {"label": "MCQ", "full": "ಬಹು ಆಯ್ಕೆ", "marks": 10, "equation": "10 × 1 = 10"},
             {"label": "FBK", "full": "ಬಿಟ್ಟ ಸ್ಥಳ", "marks": 5, "equation": "5 × 1 = 5"},
             {"label": "MTF", "full": "ಹೊಂದಿಸಿ", "marks": 5, "equation": "5 × 1 = 5"},
         ]},
        {"type": "two", "style": "fbk", "label": "II", "full": "ಆ - ವಿಭಾಗ (೨-೩ ವಾಕ್ಯ)", "total": 16, "equation": "16 ಅಂಕ",
         "children": [
             {"label": "ಪದ್ಯ", "full": "", "marks": 6},
             {"label": "ಪಾಠ", "full": "", "marks": 4},
             {"label": "ನಾಟಕ", "full": "", "marks": 6},
         ]},
        {"type": "three", "style": "2m", "label": "III", "full": "ಇ - ವಿಭಾಗ (ಸಂದರ್ಭ)", "total": 12, "equation": "12 ಅಂಕ",
         "children": [
             {"label": "ಪದ್ಯ", "full": "", "marks": 6},
             {"label": "ಪಾಠ", "full": "", "marks": 3},
             {"label": "ನಾಟಕ", "full": "", "marks": 3},
         ]},
        {"type": "four", "style": "3m", "label": "IV", "full": "ಈ - ವಿಭಾಗ (5-6 ವಾಕ್ಯ)", "total": 16, "equation": "16 ಅಂಕ",
         "children": [
             {"label": "ಪದ್ಯ", "full": "", "marks": 8},
             {"label": "ಪಾಠ", "full": "", "marks": 4},
             {"label": "ನಾಟಕ", "full": "", "marks": 4},
         ]},
        {"type": "five", "style": "5m", "label": "V", "full": "ಉ - ವಿಭಾಗ (ಭಾಷಾಭ್ಯಾಸ)", "total": 16, "equation": "16 ಅಂಕ",
         "children": [
             {"label": "ವ್ಯಾಕರಣ", "full": "Grammar", "marks": 8},
             {"label": "ಪ್ರಬಂಧ", "full": "Essay", "marks": 4},
             {"label": "ಪತ್ರ", "full": "Letter", "marks": 4},
         ]},
    ],
    "english": [
        {"type": "one", "style": "mcq", "label": "I", "full": "Part A", "total": 20, "equation": "20 marks",
         "children": [
             {"label": "MCQ", "full": "Multiple Choice", "marks": 10, "equation": "10 × 1 = 10"},
             {"label": "FBK", "full": "Verb forms", "marks": 3, "equation": "3 × 1 = 3"},
             {"label": "FBK", "full": "Brackets", "marks": 2, "equation": "2 × 1 = 2"},
             {"label": "MTH", "full": "Match nouns", "marks": 5, "equation": "5 × 1 = 5"},
         ]},
        {"type": "two", "style": "fbk", "label": "II", "full": "Part B · Chapters", "total": 30, "equation": "30 marks",
         "children": [
             {"label": "1–2 Sentence", "full": "", "sub": "Lesson & Poem", "marks": 6},
             {"label": "60 Words", "full": "", "sub": "Lesson & Poem", "marks": 12},
             {"label": "100 Words", "full": "", "sub": "Lesson & Poem", "marks": 12},
         ]},
        {"type": "three", "style": "2m", "label": "III", "full": "Part C · Comprehension", "total": 9, "equation": "9 marks",
         "children": [
             {"label": "Passage", "full": "Prose (unseen)", "marks": 9},
             {"label": "OR · Passage 2", "full": "Poetry — attempt one", "marks": 9},
         ]},
        {"type": "four", "style": "3m", "label": "IV", "full": "Part D · Grammar", "total": 16, "equation": "16 marks",
         "children": [
             {"label": "FBK", "full": "Linkers", "marks": 4},
             {"label": "Rectify Error", "full": "", "marks": 2},
             {"label": "Fill the Box", "full": "", "marks": 2},
             {"label": "Report Conversation", "full": "", "marks": 5},
             {"label": "Complete Dialogue", "full": "", "marks": 3},
         ]},
        {"type": "five", "style": "5m", "label": "V", "full": "Part E · Letter", "total": 5, "equation": "5 marks",
         "children": [
             {"label": "Letter", "full": "Job Application / Speech", "marks": 5},
         ]},
    ],
}

DEFAULT_PATTERNS = [
    {"type": "mcq", "style": "mcq", "label": "MCQ", "full": "Multiple Choice", "count": "15 Questions", "num": 15, "each": 1, "total": 15, "equation": "15 × 1 = 15"},
    {"type": "fbk", "style": "fbk", "label": "FBK", "full": "Fill in the Blanks", "count": "5 Questions", "num": 5, "each": 1, "total": 5, "equation": "5 × 1 = 5"},
    {"type": "2m", "style": "2m", "label": "2M", "full": "Short Answer", "count": "5 of 8", "num": 5, "each": 2, "total": 10, "equation": "5 × 2 = 10"},
    {"type": "3m", "style": "3m", "label": "3M", "full": "Medium Answer", "count": "5 of 8", "num": 5, "each": 3, "total": 15, "equation": "5 × 3 = 15"},
    {"type": "5m", "style": "5m", "label": "5M", "full": "Long Answer", "count": "5 of 8", "num": 5, "each": 5, "total": 25, "equation": "5 × 5 = 25"},
]

# Backwards-compatible default (physics) used by counts endpoint
PATTERNS = SUBJECT_PATTERNS["physics"]

PHYSICS_ANALYTICS = {
    "subject": "physics",
    "total_marks": 100,
    "theory_marks": 70,
    "practical_marks": 30,
    "duration": "3 hours 15 min",
    "total_questions": 40,
    "chapter_weightage": [
        {"chapter": "Electrostatics", "marks": 9},
        {"chapter": "Current Electricity", "marks": 7},
        {"chapter": "Magnetism", "marks": 8},
        {"chapter": "EMI & AC", "marks": 8},
        {"chapter": "EM Waves", "marks": 3},
        {"chapter": "Optics", "marks": 10},
        {"chapter": "Dual Nature", "marks": 4},
        {"chapter": "Atoms & Nuclei", "marks": 8},
        {"chapter": "Semiconductors", "marks": 6},
    ],
    "cognitive": [
        {"level": "Knowledge", "value": 25},
        {"level": "Understanding", "value": 35},
        {"level": "Application", "value": 28},
        {"level": "HOTS", "value": 12},
    ],
    "sections": [
        {"part": "Part A", "detail": "MCQ + FBK", "questions": 20, "marks": 20},
        {"part": "Part B", "detail": "2 Mark Qs", "questions": 8, "marks": 16},
        {"part": "Part C", "detail": "3 Mark Qs", "questions": 8, "marks": 24},
        {"part": "Part D", "detail": "5M + Numeric", "questions": 9, "marks": 40},
    ],
}


def generic_analytics(sub):
    return {
        "subject": sub["id"],
        "total_marks": 100,
        "theory_marks": 80 if sub["id"] in ("math", "cs") else 70,
        "practical_marks": 20 if sub["id"] in ("math", "cs") else 30,
        "duration": "3 hours 15 min",
        "total_questions": 40,
        "chapter_weightage": [
            {"chapter": f"Unit {i+1}", "marks": m}
            for i, m in enumerate([8, 6, 9, 7, 5, 8, 6, 4, 7])
        ],
        "cognitive": [
            {"level": "Knowledge", "value": 30},
            {"level": "Understanding", "value": 35},
            {"level": "Application", "value": 25},
            {"level": "HOTS", "value": 10},
        ],
        "sections": [
            {"part": "Part A", "detail": "MCQ + FBK", "questions": 20, "marks": 20},
            {"part": "Part B", "detail": "2 Mark Qs", "questions": 8, "marks": 16},
            {"part": "Part C", "detail": "3 Mark Qs", "questions": 8, "marks": 24},
            {"part": "Part D", "detail": "5 Mark Qs", "questions": 8, "marks": 40},
        ],
    }


SEED_QUESTIONS = [
    # MCQ
    {"subject": "physics", "pattern": "mcq", "chapter": "Electrostatics", "difficulty": "Understanding", "marks": 1,
     "question": "The SI unit of electric flux is:",
     "options": ["N·m²/C", "C/m²", "V/m", "N/C"], "answer": "N·m²/C",
     "solution": "Electric flux Φ = E·A. Unit = (N/C)·(m²) = N·m²/C. Also expressible as V·m.",
     "teacher_note": "Frequently asked from Gauss's law section."},
    {"subject": "physics", "pattern": "mcq", "chapter": "Current Electricity", "difficulty": "Application", "marks": 1,
     "question": "Two resistors of 4Ω and 6Ω are connected in parallel. The equivalent resistance is:",
     "options": ["2.4 Ω", "10 Ω", "5 Ω", "1.2 Ω"], "answer": "2.4 Ω",
     "solution": "1/R = 1/4 + 1/6 = (3+2)/12 = 5/12 → R = 12/5 = 2.4 Ω.",
     "teacher_note": ""},
    {"subject": "physics", "pattern": "mcq", "chapter": "Optics", "difficulty": "Knowledge", "marks": 1,
     "question": "For total internal reflection, light must travel from:",
     "options": ["Denser to rarer medium", "Rarer to denser medium", "Vacuum to glass", "Any medium to vacuum"],
     "answer": "Denser to rarer medium",
     "solution": "TIR occurs only when light goes from an optically denser to a rarer medium at an angle greater than the critical angle.",
     "teacher_note": ""},
    # FBK
    {"subject": "physics", "pattern": "fbk", "chapter": "Electrostatics", "difficulty": "Knowledge", "marks": 1,
     "question": "The electric field inside a charged conductor in electrostatic equilibrium is ______.",
     "options": [], "answer": "zero",
     "solution": "Charges reside on the surface; net field inside a conductor at equilibrium is zero.",
     "teacher_note": ""},
    {"subject": "physics", "pattern": "fbk", "chapter": "Atoms & Nuclei", "difficulty": "Knowledge", "marks": 1,
     "question": "The value of Rydberg constant is approximately ______ m⁻¹.",
     "options": [], "answer": "1.097 × 10⁷",
     "solution": "R = 1.097 × 10⁷ m⁻¹, used in the hydrogen spectral series formula.",
     "teacher_note": "Remember standard constants."},
    # 2M
    {"subject": "physics", "pattern": "2m", "chapter": "Magnetism", "difficulty": "Understanding", "marks": 2,
     "question": "State and explain Biot–Savart law.",
     "options": [], "answer": "",
     "solution": "The magnetic field dB due to a current element I·dl at distance r is dB = (μ₀/4π)·(I·dl·sinθ)/r². (1 mark statement + 1 mark expression/direction).",
     "teacher_note": "Direction given by right-hand rule."},
    {"subject": "physics", "pattern": "2m", "chapter": "Semiconductors", "difficulty": "Understanding", "marks": 2,
     "question": "Distinguish between intrinsic and extrinsic semiconductors (any two points).",
     "options": [], "answer": "",
     "solution": "Intrinsic: pure, conductivity depends on temperature, equal electrons & holes. Extrinsic: doped, higher conductivity, unequal carriers. (1 mark per valid point).",
     "teacher_note": ""},
    # 3M
    {"subject": "physics", "pattern": "3m", "chapter": "EMI & AC", "difficulty": "Application", "marks": 3,
     "question": "Derive an expression for the motional EMF induced in a conducting rod moving in a uniform magnetic field.",
     "options": [], "answer": "",
     "solution": "Force on charge F = qvB → work per charge = vBl → EMF ε = Blv. Derivation (2 marks) + final expression (1 mark).",
     "teacher_note": "Draw the rod-on-rails diagram."},
    {"subject": "physics", "pattern": "3m", "chapter": "Optics", "difficulty": "Understanding", "marks": 3,
     "question": "Explain the working of a compound microscope with a ray diagram.",
     "options": [], "answer": "",
     "solution": "Objective forms a real, magnified, inverted image; eyepiece acts as a simple microscope to further magnify. Magnification M = mo × me. Ray diagram (1) + working (1) + magnification (1).",
     "teacher_note": ""},
    # 5M
    {"subject": "physics", "pattern": "5m", "chapter": "Electrostatics", "difficulty": "HOTS", "marks": 5,
     "question": "Derive an expression for the electric field due to a uniformly charged infinite plane sheet using Gauss's law.",
     "options": [], "answer": "",
     "solution": "Choose a cylindrical Gaussian surface. Flux = 2EA. Charge enclosed = σA. By Gauss's law 2EA = σA/ε₀ → E = σ/(2ε₀), independent of distance. (Diagram 1 + setup 2 + derivation 2).",
     "teacher_note": "Key repeated 5-mark derivation."},
    {"subject": "physics", "pattern": "5m", "chapter": "Magnetism", "difficulty": "Application", "marks": 5,
     "question": "With a neat diagram, derive the expression for the magnetic field at the centre of a circular current loop.",
     "options": [], "answer": "",
     "solution": "Using Biot–Savart law and integrating around the loop, B = μ₀I/(2R) at the centre. (Diagram 1 + Biot–Savart 1 + integration 2 + result 1).",
     "teacher_note": ""},
    # Numeric
    {"subject": "physics", "pattern": "numeric", "chapter": "Current Electricity", "difficulty": "Application", "marks": 5,
     "question": "A wire of resistance 10Ω carries a current of 2A for 5 minutes. Calculate the heat produced.",
     "options": [], "answer": "12000 J",
     "solution": "H = I²Rt = (2)²×10×(5×60) = 4×10×300 = 12000 J = 12 kJ. Formula (1) + substitution (2) + answer with unit (2).",
     "teacher_note": "Convert time to seconds."},
    {"subject": "physics", "pattern": "numeric", "chapter": "Optics", "difficulty": "Application", "marks": 5,
     "question": "A convex lens of focal length 20 cm forms an image of an object placed 30 cm away. Find the image distance and magnification.",
     "options": [], "answer": "v = 60 cm, m = -2",
     "solution": "1/v - 1/u = 1/f → 1/v = 1/20 - 1/30 = 1/60 → v = 60 cm. m = v/u = 60/(-30) = -2 (real, inverted, magnified). Lens formula (1) + calc (3) + magnification (1).",
     "teacher_note": "Use sign convention carefully."},
]


# ---------------- Routes ----------------
@api_router.get("/")
async def root():
    return {"message": "Karnataka Board Exam Analytics API"}


@api_router.get("/subjects")
async def get_subjects():
    return [{**s, "patterns": SUBJECT_PATTERNS.get(s["id"], DEFAULT_PATTERNS)} for s in SUBJECTS]


@api_router.get("/subjects/{subject_id}")
async def get_subject(subject_id: str):
    sub = next((s for s in SUBJECTS if s["id"] == subject_id), None)
    if not sub:
        raise HTTPException(status_code=404, detail="Subject not found")
    return {**sub, "patterns": SUBJECT_PATTERNS.get(subject_id, DEFAULT_PATTERNS)}


@api_router.get("/subjects/{subject_id}/analytics")
async def get_analytics(subject_id: str):
    sub = next((s for s in SUBJECTS if s["id"] == subject_id), None)
    if not sub:
        raise HTTPException(status_code=404, detail="Subject not found")
    if subject_id == "physics":
        return PHYSICS_ANALYTICS
    return generic_analytics(sub)


@api_router.get("/patterns")
async def get_patterns(subject: str = "physics"):
    return SUBJECT_PATTERNS.get(subject, DEFAULT_PATTERNS)


PAPERS_DIR = ROOT_DIR / "papers"


@api_router.get("/papers/{subject_id}/{paper_id}")
async def get_paper(subject_id: str, paper_id: int):
    path = PAPERS_DIR / subject_id / f"mqp_{paper_id}.pdf"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Paper not found")
    data = path.read_bytes()
    return Response(
        content=data,
        media_type="application/pdf",
        headers={"Content-Disposition": "inline; filename=paper.pdf"},
    )


@api_router.get("/questions")
async def list_questions(subject: str, pattern: Optional[str] = None):
    q = {"subject": subject}
    if pattern:
        q["pattern"] = pattern
    docs = await db.questions.find(q, {"_id": 0}).sort("created_at", 1).to_list(1000)
    return docs


@api_router.get("/questions/counts")
async def question_counts(subject: str):
    counts = {}
    for p in PATTERNS:
        counts[p["type"]] = await db.questions.count_documents({"subject": subject, "pattern": p["type"]})
    return counts


@api_router.post("/questions", response_model=Question)
async def create_question(payload: QuestionCreate):
    obj = Question(**payload.model_dump())
    await db.questions.insert_one(obj.model_dump())
    return obj


@api_router.put("/questions/{question_id}", response_model=Question)
async def update_question(question_id: str, payload: QuestionUpdate):
    existing = await db.questions.find_one({"id": question_id}, {"_id": 0})
    if not existing:
        raise HTTPException(status_code=404, detail="Question not found")
    updates = {k: v for k, v in payload.model_dump().items() if v is not None}
    if updates:
        await db.questions.update_one({"id": question_id}, {"$set": updates})
    doc = await db.questions.find_one({"id": question_id}, {"_id": 0})
    return doc


@api_router.delete("/questions/{question_id}")
async def delete_question(question_id: str):
    res = await db.questions.delete_one({"id": question_id})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Question not found")
    return {"deleted": True}


@app.on_event("startup")
async def seed_data():
    count = await db.questions.count_documents({})
    if count == 0:
        docs = [Question(**q).model_dump() for q in SEED_QUESTIONS]
        await db.questions.insert_many(docs)
        logger.info(f"Seeded {len(docs)} physics questions")


app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
