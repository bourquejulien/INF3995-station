import { Component, OnInit } from '@angular/core';
import { Log } from '@app/interface/commands';
import { MissionService } from '@app/services/mission/mission.service';
import { Observable, of } from 'rxjs';

@Component({
    selector: 'app-log',
    templateUrl: './log.component.html',
    styleUrls: ['./log.component.css']
})
export class LogComponent implements OnInit {
    collapsed: boolean = true;
    selectedMissionId: string = "en cours";

    constructor(public missionService: MissionService) {
    }

    ngOnInit(): void {
    }

    public logs(): Observable<Log[]> {
        if (this.selectedMissionId === "en cours") {
            return of(this.missionService.currentLogs);
        }
        else {
            let logs = this.missionService.getMissionLogs(this.selectedMissionId);
            if (logs instanceof Observable) {
                return logs;
            }
            else {
                return of(logs);
            }
        }
    }

    public selectMission(id: string): void {
        this.selectedMissionId = id;
        this.collapsed = true;
    }

    public formatMissionId(missionId: string): string {
        return missionId.split("-")[0];
    } 
}
