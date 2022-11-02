import { HttpClient } from '@angular/common/http';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { DronePanelComponent } from '@app/component/drone-panel/drone-panel.component';
import { CommandService } from '@app/services/command/command.service';
import { DroneInfoService } from '@app/services/drone-info/drone-info.service';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

describe('DronePanelComponent', () => {
    let component: DronePanelComponent;
    let fixture: ComponentFixture<DronePanelComponent>;
    let mockCommandService: CommandService;
    let mockDroneInfoService: DroneInfoService;

    beforeEach(async () => {
        mockCommandService = new CommandService({} as HttpClient) 
        mockDroneInfoService = new DroneInfoService({} as HttpClient)
        await TestBed.configureTestingModule({
            declarations: [ DronePanelComponent ],
            providers: [
                {provide: CommandService, useValue: mockCommandService},
                {provide: DroneInfoService, useValue: mockDroneInfoService}
            ],
            imports: [
                NgbModule,
            ]
        })
        .compileComponents();
    });

    beforeEach(() => {
        fixture = TestBed.createComponent(DronePanelComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });


    it('should not call commandService if uri is empty string when calling identify', () => {
        const identifySpy = spyOn(mockCommandService, 'identify');
        component.uri = ""

        component.identify();

        expect(identifySpy).not.toHaveBeenCalled();
    });

    it('should call commandService if uri is not empty string when calling identify', () => {
        const identifySpy = spyOn(mockCommandService, 'identify');
        component.uri = "test"

        component.identify();

        expect(identifySpy).toHaveBeenCalled();
    });
});
