import React from "react";
import { useParams } from "react-router-dom";
import { Header } from "@/components/Header";
import { EXAM_CHAPTERS, SUBJECT_META } from "@/lib/examChapters";
import { Atom } from "lucide-react";

const CLASSES = [
  { key: "11", label: "1st PUC", sub: "Class 11" },
  { key: "12", label: "2nd PUC", sub: "Class 12" },
];

export default function ExamChapters() {
  const { subjectId } = useParams();
  const meta = SUBJECT_META[subjectId] || { name: "Subject", Icon: Atom, bg: "bg-slate-700" };
  const Icon = meta.Icon;
  const data = EXAM_CHAPTERS[subjectId] || {};

  return (
    <div className="min-h-screen bg-[#F8FAFC]">
      <Header showBack title={meta.name} Icon={Icon} bgClass={meta.bg} />

      <main className="mx-auto max-w-2xl space-y-8 px-4 py-8 md:px-6">
        {CLASSES.map((cls) => {
          const chapters = data[cls.key] || [];
          if (!chapters.length) return null;
          return (
            <section key={cls.key} data-testid={`class-section-${cls.key}`}>
              <div className="mb-3 flex items-center gap-2">
                <span className={`rounded-lg px-2.5 py-1 text-xs font-extrabold text-white ${meta.bg}`}>
                  {cls.label}
                </span>
                <span className="text-sm font-semibold text-slate-500">{cls.sub}</span>
                <span className="ml-auto text-xs font-medium text-slate-400">{chapters.length} chapters</span>
              </div>

              <div className="space-y-2.5">
                {chapters.map((name, i) => (
                  <div
                    key={`${cls.key}-${i}`}
                    data-testid={`chapter-${cls.key}-${i + 1}`}
                    className="flex items-center gap-3 rounded-xl border border-slate-200 bg-white px-4 py-3 shadow-sm transition-all hover:-translate-y-0.5 hover:shadow-md"
                  >
                    <span className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-lg text-sm font-extrabold text-white ${meta.bg}`}>
                      {i + 1}
                    </span>
                    <span className="text-sm font-semibold text-slate-900">{name}</span>
                  </div>
                ))}
              </div>
            </section>
          );
        })}
      </main>
    </div>
  );
}
