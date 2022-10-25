import { HttpClient } from '@angular/common/http';
import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { MissionPageComponent } from '@app/component/mission-page/mission-page.component';
import { CommandService } from '@app/services/command/command.service';

describe('MissionPageComponent', () => {
    let component: MissionPageComponent;
    let fixture: ComponentFixture<MissionPageComponent>;
    let mockCommandService: CommandService;

    beforeEach(async () => {
        mockCommandService = new CommandService({} as HttpClient) 
        await TestBed.configureTestingModule({
            declarations: [ MissionPageComponent ],
            providers: [
                {provide: CommandService, useValue: mockCommandService}
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
