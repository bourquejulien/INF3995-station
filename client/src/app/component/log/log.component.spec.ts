import { ComponentFixture, TestBed } from '@angular/core/testing';
import { LogComponent } from './log.component';
import { MissionService } from '@app/services/mission/mission.service';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

describe('LogComponent', () => {
    let component: LogComponent;
    let fixture: ComponentFixture<LogComponent>;
    let mockMissionService: MissionService;

    beforeEach(async () => {
        mockMissionService = jasmine.createSpyObj("MissionService", ["getMissionLogs"], {"missions": []});
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
