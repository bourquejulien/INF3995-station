import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { CommandService } from '@app/services/command/command.service';
import { MissionService } from '@app/services/mission/mission.service';

type Pane = "none" | "logs" | "firmware";

@Component({
    selector: 'app-mission-page',
    templateUrl: './mission-page.component.html',
    styleUrls: ['./mission-page.component.css'],
})
export class MissionPageComponent implements OnInit {
    selectedUris: string[];
    currentMissionId: string;
    isLinkCollapsed: boolean;
    currentPane: Pane;

    constructor(public commandService: CommandService, public missionService: MissionService) {
        this.selectedUris = [];
        this.currentMissionId = "";
        this.currentPane = "none";
        this.isLinkCollapsed = true;
    }

    ngOnInit(): void {
        this.commandService.getUris();
        this.commandService.retrieveMode();
        this.isLinkCollapsed = true;
    }

    connect(): void {
        this.commandService.connect();
    }

    disconnect(): void {
        this.commandService.disconnect();
    }

    identify(): void {
        this.commandService.identify({ uris: this.commandService.uris});
    }

    toggleSync(): void {
        this.commandService.toggleSync();
    }

    startMission(): void {
        this.missionService.startMission();
    }

    endMission(): void {
        this.missionService.endMission();
    }

    forceEndMission(): void {
        this.missionService.forceEndMission();
    }

    togglePane(pane: Pane): void {
        if (this.currentPane == pane) {
            this.currentPane = "none";
            return;
        }
        this.currentPane = pane;
    }
}
