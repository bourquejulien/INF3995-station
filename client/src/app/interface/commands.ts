export interface Identify {
    uris: string[]
}

export interface Log {
    timestamp_ms: number,
    mission_id: string,
    message: string,
    level: string,
}

export interface Mission {
    _id: string,
    is_simulation: boolean,
    start_time_ms: number,
    end_time_ms: number,
} 
