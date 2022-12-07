import { Injectable } from '@angular/core';
import { Observable, of, interval } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { HttpClient, HttpParams } from '@angular/common/http';
import { environment } from '@environment';
import { Log, Metric } from '@app/interface/commands';
import { MapDatabase, MapMetric, Vec2 } from '@app/interface/mapdrone';

@Injectable({
    providedIn: 'root'
})
export class DroneInfoService {
    latestMetric: Observable<Map<string, Metric>>;
    latestMapMetric: Observable<Map<string, MapMetric>>;
    allMapMetrics: Map<string, MapMetric[]>;
    oldMap: any;

    constructor(private httpClient: HttpClient) {
        this.latestMetric = new Observable((observer) => {
            interval(1000).subscribe(() => {
                this.getLatestMetric().subscribe({
                    next(response): void {
                        observer.next(new Map<string, Metric>(Object.entries(response)));
                    },
                    error(): void {
                        console.log("error");
                    },
                })
            })
        });
        this.latestMapMetric = new Observable((observer) => {
            interval(1000).subscribe(() => {
                this.getLatestMap().subscribe({
                    next(response): void {
                        observer.next(new Map<string, MapMetric>(Object.entries(response)));
                    },
                    error(): void {
                        console.log("error");
                    },
                })
            })
        });
        this.allMapMetrics = new Map();
        this.oldMap = []
    }

    getLatestMetric(): Observable<any>{
        return this.httpClient.get(`${environment.serverURL}/drone-info/latestMetric`,
            ).pipe(catchError(this.handleError('getLatestMetric', [])));
    }

    getLatestMap(): Observable<any>{
        return this.httpClient.get(`${environment.serverURL}/drone-info/latestMap`,
            ).pipe(catchError(this.handleError('latestMap', [])));
    }

    getAllMetrics(uri: string): Observable<Metric[]> {
        let queryParams = new HttpParams();
        queryParams = queryParams.append("uri", uri);
        return this.httpClient.get<Metric[]>(`${environment.serverURL}/drone-info/allMetrics`,
            {params: queryParams},
            ).pipe(catchError(this.handleError('metrics', [])));
    }

    async getAllMapMetric(): Promise<void> {
        let response = await this.httpClient.get<Map<string, MapMetric[]>>(`${environment.serverURL}/drone-info/maps`,
            ).pipe(catchError(this.handleError('mapMetric', [])))
            .toPromise() as Map<string, MapMetric[]>;
        if (response != null){
            this.allMapMetrics = new Map(Object.entries(response));
        }
    }

    getLogs(missionId: string, sinceTimestamp?: number): Observable<Log[]> {
        let queryParams = new HttpParams();
        queryParams = queryParams.append("mission_id", missionId);
        if (typeof sinceTimestamp !== "undefined") {
            queryParams = queryParams.append("since_timestamp", sinceTimestamp);
        }
        return this.httpClient.get<Log[]>(`${environment.serverURL}/drone-info/logs`,
            {params: queryParams},
            ).pipe(catchError(this.handleError('logs', [])));
    }

    private handleError<T>(operation = 'operation', result?: T) {
        return (error: any): Observable<T> => {
            console.error(error);
            return of(result as T);
        };
    }

    async getMapById(missionId: string): Promise<void> {
        let queryParams = new HttpParams();
        queryParams = queryParams.append("mission_id", missionId);
        let response = await this.httpClient.get<MapDatabase>(`${environment.serverURL}/drone-info/mapDatabase`,
            {params: queryParams},
            ).pipe(catchError(this.handleError('map database', []))).toPromise() as MapDatabase;
        this.oldMap = response.obstaclePosition;
    }
}
