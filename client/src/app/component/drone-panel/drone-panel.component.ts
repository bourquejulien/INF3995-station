import { Component, OnInit, Input } from '@angular/core';
import { CommandService } from '@app/services/command/command.service';
import { DroneInfoService } from '@app/services/drone-info/drone-info.service';

@Component({
    selector: 'app-drone-panel',
    templateUrl: './drone-panel.component.html',
    styleUrls: ['./drone-panel.component.css']
})
export class DronePanelComponent implements OnInit {
    @Input() uri: string = ""; 
    collapsed: boolean = true;
    status: string = "";
    position: string = "";

    constructor(public commandService: CommandService, public droneInfoService: DroneInfoService) { }

    ngOnInit(): void {
        this.droneInfoService.statuses.subscribe((statuses) => {
            if (statuses.get(this.uri)) {
                this.status = statuses.get(this.uri) as string;
            }
        });
        this.droneInfoService.positions.subscribe((positions) => {
            if (positions.get(this.uri)) {
                this.position = positions.get(this.uri) as string;
            }
        });
    }

    identify(): void {
        if (this.uri.length == 0) {
            return;
        }
        this.commandService.identify({ uris: [this.uri] });
    }
}
