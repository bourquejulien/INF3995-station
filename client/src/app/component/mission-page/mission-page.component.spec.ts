import { CUSTOM_ELEMENTS_SCHEMA } from "@angular/core";
import { ComponentFixture, TestBed } from "@angular/core/testing";
import { MissionPageComponent } from "@app/component/mission-page/mission-page.component";
import { CommandService } from "@app/services/command/command.service";
import { MissionService } from "@app/services/mission/mission.service";
import { NgbModule } from "@ng-bootstrap/ng-bootstrap";

describe("MissionPageComponent", () => {
    let component: MissionPageComponent;
    let fixture: ComponentFixture<MissionPageComponent>;
    let mockCommandService: CommandService;
    let mockMissionService: MissionService;

    beforeEach(async () => {
        mockCommandService = jasmine.createSpyObj(
            "CommandService",
            {
                getUris: Promise.resolve(),
                retrieveMode: Promise.resolve(),
                connect: Promise.resolve(),
                disconnect: Promise.resolve(),
                identify: Promise.resolve(),
                toggleSync: Promise.resolve(),
            },
            { uris: [] },
        );
        mockMissionService = jasmine.createSpyObj("MissionService", ["startMission", "endMission", "forceEndMission", "returnToBase"], {
            isMissionOnGoing: true,
        });
        await TestBed.configureTestingModule({
            declarations: [MissionPageComponent],
            providers: [
                { provide: CommandService, useValue: mockCommandService },
                { provide: MissionService, useValue: mockMissionService },
            ],
            imports: [NgbModule],
            schemas: [CUSTOM_ELEMENTS_SCHEMA],
        }).compileComponents();
    });

    beforeEach(() => {
        fixture = TestBed.createComponent(MissionPageComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it("should create", () => {
        expect(component).toBeTruthy();
    });

    it("should get uris on init and retrieve mode", () => {
        component.ngOnInit();
        expect(mockCommandService.getUris).toHaveBeenCalled();
        expect(mockCommandService.retrieveMode).toHaveBeenCalled();
    });

    it("should connect", () => {
        component.connect();
        expect(mockCommandService.connect).toHaveBeenCalled();
    });

    it("should diconnect", () => {
        component.disconnect();
        expect(mockCommandService.disconnect).toHaveBeenCalled();
    });

    it("should identify", () => {
        component.identify();
        expect(mockCommandService.identify).toHaveBeenCalled();
    });

    it("should toggle sync", () => {
        component.toggleSync();
        expect(mockCommandService.toggleSync).toHaveBeenCalled();
    });

    it("should start mission", () => {
        component.startMission();
        expect(mockMissionService.startMission).toHaveBeenCalled();
    });

    it("should end mission", () => {
        component.endMission();
        expect(mockMissionService.endMission).toHaveBeenCalled();
    });

    it("should force end mission", () => {
        component.forceEndMission();
        expect(mockMissionService.forceEndMission).toHaveBeenCalled();
    });

    it("should force end mission", () => {
        component.returnToBase();
        expect(mockMissionService.returnToBase).toHaveBeenCalled();
    });

    it("should toggle pan if current pane", () => {
        component.currentPane = "none";
        component.togglePane("none");
        expect(component.currentPane).toEqual("none");
    });

    it("should toggle pan if not current pane", () => {
        component.currentPane = "logs";
        component.togglePane("none");
        expect(component.currentPane).toEqual("none");
    });

    it("should handle error", () => {
        const spyConsole = spyOn(console, "log").and.stub();
        component.handleError(Error("error"));
        expect(spyConsole).toHaveBeenCalled();
    });
});
