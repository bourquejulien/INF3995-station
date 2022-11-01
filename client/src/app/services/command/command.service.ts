import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '@environment';
import { Identify } from '@app/interface/commands';

@Injectable({
    providedIn: 'root',
})
export class CommandService {
    constructor(private httpClient: HttpClient) {
        this.uris = [];
        this.isSimulation = false;
    }

    uris: string[];
    isSimulation: boolean;

    async identify(command: Identify): Promise<void> {
        await this.httpClient
            .post(`${environment.serverURL}/action/identify`, command, {
                responseType: 'text',
            })
            .toPromise();
    }

    async startMission(): Promise<void> {
        await this.httpClient
            .post(`${environment.serverURL}/mission/start`, {}, {
                responseType: 'text',
            })
            .toPromise();
    }

    async endMission(): Promise<void> {
        await this.httpClient
            .post(`${environment.serverURL}/mission/end`, {}, {
                responseType: 'text',
            })
            .toPromise();
    }

    async forceEndMission(): Promise<void> {
        await this.httpClient
            .post(`${environment.serverURL}/mission/force_end`, {}, {
                responseType: 'text',
            })
            .toPromise();
    }

    async discover(): Promise<void> {
        this.uris = await this.httpClient
            .get<string[]>(`${environment.serverURL}/discovery/discover`)
            .toPromise();
    }

    async retrieveMode(): Promise<void> {
        this.isSimulation = await this.httpClient
            .get<boolean>(`${environment.serverURL}/is_simulation`)
            .toPromise();
    }
}
