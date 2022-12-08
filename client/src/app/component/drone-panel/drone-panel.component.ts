import { Component, OnInit, Input } from "@angular/core";
import { Metric } from "@app/interface/commands";
import { CommandService } from "@app/services/command/command.service";
import { DroneInfoService } from "@app/services/drone-info/drone-info.service";

@Component({
    selector: "app-drone-panel",
    templateUrl: "./drone-panel.component.html",
    styleUrls: ["./drone-panel.component.css"],
})
export class DronePanelComponent implements OnInit {
    @Input() uri: [string, boolean] = ["", true];
    collapsed: boolean = true;
    metric: Metric | null = null;

    constructor(public commandService: CommandService, public droneInfoService: DroneInfoService) {}

    ngOnInit(): void {
        this.droneInfoService.latestMetric.subscribe((metrics: Map<string, Metric>) => {
            if (metrics.get(this.uri[0])) {
                this.metric = metrics.get(this.uri[0]) as Metric;
            }
        });
    }

    identify(): void {
        if (this.uri[0].length == 0 || !this.uri[1]) {
            return;
        }
        this.commandService.identify({ uris: [this.uri[0]] });
    }
}
