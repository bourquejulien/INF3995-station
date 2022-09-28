import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '@environment';
import { Init } from '@app/interface/commands';

@Injectable({
    providedIn: 'root',
})
export class CommandService {
    constructor(private httpClient: HttpClient) {}

    async init(command: Init): Promise<void> {
        await this.httpClient
            .post(
                `${environment.serverURL}/command`,
                {
                    command: command.command,
                    isSimulation: command.isSimulation,
                },
                {
                    responseType: 'json',
                },
            )
            .toPromise();
    }

    async startMission(droneId: string): Promise<void> {
        await this.httpClient
            .post(`${environment.serverURL}/basic/init`, droneId, {
                responseType: 'text',
            })
            .toPromise();
    }

    async endMission(droneId: string): Promise<void> {
        await this.httpClient
            .post(`${environment.serverURL}/basic/init`, droneId, {
                responseType: 'text',
            })
            .toPromise();
    }

    async discover(): Promise<void> {
        await this.httpClient
            .get(`${environment.serverURL}/discovery`, {
                responseType: 'json',
            })
            .toPromise();
    }
}
