import { Injectable } from "@angular/core";
import { HttpClient, HttpErrorResponse } from "@angular/common/http";
import { environment } from "@environment";
import { catchError } from "rxjs/operators";
import { DefaultPosition, Identify } from "@app/interface/commands";
import { BehaviorSubject, Observable, throwError } from "rxjs";

@Injectable({
    providedIn: "root",
})
export class CommandService {
    uris: Array<[string, boolean]>;
    private urisSubject: BehaviorSubject<Array<[string, boolean]>>;

    isSimulation: boolean;

    constructor(private httpClient: HttpClient) {
        this.uris = [];
        this.isSimulation = false;
        this.urisSubject = new BehaviorSubject<Array<[string, boolean]>>([]);
    }

    async connect(): Promise<void> {
        const uris = await this.httpClient
            .post<Map<string, boolean>>(`${environment.serverURL}/discovery/connect`, undefined)
            .pipe(catchError(this.handleError))
            .toPromise()
            .then((e) => Array.from(e));

        if (JSON.stringify(uris) !== JSON.stringify(this.uris)) {
            this.uris = uris;
            this.urisSubject.next(uris);
        }
    }

    async disconnect(): Promise<void> {
        await this.httpClient
            .post(`${environment.serverURL}/discovery/disconnect`, undefined, {
                responseType: "text",
            })
            .pipe(catchError(this.handleError))
            .toPromise();

        for (const uri of this.uris) {
            uri[1] = false;
        }
    }

    async identify(command: Identify): Promise<void> {
        await this.httpClient
            .post(`${environment.serverURL}/action/identify`, command, {
                responseType: "text",
            })
            .pipe(catchError(this.handleError))
            .toPromise();
    }

    async toggleSync(): Promise<void> {
        await this.httpClient
            .post(`${environment.serverURL}/action/toggle_sync`, null, {
                responseType: "text",
            })
            .pipe(catchError(this.handleError))
            .toPromise();
    }

    async setInitialPositions(defaultPositions: Map<string, DefaultPosition>): Promise<void> {
        await this.httpClient
            .post(`${environment.serverURL}/action/initial_positions`, defaultPositions, {
                responseType: "text",
            })
            .toPromise();
    }

    async getUris(): Promise<void> {
        const uris = await this.httpClient
            .get<Map<number, boolean>>(`${environment.serverURL}/discovery/uris`)
            .pipe(catchError(this.handleError))
            .toPromise()
            .then((e) => Array.from(Object.entries(e)));

        if (JSON.stringify(uris) !== JSON.stringify(this.uris)) {
            this.uris = uris;
            this.urisSubject.next(uris);
        }
    }

    async retrieveMode(): Promise<void> {
        this.isSimulation = await this.httpClient
            .get<boolean>(`${environment.serverURL}/is_simulation`)
            .pipe(catchError(this.handleError))
            .toPromise();
    }

    get urisObservable(): Observable<Array<[string, boolean]>> {
        return this.urisSubject.asObservable();
    }

    private handleError(error: HttpErrorResponse): Observable<never> {
        if (error.status === 0) return throwError(new Error('Server is unavailable'));
        return throwError(error);
    }
}
