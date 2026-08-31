// Chapter -> exam question-type (main) mapping, mirrored from the pattern pages.
// Used by the Chapter Detail page to show which "mains" a chapter appears in.

export const PHYSICS_CHAPTERS = {
  "2m": ["Electric Charges & Fields", "Electrostatic Potential & Capacitance", "Current Electricity", "Moving Charges & Magnetism", "Electromagnetic Induction", "Electromagnetic Waves", "Atoms", "Semiconductor Electronics"],
  "3m": ["Electric Charges & Fields", "Electrostatic Potential & Capacitance", "Moving Charges & Magnetism", "Magnetism & Matter", "Electromagnetic Induction", "Ray Optics and Optical Instruments", "Dual Nature of Radiation", "Nuclei"],
  "5m": ["Electric Charges & Fields", "Electrostatic Potential & Capacitance", "Current Electricity", "Moving Charges & Magnetism", "Ray Optics", "Wave Optics", "Semiconductor Electronics"],
  "numeric": ["Electric Charges & Fields", "Electrostatic Potential & Capacitance", "Current Electricity", "Alternating Current", "Ray Optics", "Wave Optics"],
};

export const CHEMISTRY_CHAPTERS = {
  "2m": ["Chemical Kinetics", "d & f Block Elements", "Haloalkanes & Haloarenes", "Alcohols, Phenols & Ethers", "Biomolecules"],
  "3m-inorg": ["d & f Block Elements", "Coordination Compounds"],
  "3m-phys": ["Solutions", "Electrochemistry", "Chemical Kinetics"],
  "5m-org": ["Haloalkanes & Haloarenes", "Alcohols, Phenols & Ethers", "Aldehydes, Ketones & Carboxylic Acids", "Amines", "Biomolecules"],
  "numeric": ["Solutions", "Electrochemistry", "Chemical Kinetics"],
};

export const MATH_CHAPTERS = {
  "2m": ["Inverse Trigonometric Functions", "Determinants", "Continuity & Differentiability", "Application of Derivatives", "Integrals", "Differential Equations", "Vector Algebra", "Three Dimensional Geometry", "Probability"],
  "3m": ["Relations and Functions", "Inverse Trigonometric Functions", "Matrices", "Continuity & Differentiability", "Application of Derivatives", "Integrals", "Vector Algebra", "Three Dimensional Geometry", "Probability"],
  "5m": ["Relations and Functions", "Matrices", "Determinants", "Continuity & Differentiability", "Integrals", "Application of Integrals", "Differential Equations"],
  // Part VI (6+4M) with per-chapter marks
  "6p4m": [
    { name: "Linear Programming", mark: 6 },
    { name: "Integrals", mark: 6 },
    { name: "Determinants", mark: 4 },
    { name: "Continuity & Differentiability", mark: 4 },
  ],
};

const MAPS = { physics: PHYSICS_CHAPTERS, chemistry: CHEMISTRY_CHAPTERS, math: MATH_CHAPTERS };

const norm = (s) => (s || "").toLowerCase().replace(/&/g, "and").replace(/[^a-z0-9]/g, "");

function nameMatches(a, b) {
  const na = norm(a);
  const nb = norm(b);
  return na === nb || na.includes(nb) || nb.includes(na);
}

// Returns [{ type, mark? }] — the distinct question types a chapter appears in.
export function chapterSections(subjectId, chapterName) {
  const lists = MAPS[subjectId];
  if (!lists || !chapterName) return [];
  const out = [];
  for (const [type, items] of Object.entries(lists)) {
    const found = items.find((it) =>
      typeof it === "string" ? nameMatches(it, chapterName) : nameMatches(it.name, chapterName)
    );
    if (found) out.push({ type, mark: typeof found === "object" ? found.mark : undefined });
  }
  return out;
}
