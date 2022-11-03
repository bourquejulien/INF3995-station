import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { Mission } from '@app/interface/commands';
import { CommandService } from '@app/services/command/command.service';
import { MissionService } from '@app/services/mission/mission.service';

@Component({
    selector: 'app-mission-page',
    templateUrl: './mission-page.component.html',
    styleUrls: ['./mission-page.component.css'],
})
export class MissionPageComponent implements OnInit {

    constructor(public commandService: CommandService, public missionService: MissionService) {
        this.selectedUris = [];
        this.logsCollapsed = false;
        this.currentMissionId = "";
    }

    selectedUris: string[];
    logsCollapsed: boolean;
    currentMissionId: string;

    ngOnInit(): void {
        this.commandService.discover();
        this.commandService.retrieveMode();
    }
    

    identify(): void {
        this.commandService.identify({ uris: this.commandService.uris});
    }

    startMission(): void {
        const self = this;
        this.missionService.startMission().subscribe({
            next(response: Mission): void {
                self.currentMissionId = response._id
            },
            error(): void {
                console.log("error");
            },
        });
    }

    endMission(): void {
        this.missionService.endMission();
        this.currentMissionId = "";
    }

    forceEndMission(): void {
        this.missionService.forceEndMission();
        this.currentMissionId = "";
    }

    
}
