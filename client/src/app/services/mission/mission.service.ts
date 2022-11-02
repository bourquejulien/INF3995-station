import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Mission } from '@app/interface/commands';
import { environment } from '@environment';
import { Observable } from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class MissionService {
    constructor(private httpClient: HttpClient) {
    }

    startMission(): Observable<Mission> {
        return this.httpClient.post<Mission>(
            `${environment.serverURL}/mission/start`, {}, {responseType: 'json'});
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
}
