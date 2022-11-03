import { Injectable } from '@angular/core';
import { Observable, of, interval } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { HttpClient, HttpParams } from '@angular/common/http';
import { environment } from '@environment';
import { Log, Metric } from '@app/interface/commands';

@Injectable({
    providedIn: 'root'
})
export class DroneInfoService {
    metrics: Observable<Map<string, Metric>>;

    constructor(private httpClient: HttpClient) {
        this.metrics = new Observable((observer) => {
            interval(1000).subscribe(() => {
                this.getMetrics().subscribe({
                    next(response): void {
                        observer.next(new Map<string, Metric>(Object.entries(response)));
                    },
                    error(): void {
                        console.log("error");
                    },
                })
            })
        });
    }

    getMetrics(): Observable<any>{
        return this.httpClient.get(`${environment.serverURL}/drone-info/metrics`,
            ).pipe(catchError(this.handleError('getStatuses', [])));
    }

    getLogs(mission_id: string, since_timestamp: number): Observable<Log[]> {
        let queryParams = new HttpParams();
        queryParams = queryParams.append("mission_id", mission_id);
        queryParams = queryParams.append("since_timestamp", since_timestamp);
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
}
