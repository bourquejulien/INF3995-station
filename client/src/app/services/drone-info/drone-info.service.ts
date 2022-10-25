import { Injectable } from '@angular/core';
import { Subscription, Observable, of, interval } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { HttpClient } from '@angular/common/http';
import { environment } from '@environment';

@Injectable({
    providedIn: 'root'
})
export class DroneInfoService {

    private _statuses: Observable<Map<string, string>>;
    private _positions: Observable<Map<string, string>>;

    constructor(private httpClient: HttpClient) {
        this._statuses = new Observable((observer) => {
            interval(1000).subscribe((x) => {
                this.getStatuses().subscribe({
                    next(response: any): void {
                        observer.next(new Map<string, string>(Object.entries(response)));
                    },
                    error(): void {
                        console.log("error");
                    },
                });
            });
        });
        this._positions = new Observable((observer) => {
            interval(1000).subscribe((x) => {
                this.getPositions().subscribe({
                    next(response: any): void {
                        observer.next(new Map<string, string>(Object.entries(response)));
                    },
                    error(): void {
                        console.log("error");
                    },
                });
            });
        });
    }

    private getStatuses(): Observable<any> {
        return this.httpClient.get(`${environment.serverURL}/drone-info/status`).pipe(catchError(this.handleError('getStatuses', [])));
    }

    private getPositions(): Observable<any> {
        return this.httpClient.get(`${environment.serverURL}/drone-info/position`).pipe(catchError(this.handleError('getPositions', [])));
    }

    private handleError<T>(operation = 'operation', result?: T) {
        return (error: any): Observable<T> => {
            console.error(error);
            return of(result as T);
        };
    }

    get statuses(): Observable<Map<string, string>> {
        return this._statuses;
    }

    get positions(): Observable<Map<string, string>> {
        return this._positions;
    } 
}
