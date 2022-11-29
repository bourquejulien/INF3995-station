import { Component, OnInit, ViewChild, ElementRef, AfterViewInit } from '@angular/core';
import { MapDrone, MapMetric } from '@app/interface/mapdrone';
import { CommandService } from '@app/services/command/command.service';
import { DroneInfoService } from '@app/services/drone-info/drone-info.service';

@Component({
    selector: 'app-map',
    templateUrl: './map.component.html',
    styleUrls: ['./map.component.css']
})
export class MapComponent implements OnInit, AfterViewInit {
    @ViewChild('basecanvas', { static: false }) basecanvas!: ElementRef;
    @ViewChild('positionscanvas', { static: false }) positionscanvas!: ElementRef;
    @ViewChild('currentcanvas', { static: false }) currentcanvas!: ElementRef;
    @ViewChild('colMission', { static: false }) colMission!: ElementRef;

    constructor(public droneInfoService: DroneInfoService, public commandService: CommandService) {
        this.resolution = 100;
        this.mapDrones = new Map();
        this.allUris = [];
        this.selectedUris = new Map();
    }

    // Canvas
    private baseCtx!: CanvasRenderingContext2D;
    private positionsCtx!: CanvasRenderingContext2D;
    private currentCtx!: CanvasRenderingContext2D;
    private canvasSize!: number;
    private pixelSize!: number;
    resolution: number; // Number of pixels to include in the map. The higher the number, the finer the image
    // Drones info
    mapDrones: Map<string, MapDrone>;
    allUris: string[];
    selectedUris: Map<string, boolean>;
    
    ngOnInit(): void {
        window.addEventListener("resize", this.resizeCanvas.bind(this), false); // Redraws the map when the window is resized
        this.commandService.getUris().then(() => { // Waiting for all uris then proceed
            this.allUris = this.commandService.uris;
            this.droneInfoService.getAllMapMetric().then(() => {
                this.createNewMapDrone();
                this.resetSelectedUris();
    
                this.droneInfoService.latestMapMetric.subscribe((metrics: Map<string, MapMetric>) => {
                    for(let i = 0; i < this.allUris.length; i++){
                        if (metrics.get(this.allUris[i])) {
                            this.updateMapMetrics(metrics.get(this.allUris[i])!, this.allUris[i]);
                            if (this.mapDrones.size > 0){
                                this.redrawMap();
                            }
                        }
                    }
                });
            });
            
        });
    }

    ngAfterViewInit(): void {
        this.initializeCanvas();
        this.updateSelected();
        this.redrawMap();
    }

    createNewMapDrone(): void{
        let previousMapDrone = this.droneInfoService.allMapMetrics;
        for(let i = 0; i < this.allUris.length; i++){
            let uri = this.allUris[i];
            let oldPositions = [];
            let oldObstacles = [];
            let oldPreviousPosition = null;
            let oldMaps = previousMapDrone!.get(uri);
            if (oldMaps){
                for(let p = 0; p < oldMaps.length; p++){
                    oldMaps[p].position.x = oldMaps[p].position.x * 20 + (this.resolution / 2);
                    oldMaps[p].position.y = oldMaps[p].position.y * 20 + (this.resolution / 2); 
                    oldPositions.push(oldMaps[p].position);
                    for(let o = 0; o < oldMaps[p].distance.length; o++){
                        oldObstacles.push(oldMaps[p].distance[o]);
                    }
                }
                oldPreviousPosition = oldPositions[oldPositions.length - 1];
            }
            let new_mapDrone: MapDrone = 
                {
                    uri : uri, 
                    color: this.generateRandomColor(), 
                    positions: oldPositions, 
                    distances: oldObstacles, 
                    currentPosition: oldPreviousPosition,
                    lastPosition: oldPreviousPosition,
                    currentDistances: [],
                }
            this.mapDrones.set(uri,new_mapDrone);
        }
    }

    updateMapMetrics(metric: MapMetric, uri: string): void{
        // Positions of drone
        let newX = metric!.position.x * 5 + 50;
        let newY = metric!.position.y * 5 + 50;
        this.mapDrones.get(uri)!.positions.push({x: newX, y: newY, z: 0});
        this.mapDrones.get(uri)!.lastPosition = this.mapDrones.get(uri)!.currentPosition;
        this.mapDrones.get(uri)!.currentPosition = {x: newX, y: newY, z: 0};
        // Positions of obstacles
        this.mapDrones.get(uri)!.currentDistances = [];
        let obstacles = metric!.distance;
        if (obstacles!.length > 0){
            this.mapDrones.get(uri)!.currentDistances = obstacles;
            for(let d = 0; d < obstacles.length; d++){
                this.mapDrones.get(uri)!.distances.push(obstacles[d]);
            }
        }
    } 

    initializeCanvas(): void {
        this.baseCtx = this.basecanvas.nativeElement.getContext('2d') as CanvasRenderingContext2D;
        this.positionsCtx = this.positionscanvas.nativeElement.getContext('2d') as CanvasRenderingContext2D;
        this.currentCtx = this.currentcanvas.nativeElement.getContext('2d') as CanvasRenderingContext2D;
        this.resizeCanvas();
    }

    drawPixel(x: number, y: number, canvas: CanvasRenderingContext2D) :void{
        let xPixelized = this.pixelize(x, canvas);
        let yPixelized = this.pixelize(y, canvas);
        canvas!.fillRect(xPixelized, yPixelized, this.pixelSize, this.pixelSize);
    }

