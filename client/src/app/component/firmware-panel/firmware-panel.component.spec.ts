import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FirmwarePanelComponent } from './firmware-panel.component';
import { FirmwareService } from '../../services/firmware/firmware.service';
import { HttpClient } from '@angular/common/http';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { HttpClientTestingModule } from "@angular/common/http/testing";

describe('FirmwarePanelComponent', () => {
    let component: FirmwarePanelComponent;
    let fixture: ComponentFixture<FirmwarePanelComponent>;

    let mockFirmwareService = new FirmwareService({} as HttpClient)


    beforeEach(async () => {
        await TestBed.configureTestingModule({
            declarations: [FirmwarePanelComponent],
            providers: [
                {provide: FirmwareService, useValue: mockFirmwareService}
            ],
            imports: [NgbModule, HttpClientTestingModule
            ]
        }).compileComponents();
    });

    beforeEach(() => {
        fixture = TestBed.createComponent(FirmwarePanelComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
