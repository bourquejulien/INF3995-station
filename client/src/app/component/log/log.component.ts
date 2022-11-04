import { Component, OnInit } from '@angular/core';
import { Log } from '@app/interface/commands';
import { MissionService } from '@app/services/mission/mission.service';

@Component({
    selector: 'app-log',
    templateUrl: './log.component.html',
    styleUrls: ['./log.component.css']
})
export class LogComponent implements OnInit {
    collapsed: boolean = true;
    selectedMissionId: string = "Mission en cours";

    constructor(public missionService: MissionService) {
    }

    ngOnInit(): void {
    }

    public logs(): Log[] {
        if (this.selectedMissionId == "Mission en cours") {
            return this.missionService.currentLogs;
        }
        else {
           return this.missionService.getMissionLogs(this.selectedMissionId);
        }
    }

    public selectMission(id: string): void {
        this.selectedMissionId = id;
        this.collapsed = true;
    }
}
