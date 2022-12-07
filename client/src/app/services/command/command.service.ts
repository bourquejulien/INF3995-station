import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '@environment';
import { DefaultPosition, Identify } from "@app/interface/commands";

@Injectable({
    providedIn: 'root',
})
export class CommandService {
    uris: Array<[string, boolean]>;
    isSimulation: boolean;

    constructor(private httpClient: HttpClient) {
        this.uris = [];
        this.isSimulation = false;
    }

    async connect(): Promise<void> {
        // TODO Sync uris with other clients
        this.uris = await this.httpClient
            .post<Map<string, boolean>>(`${environment.serverURL}/discovery/connect`, undefined)
            .toPromise()
            .then((e) => Array.from(e));
    }

    async disconnect(): Promise<void> {
        await this.httpClient
            .post(`${environment.serverURL}/discovery/disconnect`, undefined, {
                responseType: 'text',
            })
            .toPromise();
        this.uris = [];
    }

    async identify(command: Identify): Promise<void> {
        await this.httpClient
            .post(`${environment.serverURL}/action/identify`, command, {
                responseType: 'text',
            })
            .toPromise();
    }

    async toggleSync(): Promise<void> {
        await this.httpClient.post(`${environment.serverURL}/action/toggle_sync`, null,{
            responseType: 'text',
        })
            .toPromise();
    }

    async setInitialPositions(defaultPositions: Map<string, DefaultPosition>): Promise<void> {
        await this.httpClient.post(`${environment.serverURL}/action/initial_positions`, defaultPositions,{
            responseType: 'text',
        })
            .toPromise();
    }

    async getUris(): Promise<void> {
        const uris = await this.httpClient
            .get<Map<number, boolean>>(`${environment.serverURL}/discovery/uris`)
            .toPromise()
            .then((e) => Array.from(Object.entries(e)));

        if (JSON.stringify(uris) !== JSON.stringify(this.uris)) {
            this.uris = uris;
        }
    }

    async retrieveMode(): Promise<void> {
        this.isSimulation = await this.httpClient
            .get<boolean>(`${environment.serverURL}/is_simulation`)
            .toPromise();
    }
}
