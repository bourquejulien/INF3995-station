import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { Router } from '@angular/router';
import { CommandService } from '@app/services/command/command.service';

@Component({
    selector: 'app-mission-page',
    templateUrl: './mission-page.component.html',
    styleUrls: ['./mission-page.component.css'],
})
export class MissionPageComponent implements OnInit {
    @ViewChild('canvas', { static: false }) canvas!: ElementRef;

    constructor(private router: Router, public commandService: CommandService) {
        this.selectedUris = [];
        this.map = null;
    }

    selectedUris: string[];
    map: CanvasRenderingContext2D | null;

    ngOnInit(): void {
        this.commandService.discover();
        this.commandService.retrieveMode();
    }
    
    ngAfterViewInit(): void {
        this.map = this.canvas.nativeElement.getContext("2d") as CanvasRenderingContext2D;
        // this.map.fillStyle = "green";
        // this.map.fillRect(10, 10, 100, 100);
        //this.map.fillStyle = "green";
        this.map.fillRect(10, 10, 100, 100);
    }

    identify(): void {
        if (this.selectedUris.length == 0) {
            return;
        }
        this.commandService.identify({ uris: this.selectedUris });
    }

    startMission(): void {
        this.commandService.startMission({});
    }

    endMission(): void {
        this.commandService.endMission({});
    }

    forceEndMission(): void {
        this.commandService.forceEndMission({});
    }

    isUriSelected(uri: string): boolean {
        return this.selectedUris.findIndex((elem) => uri === elem) != -1;
    }

    toggleUri(uri: string): void {
        let uriPosition = this.selectedUris.findIndex((elem) => uri === elem);
        if (uriPosition == -1) {
            this.selectedUris.push(uri);
            return;
        }
        this.selectedUris.splice(uriPosition, 1);
    }
}
