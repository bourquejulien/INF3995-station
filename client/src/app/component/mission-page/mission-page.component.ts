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
        this.resolution = 80;
        this.pointsToDraw = [];
    }

    selectedUris: string[];
    mapContext: CanvasRenderingContext2D | null;
    resolution: number; // NUmber of pixels to include in the map. The higher the number, the finer the image
    pointsToDraw: {x: number; y: number}[]; // Contains the coordinates to draw to the map. Both x and y go from 0 to 100

    ngOnInit(): void {
        this.commandService.discover();
        this.commandService.retrieveMode();
        this.generateCircle(40, 60, 30);
        window.addEventListener("resize", this.redrawMap.bind(this), false); // Redraws the map when the window is resized
    }
    
    ngAfterViewInit(): void {
        this.mapContext = this.canvas.nativeElement.getContext("2d") as CanvasRenderingContext2D; // Get a reference to the canvas
        this.redrawMap();
        
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

    drawPixel(x: number, y: number, size: number): void {
        let pixelSize = size / this.resolution;
        let xCanvased = (x / 100.0) * size; // Gives the location of the point in the canvas' coordinates
        let xPixelized = Math.floor(Math.floor(xCanvased / pixelSize) * pixelSize); // Rounds to the previous multiple of the pixel size
        let yCanvased = (y / 100.0) * size;
        let yPixelized = Math.floor(Math.floor(yCanvased / pixelSize) * pixelSize);

        this.mapContext!.fillRect(xPixelized, yPixelized, pixelSize, pixelSize);
    }

    generateCircle(Xcenter: number, Ycenter: number, radius: number): void {
        this.pointsToDraw = [];

        let iterations = 200;
        for (let i = 0; i < iterations; i++) {
            let angle = (i / iterations) * 2 * Math.PI;
            let x = Xcenter + radius * Math.cos(angle);
            let y = Ycenter + radius * Math.sin(angle);
            this.pointsToDraw.push({x, y});
        }
    }

    redrawMap(): void {
        // New size of canvas is chosen according to size of parent div
        // The -50 for height is to account for the text above and below
        let canvasSize = Math.floor(Math.min(this.colMission.nativeElement.offsetWidth * 0.9, (this.colMission.nativeElement.offsetHeight - 50) * 0.9));

        this.canvas.nativeElement.width = canvasSize;
        this.canvas.nativeElement.height = canvasSize;

        this.mapContext!.fillStyle = "white";
        this.mapContext!.fillRect(0, 0, canvasSize, canvasSize);
        this.mapContext!.fillStyle = "black";
        
        for (let point of this.pointsToDraw) {
            this.drawPixel(point.x, point.y, canvasSize);
        }
    }
}
