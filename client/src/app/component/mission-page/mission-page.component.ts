import { Component, OnInit } from '@angular/core';
import { CommandService } from '@app/services/command/command.service';

@Component({
    selector: 'app-mission-page',
    templateUrl: './mission-page.component.html',
    styleUrls: ['./mission-page.component.css'],
})
export class MissionPageComponent implements OnInit {
    constructor(public commandService: CommandService) {
    }
    
    logsCollapsed: boolean = false;

    ngOnInit(): void {
        this.commandService.discover();
        this.commandService.retrieveMode()
    }

    identify(): void {
        this.commandService.identify({ uris: this.commandService.uris});
    }

    startMission(): void {
        this.commandService.startMission();
    }

    endMission(): void {
        this.commandService.endMission();
    }

    forceEndMission(): void {
        this.commandService.forceEndMission();
    }
}
