import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '@environment';
import { EndMission, Identify, Initialize, SetUp, StartMission } from '@app/interface/commands';

@Injectable({
    providedIn: 'root',
})
export class CommandService {
    constructor(private httpClient: HttpClient) {
      this.uris = []
    }

  uris: string[]

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

    async start_mission(command: StartMission): Promise<void> {
        await this.httpClient
            .post(`${environment.serverURL}/mission/start`,
            {} ,
            {
                responseType: 'json',
            })
            .toPromise();
    }

    async end_mission(command: EndMission): Promise<void> {
        await this.httpClient
            .post(`${environment.serverURL}/mission/end`,
            {},
            {
                responseType: 'json',
            })
            .toPromise();
    }

    async discover(): Promise<void> {
        this.uris = await this.httpClient
            .get<string[]>(`${environment.serverURL}/discovery`)
            .toPromise();
    }
}
