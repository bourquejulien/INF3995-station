import { Position } from "./commands";

export interface MapDrone {
    uri: string,
    color: string,
    positions: Position[],
    distances: Position[],
    currentPosition: Position | null,
    lastPosition: Position | null,
    currentDistances: Position[],
}

export interface MapMetric {
    timestamp_ms: number,
    uri: string,
    position: Position,
    distance: Position[],
}