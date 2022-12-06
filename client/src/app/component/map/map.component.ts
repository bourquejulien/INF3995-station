import { Component, OnInit, ViewChild, ElementRef, AfterViewInit } from '@angular/core';
import { MapDrone, MapMetric } from '@app/interface/mapdrone';
import { Position } from '@app/interface/commands';
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
    @ViewChild('obstaclecanvas', { static: false }) obstaclecanvas!: ElementRef;
    @ViewChild('colMission', { static: false }) colMission!: ElementRef;

    constructor(public droneInfoService: DroneInfoService, public commandService: CommandService) {
        this.resolution = 100;
        this.scalingFactor = 10;
        this.mapDrones = new Map();
        this.allUris = [];
        this.selectedUris = new Map();
    }

    // Canvas
    private baseCtx!: CanvasRenderingContext2D;
    private positionsCtx!: CanvasRenderingContext2D;
    private currentCtx!: CanvasRenderingContext2D;
    private obstacleCtx!: CanvasRenderingContext2D;
    private canvasSize!: number;
    private pixelSize!: number;
    resolution: number; // Number of pixels to include in the map. The higher the number, the finer the image
    scalingFactor: number;
    // Drones info
    mapDrones: Map<string, MapDrone>;
    allUris: string[];
    selectedUris: Map<string, boolean>;
    
    ngOnInit(): void {
        window.addEventListener("resize", this.resizeCanvas.bind(this), false); // Redraws the map when the window is resized
        this.commandService.getUris()
        .then(() => { // Waiting for all uris then proceed
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
        },
        (err) => {
            console.error(err);
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
            let oldMaps = previousMapDrone.get(uri);
            let oldPositions = []; // drone positions in server
            let oldObstacles = []; // obstacle positions in server
            let lastDronePosition = null; // last position of the drone
            if (oldMaps){
                let positionObstacle: Position = {x: 0, y: 0, z: 0};
                let positionDrone: Position = {x: 0, y: 0, z: 0};
                for(let p = 0; p < oldMaps.length; p++){
                    positionDrone.x = oldMaps[p].position.x * this.scalingFactor + (this.resolution / 2);
                    positionDrone.y = oldMaps[p].position.y * this.scalingFactor + (this.resolution / 2); 
                    oldPositions.push(positionDrone);
                    for(let obstacle = 0; obstacle < oldMaps[p].distance.length; obstacle++){
                        positionObstacle.x = oldMaps[p].distance[obstacle].x * this.scalingFactor + (this.resolution / 2);
                        positionObstacle.y = oldMaps[p].distance[obstacle].y * this.scalingFactor + (this.resolution / 2);
                        oldObstacles.push(positionObstacle);
                    }
                }
                lastDronePosition = oldPositions[oldPositions.length - 1];
            }
            let new_mapDrone: MapDrone = 
                {
                    uri : uri, 
                    color: this.generateRandomColor(), 
                    positions: oldPositions, 
                    distances: oldObstacles, 
                    currentPosition: lastDronePosition,
                    lastPosition: lastDronePosition,
                    currentDistances: [],
                }

            this.mapDrones.set(uri,new_mapDrone);
        }
    }

    updateMapMetrics(metric: MapMetric, uri: string): void{
        // Positions of drone
        let positionDrone: Position = {x: 0, y: 0, z: 0};
        positionDrone.x = metric!.position.x * this.scalingFactor + this.resolution / 2;
        positionDrone.y = metric!.position.y * this.scalingFactor + this.resolution / 2;
        this.mapDrones.get(uri)!.positions.push(positionDrone);
        this.mapDrones.get(uri)!.lastPosition = this.mapDrones.get(uri)!.currentPosition;
        this.mapDrones.get(uri)!.currentPosition = positionDrone;
        // Positions of obstacles
        this.mapDrones.get(uri)!.currentDistances = [];
        let obstacles = metric!.distance;
        if (obstacles!.length > 0){
            let currentDistances = [];
            for(let d = 0; d < obstacles.length; d++){
                let positionObstacle: Position = {x: 0, y: 0, z: 0};
                positionObstacle.x = obstacles[d].x * this.scalingFactor + this.resolution / 2;
                positionObstacle.y = obstacles[d].y * this.scalingFactor + this.resolution / 2;
                this.mapDrones.get(uri)!.distances.push(positionObstacle);
                currentDistances.push(positionObstacle);
            }
            this.mapDrones.get(uri)!.currentDistances = currentDistances;
        }
    } 

    initializeCanvas(): void {
        this.baseCtx = this.basecanvas.nativeElement.getContext('2d') as CanvasRenderingContext2D;
        this.positionsCtx = this.positionscanvas.nativeElement.getContext('2d') as CanvasRenderingContext2D;
        this.currentCtx = this.currentcanvas.nativeElement.getContext('2d') as CanvasRenderingContext2D;
        this.obstacleCtx = this.obstaclecanvas.nativeElement.getContext('2d') as CanvasRenderingContext2D;
        
        this.resizeCanvas();
    }

    drawPixel(x: number, y: number, canvas: CanvasRenderingContext2D) :void{
        let xPixelized = this.pixelize(x);
        let yPixelized = this.pixelize(y);
        canvas!.fillRect(xPixelized, yPixelized, this.pixelSize, this.pixelSize);
    }

    pixelize(pixel: number): number{
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
                    this.drawPixel(this.mapDrones.get(this.allUris[uri])!.currentPosition!.x, this.mapDrones.get(this.allUris[uri])!.currentPosition!.y, this.currentCtx)
                }
            }
        }
    }

    drawPositions(): void {
        this.positionsCtx!.lineWidth = this.pixelSize / 3;
        for(let uri = 0; uri < this.allUris.length; uri++){
            if (this.selectedUris.get(this.allUris[uri])){
                this.positionsCtx!.strokeStyle = this.mapDrones.get(this.allUris[uri])!.color;
                this.positionsCtx!.fillStyle = this.mapDrones.get(this.allUris[uri])!.color;
                
                let positions: Position[] = [this.mapDrones.get(this.allUris[uri])!.lastPosition!, this.mapDrones.get(this.allUris[uri])!.currentPosition!];
                this.drawPathPositions(positions, this.positionsCtx);
            }
        }
    }

    drawObstacles(): void {
        this.obstacleCtx!.fillStyle = "black";
        for(let uri = 0; uri < this.allUris.length; uri++){
            if (this.selectedUris.get(this.allUris[uri])){
               for(let obstacle = 0; obstacle < this.mapDrones.get(this.allUris[uri])!.currentDistances.length; obstacle++){
                    this.drawPixel(this.mapDrones.get(this.allUris[uri])!.currentDistances[obstacle].x, this.mapDrones.get(this.allUris[uri])!.currentDistances[obstacle].y, this.obstacleCtx)
                }
            }
        }
    }

    drawOldPositions(): void {
        this.positionsCtx.clearRect(0,0, this.canvasSize, this.canvasSize);
        this.positionsCtx!.lineWidth = this.pixelSize / 3;
        
        for(let uri = 0; uri < this.allUris.length; uri++){
            if (this.selectedUris.get(this.allUris[uri])){
                this.positionsCtx!.strokeStyle = this.mapDrones.get(this.allUris[uri])!.color;
                this.positionsCtx!.fillStyle = this.mapDrones.get(this.allUris[uri])!.color;
                this.drawPathPositions(this.mapDrones.get(this.allUris[uri])!.positions, this.positionsCtx);
            }
        }
    }

    drawOldObstacles(): void{
        this.obstacleCtx.clearRect(0,0, this.canvasSize, this.canvasSize);
        this.obstacleCtx!.fillStyle = "black";

        for(let uri = 0; uri < this.allUris.length; uri++){
            if (this.selectedUris.get(this.allUris[uri])){
                for(let obstacle = 0; obstacle < this.mapDrones.get(this.allUris[uri])!.distances.length; obstacle++){
                    this.drawPixel(this.mapDrones.get(this.allUris[uri])!.distances[obstacle].x, this.mapDrones.get(this.allUris[uri])!.distances[obstacle].y, this.obstacleCtx);
                }
            }
        }
    }

    drawPathPositions(positions: Position[], canvas: CanvasRenderingContext2D) : void {
        let lastPositionX = this.pixelize(positions[0].x);
        let lastPositionY = this.pixelize(positions[0].y);

        for(let pos = 1; pos < positions.length; pos++){
            let currentPositionX = this.pixelize(positions[pos].x);
            let currentPositionY = this.pixelize(positions[pos].y);

            this.positionsCtx.beginPath();
            this.positionsCtx.moveTo(lastPositionX, lastPositionY);
            this.positionsCtx.lineTo(currentPositionX, currentPositionY);
            this.positionsCtx.stroke();

            lastPositionX = currentPositionX;
            lastPositionY = currentPositionY;
        }
    }

    redrawMap(): void {
        this.drawCurrentPixels();
        this.drawPositions();
        this.drawObstacles();
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
        this.obstaclecanvas.nativeElement.width = this.canvasSize;
        this.obstaclecanvas.nativeElement.height = this.canvasSize;

        this.pixelSize = this.canvasSize / this.resolution;
        
        if (this.mapDrones.size > 0){
            this.drawOldPositions();
            this.drawOldObstacles();
        }
    }

    private whiteBackgroundCanvas(): void {
        this.baseCtx.beginPath()
        this.baseCtx.fillStyle = "white";
        this.baseCtx.fillRect(0, 0, this.canvasSize, this.canvasSize);
        this.baseCtx.fill();
        this.baseCtx.closePath();
    }

    updateSelected(): void {
        for(let i = 0; i < this.allUris.length; i++){
            this.selectedUris.set(this.allUris[i],false);
        }

        var checked = document.querySelectorAll('input[type=checkbox]:checked')
        for (var i = 0; i < checked.length; i++) {
            this.selectedUris.set(checked[i].id, true);
        }
        
        this.drawOldPositions();
        this.drawOldObstacles();
        this.redrawMap();
    }

    resetSelectedUris(): void {
        for(let i = 0; i < this.allUris.length; i++){
            this.selectedUris.set(this.allUris[i],false);
        }
    }

}
