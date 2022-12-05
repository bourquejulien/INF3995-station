import { Component, OnInit, Input } from '@angular/core';
import { Metric } from '@app/interface/commands';
import { CommandService } from '@app/services/command/command.service';
import { DroneInfoService } from '@app/services/drone-info/drone-info.service';
import { interval } from 'rxjs';

@Component({
    selector: 'app-drone-panel',
    templateUrl: './drone-panel.component.html',
    styleUrls: ['./drone-panel.component.css']
})
export class DronePanelComponent implements OnInit {
    @Input() uri: string = ""; 
    collapsed: boolean = true;
    metric: Metric | null = null;

    constructor(public commandService: CommandService, public droneInfoService: DroneInfoService) { }

    ngOnInit(): void {
        this.droneInfoService.latestMetric.subscribe((metrics: Map<string, Metric>) => {
            if (metrics.get(this.uri)) {
                this.metric = metrics.get(this.uri) as Metric;
            }
        });
    }

    identify(): void {
        if (this.uri.length == 0) {
            return;
        }
        this.commandService.identify([this.uri]);
    }
}
