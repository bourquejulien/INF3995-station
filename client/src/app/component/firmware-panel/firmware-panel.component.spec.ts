import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FirmwarePanelComponent } from './firmware-panel.component';
import { FirmwareService } from '../../services/firmware/firmware.service';
import { HttpClient } from '@angular/common/http';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { Component } from '@angular/core';
import { Observable, of } from 'rxjs';

describe('FirmwarePanelComponent', () => {
    let component: FirmwarePanelComponent;
    let fixture: ComponentFixture<FirmwarePanelComponent>;

    let mockFirmwareService: jasmine.SpyObj<FirmwareService>;

    let spyBuildFlash: jasmine.Spy;
    let spyFlashFile: jasmine.Spy;


    beforeEach(async () => {
        mockFirmwareService = jasmine.createSpyObj('FirmwareService', ['flashFile', 'buildFlash', 'flashHandler']);
        spyBuildFlash = jasmine.createSpy('buildFlash').and.returnValue(of({type: 'Observable'}));
        await TestBed.configureTestingModule({
            declarations: [FirmwarePanelComponent],
            providers: [
                {provide: FirmwareService, useValue: mockFirmwareService}
            ],
            imports: [NgbModule,
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

    it('getName should return name', () => {
        let result = component.getName("editor");
        expect(result).toMatch("Utiliser l'éditeur en ligne"); 
    });

    it('selectMode should select mode in parameter', () => {
        component.selectMode("file");
        expect(component.currentMode).toMatch("file");
        expect(component.collapsed).toBeTruthy();
        expect(component.file).toBeNull();
    });
    
    it('flash should not call flashFile if file is null', () => {
        component.currentMode = "file";
        component.file = null;
        component.flash();
        expect(mockFirmwareService['buildFlash']).not.toHaveBeenCalled();
        expect(mockFirmwareService['flashFile']).not.toHaveBeenCalled();
    });
});
