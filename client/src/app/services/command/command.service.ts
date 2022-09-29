import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '@environment';
import { EndMission, Identify, Initialize, SetUp, StartMission } from '@app/interface/commands';

@Injectable({
    providedIn: 'root',
})
export class CommandService {
    constructor(private httpClient: HttpClient) {}

    async set_up(command: SetUp): Promise<void> {
        await this.httpClient
            .post(
                `${environment.serverURL}/command/set_up`,
                {
                    isSimulation: command.isSimulation,
                },
                {
                    responseType: 'json',
                },
            )
            .toPromise();
    }

    async identify(command: Identify): Promise<void> {
        await this.httpClient
            .post(
                `${environment.serverURL}/command/identify`,
                {
                    drones: command.drones
                },
                {
                    responseType: 'json',
                },
            )
            .toPromise();
    }

    async initialize(command: Initialize): Promise<void> {
        await this.httpClient
            .post(
                `${environment.serverURL}/command/initialize`,
                {
                    drones: command.drones,
                },
                {
                    responseType: 'json',
                },
            )
            .toPromise();
    }

    async start_mission(command: StartMission): Promise<void> {
        await this.httpClient
            .post(`${environment.serverURL}/command/start_mission`, 
            {
                drones: command.drones,
            }, 
            {
                responseType: 'json',
            })
            .toPromise();
    }

    async end_mission(command: EndMission): Promise<void> {
        await this.httpClient
            .post(`${environment.serverURL}/command/end_mission`, 
            {
                drones: command.drones,
            }, 
            {
                responseType: 'json',
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