    pixelize(pixel: number, canvas: CanvasRenderingContext2D): number{
        let pixelCanvased = (pixel / 100.0) * this.canvasSize; // Gives the location of the point in the canvas' coordinates
        return Math.floor((pixelCanvased / this.pixelSize) * this.pixelSize); // Rounds to the previous multiple of the pixel size
    }

    drawCurrentPixels(): void {
        this.currentCtx.clearRect(0,0, this.canvasSize, this.canvasSize);
        this.currentCtx!.fillStyle = "red";
        for(let uri = 0; uri < this.allUris.length; uri++){
            if (this.selectedUris.get(this.allUris[uri])){
                let currentPosition = this.mapDrones.get(this.allUris[uri])!.currentPosition;
                if (currentPosition != null){
                    let x = this.mapDrones.get(this.allUris[uri])!.currentPosition!.x;
                    let y = this.mapDrones.get(this.allUris[uri])!.currentPosition!.y;
                    this.drawPixel(x, y, this.currentCtx)
                }
            }
        }
    }

    drawPositions(): void{
        this.positionsCtx!.lineWidth = this.pixelSize / 3;
        for(let uri = 0; uri < this.allUris.length; uri++){
            if (this.selectedUris.get(this.allUris[uri])){
                this.positionsCtx!.strokeStyle = this.mapDrones.get(this.allUris[uri])!.color;
                this.positionsCtx!.fillStyle = this.mapDrones.get(this.allUris[uri])!.color;
                
                let lastPosition = this.mapDrones.get(this.allUris[uri])!.lastPosition;
                if (lastPosition != null){
                    let lastPositionX = this.pixelize(lastPosition.x, this.positionsCtx);
                    let lastPositionY = this.pixelize(lastPosition.y, this.positionsCtx);
                    let currentPositionX = this.pixelize(this.mapDrones.get(this.allUris[uri])!.currentPosition!.x, this.positionsCtx);
                    let currentPositionY = this.pixelize(this.mapDrones.get(this.allUris[uri])!.currentPosition!.y, this.positionsCtx);
                    this.positionsCtx.beginPath();
                    this.positionsCtx.moveTo(lastPositionX, lastPositionY);
                    this.positionsCtx.lineTo(currentPositionX, currentPositionY);
                    this.positionsCtx.stroke();
                }
            }
        }
    }

    drawObstacle(): void{
        // to do
    }

    drawOldPositions(): void{
        this.positionsCtx.clearRect(0,0, this.canvasSize, this.canvasSize);
        this.positionsCtx!.lineWidth = this.pixelSize / 3;
        for(let uri = 0; uri < this.allUris.length; uri++){
            if (this.selectedUris.get(this.allUris[uri])){
                this.positionsCtx!.strokeStyle = this.mapDrones.get(this.allUris[uri])!.color;
                this.positionsCtx!.fillStyle = this.mapDrones.get(this.allUris[uri])!.color;

                let lastPositionX = this.pixelize(this.mapDrones.get(this.allUris[uri])!.positions[0].x, this.positionsCtx);
                let lastPositionY = this.pixelize(this.mapDrones.get(this.allUris[uri])!.positions[0].y, this.positionsCtx);
                for(let pos = 1; pos < this.mapDrones.get(this.allUris[uri])!.positions.length; pos++){
                    let currentPositionX = this.pixelize(this.mapDrones.get(this.allUris[uri])!.positions[pos].x, this.positionsCtx);
                    let currentPositionY = this.pixelize(this.mapDrones.get(this.allUris[uri])!.positions[pos].y, this.positionsCtx);
                    
                    this.positionsCtx.beginPath();
                    this.positionsCtx.moveTo(lastPositionX, lastPositionY);
                    this.positionsCtx.lineTo(currentPositionX, currentPositionY);
                    this.positionsCtx.stroke();

                    lastPositionX = currentPositionX;
                    lastPositionY = currentPositionY;
                }
            }
        }
    }

    redrawMap(): void {
        this.drawCurrentPixels();
        this.drawPositions();
        // this.drawObstacle();
    }

    generateRandomColor(): string {
        const letters = '0123456789ABCDEF';
        let color = '#';
        for (var i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }

    resizeCanvas(): void {
        this.canvasSize = Math.min(this.colMission.nativeElement.offsetWidth, this.colMission.nativeElement.offsetHeight);
        
        this.basecanvas.nativeElement.width = this.canvasSize;
        this.basecanvas.nativeElement.height = this.canvasSize;
        this.whiteBackgroundCanvas();
        
        this.positionscanvas.nativeElement.width = this.canvasSize;
        this.positionscanvas.nativeElement.height = this.canvasSize;
        this.currentcanvas.nativeElement.width = this.canvasSize;
        this.currentcanvas.nativeElement.height = this.canvasSize;

        this.pixelSize = this.canvasSize / this.resolution;
        
        if (this.mapDrones.size > 0){
            this.drawOldPositions();
        }
    }

    private whiteBackgroundCanvas(): void {
        this.baseCtx.beginPath()
        this.baseCtx.fillStyle = "white";
        this.baseCtx.fillRect(0, 0, this.canvasSize, this.canvasSize);
        this.baseCtx.fill();
        this.baseCtx.closePath();
    }

    updateSelected(): void{
        for(let i = 0; i < this.allUris.length; i++){
            this.selectedUris.set(this.allUris[i],false);
        }

        var checked = document.querySelectorAll('input[type=checkbox]:checked')
        for (var i = 0; i < checked.length; i++) {
            this.selectedUris.set(checked[i].id, true);
        }

        this.drawOldPositions();
        this.redrawMap();
    }

    resetSelectedUris(): void {
        for(let i = 0; i < this.allUris.length; i++){
            this.selectedUris.set(this.allUris[i],false);
        }
    }

}
