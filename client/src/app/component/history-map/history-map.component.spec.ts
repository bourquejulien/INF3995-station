import { HttpClientModule } from "@angular/common/http";
import { ComponentFixture, TestBed } from "@angular/core/testing";
import { DroneInfoService } from "@app/services/drone-info/drone-info.service";
import { NgbModule } from "@ng-bootstrap/ng-bootstrap";

import { HistoryMapComponent } from "./history-map.component";

describe("HistoryMapComponent", () => {
    let component: HistoryMapComponent;
    let fixture: ComponentFixture<HistoryMapComponent>;
    let historyCtxSpy: CanvasRenderingContext2D;
    let droneInfoserviceSpy: jasmine.SpyObj<DroneInfoService>;

    beforeEach(async () => {
        droneInfoserviceSpy = jasmine.createSpyObj("DroneInfoService", ["getMapById", "oldMap"]);
        await TestBed.configureTestingModule({
            declarations: [HistoryMapComponent],
            imports: [HttpClientModule, NgbModule],
            providers: [{ provide: DroneInfoService, useValue: droneInfoserviceSpy }],
        }).compileComponents();
    });

    beforeEach(() => {
        fixture = TestBed.createComponent(HistoryMapComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();

        historyCtxSpy = jasmine.createSpyObj("CanvasRendringContext", ["beginPath", "closePath", "fillRect", "fill", "fillStyle"]);
        component["historyCtx"] = historyCtxSpy;
    });

    it("should create", () => {
        expect(component).toBeTruthy();
    });

    it("should initialise canvas after view init", () => {
        const initializeCanvasSpy = spyOn(component, "initializeCanvas").and.stub();
        component.ngAfterViewInit();
        expect(initializeCanvasSpy).toHaveBeenCalled();
    });

    it("should resize canvas after view init", () => {
        const resizeCanvasSpy = spyOn(component, "resizeCanvas").and.stub();
        component.ngAfterViewInit();
        expect(resizeCanvasSpy).toHaveBeenCalled();
    });

    it("should resize canvas", () => {
        component.resizeCanvas();
        expect(component.canvasSize).toEqual(84);
        expect(component.historycanvas.nativeElement.width).toEqual(84);
        expect(component.historycanvas.nativeElement.height).toEqual(84);
        expect(component.pixelSize).toEqual(0.84);
    });

    it("should put blank background after resize", () => {
        component.resizeCanvas();
        expect(historyCtxSpy.beginPath).toHaveBeenCalled();
        expect(historyCtxSpy.fillStyle).toEqual("white");
        expect(historyCtxSpy.fillRect).toHaveBeenCalled();
        expect(historyCtxSpy.fill).toHaveBeenCalled();
        expect(historyCtxSpy.closePath).toHaveBeenCalled();
    });

    it("should set canvasrenderingcontext on initialisation", () => {
        const resizeCanvasSpy = spyOn(component, "resizeCanvas").and.stub();
        component.initializeCanvas();
        expect(historyCtxSpy).toBeDefined();
        expect(resizeCanvasSpy).toHaveBeenCalled();
    });

    it("should change id on selection of mission", () => {
        let testId = "test";
        droneInfoserviceSpy.getMapById.and.returnValue(Promise.resolve());
        component.selectMission(testId);
        expect(component.selectedMissionId).toEqual("test");
    });

    it("should collapse after set of selection mission", () => {
        let testId = "test";
        droneInfoserviceSpy.getMapById.and.returnValue(Promise.resolve());
        component.selectMission(testId);
        expect(component.collapsed).toBeDefined();
    });

    it("should resize after set of selection mission", () => {
        let testId = "test";
        const resizeCanvasSpy = spyOn(component, "resizeCanvas").and.stub();
        droneInfoserviceSpy.getMapById.and.returnValue(Promise.resolve());
        component.selectMission(testId);
        expect(resizeCanvasSpy).toHaveBeenCalled();
    });

    it("should get map in drone service after set of selection mission", () => {
        let testId = "test";
        droneInfoserviceSpy.getMapById.and.returnValue(Promise.resolve());
        component.selectMission(testId);
        expect(droneInfoserviceSpy.getMapById).toHaveBeenCalled();
    });

    it("should pixelise before drawing pixel", () => {
        const pixelizeSpy = spyOn(component, "pixelize").and.stub();
        component.drawPixel(0, 0, historyCtxSpy);
        expect(pixelizeSpy).toHaveBeenCalledTimes(2);
    });

    it("should fill pixel when draing pixel", () => {
        component.drawPixel(0, 0, historyCtxSpy);
        expect(historyCtxSpy.fillRect).toHaveBeenCalled();
    });

    it("should pixelise pixel", () => {
        component.canvasSize = 100;
        expect(component.pixelize(1)).toEqual(1);
    });
});
