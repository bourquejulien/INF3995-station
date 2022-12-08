import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CodeEditorComponent } from './code-editor.component';
import { CommandService } from '../../services/command/command.service';
import { DroneInfoService } from '../../services/drone-info/drone-info.service';
import { FirmwareService } from '../../services/firmware/firmware.service';
import { HttpClient } from '@angular/common/http';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';

describe('CodeEditorComponent', () => {
    let component: CodeEditorComponent;
    let fixture: ComponentFixture<CodeEditorComponent>;
    let keyboardEvent: KeyboardEvent;

    let mockFirmwareService = new FirmwareService({} as HttpClient);

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

    it('should call getFile if key pressed is Enter', () => {
        keyboardEvent = { key: "Enter" } as KeyboardEvent;
        const handleKeySpy = spyOn(component, 'getFile');
        component.handleKey(keyboardEvent);
        expect(handleKeySpy).toHaveBeenCalled();
    });
    
    it('should not call getFile if key pressed is not Enter', () => {
        keyboardEvent = { key: "a" } as KeyboardEvent;
        const handleKeySpy = spyOn(component, 'getFile');
        component.handleKey(keyboardEvent);
        expect(handleKeySpy).not.toHaveBeenCalled();
    });

    it('getFile should return if filePath is empty', () => {
        component.filePath = "";
        const firmwareFileSpy = spyOn(mockFirmwareService, 'getFile');
        component.getFile();
        expect(firmwareFileSpy).not.toHaveBeenCalled();
    });

    it('editFile should return if filePath is empty', () => {
        component.filePath = "";
        const firmwareFileSpy = spyOn(mockFirmwareService, 'editFile');
        component.editFile();
        expect(firmwareFileSpy).not.toHaveBeenCalled();
    });

    it('editFile should return if fileContent is empty', () => {
        component.fileContent = "";
        const firmwareFileSpy = spyOn(mockFirmwareService, 'editFile');
        component.editFile();
        expect(firmwareFileSpy).not.toHaveBeenCalled();
    });
});
