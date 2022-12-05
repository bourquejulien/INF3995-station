import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '@environment';

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
            .toPromise();
    }

    async disconnect(): Promise<void> {
        await this.httpClient
            .post(`${environment.serverURL}/discovery/disconnect`, undefined)
            .toPromise();
        this.uris = [];
    }

    async identify(uris: string[]): Promise<void> {
        await this.httpClient
            .post(`${environment.serverURL}/action/identify`, uris)
            .toPromise();
    }

    async toggleSync(): Promise<void> {
        await this.httpClient
            .post(`${environment.serverURL}/action/toggle_sync`, null)
            .toPromise();
    }

    async getUris(): Promise<void> {
        this.uris = await this.httpClient
            .get<string[]>(`${environment.serverURL}/discovery/uris`)
            .toPromise();
    }

    async retrieveMode(): Promise<void> {
        this.isSimulation = await this.httpClient
            .get<boolean>(`${environment.serverURL}/is_simulation`)
            .toPromise();
    }
}
