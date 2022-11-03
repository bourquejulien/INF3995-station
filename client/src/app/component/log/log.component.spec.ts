import { ComponentFixture, TestBed } from '@angular/core/testing';
import { LogComponent } from './log.component';
import { HttpClient } from '@angular/common/http';
import { MissionService } from '@app/services/mission/mission.service';
import { DroneInfoService } from '@app/services/drone-info/drone-info.service';
import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

describe('LogComponent', () => {
    let component: LogComponent;
    let fixture: ComponentFixture<LogComponent>;
    let mockMissionService: MissionService;

    beforeEach(async () => {
        mockMissionService = new MissionService({} as HttpClient, {} as DroneInfoService)
        await TestBed.configureTestingModule({
            declarations: [ LogComponent ],
            providers: [
                {provide: MissionService, useValue: mockMissionService}
            ],
            imports: [
                NgbModule
            ]
        })
        .compileComponents();
    });

    beforeEach(() => {
        fixture = TestBed.createComponent(LogComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
