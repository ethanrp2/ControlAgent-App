'use client';

import React, { useState } from 'react';
import { Tab } from '@headlessui/react';
import { CheckCircleIcon, ExclamationCircleIcon } from '@heroicons/react/24/outline';
import ToolSelector from './components/ToolSelector';
import { evaluateController, ControlInputs, ApiResponse } from "./lib/api";
import Image from 'next/image';


interface Iteration {
  id: number;
  omegaL: number;
  beta: number;
  Ts: number;
  phiM: number;
  ess: number;
  status: string;
}

const iterations: Iteration[] = [
  { id: 1, omegaL: 1.2, beta: 0.5, Ts: 2.3, phiM: 45, ess: 0.01, status: 'fail' },
  { id: 2, omegaL: 1.5, beta: 0.7, Ts: 3.1, phiM: 30, ess: 0.02, status: 'ok' },
];

const metricKeyMap: Record<string, keyof Iteration> = {
  'Ts': 'Ts',
  'φm': 'phiM',
  'ess': 'ess'
};

export default function ControlAgentDesigner() {
  // const [darkMode, setDarkMode] = useState(false);
  const [b0, setB0] = useState("10.645786319352997");
  const [den0, setDen0] = useState("1");
  const [den1, setDen1] = useState("1.5623926006892073");
  const [scenario, setScenario] = useState("fast");

  const [phaseMargin, setPhaseMargin] = useState("48.553825399337036");
  const [tsMin, setTsMin] = useState("0.0011969995294049103");
  const [tsMax, setTsMax] = useState("0.9163742832003272");
  const [ess, setEss] = useState("0.0001");
  const [status] = useState('running');

  const [tau, setTau] = useState("0");

  const tsError = tsMin !== '' && tsMax !== '' && (Number(tsMin) < 0 || Number(tsMax) < 0 || Number(tsMin) > Number(tsMax));
  const formValid = b0 && den0 && den1 && phaseMargin && tsMin && tsMax && ess && !tsError && Number(tsMin) < Number(tsMax) && Number(tsMin) > 0;

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ApiResponse | null>(null);
  const [error, setError] = useState<string|null>(null);

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
  };
  
  return (
    <div className={'dark'}>
      <div className="min-h-screen bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 font-sans">
        <header className="fixed top-0 w-full bg-white dark:bg-gray-800 shadow-md z-20 px-6 py-4 flex justify-between items-center">
          <div className="text-xl font-bold">ControlAgent Designer</div>
          <nav className="flex items-center space-x-6">
            <ToolSelector />
            <a href="#">History</a>
            <a href="#">Docs</a>
            {/* <Switch checked={darkMode} onChange={setDarkMode} className="relative inline-flex h-6 w-11 items-center rounded-full bg-gray-200 dark:bg-gray-600 focus:outline-none">
              <span className="sr-only">Toggle dark mode</span>
              <span className={`${darkMode ? 'translate-x-6' : 'translate-x-1'} inline-block h-4 w-4 transform rounded-full bg-white transition`} />
            </Switch> */}
            <Image
              src="https://i.pravatar.cc/4"
              alt="Profile"
              width={32}
              height={32}
              className="rounded-full border-2 border-gray-200 dark:border-gray-600"
            />
          </nav>
        </header>

        <main className="pt-20 p-6 grid grid-cols-12 gap-6">
          <section className="col-span-4 sticky top-20">
            <form onSubmit={onSubmit} className="bg-white dark:bg-gray-800 shadow-md rounded-2xl p-6">
              <h2 className="text-lg font-semibold mb-4">Task Setup</h2>
              <div className="space-y-4">
                <div className="grid grid-cols-1 gap-4">
                  <div>
                    <label className="block text-sm font-medium">Numerator b₀:</label>
                    <input
                      type="number"
                      step="any"
                      value={b0}
                      onChange={e => setB0(e.target.value)}
                      className="mt-1 block w-full rounded-2xl p-2 border border-gray-200 dark:border-gray-600"
                      placeholder="b₀"
                      required
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium">Denominator a₀:</label>
                      <input
                        type="number"
                        step="any"
                        value={den0}
                        onChange={e => setDen0(e.target.value)}
                        className="mt-1 block w-full rounded-2xl p-2 border border-gray-200 dark:border-gray-600"
                        placeholder="a₀"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium">Denominator a₁:</label>
                      <input
                        type="number"
                        step="any"
                        value={den1}
                        onChange={e => setDen1(e.target.value)}
                        className="mt-1 block w-full rounded-2xl p-2 border border-gray-200 dark:border-gray-600"
                        placeholder="a₁"
                        required
                      />
                    </div>
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium">Phase Margin ≥</label>
                  <div className="relative">
                    <input
                      type="number"
                      className="w-full rounded-2xl pr-10 p-2 border border-gray-200 dark:border-gray-600"
                      placeholder="45"
                      value={phaseMargin}
                      onChange={e => setPhaseMargin(e.target.value)}
                      required
                    />
                    <span className="absolute inset-y-0 right-3 flex items-center">°</span>
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium">Settling Time</label>
                  <div className="flex items-center space-x-2">
                    <input
                      type="number"
                      className="w-full rounded-2xl p-2 border border-gray-200 dark:border-gray-600"
                      placeholder="0.0048"
                      value={tsMin}
                      onChange={e => setTsMin(e.target.value)}
                      required
                    />
                    <div className="text-gray-500">–</div>
                    <input
                      type="number"
                      className="w-full rounded-2xl p-2 border border-gray-200 dark:border-gray-600"
                      placeholder="3.7264"
                      value={tsMax}
                      onChange={e => setTsMax(e.target.value)}
                      required
                    />
                  </div>
                  <p className={tsError ? 'text-red-600 text-xs' : 'text-gray-500 text-xs'}>0.0048 ≤ Ts ≤ 3.7264</p>
                </div>
                <div>
                  <label className="block text-sm font-medium">Steady‑State Error ≤</label>
                  <div className="relative">
                    <input
                      type="number"
                      className="w-full rounded-2xl pr-10 p-2 border border-gray-200 dark:border-gray-600"
                      placeholder="0.01"
                      value={ess}
                      onChange={e => setEss(e.target.value)}
                      required
                    />
                    <span className="absolute inset-y-0 right-3 flex items-center">–</span>
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium">Scenario</label>
                  <select
                    value={scenario}
                    onChange={e => setScenario(e.target.value)}
                    className="mt-1 block w-full rounded-2xl p-2 border border-gray-200 dark:border-gray-600"
                    required
                  >
                    <option value="fast">Fast</option>
                    <option value="slow">Slow</option>
                    <option value="custom">Custom</option>
                  </select>
                </div>
                <button
                  type="submit"
                  disabled={!formValid || loading}
                  className={`w-full py-2 rounded-2xl text-white font-semibold shadow-md transition ${
                    formValid && !loading ? 'bg-indigo-600 hover:bg-indigo-700' : 'bg-gray-300 cursor-not-allowed'
                  }`}
                >
                  {loading ? 'Processing...' : 'Start Design'}
                </button>
              </div>
            </form>
          </section>

          <section className="col-span-8 overflow-y-auto space-y-6">
            <div className="bg-white dark:bg-gray-800 shadow-md rounded-2xl p-6">
              <h2 className="text-lg font-semibold mb-4">Run Dashboard</h2>
              <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-lg h-3 mb-4">
                <div className="bg-indigo-600 h-3 rounded-lg w-1/3 transition-width duration-300" />
              </div>
              <div className="space-y-4">
                {iterations.map(iter => (
                  <div key={iter.id} className="bg-white dark:bg-gray-700 shadow-md rounded-xl p-4 animate-slide-in">
                    <div className="flex items-center justify-between mb-2">
                      <span className="bg-indigo-600 text-white text-sm px-2 py-1 rounded-full">Iter {iter.id}</span>
                    </div>
                    <div className="grid grid-cols-2 gap-4 text-sm mb-2">
                      <div>ω<sub>L</sub>: {iter.omegaL}</div>
                      <div>β: {iter.beta}</div>
                    </div>
                    <div className="flex space-x-2">
                      {['Ts', 'φm', 'ess'].map(key => (
                        <span key={key} className="flex items-center space-x-1 px-2 py-1 rounded-full text-xs font-medium bg-gray-100 dark:bg-gray-600">
                          {iter.status === 'ok' ? <CheckCircleIcon className="w-4 h-4 text-green-500" /> : <ExclamationCircleIcon className="w-4 h-4 text-red-500" />}
                          <span>{key}: {iter[metricKeyMap[key]]}</span>
                        </span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-white dark:bg-gray-800 shadow-md rounded-2xl p-6">
              <Tab.Group>
                <Tab.List className="flex space-x-4 border-b border-gray-200 dark:border-gray-700 mb-4">
                  {['Step Response', 'Bode Plot'].map(tab => (
                    <Tab key={tab} className={({ selected }) => `py-2 px-4 text-sm font-medium rounded-t-xl ${selected ? 'bg-white dark:bg-gray-900 shadow-md' : 'text-gray-500 dark:text-gray-400'}`}>
                      {tab}
                    </Tab>
                  ))}
                </Tab.List>
                <Tab.Panels>
                  {['Step Response', 'Bode Plot'].map(tab => (
                    <Tab.Panel key={tab} className="pb-4">
                      <div className="w-full aspect-w-16 aspect-h-9 bg-gray-200 dark:bg-gray-700 rounded-xl flex items-center justify-center">
                        <span className="text-gray-400 italic">{tab} Placeholder</span>
                      </div>
                    </Tab.Panel>
                  ))}
                </Tab.Panels>
              </Tab.Group>
            </div>

            <div className="bg-yellow-50 dark:bg-yellow-900 border-l-4 border-yellow-400 dark:border-yellow-600 rounded-2xl p-6">
              <h3 className="font-semibold mb-2">Insight</h3>
              <p className="text-sm">Latest iteration failed: adjust specs.</p>
            </div>

            {result && (
              <div className="bg-gray-100 dark:bg-gray-700 rounded-2xl p-6 mt-6">
                <h3 className="font-semibold mb-2">API Result</h3>
                <pre className="whitespace-pre-wrap text-sm bg-white dark:bg-gray-800 p-4 rounded shadow-inner">
                  {JSON.stringify(result, null, 2)}
                </pre>
              </div>
            )}

            {status === 'done' && (
              <div className="bg-white dark:bg-gray-800 shadow-md rounded-2xl p-6 animate-fade-in">
                <h2 className="text-lg font-semibold mb-4">Final Results</h2>
                <div className="grid grid-cols-2 gap-6">
                  <div>
                    <p className="font-mono text-sm">{'\\(K(s)=\frac{3.317s}{1.917s+1.818}\\)'}</p>
                  </div>
                  <div>
                    <table className="w-full text-sm mb-4">
                      <thead>
                        <tr><th className="text-left">Metric</th><th className="text-left">Value</th></tr>
                      </thead>
                      <tbody>
                        {[
                          { name: 'Phase Margin', value: '45°' },
                          { name: 'Settling Time', value: '2.3s' },
                          { name: 'ess', value: '0.01' },
                        ].map(r => (
                          <tr key={r.name}>
                            <td className="flex items-center space-x-1"><CheckCircleIcon className="w-4 h-4 text-green-500" /><span>{r.name}</span></td>
                            <td>{r.value}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                    <div className="flex space-x-4">
                      <button className="flex-1 py-2 rounded-2xl bg-gray-200 dark:bg-gray-700 text-sm font-medium hover:bg-gray-300">Copy JSON</button>
                      <button className="flex-1 py-2 rounded-2xl bg-indigo-600 text-white text-sm font-medium hover:bg-indigo-700">Download Plots</button>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {error && (
              <div className="mt-4 p-4 bg-red-50 dark:bg-red-900/50 text-red-600 dark:text-red-300 rounded-lg">
                {error}
              </div>
            )}
          </section>
        </main>

        <button className="fixed bottom-6 right-6 bg-indigo-600 hover:bg-indigo-700 text-white p-4 rounded-full shadow-lg">Export</button>

        <style jsx global>{`
          @keyframes slideIn { from { transform: translateX(100%); opacity: 0 } to { transform: translateX(0); opacity: 1 } }
          .animate-slide-in { animation: slideIn 300ms ease-out; }
          @keyframes fadeIn { from { opacity: 0 } to { opacity: 1 } }
          .animate-fade-in { animation: fadeIn 500ms ease-in; }
        `}</style>
      </div>
    </div>
  );
}
