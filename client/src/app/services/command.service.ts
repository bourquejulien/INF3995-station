import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '@environment';

@Injectable({
    providedIn: 'root',
})
export class CommandService {
    constructor(private httpClient: HttpClient) {}

    async initFlight(droneId: string): Promise<void> {
        await this.httpClient
            .post(`${environment.serverURL}/basic/init`, droneId, {
                responseType: 'text',
            })
            .toPromise();
    }

    async takeoff(droneId: string): Promise<void> {
        await this.httpClient
            .post(`${environment.serverURL}/basic/init`, droneId, {
                responseType: 'text',
            })
            .toPromise();
    }
}
