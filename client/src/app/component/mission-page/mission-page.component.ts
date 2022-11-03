import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { Mission } from '@app/interface/commands';
import { CommandService } from '@app/services/command/command.service';
import { MissionService } from '@app/services/mission/mission.service';

@Component({
    selector: 'app-mission-page',
    templateUrl: './mission-page.component.html',
    styleUrls: ['./mission-page.component.css'],
})
export class MissionPageComponent implements OnInit {
    // @ViewChild('canvas', { static: false }) canvas!: ElementRef;
    // @ViewChild('colMission', { static: false }) colMission!: ElementRef;

    constructor(public commandService: CommandService, public missionService: MissionService) {
        this.selectedUris = [];
        // this.mapContext = null;
        // this.resolution = 80;
        // this.wallPositions = [];
        // this.dronePosition = {x: this.randomInInterval(20, 80), y: this.randomInInterval(20, 80)};
        this.logsCollapsed = false;
        this.currentMissionId = "";
    }

    selectedUris: string[];
    // mapContext: CanvasRenderingContext2D | null;
    // resolution: number; // NUmber of pixels to include in the map. The higher the number, the finer the image
    // wallPositions: {x: number; y: number}[]; // Contains the coordinates of the walls to draw to the map. Both x and y go from 0 to 100
    // dronePosition: {x: number; y: number}; // The current position of the drone
    logsCollapsed: boolean;
    currentMissionId: string;

    ngOnInit(): void {
        this.commandService.discover();
        this.commandService.retrieveMode();
        // this.generateCircle(40, 60, 30);
        // window.addEventListener("resize", this.redrawMap.bind(this), false); // Redraws the map when the window is resized
        // window.setInterval(() => {
        //     this.dronePosition = {x: this.randomInInterval(20.0, 80.0), y: this.randomInInterval(20.0, 80.0)};
        //     this.redrawMap();
        // }, 1000);
    }
    
    // ngAfterViewInit(): void {
    //     this.mapContext = this.canvas.nativeElement.getContext("2d") as CanvasRenderingContext2D; // Get a reference to the canvas
    //     this.redrawMap();
        
    // }

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

    // drawPixel(x: number, y: number, sizeOfCanvas: number): void {
    //     let pixelSize = sizeOfCanvas / this.resolution;
    //     let xCanvased = (x / 100.0) * sizeOfCanvas; // Gives the location of the point in the canvas' coordinates
    //     let xPixelized = Math.floor(Math.floor(xCanvased / pixelSize) * pixelSize); // Rounds to the previous multiple of the pixel size
    //     let yCanvased = (y / 100.0) * sizeOfCanvas;
    //     let yPixelized = Math.floor(Math.floor(yCanvased / pixelSize) * pixelSize);

    //     this.mapContext!.fillRect(xPixelized, yPixelized, pixelSize, pixelSize);
    // }

    // generateCircle(Xcenter: number, Ycenter: number, radius: number): void {
    //     this.wallPositions = [];

    //     let iterations = 200;
    //     for (let i = 0; i < iterations; i++) {
    //         let angle = (i / iterations) * 2 * Math.PI;
    //         let x = Xcenter + radius * Math.cos(angle);
    //         let y = Ycenter + radius * Math.sin(angle);
    //         this.wallPositions.push({x, y});
    //     }
    // }

    // redrawMap(): void {
    //     // New size of canvas is chosen according to size of parent div
    //     // The -50 for height is to account for the text above and below
    //     let canvasSize = Math.floor(Math.min(this.colMission.nativeElement.offsetWidth * 0.9, (this.colMission.nativeElement.offsetHeight - 50) * 0.9));

    //     this.canvas.nativeElement.width = canvasSize;
    //     this.canvas.nativeElement.height = canvasSize;

    //     this.mapContext!.fillStyle = "white";
    //     this.mapContext!.fillRect(0, 0, canvasSize, canvasSize);

    //     this.mapContext!.fillStyle = "black";
    //     for (let point of this.wallPositions) {
    //         this.drawPixel(point.x, point.y, canvasSize);
    //     }

    //     this.mapContext!.fillStyle = "red";
    //     this.drawPixel(this.dronePosition.x, this.dronePosition.y, canvasSize);
    // }

    // private randomInInterval(min: number, max: number): number{
    //     return Math.random() * (max - min) + min;
    // }
      
}
