"use client";
import { useState } from "react";
import { evaluateController, ControlInputs, ApiResponse } from "./lib/api";

export default function HomePage() {
  // form state for each field
  const [b0, setB0] = useState("1");
  const [den0, setDen0] = useState("1");
  const [den1, setDen1] = useState("1");
  const [tau, setTau] = useState("0");
  const [phaseMargin, setPhaseMargin] = useState("45");
  const [tsMin, setTsMin] = useState("0.1");
  const [tsMax, setTsMax] = useState("5");
  const [ess, setEss] = useState("0.01");
  const [scenario, setScenario] = useState("fast");

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ApiResponse | null>(null);
  const [error, setError] = useState<string|null>(null);

  const submitDisabled =
    !b0 || !den0 || !den1 || !phaseMargin || !tsMin || !tsMax || !ess ||
    Number(tsMin) < 0 ||
    Number(tsMax) < Number(tsMin);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    const inputs: ControlInputs = {
      num: [parseFloat(b0)],
      den: [parseFloat(den0), parseFloat(den1)],
      tau: parseFloat(tau) || undefined,
      phase_margin_min: parseFloat(phaseMargin),
      settling_time_min: parseFloat(tsMin),
      settling_time_max: parseFloat(tsMax),
      steadystate_error_max: parseFloat(ess),
      scenario,
    };

    try {
      const resp = await evaluateController(inputs);
      setResult(resp);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'An unknown error occurred');
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="max-w-xl mx-auto p-6 space-y-6">
      <h1 className="text-2xl font-bold">ControlAgent Designer</h1>
      <form onSubmit={onSubmit} className="space-y-4">
        <div>
          <label>Numerator b₀:</label>
          <input
            type="number" step="any"
            value={b0}
            onChange={e => setB0(e.target.value)}
            className="block w-full rounded p-2 border"
          />
        </div>
        <div>
          <label>Denominator a₀:</label>
          <input
            type="number" step="any"
            value={den0}
            onChange={e => setDen0(e.target.value)}
            className="block w-full rounded p-2 border"
          />
        </div>
        <div>
          <label>Denominator a₁:</label>
          <input
            type="number" step="any"
            value={den1}
            onChange={e => setDen1(e.target.value)}
            className="block w-full rounded p-2 border"
          />
        </div>
        <div>
          <label>Time Delay τ (optional):</label>
          <input
            type="number" step="any"
            value={tau}
            onChange={e => setTau(e.target.value)}
            className="block w-full rounded p-2 border"
          />
        </div>
        <div>
          <label>Phase Margin ≥ (deg):</label>
          <input
            type="number" step="any"
            value={phaseMargin}
            onChange={e => setPhaseMargin(e.target.value)}
            className="block w-full rounded p-2 border"
          />
        </div>
        <div>
          <label>Settling Time Min (s):</label>
          <input
            type="number" step="any"
            value={tsMin}
            onChange={e => setTsMin(e.target.value)}
            className="block w-full rounded p-2 border"
          />
        </div>
        <div>
          <label>Settling Time Max (s):</label>
          <input
            type="number" step="any"
            value={tsMax}
            onChange={e => setTsMax(e.target.value)}
            className="block w-full rounded p-2 border"
          />
        </div>
        <div>
          <label>Steady-State Error ≤ :</label>
          <input
            type="number" step="any"
            value={ess}
            onChange={e => setEss(e.target.value)}
            className="block w-full rounded p-2 border"
          />
        </div>
        <div>
          <label>Scenario Tag:</label>
          <input
            type="text"
            value={scenario}
            onChange={e => setScenario(e.target.value)}
            className="block w-full rounded p-2 border"
          />
        </div>
        <button
          type="submit"
          disabled={submitDisabled || loading}
          className={`w-full p-2 rounded ${
            submitDisabled ? "bg-gray-300" : "bg-indigo-600 text-white"
          }`}
        >
          {loading ? "Running…" : "Start Design"}
        </button>
      </form>

      {error && (
        <div className="mt-4 p-4 bg-red-50 dark:bg-red-900/50 text-red-600 dark:text-red-300 rounded-lg">
          {error}
        </div>
      )}

      {result && (
        <div className="mt-6 p-4 bg-gray-100 rounded">
          <h2 className="font-bold text-lg">Result:</h2>
          <pre className="whitespace-pre-wrap text-sm">{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </main>
  );
}