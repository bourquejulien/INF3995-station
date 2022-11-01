import { Component, OnInit } from '@angular/core';
import { Log } from '@app/interface/commands';
import { DroneInfoService } from '@app/services/drone-info/drone-info.service';
import { interval } from 'rxjs';

@Component({
    selector: 'app-log',
    templateUrl: './log.component.html',
    styleUrls: ['./log.component.css']
})
export class LogComponent implements OnInit {
    missionId: string = "";
    logs: Log[] = [];
    count: number[] = [];

    constructor(public droneInfoService: DroneInfoService) {
    }

    ngOnInit(): void {
        // TODO: get latest mission from database
        this.missionId = "stubMissionId";
        const self = this;
        interval(1000).subscribe(() => {
            this.droneInfoService.getLogs(this.missionId, this.logs.length).subscribe({
                next(response: Log[]): void {
                    self.logs = self.logs.concat(response)
                },
                error(): void {
                    console.log("error");
                },
            });
        });
    }
}