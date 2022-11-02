import { Component, OnInit } from '@angular/core';
import { Mission } from '@app/interface/commands';
import { CommandService } from '@app/services/command/command.service';
import { MissionService } from '@app/services/mission/mission.service';

@Component({
    selector: 'app-mission-page',
    templateUrl: './mission-page.component.html',
    styleUrls: ['./mission-page.component.css'],
})
export class MissionPageComponent implements OnInit {
    logsCollapsed: boolean = false;
    currentMissionId: string = "";

    constructor(public commandService: CommandService, public missionService: MissionService) {
    }
    
    ngOnInit(): void {
        this.commandService.discover();
        this.commandService.retrieveMode()
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
    }

    forceEndMission(): void {
        this.missionService.forceEndMission();
    }
}
