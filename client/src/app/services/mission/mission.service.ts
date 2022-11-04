import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Log, Mission } from '@app/interface/commands';
import { environment } from '@environment';
import { interval, Observable, Subscription } from 'rxjs';
import { DroneInfoService } from '../drone-info/drone-info.service';

@Injectable({
    providedIn: 'root'
})
export class MissionService {
    private _isMissionOngoing: boolean = false;
    private _currentMission: Mission | null = null;
    private _currentLogs: Log[] = [];

    missionSubscription: Subscription = new Subscription();
    private logSubscription: Subscription = new Subscription();

    private _missions: {"mission": Mission, "logs": Log[]}[] = [];

    constructor(private httpClient: HttpClient, private droneInfoService: DroneInfoService) {
        let self = this;

        this.missionSubscription = interval(1000).subscribe(() => {
            this.getMission().subscribe({
                next(response): void {
                    let is_mission = Object.keys(response).length > 0
                    if(!self._isMissionOngoing && is_mission){
                        self.setupMission(response as Mission);
                    }
                    if (self._isMissionOngoing && !is_mission){
                        self.terminateMission()
                    }
                },
                error(): void {
                    console.log("error");
                },
            })
        });
    }

    getMission(): Observable<Mission | {}>{
        return this.httpClient.get<Mission>(`${environment.serverURL}/mission/current_mission`);
    }

    private logSubscribe(mission_id: string): void {
        const self = this;
        this.logSubscription = interval(1000).subscribe(() => {
            let since_timestamp = 0;
            if (this._currentLogs.length > 0) {
                since_timestamp = this._currentLogs[this._currentLogs.length - 1].timestamp_ms;
            }
            this.droneInfoService.getLogs(mission_id, since_timestamp).subscribe({
                next(response: Log[]): void {
                    self._currentLogs = self.currentLogs.concat(response);
                    console.log(self._currentLogs)
                },
                error(): void {
                    console.log("error");
                },
            });
        });
    }

    private logUnsubscribe(): void {
        this.logSubscription.unsubscribe();
    }

    private setupMission(mission: Mission): void {
        this._currentLogs = [];
        this._currentMission = mission;
        this._isMissionOngoing = true;
        this.logSubscribe(mission._id);
    }

    private terminateMission(): void {
        if (!this._currentMission) return;
        this.missions.push({
            "mission": this._currentMission,
            "logs": this._currentLogs
        });
        this.logUnsubscribe();
        this._isMissionOngoing = false;
    }

    public startMission(): void {
        if (this.isMissionOngoing) return;
        const self = this;
        this.httpClient.post<Mission>(`${environment.serverURL}/mission/start`, {}, {responseType: 'json'})
        .subscribe({
            next(response: Mission): void {
                self.setupMission(response)
            },
            error(): void {
                console.log("Mission start error");
            },
        });
    }

    public endMission(): void {
        if (!this.isMissionOngoing) return;
        const self = this;
        this.httpClient.post(`${environment.serverURL}/mission/end`, {}, {responseType: 'text'})
        .subscribe({
            next() {
                self.terminateMission();
            },
            error(): void {
                console.log("Mission end error");
            }
        });
    }

    public forceEndMission(): void {
        if (!this.isMissionOngoing) return;
        const self = this;
        this.httpClient.post(`${environment.serverURL}/mission/force_end`, {}, {responseType: 'text'})
        .subscribe({
            next() {
                self.terminateMission();
            },
            error(): void {
                console.log("Mission force end error");
            }
        });
    }

    public getMissionLogs(id: string): Log[] {
        for (let i = 0; i < this._missions.length; i++) {
            if (this._missions[i]["mission"]["_id"] == id) {
                return this._missions[i]["logs"];
            }
        }
        return [];
    }

    public get isMissionOngoing() {
        return this._isMissionOngoing;
    }

    public get currentMission() {
        return this._currentMission;
    }

    public get missions() {
        return this._missions;
    }

    public get currentLogs() {
        return this._currentLogs;
    }
}
