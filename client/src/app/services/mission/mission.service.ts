import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Log, Mission } from '@app/interface/commands';
import { environment } from '@environment';
import { interval, Observable, Subscription } from 'rxjs';
import { DroneInfoService } from '../drone-info/drone-info.service';

const MISSION_HISTORY_SIZE = 10;

@Injectable({
    providedIn: 'root'
})
export class MissionService {
    private _isMissionOngoing: boolean = false;
    private _currentMission: Mission | null = null;
    private _currentLogs: Log[] = [];

    private _currentMissionSubscription: Subscription = new Subscription();
    private _logSubscription: Subscription = new Subscription();

    private _missions: {"mission": Mission, "logs": Log[]}[] = [];

    constructor(private httpClient: HttpClient, private droneInfoService: DroneInfoService) {
        let self = this;

        this.getLastMissions(MISSION_HISTORY_SIZE).subscribe({
            next(response: Mission[]): void {
                for(let mission of response) {
                    self._missions.push({"mission": mission, "logs": [] as Log[]})
                }
            },
            error(): void {
                console.log("error");
            }
        })

        this._currentMissionSubscription = interval(5000).subscribe(() => {
            this.getCurrentMission().subscribe({
                next(response): void {
                    let is_mission = Object.keys(response).length > 0;
                    if(!self._isMissionOngoing && is_mission){
                        self.setupMission(response as Mission);
                    }
                    if (self._isMissionOngoing && !is_mission){
                        self.terminateMission();
                    }
                },
                error(): void {
                    console.log("error");
                },
            })
        });
    }

    private getLastMissions(missions_number: number): Observable<Mission[]>{
        let queryParams = new HttpParams();
        queryParams = queryParams.append("missions_number", missions_number);
        return this.httpClient.get<Mission[]>(`${environment.serverURL}/mission/`,
            {params: queryParams},
        );
    }

    private getCurrentMission(): Observable<Mission | {}> {
        return this.httpClient.get<Mission>(`${environment.serverURL}/mission/current_mission`);
    }

    private logSubscribe(missionId: string): void {
        const self = this;
        this._logSubscription = interval(1000).subscribe(() => {
            let sinceTimestamp = 0;
            if (this._currentLogs.length > 0) {
                sinceTimestamp = this._currentLogs[this._currentLogs.length - 1].timestamp_ms;
            }
            this.droneInfoService.getLogs(missionId, sinceTimestamp=sinceTimestamp).subscribe({
                next(response: Log[]): void {
                    self._currentLogs = self.currentLogs.concat(response);
                },
                error(): void {
                    console.log("error");
                },
            });
        });
    }

    private logUnsubscribe(): void {
        this._logSubscription.unsubscribe();
    }

    private setupMission(mission: Mission): void {
        this._currentLogs = [];
        this._currentMission = mission;
        this._isMissionOngoing = true;
        this.logSubscribe(mission.id);
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

    public getMissionLogs(id: string): Log[] | Observable<Log[]>{
        for (let i = 0; i < this._missions.length; i++) {
            if (this._missions[i]["mission"]["id"] == id) {
                if (this._missions[i]["logs"].length == 0) {
                    let observable = this.droneInfoService.getLogs(id);
                    const self = this;
                    observable.subscribe({
                        next(logs: Log[]): void {
                            self._missions[i]["logs"] = logs;
                        },
                    });
                    return observable;
                }
                else {
                    return this._missions[i]["logs"];
                }
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
