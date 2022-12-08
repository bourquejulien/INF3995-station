import { AfterViewInit, Component, ElementRef, OnInit, ViewChild } from "@angular/core";
import { Vec2 } from "@app/interface/mapdrone";
import { DroneInfoService } from "@app/services/drone-info/drone-info.service";
import { MissionService } from "@app/services/mission/mission.service";

@Component({
    selector: "app-history-map",
    templateUrl: "./history-map.component.html",
    styleUrls: ["./history-map.component.css"],
})
export class HistoryMapComponent implements OnInit, AfterViewInit {
    @ViewChild("historycanvas", { static: false }) historycanvas!: ElementRef;
    @ViewChild("mapcontainer", { static: false }) mapcontainer!: ElementRef;

    // Mission selection
    collapsed: boolean = true;
    selectedMissionId: string = "à afficher";
    // Canvas
    canvasSize!: number;
    historyCtx!: CanvasRenderingContext2D;
    pixelSize!: number;
    resolution: number = 100;
    scalingFactor: number = 5;
    // Positions
    positions: Vec2[];

    constructor(public droneInfoservice: DroneInfoService, public missionService: MissionService) {
        this.positions = [];
    }

    ngOnInit(): void {
        window.addEventListener("resize", this.resizeCanvas.bind(this), false); // Redraws the map when the window is resized
    }

    ngAfterViewInit(): void {
        this.initializeCanvas();
    }

    resizeCanvas(): void {
        this.canvasSize = Math.min(this.mapcontainer.nativeElement.offsetWidth, this.mapcontainer.nativeElement.offsetHeight);
        this.canvasSize = 0.75 * this.canvasSize;
        this.historycanvas.nativeElement.width = this.canvasSize;
        this.historycanvas.nativeElement.height = this.canvasSize;
        this.pixelSize = this.canvasSize / this.resolution;
        this.whiteBackgroundCanvas();
    }

    initializeCanvas(): void {
        this.historyCtx = this.historycanvas.nativeElement.getContext("2d") as CanvasRenderingContext2D;
        this.resizeCanvas();
    }

    public selectMission(id: string): void {
        this.selectedMissionId = id;
        this.collapsed = true;
        this.resizeCanvas();
        this.getMapById();
    }

    private getMapById(): void {
        this.droneInfoservice.getMapById(this.selectedMissionId).then(() => {
            this.positions = this.droneInfoservice.oldMap;
            this.drawMap();
        });
    }

    drawPixel(x: number, y: number, canvas: CanvasRenderingContext2D): void {
        let xPixelized = this.pixelize(x * this.scalingFactor + this.resolution / 2);
        let yPixelized = this.pixelize(y * this.scalingFactor + this.resolution / 2);
        canvas!.fillRect(xPixelized, yPixelized, this.pixelSize, this.pixelSize);
    }

    pixelize(pixel: number): number {
        let pixelCanvased = (pixel / 100.0) * this.canvasSize; // Gives the location of the point in the canvas' coordinates
        return Math.floor((pixelCanvased / this.pixelSize) * this.pixelSize); // Rounds to the previous multiple of the pixel size
    }

    private drawMap(): void {
        this.whiteBackgroundCanvas();
        this.historyCtx.fillStyle = "black";
        for (let p = 0; p < this.positions.length; p++) {
            this.drawPixel(this.positions[p].x, this.positions[p].y, this.historyCtx);
        }
    }

    private whiteBackgroundCanvas(): void {
        this.historyCtx.beginPath();
        this.historyCtx.fillStyle = "white";
        this.historyCtx.fillRect(0, 0, this.canvasSize, this.canvasSize);
        this.historyCtx.fill();
        this.historyCtx.closePath();
    }
}
