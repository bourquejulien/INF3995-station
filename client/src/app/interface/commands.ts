export interface Identify {
    uris: string[]
}

export interface Log {
    timestamp_ms: number,
    mission_id: string,
    message: string,
    level: string,
}
