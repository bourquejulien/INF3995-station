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
    logs: Observable<Log[]> = new Observable();

    constructor(public missionService: MissionService) {
    }

    ngOnInit(): void {
    }

    public selectMission(id: string): void {
        this.selectedMissionId = id;
        this.collapsed = true;
        if (this.selectedMissionId === "en cours") {
            this.logs = of(this.missionService.currentLogs);
        }
        else {
            let logs = this.missionService.getMissionLogs(this.selectedMissionId);
            if (logs instanceof Observable) {
                this.logs = logs;
            }
            else {
                this.logs = of(logs);
            }
        }
    }

    public formatId(id: string): string {
        return id.split("-")[0];
    }
}
