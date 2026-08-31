import React, { useState } from "react";
import { Header } from "@/components/Header";
import { toast } from "sonner";
import { Stethoscope, FileText } from "lucide-react";

// Previous-year NEET / AIPMT papers, grouped year-wise.
const PAPERS = [
  { year: 2026, items: [
    { name: "RE-NEET 2026", date: "21st June 2026 at 2:00 PM" },
    { name: "NEET 2026", date: "3rd May 2026 at 2:00 PM" },
  ] },
  { year: 2025, items: [
    { name: "NEET 2025", date: "4th May 2025 at 2:00 PM" },
  ] },
  { year: 2024, items: [
    { name: "NEET 2024 (Re-Examination)", date: "24th June 2024 at 2:00 PM" },
    { name: "NEET 2024", date: "5th May 2024 at 2:00 PM" },
  ] },
  { year: 2023, items: [
    { name: "NEET 2023 Manipur", date: "6th June 2023 at 10:00 AM" },
    { name: "NEET 2023", date: "7th May 2023 at 10:00 AM" },
  ] },
  { year: 2022, items: [
    { name: "NEET 2022 Phase 2", date: "4th September 2022 at 10:00 AM" },
    { name: "NEET 2022 Phase 1", date: "17th July 2022 at 10:00 AM" },
  ] },
  { year: 2021, items: [
    { name: "NEET 2021", date: "12th September 2021 at 2:00 PM" },
  ] },
  { year: 2020, items: [
    { name: "NEET 2020 Phase 1", date: "13th September 2020 at 2:00 PM" },
  ] },
  { year: 2019, items: [
    { name: "NEET 2019", date: "5th May 2019 at 2:00 PM" },
  ] },
  { year: 2018, items: [
    { name: "NEET 2018", date: "6th May 2018 at 10:00 AM" },
  ] },
  { year: 2017, items: [
    { name: "NEET 2017", date: "7th May 2017 at 10:00 AM" },
  ] },
  { year: 2016, items: [
    { name: "NEET 2016 Phase 2", date: "24th July 2016 at 10:00 AM" },
    { name: "NEET 2016 Phase 1", date: "1st May 2016 at 10:00 AM" },
  ] },
  { year: 2015, items: [
    { name: "AIPMT 2015", date: "25th July 2015 at 10:00 AM" },
    { name: "AIPMT 2015 Cancelled Paper", date: "3rd May 2015 at 10:00 AM" },
  ] },
  { year: 2014, items: [
    { name: "AIPMT 2014", date: "4th May 2014 at 10:00 AM" },
  ] },
  { year: 2013, items: [
    { name: "NEET 2013 (Karnataka)", date: "18th May 2013 at 10:00 AM" },
    { name: "NEET 2013", date: "5th May 2013 at 10:00 AM" },
  ] },
];

export default function NeetPapers() {
  const [activeYear, setActiveYear] = useState("all");
  const soon = () => toast("Coming soon", { description: "Papers will be added shortly." });

  const groups = activeYear === "all" ? PAPERS : PAPERS.filter((g) => g.year === activeYear);

  return (
    <div className="min-h-screen bg-[#F8FAFC]">
      <Header showBack title="NEET" Icon={Stethoscope} bgClass="bg-rose-600" />

      <main className="mx-auto max-w-2xl px-4 py-6 md:px-6">
        <h1 className="mb-4 text-lg font-extrabold tracking-tight text-slate-900">Previous Year Question Papers</h1>

        {/* Year filter chips */}
        <div className="mb-5 flex gap-2 overflow-x-auto pb-2">
          <button
            data-testid="year-chip-all"
            onClick={() => setActiveYear("all")}
            className={`shrink-0 rounded-full px-4 py-1.5 text-sm font-bold transition-all ${
              activeYear === "all" ? "bg-rose-600 text-white" : "border border-slate-200 bg-white text-slate-600"
            }`}
          >
            All Years
          </button>
          {PAPERS.map((g) => (
            <button
              key={g.year}
              data-testid={`year-chip-${g.year}`}
              onClick={() => setActiveYear(g.year)}
              className={`shrink-0 rounded-full px-4 py-1.5 text-sm font-bold transition-all ${
                activeYear === g.year ? "bg-rose-600 text-white" : "border border-slate-200 bg-white text-slate-600"
              }`}
            >
              {g.year}
            </button>
          ))}
        </div>

        {/* Year-wise groups */}
        <div className="space-y-6">
          {groups.map((g) => (
            <section key={g.year} data-testid={`year-group-${g.year}`}>
              <h2 className="mb-2.5 text-sm font-extrabold text-slate-500">{g.year}</h2>
              <div className="space-y-3">
                {g.items.map((p, i) => (
                  <div
                    key={i}
                    data-testid={`paper-${g.year}-${i}`}
                    className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm"
                  >
                    <div className="flex items-start gap-3">
                      <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-rose-50 text-rose-600">
                        <FileText className="h-4 w-4" />
                      </span>
                      <div className="min-w-0 flex-1">
                        <p className="text-sm font-extrabold text-slate-900">{p.name}</p>
                        <p className="text-xs text-slate-500">{p.date}</p>
                        <div className="mt-1.5 flex gap-1.5">
                          <span className="rounded-md border border-slate-200 bg-slate-50 px-2 py-0.5 text-[11px] font-semibold text-slate-600">English</span>
                          <span className="rounded-md border border-slate-200 bg-slate-50 px-2 py-0.5 text-[11px] font-semibold text-slate-600">हिन्दी</span>
                        </div>
                      </div>
                    </div>
                    <div className="mt-3 flex gap-2">
                      <button
                        onClick={soon}
                        className="flex-1 rounded-lg bg-rose-600 py-2 text-sm font-bold text-white transition-all hover:bg-rose-700"
                      >
                        Take Test
                      </button>
                      <button
                        onClick={soon}
                        className="flex-1 rounded-lg border border-rose-200 bg-rose-50 py-2 text-sm font-bold text-rose-600 transition-all hover:bg-rose-100"
                      >
                        Practice
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </section>
          ))}
        </div>
      </main>
    </div>
  );
}
