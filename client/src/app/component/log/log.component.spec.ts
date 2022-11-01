import { ComponentFixture, TestBed } from '@angular/core/testing';
import { LogComponent } from './log.component';
import { DroneInfoService } from '@app/services/drone-info/drone-info.service';
import { HttpClient } from '@angular/common/http';

describe('LogComponent', () => {
    let component: LogComponent;
    let fixture: ComponentFixture<LogComponent>;
    let mockDroneInfoService: DroneInfoService;

    beforeEach(async () => {
        mockDroneInfoService = new DroneInfoService({} as HttpClient)
        await TestBed.configureTestingModule({
            declarations: [ LogComponent ],
            providers: [
                {provide: DroneInfoService, useValue: mockDroneInfoService}
            ],
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
