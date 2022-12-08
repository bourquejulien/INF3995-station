import { HttpClientModule } from '@angular/common/http';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { CommandService } from '@app/services/command/command.service';

import { MapComponent } from './map.component';
import { BehaviorSubject, Subject } from "rxjs";

describe('MapComponent', () => {
    let component: MapComponent;
    let fixture: ComponentFixture<MapComponent>;
    let mockCommandService: CommandService;
    let baseCtxSpy: CanvasRenderingContext2D;
    let positionsCtxSpy: CanvasRenderingContext2D;
    let currentCtxSpy: CanvasRenderingContext2D;
    let obstacleCtxSpy: CanvasRenderingContext2D;

    beforeEach(async () => {
        mockCommandService = jasmine.createSpyObj("CommandService", {"getUris": Promise.resolve(), "retrieveMode": Promise.resolve(),}, {"urisObservable": new Subject<[string, boolean][]>().asObservable() });
        await TestBed.configureTestingModule({
            declarations: [ MapComponent ],
            imports: [HttpClientModule],
            providers: [
                {provide: CommandService, useValue: mockCommandService},
            ]
        })
        .compileComponents();
    });

    beforeEach(() => {
        fixture = TestBed.createComponent(MapComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();

        baseCtxSpy = jasmine.createSpyObj('CanvasRendringContext', ['beginPath', 'closePath', 'fillRect', 'fill', 'fillStyle']);
        component['baseCtx'] = baseCtxSpy;
        positionsCtxSpy = jasmine.createSpyObj('CanvasRendringContext', ['beginPath', 'closePath', 'fillRect', 'fill', 'fillStyle', 'moveTo', 'stroke', 'lineTo', 'clearRect', 'lineWidth']);
        component['positionsCtx'] = positionsCtxSpy;
        currentCtxSpy = jasmine.createSpyObj('CanvasRendringContext', ['beginPath', 'closePath', 'fillRect', 'fill', 'fillStyle', 'clearRect']);
        component['currentCtx'] = currentCtxSpy;
        obstacleCtxSpy = jasmine.createSpyObj('CanvasRendringContext', ['beginPath', 'closePath', 'fillRect', 'fill', 'fillStyle', 'clearRect']);
        component['obstacleCtx'] = obstacleCtxSpy;
    });

    it('should pixelise', () => {
        component['drawPixel'](0,0,currentCtxSpy);
        expect(currentCtxSpy.fillRect).toHaveBeenCalled();
    
    });

    it('should draw current pixel', () => {
        component['pixelSize'] = 3;
        component['allUris'] = ["a"];
        component['selectedUris'] = new Map(component.allUris.map((e) => [e, false]));
        component['drawCurrentPixels']();
        expect(currentCtxSpy.clearRect).toHaveBeenCalled();
        expect(currentCtxSpy.fillStyle).toEqual("red");
    
    });

    it('should draw positions', () => {
        component['pixelSize'] = 3;
        component['allUris'] = ["a"];
        component['selectedUris'] = new Map(component.allUris.map((e) => [e, false]));
        component['drawPositions']();
        expect(positionsCtxSpy.lineWidth).toEqual(1);
    });

    it('should draw obstacles', () => {
        component['allUris'] = ["a"];
        component['selectedUris'] = new Map(component.allUris.map((e) => [e, false]));
        component['drawObstacles']();
        expect(obstacleCtxSpy.fillStyle).toEqual("black");
    });

    it('should draw old positions', () => {
        component['allUris'] = ["a"];
        component['selectedUris'] = new Map(component.allUris.map((e) => [e, false]));
        component['drawOldPositions']();
        expect(positionsCtxSpy.clearRect).toHaveBeenCalled();
    });

    it('should draw old obstacles', () => {
        component['allUris'] = ["a"];
        component['selectedUris'] = new Map(component.allUris.map((e) => [e, false]));
        component['drawOldObstacles']();
        expect(obstacleCtxSpy.clearRect).toHaveBeenCalled();
        expect(obstacleCtxSpy.fillStyle).toEqual("black");
    });

    it('should draw path positions', () => {
        const positions = [{x:0, y:0, z:0}, {x:1, y:1, z:1}];
        component['drawPathPositions'](positions, positionsCtxSpy);
        expect(positionsCtxSpy.beginPath).toHaveBeenCalledTimes(1);
        expect(positionsCtxSpy.moveTo).toHaveBeenCalledTimes(1);
        expect(positionsCtxSpy.lineTo).toHaveBeenCalledTimes(1);
        expect(positionsCtxSpy.stroke).toHaveBeenCalledTimes(1);

    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });

    it('should generate random color', () => {
        const test1 = component['generateRandomColor']();
        const test2 = component['generateRandomColor']();
        expect(test1).not.toEqual(test2);
    });

    it('should resize canvas and change canvas size', () => {
        spyOn(component.colMission.nativeElement,'offsetWidth').and.returnValue(100);
        spyOn(component.colMission.nativeElement,'offsetWidth').and.returnValue(100);
        component['resizeCanvas']();
        expect(component['canvasSize']).toEqual(150);
    });

    it('should resize canvas and change pixel size', () => {
        spyOn(component.colMission.nativeElement,'offsetWidth').and.returnValue(100);
        spyOn(component.colMission.nativeElement,'offsetWidth').and.returnValue(100);
        component['resizeCanvas']();
        expect(component['pixelSize']).toEqual(1.5);
    });

    it('should white background base canvas', () => {
        component['whiteBackgroundCanvas']();
        expect(baseCtxSpy.beginPath).toHaveBeenCalled();
        expect(baseCtxSpy.fillStyle).toEqual("white");
        expect(baseCtxSpy.fillRect).toHaveBeenCalled();
        expect(baseCtxSpy.fill).toHaveBeenCalled();
        expect(baseCtxSpy.closePath).toHaveBeenCalled();
    });

    it('should reset after selection', () => {
        component['allUris'] = ["test1", "test2"];
        let testMap = new Map(component.allUris.map((e) => [e, false]));
        component['resetSelectedUris']();
        expect(component.selectedUris).toEqual(testMap);
    });
});
