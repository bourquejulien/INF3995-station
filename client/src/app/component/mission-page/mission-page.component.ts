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
    @ViewChild('colMission', { static: false }) colMission!: ElementRef;

    constructor(private router: Router, public commandService: CommandService) {
        this.selectedUris = [];
        this.mapContext = null;
        this.pixelSize = 6;
    }

    selectedUris: string[];
    mapContext: CanvasRenderingContext2D | null;
    pixelSize: number;

    ngOnInit(): void {
        this.commandService.discover();
        this.commandService.retrieveMode();
        window.addEventListener("resize", this.resizeMap.bind(this), false);
    }
    
    ngAfterViewInit(): void {
        this.mapContext = this.canvas.nativeElement.getContext("2d") as CanvasRenderingContext2D;
        this.resizeMap();
        
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

    drawPixel(X: number, Y: number): void {
        let Xpixelized = Math.floor(X / this.pixelSize) * this.pixelSize; // Rounds to the previous multiple of the pixel size
        let Ypixelized = Math.floor(Y / this.pixelSize) * this.pixelSize;
        this.mapContext!.fillRect(Xpixelized, Ypixelized, this.pixelSize, this.pixelSize);
    }

    drawCircle(Xcenter: number, Ycenter: number, radius: number): void {
        let iterations = 200;
        for (let i = 0; i < iterations; i++) {
            let angle = (i / iterations) * 2 * Math.PI;
            let x = Xcenter + radius * Math.cos(angle);
            let y = Ycenter + radius * Math.sin(angle);
            this.drawPixel(x, y);
        }
    }

    resizeMap(): void {
        let canvasSize = Math.min(this.colMission.nativeElement.offsetWidth * 0.9, (this.colMission.nativeElement.offsetHeight - 50) * 0.9);

        this.canvas.nativeElement.width = canvasSize;
        this.canvas.nativeElement.height = canvasSize;

        let width = this.canvas.nativeElement.width;
        let height = this.canvas.nativeElement.height;
        this.mapContext!.fillStyle = "white";
        this.mapContext!.fillRect(0, 0, width, height);
        this.mapContext!.fillStyle = "black";
        this.drawCircle(150, 200, 145);
    }
}
