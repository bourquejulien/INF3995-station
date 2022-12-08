import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HistoryPanelComponent } from './history-panel.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { MissionService } from '@app/services/mission/mission.service';

describe('HistoryPanelComponent', () => {
    let component: HistoryPanelComponent;
    let fixture: ComponentFixture<HistoryPanelComponent>;
    let mockMissionService: MissionService;

    beforeEach(async () => {
        mockMissionService = jasmine.createSpyObj("MissionService", [], {"missions": []});
        await TestBed.configureTestingModule({
            declarations: [HistoryPanelComponent],
            providers: [
                {provide: MissionService, useValue: mockMissionService}
            ],
            imports: [
                NgbModule,
                HttpClientTestingModule
            ]
        }).compileComponents();
    });

    beforeEach(() => {
        fixture = TestBed.createComponent(HistoryPanelComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });

    it('should set attribute in ngOnInit', () => {
        component.ngOnInit();
        expect(component.collapsed).toEqual(true);
        expect(component.selectedMission).toEqual(undefined);
        expect(component.currentAttribute).toEqual("start_time_ms");
    });

    it('should not get attribute name if not find', () => {
        spyOn(component.attributes, 'find').and.returnValue(undefined);
        const returnValue = component.getAttributeName("id");
        expect(returnValue).toEqual("Aucun");
    });

    it('should  get attribute name if find', () => {
        const returnValue = component.getAttributeName("id");
        expect(returnValue).toEqual("Id");
    });

    it('should  return attribute as number', () => {
        const mockMission = {
            total_time: 1,
            id: "test",
            is_simulation: true,
            total_distance: 0,
            drone_count: 1,
            start_time_ms: 0,
            end_time_ms: 1,
        };
        const returnValue = component.getAttributeAsNumber(mockMission, "total_time");
        expect(returnValue).toEqual(1);
    });

    it('should select attribute', () => {
        component.selectAttribute("id");
        expect(component.currentAttribute).toEqual("id");
        expect(component.collapsed).toEqual(true);
    });

    it('should return true if it`s a date', () => {
        const returnValue = component.isDate("end_time_ms");
        expect(returnValue).toEqual(true);
    });

    it('should return false if it`s not a date', () => {
        const returnValue = component.isDate("id");
        expect(returnValue).toEqual(false);
    });

    it('should return false if it is not history', () => {
        const returnValue = component.isHistory;
        expect(returnValue).toEqual(false);
    });

    it('toNUmber should convert correctly', () => {
        expect(component["toNumber"](false)).toEqual(0);
        expect(component["toNumber"](true)).toEqual(1);
        expect(component["toNumber"]("ab")).toEqual(195);
        expect(component["toNumber"](10)).toEqual(10);
    });

    it('should return no missions if missionservice is empty', () => {
        expect(component.missions).toEqual([]);
    });
});
