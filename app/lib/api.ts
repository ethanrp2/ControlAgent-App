// app/lib/api.ts

export interface ControlInputs {
    num: number[];                
    den: number[];                
    tau?: number;                 
    phase_margin_min: number;
    settling_time_min: number;
    settling_time_max: number;
    steadystate_error_max: number;
    scenario?: string;
  }
  
  export interface ApiResponse {
    success: boolean;
    data: unknown;      // <-- now unknown instead of any
    detail?: string;
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
      const err = await res.json() as { detail?: string };
      throw new Error(err.detail ?? res.statusText);
    }
    // it's OK to return unknown here; the consumer can inspect/validate
    return res.json() as Promise<ApiResponse>;
  }