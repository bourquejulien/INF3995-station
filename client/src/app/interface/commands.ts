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
    id: string,
    is_simulation: boolean,
    total_distance: number,
    drone_count: number,
    start_time_ms: number,
    end_time_ms: number,
}

export interface Position {
    x: number,
    y: number,
    z: number,
}

export interface Metric {
    _id: string,
    timestamp_ms: number,
    position: Position,
    status: string,
    drone_uri: string,
    mission_id: string,
}
