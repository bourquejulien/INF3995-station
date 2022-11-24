import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CodeEditorComponent } from './code-editor.component';
import { CommandService } from '../../services/command/command.service';
import { DroneInfoService } from '../../services/drone-info/drone-info.service';
import { FirmwareService } from '../../services/firmware/firmware.service';
import { HttpClient } from '@angular/common/http';

describe('CodeEditorComponent', () => {
    let component: CodeEditorComponent;
    let fixture: ComponentFixture<CodeEditorComponent>;

    let mockFirmwareService = new FirmwareService({} as HttpClient)

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            declarations: [CodeEditorComponent],
            providers: [
                {provide: FirmwareService, useValue: mockFirmwareService}
            ],
        }).compileComponents();
    });

    beforeEach(() => {
        fixture = TestBed.createComponent(CodeEditorComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
