import { HttpClient } from '@angular/common/http';
import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { MissionPageComponent } from '@app/component/mission-page/mission-page.component';
import { CommandService } from '@app/services/command/command.service';
import { DroneInfoService } from '@app/services/drone-info/drone-info.service';
import { MissionService } from '@app/services/mission/mission.service';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

describe('MissionPageComponent', () => {
    let component: MissionPageComponent;
    let fixture: ComponentFixture<MissionPageComponent>;
    let mockCommandService: CommandService;
    let mockMissionService: MissionService;

    beforeEach(async () => {
        mockCommandService = jasmine.createSpyObj("CommandService", ["getUris", "retrieveMode"]);
        mockMissionService = jasmine.createSpyObj("MissionService", [""]);
        await TestBed.configureTestingModule({
            declarations: [ MissionPageComponent ],
            providers: [
                {provide: CommandService, useValue: mockCommandService},
                {provide: MissionService, useValue: mockMissionService}
            ],
            imports: [
            NgbModule
            ],
            schemas: [CUSTOM_ELEMENTS_SCHEMA]
        })
        .compileComponents();
    });

    beforeEach(() => {
        fixture = TestBed.createComponent(MissionPageComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
