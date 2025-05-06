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

  export interface FinalTaskDesignResult {
    conversation_round: number;
    controller_type: string;
    parameters: Record<string, number>;
    performance: {
      settling_time: number;
      overshoot: number;
      steady_state_error: number;
      phase_margin: number;
    };
  }
  
  export interface ApiResponse {
    is_success: boolean;
    msg: string;      // <-- now unknown instead of any
    final_result: FinalTaskDesignResult;
  }

  export interface TaskDesignResult {
    success: boolean;
    parameters: Record<string, number>;
    performance: {
      phase_margin?: number;
      settling_time_min?: number;
      settling_time_max?: number;
      steadystate_error?: number;
    };
    conversation_round: number;
  }
  
export async function evaluateController(
  inputs: ControlInputs
): Promise<ApiResponse> {
  // Uses a temporary dev server. Can update this to a production level when development is complete
  const res = await fetch("https://controlagent-app-noah-dev.onrender.com/api/complete_task", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(inputs),
  });

  if (!res.ok) {
    const err = await res.json() as { detail?: string };
    throw new Error(err.detail ?? res.statusText);
  }

  return res.json() as Promise<ApiResponse>;
}

export function connectWebSocket(
  inputs: ControlInputs,
  onResult: (data: TaskDesignResult) => void,
  onComplete?: () => void,
  onError?: (err: Error | CloseEvent) => void
): WebSocket {
  const ws = new WebSocket("wss://controlagent-app-noah-dev.onrender.com/api/complete_task");

  ws.onopen = () => {
    ws.send(JSON.stringify(inputs));
  };

  ws.onmessage = (event) => {
    const data = JSON.parse(event.data) as TaskDesignResult;
    onResult(data);

    if (data.conversation_round === -1) {
      ws.close();
      onComplete?.();
    }
  };

  ws.onerror = (event) => {
    console.error("WebSocket error", event);
    onError?.(new Error("WebSocket error occurred"));
  };

  ws.onclose = (event) => {
    if (event.code !== 1000) {
      console.warn("WebSocket closed unexpectedly:", event);
      onError?.(event);
    }
  };

  return ws;
}