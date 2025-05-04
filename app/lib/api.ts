// app/lib/api.ts
export interface ControlInputs {
    num: number[];                // e.g. [b0]
    den: number[];                // e.g. [a0, a1]
    tau?: number;                 // optional delay
    phase_margin_min: number;
    settling_time_min: number;
    settling_time_max: number;
    steadystate_error_max: number;
    scenario?: string;
  }
  
  export interface ApiResponse {
    success: boolean;
    data: any;  // whatever your runner returns
    detail?: string; // on error
  }
  
  export async function evaluateController(
    inputs: ControlInputs
  ): Promise<ApiResponse> {
    const res = await fetch("https://control-agent.onrender.com/api/evaluate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(inputs),
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || res.statusText);
    }
    return res.json();
  }