import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { environment } from '@environment';
import { catchError } from 'rxjs/operators';
import { Observable, throwError } from 'rxjs';

@Injectable({
    providedIn: 'root',
})
export class CommandService {
    uris: string[];
    isSimulation: boolean;

    constructor(private httpClient: HttpClient) {
        this.uris = [];
        this.isSimulation = false;
    }

    async connect(): Promise<void> {
        this.uris = await this.httpClient
            .post<string[]>(`${environment.serverURL}/discovery/connect`, undefined)
            .pipe(catchError(this.handleError))
            .toPromise();
    }

    async disconnect(): Promise<void> {
        await this.httpClient
            .post(`${environment.serverURL}/discovery/disconnect`, undefined)
            .pipe(catchError(this.handleError))
            .toPromise();
        this.uris = [];
    }

    async identify(uris: string[]): Promise<void> {
        await this.httpClient
            .post(`${environment.serverURL}/action/identify`, uris)
            .pipe(catchError(this.handleError))
            .toPromise();
    }

    async toggleSync(): Promise<void> {
        await this.httpClient
            .post(`${environment.serverURL}/action/toggle_sync`, null)
            .pipe(catchError(this.handleError))
            .toPromise();
    }

    async getUris(): Promise<void> {
        this.uris = await this.httpClient
            .get<string[]>(`${environment.serverURL}/discovery/uris`)
            .pipe(catchError(this.handleError))
            .toPromise();
    }

    async retrieveMode(): Promise<void> {
        this.isSimulation = await this.httpClient
            .get<boolean>(`${environment.serverURL}/is_simulation`)
            .pipe(catchError(this.handleError))
            .toPromise();
    }

    private handleError(error: HttpErrorResponse): Observable<never> {
        if (error.status === 0) return throwError(new Error('Server is unavailable'));
        return throwError(error);
    }
}
